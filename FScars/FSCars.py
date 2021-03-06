from parapy.core import *
from parapy.geom import *
from parapy.mesh import salome

#from FScars import Connector
from Rearwing import RearWing
from Imported_geometry import ImportedGeometry
from parapy.core import action
from parapy.core.decorators import Action
from parapy.lib.su2 import *
from SU2Preprocessing import preprocessing, changevelocity
import subprocess
import os
from parapy.gui.wx_utils import popup
import vtk
from Connector import Connector
import enum
from parapy.exchange.step import STEPWriter

from parapy.core.widgets import (
     Dropdown
    )
from parapy.exchange.step.reader import STEPReader
from SU2PostprocessingHelpers import *


class FSCar(Base):
    velocity = Input(10)
    rideHeight = Input()

    boundingboxheight = Input(2 * 10 ** 3)
    boundingboxwidth = Input(1 * 10 ** 3)
    boundingboxlength = Input(6 * 10 ** 3)
    boundingboxinlet = Input(2.5 * 10 ** 3)
    meshresolution = Input(0.02 * 10 ** 3)
    plot_resolution_margin = Input(20)
    plot_xcut_loc = Input(20)
    plot_ycut_loc = Input(30)
    plot_zcut_loc = Input(50)

    @Part
    def rear_wing(self):
        return RearWing()

    @Part
    def imported_geometry(self):
        return ImportedGeometry()

    # @Part
    # def connector(self):
    #     return Connector()

    ## CONSTRUCTING MESH ##

    @Part
    def bounding_box(self):
        return Box(self.boundingboxlength, self.boundingboxwidth, self.boundingboxheight,
                   position=Position(Point(-self.boundingboxinlet, 0, 0)), transparency=0.4)

    @Part
    def geometry_to_mesh(self):
        return SubtractedSolid(shape_in=self.bounding_box, tool=[self.imported_geometry.chassis,
                                                                 self.imported_geometry.wheel2,
                                                                 self.imported_geometry.wheel1,
                                                                 self.rear_wing.wing_element.wing_loft_solid,
                                                                 self.rear_wing.wing_element.wing_loft_solid2,
                                                                 self.rear_wing.wing_element.wing_loft_solid3,
                                                                 self.rear_wing.end_plates.end_plate1,
                                                                 self.rear_wing.end_plates.end_plate2],
                               transparency=0.7)

    @Part
    def mesh(self):
        return salome.Mesh(shape_to_mesh=self.geometry_to_mesh,
                           controls=[salome.FixedLength(shape_to_mesh=self.geometry_to_mesh,
                                                        length=self.meshresolution),
                                     salome.Tri(shape_to_mesh=self.geometry_to_mesh),
                                     salome.Tetra(shape_to_mesh=self.geometry_to_mesh)],
                           groups=[self.geometry_to_mesh.faces[0], self.geometry_to_mesh.faces[1],
                                   self.geometry_to_mesh.faces[2], self.geometry_to_mesh.faces[3],
                                   self.geometry_to_mesh.faces[4], self.geometry_to_mesh.faces[5],
                                   self.geometry_to_mesh.faces[6:]])



    @action(context=Action.Context.INSPECTOR, label="Once generated, export mesh", button_label="Export")
    def export_mesh(self):
        popup("Process Initiated", "Mesh is being exported - check Python log for status", cancel_button=False)
        print("Generating Mesh: ...")
        parapy.lib.su2.write_su2(self.mesh, "mesh_of_car.su2")
        preprocessing("mesh_of_car.su2", ["Front", "Right", "Top", "Left", "Bottom", "Rear", "Wall"])

    @action(context=Action.Context.INSPECTOR, label="Change Velocity", button_label="Update")
    def update_velocity(self):
        changevelocity(self.velocity)
        popup("Success", "Velocity in config file has been changed to " + str(self.velocity) + "m/s!",
              cancel_button=False)

    @action(context=Action.Context.INSPECTOR, label="Run SU2", button_label="Run")
    def run_SU2(self):
        popup("Process Initiated", "SU2 is being run - check Python log for status", cancel_button=False)
        stream = os.popen("%SU2_RUN%SU2_CFD SU2_config.cfg")
        output = stream.read()
        output

    type_for_plot = Input("Pressure", widget=Dropdown(["Pressure", "Velocity"]))

    @action(context=Action.Context.INSPECTOR, label="Produce y-cut plot", button_label="Run")
    def produce_ycutplot(self):
        cut_in_y(self.type_for_plot, self.plot_ycut_loc, self.plot_resolution_margin)

    @action(context=Action.Context.INSPECTOR, label="Produce x-cut plot", button_label="Run")
    def produce_xcutplot(self):
        cut_in_x(self.type_for_plot, self.plot_xcut_loc, self.plot_resolution_margin)

    @action(context=Action.Context.INSPECTOR, label="Produce z-cut plot", button_label="Run")
    def produce_zcutplot(self):
        cut_in_z(self.type_for_plot, self.plot_zcut_loc, self.plot_resolution_margin)

    @Part
    def writer_fullcar(self):
        return STEPWriter(trees=[self.rear_wing, self.imported_geometry], filename="ExportFullCar.stp")

    @Part
    def writer_rearwing(self):
        return STEPWriter(trees=[self.rear_wing], filename="ExportRearWing.stp")


    @action(context=Action.Context.INSPECTOR, label="Write STEP of entire car", button_label="Export")
    def write_step(self):
        self.writer_fullcar.write()

    @action(context=Action.Context.INSPECTOR, label="Write STEP of rear wing", button_label="Export")
    def write_step2(self):
        self.writer_rearwing.write()



if __name__ == '__main__':
    from parapy.gui import display

    obj = FSCar()

    display(obj)