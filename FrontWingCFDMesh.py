import parapy.lib.su2
from parapy.geom import Box, translate
# from parapy.mesh import FaceGroup, salome
#from parapy.lib.su2 import *
from parapy.exchange.step.reader import STEPReader
import numpy as np
from parapy.core import *
from parapy.geom import *
from parapy.mesh import salome
from parapy.lib.su2 import *

parapy.lib.su2.
from parapy.mesh.core.controls import MeshControl

# #
# CarInSTP = STEPReader(filename = "FrontWing.stp")
# #
# frontwing = CarInSTP.children[0]#.children[0]
# #
# #print(frontwing.shapes)
#
# actuallyabox = STEPReader(filename = "ActuallyABox.stp")
#
# boxtosplit = actuallyabox.children[0]
#
# boundingbox = STEPReader(filename = "Tyrewake.stp")
#
# frontwingboundingbox = boundingbox.children[1] + boundingbox.children[0]



# newbox = SubtractedSolid(shape_in = boundingbox, tool =  actuallyabox)

# Completecar = STEPReader(filename = "DUT21_CFDBaseline.stp")
#
# SidediffwithTOPO = Completecar.children[0].children[0]

class ImportedGeometry(GeomBase):
	CarInSTP = STEPReader(filename = "DUT21_CFDBaseline.stp")
	CompleteCar = STEPReader(filename = "DUT21_CFD_Baseline_002.stp")
	SimpleChassis = STEPReader(filename=  "SimpleChassisV3.stp")

	@Part
	def chassistep(self):
		return STEPReader(filename = "DUT21_Chassis_ChassisKeychain A.1.stp")

	@Part
	def entirecar(self):
		return STEPReader(filename = "DUT21_CFDBaseline.stp")

	@Part
	def box(self):
		return Box(6*10**3, 1*10**3, 2*10**3, position = Position(Point(-2.5*10**3,-0.0*10**3,0)),  color="RED", transparency=0.4)

	@Part
	def sidediff(self):
		return SewnSolid(self.CarInSTP.children[0].children[1].children[1].children[0])


	@Part
	def frontwing(self):
		return SewnSolid(self.CarInSTP.children[0].children[0].children[0])

	@Part
	def headrest(self):
		return SewnSolid(self.CompleteCar.children[0].children[0].children[1].children[1].children[0])


	@Part
	def rearwing(self):
		return SewnSolid(self.CompleteCar.children[0].children[3].children[0].children[0])

	@Part
	def chassis(self):
		return SewnSolid( self.SimpleChassis.children[0].children[0].children[0])

	@Part
	def wheel1(self):
		return SewnSolid(self.SimpleChassis.children[0].children[0].children[1])

	@Part
	def wheel2(self):
		return SewnSolid(self.SimpleChassis.children[0].children[0].children[2])

	# @Part
	# def chassis(self):
	# 	return SewnSolid(self.SimpleChassis.children[1])

	#
	# @Part
	# def chassis(self):
	# 	return ScaledShape(shape_in = self.smallchassis, reference_point=Point(0, 0, 0),
	# 					   factor=10)

	# @Part
	# def mainhoop(self):
	# 	return SewnSolid(self.CarInSTP.children[0].children[2].children[1])

	#
	# @Part
	# def combinedsolid(self):
	# 	return FusedSolid(shape_in = self.frontwing, tool = self.sidediff)

	@Part
	def Boundingboxsubtractions(self):
		return SubtractedSolid(shape_in = self.box, tool = [self.chassis, self.wheel1, self.wheel2], transparency = 0.4, color = 'blue')

	@Part
	def grid1dfrontwing(self):
		return salome.Mesh(shape_to_mesh=self.Boundingboxsubtractions,controls=[salome.FixedLength(shape_to_mesh=self.Boundingboxsubtractions, length = 0.01*10**3)])

	@Part
	def grid1dsidediff(self):
		return salome.Mesh(shape_to_mesh=self.sidediff,controls=[salome.FixedNumber(shape_to_mesh=self.sidediff, no=5)])

	@Part
	def grid2dfrontwing(self):
		return salome.Mesh(shape_to_mesh=self.frontwing,controls=[salome.FixedLength(shape_to_mesh=self.frontwing, length = 0.03*10**3), salome.Tri(shape_to_mesh=self.frontwing)])

	@Part
	def grid(self):
		return salome.Mesh(shape_to_mesh=self.Boundingboxsubtractions,controls=[salome.FixedLength(shape_to_mesh=self.Boundingboxsubtractions, length = 0.05*10**3), salome.Tri(shape_to_mesh=self.Boundingboxsubtractions), salome.Tetra(shape_to_mesh=self.Boundingboxsubtractions)],
						   groups=[self.Boundingboxsubtractions.faces[0], self.Boundingboxsubtractions.faces[1], self.Boundingboxsubtractions.faces[2], self.Boundingboxsubtractions.faces[3], self.Boundingboxsubtractions.faces[4], self.Boundingboxsubtractions.faces[5], self.Boundingboxsubtractions.faces[6:]])

	@Part
	def grid2(self):
		return salome.Mesh(shape_to_mesh=self.sidediff,controls=[salome.FixedLength(shape_to_mesh=self.sidediff, length= 0.5*10**3), salome.Tri(shape_to_mesh=self.sidediff)])




