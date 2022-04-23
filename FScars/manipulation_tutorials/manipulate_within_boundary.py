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

"""This example shows how to use on_motion to constrain the object's translation
to inside a given volume.
"""


from parapy.core import Attribute
from parapy.geom import Cube, Box
from parapy.gui import Manipulable
from parapy.gui.manipulation import EndEvent, MotionEvent


class PlaneBoundCube(Cube, Manipulable):
    label = 'right-click me in the viewer to start manipulating'
    centered = True

    @Attribute(in_tree=True)
    def boundary(self):
        edges = Box(4, 4, 2, centered=True, color='blue', transparency=.2).edges
        for e in edges:
            e.color = 'red'
        return edges

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

    obj = PlaneBoundCube(1)
    display(obj)