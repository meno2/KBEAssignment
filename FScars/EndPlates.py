from parapy.core import *
from parapy.geom import *

class EndPlate(GeomBase):
    height=Input(900)
    width=Input(10)
    length=Input(1000)

    @Part
    def end_plate1(self):
        return Box(width=self.width,
                   length=self.length,
                   height=self.height,
                   color="red",
                   position= translate(rotate(self.position,"z", 90, deg=True), "y", -2210, "z", 700, "x", -500))

    # @Part
    # def end_plate2(self):
    #     return Box(width=10,
    #                length=900,
    #                height=900,
    #                position= translate(rotate(translate(self.position, "y",1000), "z", 90, deg=True),"y", -2100, "z", 700, "x", -500),
    #                color="red")

    @Part
    def end_plate2(self):
        return MirroredShape(shape_in=self.end_plate1, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1), color="red")

if __name__ == '__main__':
    from parapy.gui import display
    obj = EndPlate()
    display(obj)