class MeshedCar(GeomBase):
	tyreboundingbox =  STEPReader(filename = "Tyrewake.stp")
	#
	# @Part
	# def boundingbox(self):
	# 	return self.tyreboundingbox.children[0]


class MeshedBoundingBox(GeomBase):

	@Part
	def box(self):
		return Box(2*10**3, 2*10**3, 2*10**3, color="RED", transparency=0.4)

	@Part
	def drivetrain(self):
		return Cylinder(0.2, 0.3)

	@Part
	def drivetrain_positioned(self):
		return Cylinder(0.2*10**3, 0.3*10**3,
						position=rotate(translate(self.position, "x", 1*10**3, "y", 1*10**3, "z", 0.2*10**3), "x", np.pi / 2))

	@Part
	def drivetrain_filleted_positioned(self):
		return FilletedSolid(self.drivetrain_positioned, radius=0.05*10**3)

	@Part
	def MeshVolume(self):
		return SubtractedSolid(shape_in=self.box, tool=self.drivetrain_filleted_positioned, transparency=0.7)

	@Part
	def grid(self):
		return salome.Mesh(shape_to_mesh=self.MeshVolume, controls=[salome.FixedLength(shape_to_mesh=self.MeshVolume, length=0.01*10**3), salome.Tri(shape_to_mesh=self.MeshVolume),   salome.Tetra(shape_to_mesh=self.MeshVolume)],
						   groups=[self.MeshVolume.faces[0], self.MeshVolume.faces[1], self.MeshVolume.faces[2], self.MeshVolume.faces[3], self.MeshVolume.faces[4], self.MeshVolume.faces[5], self.MeshVolume.faces[6:]], filename = "DrivetrainMesh.msh")



#
# def ConstructMesh():
# 	ctrl_1d = salome.FixedLength(shape_to_mesh=MeshedBoundingBox.MeshVolume, length=0.1)
# 	ctrl_2d = salome.Tri(shape_to_mesh=MeshedBoundingBox.MeshVolume)
# 	ctrl_3d = salome.Tetra(shape_to_mesh=MeshedBoundingBox.MeshVolume)
# 	mesh = salome.Mesh(shape_to_mesh=MeshedBoundingBox.MeshVolume, controls=[ctrl_1d, ctrl_2d, ctrl_3d])
# 	return MeshedBoundingBox.MeshVolume, mesh


#
# ctrl_1d = salome.FixedLength(shape_to_mesh=frontwingboundingbox, length=10)
# ctrl_2d = salome.Tri(shape_to_mesh=frontwingboundingbox)
# ctrl_3d = salome.Tetra(shape_to_mesh=frontwingboundingbox)
# mesh = salome.Mesh(shape_to_mesh=frontwingboundingbox,
# 				   controls=[ctrl_1d, ctrl_2d, ctrl_3d],
# 				   logfilename="test.log",
# 				   )


if __name__ == '__main__':
	from parapy.gui import display

	Completecar = STEPReader(filename = "SimpleChassisV3.stp")

	# Headrest = Completecar.children[0].children[0].children[1].children[1].children[0]
	#Rearwing = Completecar.children[0].children[3].children[0].children[0]
	Chassis = Completecar.children[0].children[0].children[0]
	# mesh.write(r"test.unv")
	obj = MeshedBoundingBox()
	obj2 = ImportedGeometry()
	#Volume, Mesh = ConstructMesh()

	display((obj, obj2, Completecar, Chassis )) #, Rearwing, Chassis))

	#obj.grid.groups[0].label = "Rear"

	print("Writing Grid:")
	parapy.lib.su2.write_su2(obj2.grid, "RearWingGrid.su2")
	print("Done! ")




