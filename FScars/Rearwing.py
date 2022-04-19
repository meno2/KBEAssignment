from parapy.core import *
from parapy.geom import *
from WingElement import WingElement
from EndPlates import EndPlate

class RearWing(GeomBase):

    # @Attribute
    # def compute_downforce(self):
    #     return
    #
    # @Attribute
    # def compute_drag(self):
    #     return
    #
    # @Part
    # def connector(self):
    #     return Connector(stiffness=self.stiffness,
    #                      material= self.material)
    @Part
    def wing_element(self):
        return WingElement(label="aircraft",
                      airfoil_name="2412")
    @Part
    def end_plates(self):
        return EndPlate(height=self.height,
                         width=self.width,
                         depth=self.depth)
