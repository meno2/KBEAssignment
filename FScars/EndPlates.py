from parapy.core import *
from parapy.geom import *
from parapy.gui.wx_utils import popup
from parapy.core.decorators import Action

class EndPlate(GeomBase):
    height=Input(900)
    width=Input(10)
    length=Input(1000)
    height_from_floor= Input(1300)
    distance_from_wheel=Input(500)


    @Part
    def end_plate1(self):
        return Box(width=self.width,
                   length=self.length,
                   height=self.height,
                   color="red",
                   position= translate(rotate(self.position,"z", 90, deg=True), "y", -2210,
                                       'z' , self.height_from_floor if self.height_from_floor<1200  else 700

                                       ,"x", self.distance_from_wheel if self.distance_from_wheel<= 500 else -520))



    @Part
    def end_plate2(self):
        return MirroredShape(shape_in=self.end_plate1, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1), color="red")

    @Action  #to check for the dimension limitations
    def height_from_ground(self):
            popupstring = str(
                "if the given height of the end plate is lower than 1.2 m from the ground so it has changed to the deffault value of 700 cm")
            popup("Warning", popupstring, cancel_button=False)
    @Action
    def distance_from_wheels(self):
        popupstring = str(
            "if the given position of end plates is exceeding the most inboard part of the wheel so it has been lowered to the diffault value of 500")
        popup("Warning", popupstring, cancel_button=False)


if __name__ == '__main__':
    from parapy.gui import display
    obj = EndPlate()
    display(obj)
