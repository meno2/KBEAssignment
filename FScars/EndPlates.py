from parapy.core import *
from parapy.geom import *

class EndPlate(GeomBase):
    height=Input()
    width=Input()
    depth=Input()

    @Part
    def end_plate1(self):
        return Box(width=10,
                   length=900,
                   height=900,
                   color="red",
                   position= translate(rotate(self.position,"z", 90, deg=True), "y", -2000, "z", 500, "x", -400))

    @Part
    def end_plate2(self):
        return Box(width=10,
                   length=900,
                   height=900,
                   position= translate(rotate(translate(self.position, "y",1000), "z", 90, deg=True),"y", -2000, "z", 500, "x", -400),
                   color="red")



if __name__ == '__main__':
    from parapy.gui import display
    obj = EndPlate()
    display(obj)
