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

"""The purpose of this example is to show that you can manipulate an object
in arbitrary directions/modes, as many of them at a time as you like.
"""


from parapy.core import Part
from parapy.geom import Vector, Cube, Plane, Point
from parapy.gui import Manipulable
from parapy.gui.manipulation import (
    Translation, Rotation, MotionEvent, EndEvent)


def fan_out(vector: Vector, normal: Vector, n=10):
    step = 180 / n
    for i in range(n):
        yield vector.rotate(normal, i * step, deg=True)


class FunkyVectorCube(Cube, Manipulable):
    label = 'right-click me in the viewer to start manipulating'
    centered = True

    # crazy amount of funky modes
    modes = (
            list(map(
                Translation,
                fan_out(Vector(1, 0, 0), Vector(0, 0, 1)))) +
            list(map(
                Rotation,
                fan_out(Vector(0, 0, 1), Vector(0, 1, 0))))
    )

    @Part
    def plane(self):
        return Plane(display_mode='shaded', color='blue', v_dim=4,
                     transparency=.2,
                     reference=Point(), normal=Vector(0, 0, 1))

    def on_motion(self, evt: MotionEvent):
        current_position = evt.current_position
        if -2 > current_position.y or current_position.y > 2:
            evt.Veto()
        if -2 > current_position.x or current_position.x > 2:
            evt.Veto()
        if -1 > current_position.z or current_position.z > 1:
            evt.Veto()

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.gui import display

    obj = FunkyVectorCube(1)
    display(obj)