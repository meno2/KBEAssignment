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

"""In this example we demonstrate the 'relative' and 'relative_center' options
 of Rotation.
"""


from parapy.core import Input
from parapy.core.widgets import CheckBox
from parapy.geom import Cube, VZ, VX, Point
from parapy.gui.manipulation import (
    EndEvent, Manipulable, Rotation, Translation)




class RotateExample(Cube, Manipulable):
    label = 'right-click me in the viewer to start manipulating'

    centered = True
    # whether the rotation normal is relative to the object's position
    # during manipulation, or not. If False, rotating the object with the
    # VX handle will not rotate the normal for the VZ rotation handle.
    normal_relative = Input(True, widget=CheckBox)
    center_relative = Input(True, widget=CheckBox)
    offset = Input(1)

    # do not invalidate on position change
    @property
    def modes(self):
        return (Rotation(VZ,
                         center=Point(self.offset, 0, 0),
                         relative=self.normal_relative,
                         relative_center=self.center_relative,
                         handle_color='blue',
                         show_guide=True),
                Rotation(VX, handle_color='red', show_guide=True),
                Translation(VZ, show_guide=True, handle_color='green'))

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.gui import display

    obj = RotateExample(1)
    display(obj)