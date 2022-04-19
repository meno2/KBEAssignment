from parapy.core import *
from parapy.geom import *

class EndPlate(GeomBase):
    height=Input()
    width=Input()
    depth=Input()

    @Part
    def end_plate1(self):
        return Box(width=0.01,
                   length=0.7,
                   height=0.7,
                   color="red",
                   position= translate(rotate(self.position,"z", 90, deg=True), "y", -1.2))

    @Part
    def end_plate2(self):
        return Box(width=0.01,
                   length=0.7,
                   height=0.7,
                   position= translate(rotate(translate(self.position, "y",1), "z", 90, deg=True),"y", -1.2),
                   color="red")



if __name__ == '__main__':
    from parapy.gui import display
    obj = EndPlate()
    display(obj)
