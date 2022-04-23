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

"""This example shows how to use relative translation in
combination with rotation."""



from parapy.geom import Cube, VZ
from parapy.gui import Manipulable
from parapy.gui.manipulation import EndEvent
from parapy.gui.manipulation.modes import (
    PRIMARY_AXIS_ROTATIONS,
    Translation)


class AbsoluteTranslationCube(Cube, Manipulable):
    label = 'right-click me in the viewer to start manipulating'
    centered = True
    modes = PRIMARY_AXIS_ROTATIONS + (
        Translation(VZ, relative=False),)

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.gui import display

    obj = AbsoluteTranslationCube(1)
    display(obj)