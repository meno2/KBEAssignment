#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2021 ParaPy Holding B.V.
#
# You may use the contents of this file in your application code.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR
# PURPOSE.

"""This example is about creating a custom Mode, allowing the user to
manipulate objects in a grid; it acts very much like PlanarTranslation, but
the increment discretizes the translation not radially from the manipulation
start point, but along both binormals of the plane normal independently.

Also this mode showcases guides that are highlighted when the object is aligned
with them, to help the user move 'along' them.

Display MyObj and right-click it in the viewer to start manipulating it.
"""


import typing
from functools import partial

from OCC.gui.interactive_objects import make_ais_line

from parapy.core import Input, Attribute, child, Part
from parapy.core.widgets import MultiCheckBox
from parapy.geom import (
    Vector, Box, RectangularFace, Position, Point, VZ, VX, VY)
from parapy.geom.generic.transformation import rebase_vector
from parapy.gui import display, Manipulable
from parapy.gui.manipulation.events import EndEvent
from parapy.gui.manipulation.gizmo import Gizmo, HandleBase
from parapy.gui.manipulation.globs import DEFAULT_AXES
from parapy.gui.manipulation.modes import (
    ManipulationMode, UpdateAISShapeReturnType)
from parapy.gui.manipulation.utils import ais_set_style, vector_to_color

if typing.TYPE_CHECKING:
    from OCC.wrapper.AIS import Handle_AIS_Shape  # noqa


def round_to_multiple_of(x, base):
    return base * round(x / base)


class GridTranslation(ManipulationMode):
    # this mode needs a cell_size kwarg input
    _name = 'grid'
    __copy_attrs__ = 'normal',
    default_axis_colors = ('red', 'blue', 'green')

    def __init__(self, normal, increment, *args, **kwargs):
        super().__init__(*args, increment=increment, **kwargs)
        self.normal = normal

    # determine what color should the gizmo handle for this mode be, based on a
    # trio of colors corresponding to absolute X, Y, Z axes.
    def _get_handle_color(self, xyz_component_colors):
        return vector_to_color(self.normal, xyz_component_colors)

    def transformed(self, to_position: Position):
        return self.copy(
            reference=to_position,
            normal=rebase_vector(self.normal, self.reference, to_position))

    # define a projector: a function mapping an on-screen (viewer) click to a
    # world position
    def project(self, viewer, x, y, position) -> Point:
        return viewer.screen_to_point_in_plane(x, y, position.location,
                                               self.normal)

    # define a transformer: a function that given an initial position and a
    # transformation vector(given in terms of previous and current location)
    # returns the new position. In this case all we want to do is 'round' the
    # vector to the nearest multiple of our grid's cell size.
    def transform(self, start_position: Position,
                  previous_location: Point,
                  current_location: Point) -> Position:
        transformation_vector = current_location - previous_location
        rounder = partial(round_to_multiple_of, base=self.increment)
        resized = Vector(*map(rounder, transformation_vector))
        return start_position + resized

    # define _create_guides to determine what is shown once a manipulation
    # in this
    # mode begins
    def _create_guides(self, start_pos, previous_pos, current_pos, scale
                       ) -> typing.Sequence['Handle_AIS_Shape']:
        lines = []
        for direction, color in zip(current_pos.orientation,
                                    self.default_axis_colors):
            if direction.is_almost_equal(self.normal):
                continue
            line = make_ais_line(current_pos.location, direction)
            ais_set_style(line, color)
            lines.append(line)
        return lines

    # if you so desire, specify an _update_guides method to update
    # the guides during transformation. Example: turn cyan one of the axes
    # when you are currently aligned with it.
    def _update_guides(self, ais_shapes, initial_pos,
                       previous_pos, current_pos
                       ) -> UpdateAISShapeReturnType:
        vec = (current_pos - previous_pos)
        if vec.norm == 0:
            return
        colors = []
        directions = []
        for v, color in zip(current_pos.orientation,
                            self.default_axis_colors):
            if not v.is_almost_equal(self.normal):
                directions.append(v)
                colors.append(color)

        for ais_shape, color, direction in zip(
                ais_shapes, colors, directions):
            if abs(vec.normalized).is_almost_equal(direction):
                # highlight that we're moving along this axis
                ais_set_style(ais_shape, 'cyan')
            else:
                ais_set_style(ais_shape, color)


class GridHandle(HandleBase, RectangularFace):
    mode: GridTranslation = Input()

    reference = Input()
    normal = Input()

    @Attribute
    def position(self):
        return self.reference.align(self.reference.Vz,
                                    self.normal)


class GridGizmo(Gizmo):
    # we need to create a gizmo with some shapes that we can drag and drop
    # to use the grid manipulation mode.
    cell_size = Input(1)
    grid_translation_normals = Input(
        DEFAULT_AXES, widget=MultiCheckBox(DEFAULT_AXES,
                                           labels=list('xyz')))

    @Attribute
    def grid_modes(self):
        return self._get_modes_of_type(GridTranslation)

    # adding the grid handles as a part will make them higlightable and
    # draggable
    # during manipulation
    @Part
    def grid_handles(self):
        return GridHandle(width=self.size, length=self.size,  # noqa
                          quantify=len(self.grid_modes),
                          mode=self.grid_modes[child.index],
                          reference=self.position,
                          normal=self.grid_modes[child.index].normal,
                          color=self._to_color(child.mode)  # noqa
                          )


if __name__ == '__main__':
    class MyObj(Box, Manipulable):
        label = 'right-click me in the viewer to start manipulating'

        # instruct the Manipulable to use our gizmo subclass

        cell_size = Input(1)

        # determine which manipulation modes should be available
        # (warning: if you were to activate 'plane' as well, the gizmo shapes
        # would overlap with
        # those for the grid mode)
        @Attribute
        def modes(self):
            mode = GridTranslation(VX, show_guide=self.show_guides,
                                   increment=self.cell_size)
            return [mode, mode.copy(normal=VY), mode.copy(normal=VZ)]

        def on_submit(self, evt: EndEvent):
            self.position = evt.current_position

        @Attribute
        def gizmo(self):
            return GridGizmo(
                position=self.position,
                cell_size=self.cell_size,
                modes=self.modes
            )


    display([Box(
        1, 1, 1, centered=True, color='red', label='static box',
        position=Position().translate(x=1)),
        MyObj(
            1, 1, 1, centered=True,
            color='green')],
        autodraw=True)