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

"""This example is about creating custom ManipulationModes that override
the default ones' guides.
We create:
 MyColorChangeMode: a Translation Mode whose guides change color during
    manipulation, based on the total translation distance;
 MyReplaceMode: a Translation Mode whose guides are replaced by guides with
    a different shape (circles) based on whether the current position is
    inside a boundary area;
 MyOtherMode: a Rotation Mode replacing the default 'line-and-circle' guide with
    a pair of cones indicating the rotation center and normal.

Display and right-click MyCube in the viewer to start manipulating.
"""


import typing

from OCC.gui.interactive_objects import make_ais_coloredshape

from parapy.geom import LineSegment, Position, Cone
from parapy.gui.manipulation import Translation, Rotation
from parapy.gui.manipulation.modes import UpdateAISShapeReturnType
from parapy.gui.manipulation.utils import ais_set_style

if typing.TYPE_CHECKING:
    from OCC.wrapper.AIS import Handle_AIS_Shape  # noqa


class MyColorChangeMode(Translation):
    """an axis mode that colors the guide green when within 10 world units
    of the start position; after that, the line becomes red
    """

    def _create_guides(self, start_pos, previous_pos, current_pos,
                       scale) -> typing.Sequence['Handle_AIS_Shape']:
        ais = super()._create_guides(start_pos, previous_pos,
                                     current_pos, scale)[0]
        ais_set_style(ais, color='green')
        return [ais]  # return a sequence

    def _update_guides(self, ais_shapes,
                       initial_pos: Position,
                       previous_pos: Position,
                       current_pos: Position
                       ) -> UpdateAISShapeReturnType:
        ais = ais_shapes[0]  # the colored ais LineSegment

        # a red circle replaces the old ais shape if we're further
        # than 10 world units; else we use the default linesegment.
        color = 'green'
        if (current_pos - initial_pos).length > 10:
            color = 'red'
        ais_set_style(ais, color=color)
        return None


class MyReplaceMode(Translation):
    """an axis mode that uses a green segment as guide when within 10 world
    units
    of the start position; after that, replaces it with a red circle.
    """

    def _create_guides(self, start_pos, previous_pos, current_pos,
                       scale) -> typing.Sequence['Handle_AIS_Shape']:
        # replace the default black line with a green segment
        # give the end poitn a little offset to avoid overlapping start/end
        segment = LineSegment(previous_pos,
                              current_pos + self.axis * 0.001)
        # make_ais_coloredshape sometimes misbehaves
        ais = make_ais_coloredshape(segment.TopoDS_Shape)
        ais_set_style(ais, color='green')
        return [ais]  # return a sequence

    def _update_guides(self, ais_shapes,
                       initial_pos: Position,
                       previous_pos: Position,
                       current_pos: Position
                       ) -> UpdateAISShapeReturnType:
        ais = ais_shapes[0]  # the colored ais LineSegment
        # a red circle replaces the old ais shape if we're further
        # than 10 world units; else we use the default linesegment.
        if (current_pos - initial_pos).length > 10:
            color, transparency = (150, 0, 0), 0
            circle = Circle(position=current_pos, radius=1, color=color,
                            transparency=transparency)
            new_ais = make_ais_coloredshape(circle.TopoDS_Shape)
            return ((ais, new_ais),)

        new_ais = \
            self._create_guides(initial_pos, previous_pos, current_pos, 1)[0]
        return ((ais, new_ais),)


class MyOtherMode(Rotation):
    # a rotation mode that instead of the default 'line and circle' guide
    # has two cones to mark the rotation normal.

    def _make_ais_cone(self, position):
        cone = Cone(radius1=.5, radius2=0, height=1.5,
                    position=position.translate(z_=1.5))
        ais_cone = make_ais_coloredshape(cone.TopoDS_Shape)
        ais_set_style(ais_cone, color='purple', transp=.5)
        return ais_cone

    def _create_guides(self, start_pos, previous_pos, current_pos,
                       scale) -> typing.Sequence['Handle_AIS_Shape']:
        pos = Position(self.center)
        ais_cone_top = self._make_ais_cone(pos.align(pos.Vz, -self.normal,
                                                     warn=False))
        ais_cone_bot = self._make_ais_cone(pos.align(pos.Vz, self.normal,
                                                     warn=False))
        return [ais_cone_top, ais_cone_bot]


if __name__ == '__main__':
    from parapy.gui import display, Manipulable
    from parapy.geom import Cube, Circle, Point
    from parapy.core import Part
    from parapy.gui.manipulation import EndEvent


    class MyCube(Cube, Manipulable):
        label = "right click me in the viewer to start manipulating"
        centered = True

        @Part
        def green_zone(self):
            return Circle(radius=10, position=self.position, color='green')

        modes = [
            MyColorChangeMode('x', show_guide=True),
            MyReplaceMode('y', show_guide=True),
            MyOtherMode('z', show_guide=True, center=Point(),
                        relative_center=False)]

        def on_submit(self, evt: EndEvent):
            self.position = evt.current_position


    obj = MyCube(1)
    display(obj)