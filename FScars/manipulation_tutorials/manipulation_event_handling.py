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

"""Example showing how to make a manipulable plane and use it to split
a Sphere while limiting the motion of the Manipulable Plane, only allowing
to drag along the z-axis, showing an alternative ghost and placing the
Manipulator on a different Position.
"""

"""This example demonstrates how to use on_setup and on_teardown to display a 
text label in the viewer during manipulation and clean it up afterwards. 
"""


import math

from parapy.core import Attribute
from parapy.core import Input, HiddenPart, Part
from parapy.geom import GeomBase, Box, SubtractedSolid, Sphere, HalfSpaceSolid
from parapy.geom import (
    Plane, Position, RectangularFace, rotate, TextLabel)
from parapy.gui.manipulation import Manipulable, EndEvent, MotionEvent


class ManipulablePlane(Plane, Manipulable):
    label = "right-click me in the viewer"

    # flips the direction for translation at runtime
    flip = Input(False)

    # allow rotating around x
    rotation_normals = ['x']

    @Part(in_tree=False)
    def ghost(self):
        """The 'ghost' that is dragged along with the gizmo.

        One can specify any :class:`~parapy.core.abstract.DrawableParapyObject`
        that will act as a ghost. If set to self, the manipulable object itself
        will move. Set the ghost to :py:`None` if no shape, apart from the
        gizmo, should move along with the manipulation.

        .. caution:: the ghost should not be updated/changed when
            the manipulation :attr:`is_active`.

        :rtype: parapy.core.abstract.DrawableParapyObject | None
        """
        return RectangularFace(width=self.v_dim,
                               length=self.v_dim,
                               display_mode='shaded',
                               transparency=.5,
                               color='red')

    @Attribute
    def gizmo_position(self):
        # override the position at which the gizmo is shown
        # show the gizmo in the corner of the ghost
        position = Position(self.ghost.points[1], self.orientation)

        if self.flip:
            position = rotate(position, 'x', math.pi)

        return position

    @Part(in_tree=False)
    def text_label(self):
        return TextLabel(text='Chop me!',
                         size=50,
                         position=self.position.translate(x=2.5, y=2.5),
                         color='blue')

    def on_setup(self, viewer):
        viewer.display([self.text_label])
        viewer.refresh(True)

    def on_teardown(self, viewer):
        viewer.hide([self.text_label])
        viewer.refresh(True)

    def on_submit(self, evt: EndEvent):
        """override this method to handle the manipulation events.
        """
        self.reference = evt.current_position

    def on_motion(self, evt: MotionEvent):
        """override this method to handle the manipulation events.
        """
        current_position = evt.current_position
        if current_position.z < -1:  # Override it to be z=-1
            location = current_position.location.replace(z=-1)
            evt.current_position = current_position.replace(location=location)
        elif current_position.z > 1:  # Override it to be z=1
            location = current_position.location.replace(z=1)
            evt.current_position = current_position.replace(location=location)


class HollowSphereSplitter(GeomBase):
    __initargs__ = "splitting_plane"
    radius = Input(1)
    splitting_plane: Plane = Input(in_tree=True)

    @HiddenPart
    def box(self):
        return Box(self.radius * 1.1, self.radius * 1.1,
                   self.radius * 1.1, centered=True)

    @HiddenPart
    def sphere(self):
        return SubtractedSolid(
            Sphere(radius=self.radius,
                   transparency=0.9,
                   color="blue"), self.box)

    @Part(in_tree=False)
    def half_space_solid(self):
        return HalfSpaceSolid(self.splitting_plane)

    @Part
    def result(self):
        return SubtractedSolid(self.sphere, self.half_space_solid,
                               color="green")


if __name__ == '__main__':
    from parapy.gui import display

    obj = HollowSphereSplitter(ManipulablePlane(v_dim=4))
    display(obj)