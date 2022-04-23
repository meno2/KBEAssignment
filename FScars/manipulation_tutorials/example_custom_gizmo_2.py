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

"""this example shows how to create a custom generic Gizmo replacing
the '2d' look of the default Gizmo with a 3d one.
Run the example, then right click on the MyBase's shape in the viewer
to start manipulating it.
"""


import typing

from parapy.cae.nastran import Arrow
from parapy.core import Input, Attribute, Part, child
from parapy.geom import (
    CircularFace, Position, Sphere, BRep,
    RectangularFace, Compound)
from parapy.gui.manipulation import Gizmo
from parapy.gui.manipulation.gizmo import HandleBase
from parapy.gui.manipulation.modes import (
    Translation,
    PlanarTranslation, Rotation)


class AxisHandle(HandleBase, Compound):
    mode: Translation = Input()
    head_length = Input()
    double = Input(False)
    reference: Position = Input()

    @Attribute
    def direction(self):
        return self.transformed_mode.axis

    @Part
    def built_from(self):
        return Arrow(
            quantify=2 if self.double else 1,
            point=self.reference.location,
            direction=-self.direction if child.index else self.direction,
            head_length=self.head_length,
        )


class PlanarHandle(HandleBase, CircularFace):
    mode: PlanarTranslation = Input()
    reference: Position = Input()

    @Attribute
    def face_normal(self):
        return self.transformed_mode.normal

    @Attribute
    def position(self):
        reference = self.reference
        vz = self.face_normal
        reference_z = reference.Vz
        if reference_z.is_almost_equal(vz):
            return reference
        return reference.align(reference_z, vz)


class RotationHandle(HandleBase, RectangularFace):
    mode: Rotation = Input()
    distance = Input()
    size = Input(1)
    reference: Position = Input()

    @Attribute
    def width(self):
        return self.size / 3

    @Attribute
    def length(self):
        return self.size / 3

    @Attribute
    def face_normal(self):
        return self.transformed_mode.normal

    @Attribute
    def position(self):
        reference = self.reference
        vz = self.face_normal
        reference_z = reference.Vz
        if reference_z.is_almost_equal(vz):  # avoid collision between z and y
            reference = reference.rotate(z=90, deg=True)
        else:
            reference = reference.align(reference_z, vz)
        return reference.translate(x=self.distance * self.size
                                   ).rotate(z=45, deg=True)


class MyGizmo(Gizmo):
    #: distance of rotation handle from self (scaled internally)
    #: :type: numbers.Number
    rotation_handle_distance = Input(1.6)

    #: toggles whether translation arrows for the 'axis' mode should be
    # displayed
    #: both in the positive and the negative direction of the
    # translation_axes. If False:
    #: arrows only on 'positive' axis direction. If True: also 'negative'. If
    # None: negative only.
    #: typing.Optional[bool]
    bidirectional_arrows = Input(True)

    @Part
    def arrows(self):
        return AxisHandle(
            quantify=len(self._axis_modes),
            mode=self._axis_modes[child.index],
            reference=self.position,
            double=self.bidirectional_arrows,
            color=self._to_color(child.mode),
            head_length=self.size / 3)

    @Part(in_tree=False)
    def _planar_handles(self):
        return PlanarHandle(
            quantify=len(self._plane_modes),
            mode=self._plane_modes[child.index],
            reference=self.position,
            radius=self.size,
            color=self._to_color(child.mode)
        )

    @Part(in_tree=False)
    def _center_sphere(self):
        return Sphere(radius=self.size / 10,
                      color=self.center_color)

    @Attribute(in_tree=True)
    def center(self) -> typing.Sequence[BRep]:
        if self._plane_modes:
            return self._planar_handles
        return [self._center_sphere]

    @Part
    def rotation_handles(self):
        return RotationHandle(
            quantify=len(self._rotation_modes),
            mode=self._rotation_modes[child.index],
            reference=self.position,
            size=self.size,
            distance=self.rotation_handle_distance,
            color=self._to_color(child.mode),
        )


if __name__ == '__main__':
    from parapy.geom import Cube
    from parapy.gui import display
    from parapy.gui.manipulation.modes import ALL_TRANSFORMATIONS
    from parapy.gui import Manipulable


    class MyBase(Manipulable, Cube):
        label = 'right-click me in the viewer to start manipulating'
        dimension = 1
        modes = ALL_TRANSFORMATIONS
        GIZMO_CLS = MyGizmo

        def on_submit(self, evt):
            self.position = evt.current_position


    display(MyBase())