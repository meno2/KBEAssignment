from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve

from ref_frame import Frame

import numpy as np
from parapy.core.decorators import Action
from parapy.gui.wx_utils import popup


class WingElement(GeomBase):

    angleOfIncidence = Input(-20*np.pi/90)
    span = Input(1000)
    airfoil_name = Input("2412")
    chord = Input(500)

    Emod = Input(56.9*10**9)

    wing1_skin_thickness = Input(0.0001*10**3)
    wing2_skin_thickness = Input(0.0001*10**3)
    wing3_skin_thickness = Input(0.0001*10**3)


    @Part
    def ref_frame(self):
        return Frame(pos=self.position)  # this helps visualizing the aircraft reference frame, /
        # which, in this case, is the same as the global reference frame XOY)

    #here we get the airfoil from KBEutils

    @Part  (in_tree=False)
    def airfoil1_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position= translate(rotate(self.position, "x", 180, deg=True), "x", 1800, "y", 500,"z", -800))

    @Part (in_tree= False) # the airfoil is scaled to suitable  size
    def airfoil1_scaled(self):
        return ScaledCurve(curve_in= self.airfoil1_unscaled,
                           reference_point= self.airfoil1_unscaled.end,
                           factor= self.chord,
                           mesh_deflection=0.0001)


    @Part   (in_tree=False)
    def airfoil2_unscaled(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name,
                                 position=translate(rotate(translate(self.position, 'y', self.span, "x", 1800), "x", 180, deg=True), "y", 500, "z", -800))

    @Part (in_tree=False)
    def airfoil2_scaled(self):
        return ScaledCurve(curve_in=self.airfoil2_unscaled,
                           reference_point=self.airfoil2_unscaled.start,
                           factor=self.chord,
                           mesh_deflection=0.0001)

    @Part
    def wing_loft_solid(self):  # generate the wing solid
        return LoftedSolid([self.airfoil1_scaled, self.airfoil2_scaled],
                           mesh_deflection=0.0001)


    ##
    ## Structures Module for wing 1:
    ##

    @Part(in_tree=False)
    def wing1_structure_shell(self):
        return LoftedShell([self.airfoil2_scaled, self.airfoil1_scaled])

    @Part(in_tree=False)
    def wing1_line1(self):
        return LineSegment(start=self.wing1_structure_shell.edges[1].start, end=self.wing1_structure_shell.edges[1].end)

    @Part(in_tree=False)
    def wing1_line2(self):
        return LineSegment(start=self.wing1_structure_shell.edges[1].start, end=(self.wing1_structure_shell.edges[1].start-Point(5,0,0)))

    @Part(in_tree=False)
    def wing1_line3(self):
        return LineSegment(start=self.wing1_structure_shell.edges[1].end, end = (self.wing1_structure_shell.edges[1].end-Point(5,0,0)))

    @Part(in_tree=False)
    def wing1_line4(self):
        return LineSegment(start=(self.wing1_structure_shell.edges[1].start-Point(5,0,0)), end=(self.wing1_structure_shell.edges[1].end-Point(5,0,0)))

    @Part(in_tree=False)
    def wing1_filledsurface(self):
        return FilledSurface(curves=[self.wing1_line1, self.wing1_line2, self.wing1_line3, self.wing1_line4])

    @Part(in_tree=False)
    def wing1_structure(self):
        return LoftedSolid([self.airfoil2_scaled, self.airfoil1_scaled])

    @Part(in_tree=False)
    def wing1_extrudedsolid(self):
        return ExtrudedShell(profile=self.wing1_filledsurface, distance=100, mirrored_extent=True)

    @Part(in_tree=False)
    def wing1_subtractshell(self):
        return Subtracted(shape_in=self.wing1_structure, tool=self.wing1_extrudedsolid.bbox.box)

    @Part(in_tree=False)
    def wing1_fusedshell(self):
        return FusedShell(shape_in=self.wing1_subtractshell.faces[0], tool=self.wing1_subtractshell.faces[1])

    @Part(in_tree=False)
    def wing1_structure_thickshell2(self):
        return ThickShell(built_from=self.wing1_fusedshell, offset = -self.wing1_skin_thickness)

    @Attribute
    @Action
    def Airfoil1bending(self):
        iyy = self.wing1_structure_thickshell2.faces[2].matrix_of_inertia[1][1]*10**-16

        length = (self.airfoil2_scaled.position[1] - self.airfoil1_scaled.position[1])/1000
        load = 200
        deflection = load*length**3/(48*iyy*self.Emod)

        popupstring = str(("With a load of "+ str(load)+ "N on wing 1, the deflection is found to be " + str(round(deflection,3))+  " mm"))
        popup("Calculated Deflection", popupstring, cancel_button=False)

        if deflection/load > 10/200:
            popupstring = str("Warning! Deflections exceed the maximum allowable deflections according to "
                              "Formula Student regulations! Consider changing the geometry or ply thickness.")
            popup("Warning!", popupstring, cancel_button=False)

    ##
    ## Defining Wing 2:
    ##

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


    ##
    ## Structures Module for wing 2:
    ##

    @Part(in_tree=False)
    def wing2_structure_shell(self):
        return LoftedShell([self.airfoil4_scaled, self.airfoil3_scaled])

    @Part(in_tree=False)
    def wing2_line1(self):
        return LineSegment(start=self.wing2_structure_shell.edges[1].start, end=self.wing2_structure_shell.edges[1].end)

    @Part(in_tree=False)
    def wing2_line2(self):
        return LineSegment(start=self.wing2_structure_shell.edges[1].start, end=(self.wing2_structure_shell.edges[1].start-Point(5,0,0)))

    @Part(in_tree=False)
    def wing2_line3(self):
        return LineSegment(start=self.wing2_structure_shell.edges[1].end, end = (self.wing2_structure_shell.edges[1].end-Point(5,0,0)))

    @Part(in_tree=False)
    def wing2_line4(self):
        return LineSegment(start=(self.wing2_structure_shell.edges[1].start-Point(5,0,0)), end=(self.wing2_structure_shell.edges[1].end-Point(5,0,0)))

    @Part(in_tree=False)
    def wing2_filledsurface(self):
        return FilledSurface(curves=[self.wing2_line1, self.wing2_line2, self.wing2_line3, self.wing2_line4])

    @Part(in_tree=False)
    def wing2_structure(self):
        return LoftedSolid([self.airfoil4_scaled, self.airfoil3_scaled])

    @Part(in_tree=False)
    def wing2_extrudedsolid(self):
        return ExtrudedShell(profile=self.wing2_filledsurface, distance=100, mirrored_extent=True)

    @Part(in_tree=False)
    def wing2_subtractshell(self):
        return Subtracted(shape_in=self.wing2_structure, tool=self.wing2_extrudedsolid.bbox.box)

    @Part(in_tree=False)
    def wing2_fusedshell(self):
        return FusedShell(shape_in=self.wing2_subtractshell.faces[0], tool=self.wing2_subtractshell.faces[1])

    @Part(in_tree=False)
    def wing2_structure_thickshell2(self):
        return ThickShell(built_from=self.wing2_fusedshell, offset = -self.wing2_skin_thickness)

    @Attribute
    @Action
    def Airfoil2bending(self):
        Iyy = self.wing2_structure_thickshell2.faces[2].matrix_of_inertia[1][1]*10**-16

        length = (self.airfoil4_scaled.position[1] - self.airfoil3_scaled.position[1])/1000
        load = 200
        deflection = load*length**3/(48*Iyy*self.Emod)

        popupstring = str(("With a load of " + str(load) + "N on wing 2, the deflection is found to be "
                           + str(round(deflection, 3))+ " mm"))
        popup("Calculated Deflection", popupstring, cancel_button=False)

        if deflection/load > 10/200:
            popupstring = str("Warning! Deflections exceed the maximum allowable deflections according to "
                              "Formula Student regulations! Consider changing the geometry or ply thickness.")
            popup("Warning!", popupstring, cancel_button=False)

    ##
    ## Defining Wing 3:
    ##




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

    ##
    ## Structures Module for wing 3:
    ##

    @Part(in_tree=False)
    def wing3_structure_shell(self):
        return LoftedShell([self.airfoil6_scaled, self.airfoil5_scaled])

    @Part(in_tree=False)
    def wing3_line1(self):
        return LineSegment(start=self.wing3_structure_shell.edges[1].start, end=self.wing3_structure_shell.edges[1].end)

    @Part(in_tree=False)
    def wing3_line2(self):
        return LineSegment(start=self.wing3_structure_shell.edges[1].start, end=(self.wing3_structure_shell.edges[1].start-Point(5,0,0)))

    @Part(in_tree=False)
    def wing3_line3(self):
        return LineSegment(start=self.wing3_structure_shell.edges[1].end, end = (self.wing3_structure_shell.edges[1].end-Point(5,0,0)))

    @Part(in_tree=False)
    def wing3_line4(self):
        return LineSegment(start=(self.wing3_structure_shell.edges[1].start-Point(5,0,0)), end=(self.wing3_structure_shell.edges[1].end-Point(5,0,0)))

    @Part(in_tree=False)
    def wing3_filledsurface(self):
        return FilledSurface(curves=[self.wing3_line1, self.wing3_line2, self.wing3_line3, self.wing3_line4])

    @Part(in_tree=False)
    def wing3_structure(self):
        return LoftedSolid([self.airfoil6_scaled, self.airfoil5_scaled])

    @Part(in_tree=False)
    def wing3_extrudedsolid(self):
        return ExtrudedShell(profile=self.wing3_filledsurface, distance=100, mirrored_extent=True)

    @Part(in_tree=False)
    def wing3_subtractshell(self):
        return Subtracted(shape_in=self.wing3_structure, tool=self.wing3_extrudedsolid.bbox.box)

    @Part(in_tree=False)
    def wing3_fusedshell(self):
        return FusedShell(shape_in=self.wing3_subtractshell.faces[0], tool=self.wing3_subtractshell.faces[1])

    @Part(in_tree=False)
    def wing3_structure_thickshell2(self):
        return ThickShell(built_from=self.wing3_fusedshell, offset = -self.wing3_skin_thickness)

    @Attribute
    @Action  # checking for bending requirements
    def Airfoil3bending(self):
        #Ixx = self.wing3_structure_thickshell2.faces[2].matrix_of_inertia[0][0]*10**-16
        iyy = self.wing3_structure_thickshell2.faces[2].matrix_of_inertia[1][1]*10**-16
        #Izz = self.wing3_structure_thickshell2.faces[2].matrix_of_inertia[2][2]*10**-16

        length = (self.airfoil6_scaled.position[1] - self.airfoil5_scaled.position[1])/1000
        load = 250
        deflection = load*length**3/(48*iyy*self.Emod)

        popupstring = str(("With a load of" + str(load) + "N on wing 3, the deflection is found to be " +
                           str(round(deflection, 3)) + " mm"))
        popup("Calculated Deflection", popupstring, cancel_button=False)

        if deflection/load > 10/200:
            popupstring = str("Warning! Deflections exceed the maximum allowable deflections according to "
                              "Formula Student regulations! Consider changing the geometry or ply thickness.")
            popup("Warning!", popupstring, cancel_button=False)

    @Attribute
    @Action
    def ExportDeflections(self):
        file = open("DeflectionsResults.txt", "w")

        lines = []

        lines.append("Wing 1 skin thickness: \n")
        lines.append(str(self.wing1_skin_thickness) + "\t [mm] \n")
        lines.append("Wing 1 chord length: \n")
        lines.append(str( self.chord) + "\t [mm] \n")
        lines.append("Wing 2 skin thickness: \n")
        lines.append(str(self.wing2_skin_thickness) + "\t [mm] \n")
        lines.append("Wing 2 chord length: \n")
        lines.append(str( self.chord*0.8) + "\t [mm] \n")

        lines.append("Wing 3 skin thickness: \n")
        lines.append(str(self.wing3_skin_thickness) + "\t [mm] \n")
        lines.append("Wing 3 chord length: \n")
        lines.append(str( self.chord*0.5) + "\t [mm] \n \n \n")

        #Wing 1 deflection:
        lines.append("Wing 1 Deflection calculation: \n")
        iyy = self.wing1_structure_thickshell2.faces[2].matrix_of_inertia[1][1]*10**-16
        length = (self.airfoil2_scaled.position[1] - self.airfoil1_scaled.position[1])/1000
        load = 200
        deflection = load*length**3/(48*iyy*self.Emod)

        lines.append(str(("With a load of " + str(load) + "N on wing 1, the deflection is found to be " +
                          str(round(deflection, 3))+ " mm \n  \n")))


        #Wing 2 deflection:
        lines.append("Wing 2 Deflection calculation: \n")
        iyy = self.wing2_structure_thickshell2.faces[2].matrix_of_inertia[1][1]*10**-16
        length = (self.airfoil4_scaled.position[1] - self.airfoil3_scaled.position[1])/1000
        load = 200
        deflection = load*length**3/(48*iyy*self.Emod)

        lines.append(str(("With a load of " + str(load) + "N on wing 2, the deflection is found to be " +
                          str(round(deflection, 3)) + " mm \n \n ")))


        #Wing 3 deflection:
        lines.append("Wing 3 Deflection calculation: \n")
        iyy = self.wing3_structure_thickshell2.faces[2].matrix_of_inertia[1][1]*10**-16
        length = (self.airfoil6_scaled.position[1] - self.airfoil5_scaled.position[1])/1000
        load = 200
        deflection = load*length**3/(48*iyy*self.Emod)

        lines.append(str(("With a load of " + str(load) + "N on wing 3, the deflection is found to be " +
                          str(round(deflection, 3)) + " mm \n \n ")))

        popup("Export Result", "The Deflection Calculations have successfully been exported to DeflectionsResults.txt",
              cancel_button=False)

        file.writelines(lines)
        file.close()


if __name__ == '__main__':
    from parapy.gui import display

    obj = WingElement(label="wing element"
                      )
    display(obj)
