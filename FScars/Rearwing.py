from parapy.core import *
from parapy.geom import *
from WingElement import WingElement
from EndPlates import EndPlate
from Connector import Connector
class RearWing(GeomBase):


    @Part
    def wing_element(self):
        return WingElement(label="Wing element",
                      airfoil_name="2412")
    @Part
    def end_plates(self):
        return EndPlate()

    @Part
    def connector(self):
        return Connector()

if __name__ == '__main__':
    from parapy.gui import display

    obj = RearWing()
    display(obj)