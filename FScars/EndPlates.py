from parapy.core import *
from parapy.geom import *

class EndPlate(GeomBase):
    height=Input()
    width=Input()
    depth=Input()

    @Part
    def end_plate1(self):
        return Box(width=0.01,
                   length=0.9,
                   height=0.9,
                   color="red",
                   position= translate(rotate(self.position,"z", 90, deg=True), "y", -1.3, "z", -0.1))

    @Part
    def end_plate2(self):
        return Box(width=0.01,
                   length=0.9,
                   height=0.9,
                   position= translate(rotate(translate(self.position, "y",1), "z", 90, deg=True),"y", -1.3, "z", -0.1),
                   color="red")



if __name__ == '__main__':
    from parapy.gui import display
    obj = EndPlate()
    display(obj)
