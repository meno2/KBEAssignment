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

"""This example shows how to make an object manipulable in the viewer without
inheriting from ManipulableBase, managing the Manipulation context manually."""


from parapy.core import action, Input
from parapy.core.widgets import Dropdown
from parapy.geom import Cube
from parapy.gui.manipulation import (
    EndEvent, Manipulation, Gizmo,
    PRIMARY_AXIS_TRANSLATIONS, PRIMARY_AXIS_PLANAR_TRANSLATIONS,
    PRIMARY_AXIS_ROTATIONS)
from parapy.gui.manipulation.modes import ALL_TRANSFORMATIONS

trsl_options = [
    PRIMARY_AXIS_TRANSLATIONS,
    PRIMARY_AXIS_TRANSLATIONS + PRIMARY_AXIS_PLANAR_TRANSLATIONS,
    PRIMARY_AXIS_TRANSLATIONS + PRIMARY_AXIS_ROTATIONS,
    ALL_TRANSFORMATIONS,
]


class MyCube(Cube):
    label = "click on the 'manipulate' action to start"

    centered = True

    transformations = Input(PRIMARY_AXIS_TRANSLATIONS, widget=Dropdown(
        labels=['translations only', 'translations + planar',
                'translations + rotations', 'all'], values=trsl_options))

    def on_submit(self, evt: EndEvent):
        self.position = evt.current_position

    @action
    def manipulate(self):
        viewer = get_top_window().viewer
        gizmo = Gizmo(position=self.position,
                      modes=self.transformations)

        manipulation = Manipulation(self, viewer, gizmo,
                                    ghost=self,
                                    on_submit=self.on_submit)
        manipulation.start()


if __name__ == '__main__':
    from parapy.gui import display, get_top_window

    obj = MyCube(2)
    display([obj, Cube(.5),
             Cube(.6, color='red', position=obj.position.translate(x=3))])