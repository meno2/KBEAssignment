from parapy.core import *
from parapy.geom import *
from parapy.exchange.step.reader import STEPReader
import numpy as np

class ImportedGeometry(GeomBase):


	GeometrySTEP = STEPReader(filename=  "GeometryToImport.stp")

	@Part
	def bounding_box(self):
		return Box(self.boundingboxlength, self.boundingboxwidth, self.boundingboxheight, position = Position(Point(-self.boundingboxinlet, 0, 0)), transparency = 0.4)

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
	def geometry_to_mesh(self):
		return SubtractedSolid(shape_in = self.bounding_box, tool= [self.chassis, self.wheel2, self.wheel1], transparency = 0.7)