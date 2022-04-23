from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve
from Airfoil import Airfoil
from ref_frame import Frame
from EndPlates import EndPlate
import numpy as np


class WingElement(GeomBase):

    angleOfIncidence = Input(-20*np.pi/90)
    #liftCoefficient = Input()
    #dragCoefficient = Input()
    span = Input(1000)
    #meanChord = Input()
    twistDistribution = Input()
    airfoil_name=Input()
    chord=Input()

    @Part
    def aircraft_frame(self):
        return Frame(pos=self.position)  # this helps visualizing the aircraft reference frame, /
        # which, in this case, is the same as the global reference frame XOY)
    @Part
    def wing_frame(self):
        return Frame(pos=self.position)


    @Part   (in_tree=False)
    def airfoil1_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position= translate(rotate(self.position, "x", 180, deg=True), "x", 1800, "y", 500,"z", -800))

    @Part (in_tree= False)
    def airfoil1_scaled(self):
        return ScaledCurve(curve_in= self.airfoil1_unscaled,
                           reference_point= self.airfoil1_unscaled.end,
                           factor= 500,
                           mesh_deflection=0.0001)


    @Part   (in_tree=False)
    def airfoil2_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, 'y', self.span, "x", 1800), "x", 180, deg=True), "y", 500, "z", -800))

    @Part (in_tree=False)
    def airfoil2_scaled(self):
        return ScaledCurve(curve_in=self.airfoil2_unscaled,
                           reference_point=self.airfoil2_unscaled.start,
                           factor=500,
                           mesh_deflection=0.0001)


    # @Part
    # def wing_loft_surf(self):  # generate a surface
    #     return LoftedSurface([self.airfoil1_scaled, self.airfoil2_scaled],
    #                          mesh_deflection=0.0001)

    @Part
    def wing_loft_solid(self):  # generate a surface
        return LoftedSolid([self.airfoil1_scaled, self.airfoil2_scaled],
                             mesh_deflection=0.0001)

    @Part (in_tree=False)
    def airfoil3_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, "z", 50, "x", 2200, "y", -500), "x", 180, deg=True), "z", -800))



    @Part (in_tree=False)
    def airfoil3_scaled(self):
        return ScaledCurve(curve_in=self.airfoil3_unscaled,
                           reference_point=self.airfoil3_unscaled.start,
                           factor=500,
                           mesh_deflection=0.0001)

    @Part (in_tree=False)
    def airfoil4_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, 'y', self.span, "z", 50, "x", 2200), "x", 180, deg=True
                                                    ),"y", 500, "z", -800))

    @Part (in_tree= False)
    def airfoil3_scaled_rotated(self):
        return RotatedCurve(curve_in = self.airfoil3_scaled, angle = self.angleOfIncidence, rotation_point = self.airfoil3_scaled.position, vector = Vector(0,1,0))

    @Part (in_tree= False)
    def airfoil4_scaled_rotated(self):
        return RotatedCurve(curve_in = self.airfoil4_scaled, angle = self.angleOfIncidence, rotation_point = self.airfoil4_scaled.position, vector = Vector(0,1,0))



    @Part (in_tree= False)
    def airfoil4_scaled(self):
        return ScaledCurve(curve_in=self.airfoil4_unscaled,
                           reference_point=self.airfoil4_unscaled.start,
                           factor=500,
                           mesh_deflection=0.0001)



    @Part
    def wing_loft_solid2(self):  # generate a surface
        return LoftedSolid([self.airfoil3_scaled_rotated, self.airfoil4_scaled_rotated],

                             mesh_deflection=0.0001)

    @Part   (in_tree=False)
    def airfoil5_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, "z", 300, "x", 2400, "y", -500), "x", 180, deg=True), "z", -800))



    @Part (in_tree=False)
    def airfoil5_scaled(self):
        return ScaledCurve(curve_in=self.airfoil5_unscaled,
                           reference_point=self.airfoil5_unscaled.start,
                           factor=500,
                           mesh_deflection=0.0001)

    @Part  (in_tree=False)
    def airfoil6_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, 'y', self.span, "z", 300, "x" , 2400), "x", 180, deg=True), "y", 500, "z", -800))


    @Part (in_tree= False)
    def airfoil6_scaled(self):
        return ScaledCurve(curve_in=self.airfoil6_unscaled,
                           reference_point=self.airfoil6_unscaled.start,
                           factor=500,
                           mesh_deflection=0.0001)

    @Part (in_tree= False)
    def airfoil5_scaled_rotated(self):
        return RotatedCurve(curve_in=self.airfoil5_scaled, angle=-80 * np.pi / 180,
                            rotation_point=self.airfoil5_scaled.position, vector=Vector(0, 1, 0))

    @Part (in_tree=False)
    def airfoil6_scaled_rotated(self):
        return RotatedCurve(curve_in=self.airfoil6_scaled, angle=-80 * np.pi / 180,
                            rotation_point=self.airfoil6_scaled.position, vector=Vector(0, 1, 0))
    @Part
    def wing_loft_solid3(self):  # generate a surface
        return LoftedSolid([self.airfoil5_scaled_rotated, self.airfoil6_scaled_rotated],
                             mesh_deflection=0.0001)
    # @Part
    # def airfoil1_scaled_edits(self):
    #     return RotatedCurve(curve_in = self.airfoil1_scaled, angle = 20*np.pi/90, rotation_point = self.airfoil1_scaled.position, vector = Vector(0,1,0))

if __name__ == '__main__':
    from parapy.gui import display

    obj = WingElement(label="aircraft",
                      airfoil_name="2412"
                      )
    display(obj)


