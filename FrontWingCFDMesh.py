from parapy.geom import Box, translate
#from parapy.mesh import FaceGroup, salome

from parapy.exchange.step.reader import STEPReader
from parapy.geom import *
from parapy.core import *
from parapy.mesh import salome


CarInSTP = STEPReader(filename = "DUT21_CFDBaseline.stp")

frontwing = CarInSTP.children[0].children[0]#.children[0]

#print(frontwing.shapes)

actuallyabox = STEPReader(filename = "ActuallyABox.stp")

boxtosplit = actuallyabox.children[0]

boundingbox = STEPReader(filename = "FrontWingVolume.stp")

frontwingboundingbox = boundingbox.children[0]

#newbox = SubtractedSolid(shape_in = boundingbox, tool =  actuallyabox)



#
# class ImportedGeometry(GeomBase):
# 	CarInSTP = STEPReader(filename = "DUT21_CFDBaseline.stp")
#
# 	@Part
# 	def frontwing(self):
# 		return FrontWing(self.CarInSTP.children[0].children[0].children[0])


#
# box = Box(1, 1, 1, color="RED", transparency=0.4)
ctrl_1d = salome.FixedLength(shape_to_mesh=frontwingboundingbox, length=0.1)
ctrl_2d = salome.Tri(shape_to_mesh=frontwingboundingbox)
ctrl_3d = salome.Tetra(shape_to_mesh=frontwingboundingbox)
mesh = salome.Mesh(shape_to_mesh=frontwingboundingbox,
				   controls=[ctrl_1d, ctrl_2d, ctrl_3d],
				   logfilename="test.log")




if __name__ == '__main__':
	from parapy.gui import display
	# mesh.write(r"test.unv")
	display((boxtosplit, frontwingboundingbox, mesh))