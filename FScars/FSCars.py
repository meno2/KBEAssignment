from parapy.core import *
from parapy.geom import *
from parapy.mesh import salome
from Rearwing import RearWing
from Imported_geometry import ImportedGeometry


class FSCar(Base):
    speed = Input()
    rideHeight = Input()

    boundingboxheight = Input(2*10**3)
    boundingboxwidth = Input(1*10**3)
    boundingboxlength = Input(6*10**3)
    boundingboxinlet = Input(2.5*10**3)
    meshresolution = Input(0.02*10**3)


    @Part
    def rear_wing(self):
        return RearWing()

    @Part
    def imported_geometry(self):
        return ImportedGeometry()

    ## CONSTRUCTING MESH

    @Part
    def bounding_box(self):
        return Box(self.boundingboxlength, self.boundingboxwidth, self.boundingboxheight, position=Position(Point(-self.boundingboxinlet, 0, 0)), transparency=0.4)

    @Part
    def geometry_to_mesh(self):
        return SubtractedSolid(shape_in=self.bounding_box, tool=[self.imported_geometry.chassis, self.imported_geometry.wheel2, self.imported_geometry.wheel1],
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


if __name__ == '__main__':
    from parapy.gui import display

    obj = FSCar()
    display(obj)