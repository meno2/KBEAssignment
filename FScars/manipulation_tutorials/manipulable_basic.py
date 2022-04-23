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

"""This example shows how to make an object manipulable by using the
ManipulableBase mixin."""



from parapy.geom import Cube
from parapy.gui.manipulation import (
    EndEvent, ManipulableBase)
from parapy.gui.manipulation.modes import ALL_TRANSFORMATIONS


class ManipulableCube(ManipulableBase, Cube):
    label = 'right-click me in the viewer to start manipulating'
    centered = True

    modes = ALL_TRANSFORMATIONS

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position


if __name__ == '__main__':
    from parapy.gui import display

    obj = ManipulableCube(2)
    display(obj)