from parapy.core import *
from parapy.geom import *
from parapy.exchange.step.reader import STEPReader


class ImportedGeometry(GeomBase):
	GeometrySTEP = STEPReader(filename=  "GeometryToImport.stp")

	@Part
	def chassis(self):
		return SewnSolid(self.GeometrySTEP.children[0].children[0].children[0])

	@Part
	def wheel1(self):
		return SewnSolid(self.GeometrySTEP.children[0].children[0].children[1])

	@Part
	def wheel2(self):
		return SewnSolid(self.GeometrySTEP.children[0].children[0].children[2])

	@Part
	def chassis_mirrored(self):
		return MirroredShape(shape_in = self.chassis, reference_point=Point(0,0,0), vector1=Vector(1,0,0), vector2=(Vector(0,0,1)))

	@Part
	def wheel3(self):
		return MirroredShape(shape_in = self.wheel1, reference_point=Point(0,0,0), vector1=Vector(1,0,0), vector2=(Vector(0,0,1)))

	@Part
	def wheel4(self):
		return MirroredShape(shape_in = self.wheel2, reference_point=Point(0,0,0), vector1=Vector(1,0,0), vector2=(Vector(0,0,1)))
