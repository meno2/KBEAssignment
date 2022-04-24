from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve
from Airfoil import Airfoil
from ref_frame import Frame
from EndPlates import EndPlate
import numpy as np
from parapy.core.decorators import Action
from parapy.gui.wx_utils import popup


class WingElement(GeomBase):

    angleOfIncidence = Input(-20*np.pi/90)
    #liftCoefficient = Input()
    #dragCoefficient = Input()
    span = Input(1000)
    #meanChord = Input()
    twistDistribution = Input()
    airfoil_name=Input()
    chord=Input(500)

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
                           factor= self.chord,
                           mesh_deflection=0.0001)


    @Part   (in_tree=False)
    def airfoil21_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, 'y', self.span, "x", 1800), "x", 180, deg=True), "y", 500, "z", -800))

    @Part (in_tree=False)
    def airfoil21_scaled(self):
        return ScaledCurve(curve_in=self.airfoil21_unscaled,
                           reference_point=self.airfoil21_unscaled.start,
                           factor=self.chord,
                           mesh_deflection=0.0001)

    @Part
    def wing_loft_solid(self):  # generate a surface
        return LoftedSolid([self.airfoil1_scaled, self.airfoil21_scaled],
                             mesh_deflection=0.0001)

    # @Part(in_tree=False)
    # def airfoil22_unscaled(self):
    #     return Naca4AirfoilCurve(designation=self.airfoil_name,
    #                              position=translate(
    #                                  rotate(translate(self.position, 'y', self.span , "x", 1800), "x", 180,
    #                                         deg=True), "y", 500, "z", -800))

    # @Part(in_tree=False)
    # def airfoil22_scaled(self):
    #     return ScaledCurve(curve_in=self.airfoil22_unscaled,
    #                        reference_point=self.airfoil22_unscaled.start,
    #                        factor=self.chord,
    #                        mesh_deflection=0.0001)
    #
    # @Part(in_tree=False)
    # def airfoil22_scaled_rotated(self):
    #     return RotatedCurve(curve_in=self.airfoil22_scaled, angle=5*np.pi/180,
    #                         rotation_point=self.airfoil22_scaled.position, vector=Vector(0, 1, 0))

    # @Part(in_tree=False)
    # def airfoil21_scaled_rotated(self):
    #     return RotatedCurve(curve_in=self.airfoil21_scaled, angle=-2 * np.pi / 180,
    #                         rotation_point=self.airfoil21_scaled.position, vector=Vector(0, 1, 0))


    # @Part
    # def wing_loft_solid21(self):  # generate a surface
    #     return LoftedSolid([self.airfoil21_scaled_rotated, self.airfoil22_scaled_rotated],
    #                        mesh_deflection=0.0001)

    @Part (in_tree=False)
    def airfoil3_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, "z", 50, "x", 2200, "y", -500), "x", 180, deg=True), "z", -800))



    @Part (in_tree=False)
    def airfoil3_scaled(self):
        return ScaledCurve(curve_in=self.airfoil3_unscaled,
                           reference_point=self.airfoil3_unscaled.start,
                           factor=self.chord*0.8,
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
                           factor=self.chord*0.8,
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
                           factor=self.chord*0.5,
                           mesh_deflection=0.0001)

    @Part  (in_tree=False)
    def airfoil6_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, 'y', self.span, "z", 300, "x" , 2400), "x", 180, deg=True), "y", 500, "z", -800))


    @Part (in_tree= False)
    def airfoil6_scaled(self):
        return ScaledCurve(curve_in=self.airfoil6_unscaled,
                           reference_point=self.airfoil6_unscaled.start,
                           factor=self.chord*0.5,
                           mesh_deflection=0.0001)

    @Part(in_tree=False)
    def wing3_structure_shell(self):
        return LoftedShell([self.airfoil6_scaled, self.airfoil5_scaled])

    @Part (in_tree= False)
    def wing3_structure_thickshell(self):
        return ThickShell(built_from=self.wing3_structure_shell, offset = -0.0001*10**3)

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

    @Part
    def randombox(self):
        return Box(1,1,2,position=Position(Point(0, 0, 0)))

    @Part
    def randombox_translated(self):
        return TranslatedShape(shape_in = self.randombox, displacement=Vector(-self.randombox.cog[0], -self.randombox.cog[1], -self.randombox.cog[2]))


    @Action
    def beambending(self):

        density = 1400 #kg/m3
        Emod = 56.9 * 10**9 #Pa

        Ixx = self.wing3_structure_thickshell.matrix_of_inertia[0][0] * density/((10**3)**5)
        Iyy = self.wing3_structure_thickshell.matrix_of_inertia[1][1] * density/((10**3)**5)
        Izz = self.wing3_structure_thickshell.matrix_of_inertia[2][2] * density/((10**3)**5)

        print(Ixx, Iyy, Izz)

        length = (self.airfoil6_scaled.position[1] - self.airfoil5_scaled.position[1])/1000
        load = 250
        deflection = load*length**3/(48*Iyy*Emod)

        popupstring = str(("With a load of "+ str(load)+ "N on wing 3, the deflection is found to be " + str(deflection)+  " mm"))
        popup("Calculated Deflection", popupstring, cancel_button=False)




if __name__ == '__main__':
    from parapy.gui import display

    obj = WingElement(label="aircraft",
                      airfoil_name="2412"
                      )
    display(obj)


