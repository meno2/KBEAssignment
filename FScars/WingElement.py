from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve
from Airfoil import Airfoil
from ref_frame import Frame
from EndPlates import EndPlate


class WingElement(GeomBase):
    angleOfIncidence = Input()
    liftCoefficient = Input()
    dragCoefficient = Input()
    span = Input()
    meanChord = Input()
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


    @Part  # (in_tree=False)
    def airfoil1_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name)

    @Part
    def airfoil1_scaled(self):
        return ScaledCurve(curve_in= self.airfoil1_unscaled,
                           reference_point= self.airfoil1_unscaled.start,
                           factor= 0.5,
                           mesh_deflection=0.0001)


    @Part  # (in_tree=False)
    def airfoil2_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(self.position, 'y', 1))

    @Part
    def airfoil2_scaled(self):
        return ScaledCurve(curve_in=self.airfoil2_unscaled,
                           reference_point=self.airfoil2_unscaled.start,
                           factor=0.5,
                           mesh_deflection=0.0001)

    @Part
    def wing_loft_surf(self):  # generate a surface
        return LoftedSurface([self.airfoil1_scaled, self.airfoil2_scaled],
                             mesh_deflection=0.0001)

    @Part  # (in_tree=False)
    def airfoil3_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(self.position, "z", 0.25))

    # @Part  # (in_tree=False)
    # def airfoil3_unscaled(self):
    #     return Naca4AirfoilCurve(designation=self.airfoil_name,
    #                              position=translate(rotate(self.position, Vector(0, 1, 0), 45, deg=True), "z", 0.5, "x",
    #                                                 -0.5))

    @Part
    def airfoil3_scaled(self):
        return ScaledCurve(curve_in=self.airfoil3_unscaled,
                           reference_point=self.airfoil3_unscaled.start,
                           factor=0.5,
                           mesh_deflection=0.0001)

    @Part  # (in_tree=False)
    def airfoil4_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(translate(self.position, 'y', 1),
                                                    "z", 0.25))

    # @Part  # (in_tree=False)
    # def airfoil4_unscaled(self):
    #     return Naca4AirfoilCurve(designation=self.airfoil_name,
    #                              position=translate(
    #                                  rotate(translate(self.position, 'y', 1), Vector(0, 1, 0), 45, deg=True),
    #                                  "z", 0.5, "x", -0.5))


    @Part
    def airfoil4_scaled(self):
        return ScaledCurve(curve_in=self.airfoil4_unscaled,
                           reference_point=self.airfoil4_unscaled.start,
                           factor=0.5,
                           mesh_deflection=0.0001)

    @Part
    def wing_loft_surf2(self):  # generate a surface
        return LoftedSurface([self.airfoil3_scaled, self.airfoil4_scaled],

                             mesh_deflection=0.0001)

    @Part  # (in_tree=False)
    def airfoil5_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(self.position, "z", 0.5))

    # @Part  # (in_tree=False)
    # def airfoil5_unscaled(self):
    #     return Naca4AirfoilCurve(designation=self.airfoil_name,
    #                              position=rotate(translate(self.position, "z", 0.5), "y", 80, deg=True))

    @Part
    def airfoil5_scaled(self):
        return ScaledCurve(curve_in=self.airfoil5_unscaled,
                           reference_point=self.airfoil5_unscaled.start,
                           factor=0.5,
                           mesh_deflection=0.0001)

    @Part  # (in_tree=False)
    def airfoil6_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(translate(self.position, 'y', 1), "z", 0.5))
    #
    # @Part  # (in_tree=False)
    # def airfoil6_unscaled(self):
    #     return Naca4AirfoilCurve(designation=self.airfoil_name,
    #                              position=rotate(translate(translate(self.position, 'y', 1), "z", 0.5), "y", 80,
    #                                              deg=True))

    @Part
    def airfoil6_scaled(self):
        return ScaledCurve(curve_in=self.airfoil6_unscaled,
                           reference_point=self.airfoil6_unscaled.start,
                           factor=0.5,
                           mesh_deflection=0.0001)
    @Part
    def wing_loft_surf3(self):  # generate a surface
        return LoftedSurface([self.airfoil5_scaled, self.airfoil6_scaled],
                             mesh_deflection=0.0001)

if __name__ == '__main__':
    from parapy.gui import display

    obj = WingElement(label="aircraft",
                      airfoil_name="2412"
                      )
    display(obj)


