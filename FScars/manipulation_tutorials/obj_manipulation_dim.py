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
LengthDimension in the viewer during manipulation and clean it up afterwards,
and how to use on_motion to update it. 
"""


from parapy.core import Input
from parapy.core.widgets import CheckBox
from parapy.geom import (
    Plane, Position, LengthDimension)
from parapy.gui import Manipulable


class ManipulablePlane(Plane, Manipulable):
    label = "right-click me in the viewer"

    dim_relative_to_starting_point = Input(True, widget=CheckBox)

    _dim = None
    _dim_displayed = None

    def on_setup(self, viewer):
        self.create_dimension()

    def on_teardown(self, viewer):
        self.remove_dimension(viewer)
        viewer.refresh()

    def on_submit(self, evt):
        """override this method to handle the manipulation events.
        """
        self.reference = evt.current_position

    def on_motion(self, evt):
        """override this method to handle the manipulation events.
        """
        if self.dim_relative_to_starting_point:
            previous_pos = evt.start_position
        else:
            previous_pos = evt.previous_position
        self.update_dimension(previous_pos,
                              evt.current_position,
                              evt.source)

    def create_dimension(self):
        # create a LengthDimension
        start_loc = self.location
        plane = Plane(reference=start_loc, normal=self.position.Vz)
        dim = LengthDimension(start_loc, start_loc, in_plane=plane,
                              text="{value:1.2f}",
                              dimension_scale=0.1,
                              fly_out=1.5)
        self._dim = dim
        self._dim_displayed = False

    def update_dimension(self, start_position, current_position, viewer):
        dim = self._dim
        dim_displayed = self._dim_displayed
        if current_position == start_position:
            # remove the dimension if there is no distance to display
            if dim_displayed:
                self._dim_displayed = False
                viewer.remove([dim])
        else:
            dim.other_shape = current_position  # update dimension object
            if not dim_displayed:
                self._dim_displayed = True
                viewer.display([dim])
            else:
                viewer.refresh()  # flush dimension-bound listeners

    def remove_dimension(self, viewer):
        dim = self._dim
        if self._dim_displayed:
            viewer.remove([dim], update=True)
            self._dim_displayed = False
        self._dim = None


if __name__ == '__main__':
    from parapy.gui import display

    obj = ManipulablePlane(v_dim=4,
                           translation_axes=['x', 'y'],
                           rotation_normals=[],
                           plane_normals=['z'])
    display((Position(), obj))