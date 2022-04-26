from parapy.core import *
from parapy.geom import *
import numpy as np

class Connector(GeomBase):
    youngs_modulus = Input()
    force = Input()
    length = Input()
    area = ()
    force_type = Input()  # ditributed or point

    @Attribute
    def moment_of_inertia(self):
        return

    @Attribute
    def deflection_point(self):
        return self.force * self.length ** 3 / (48 * self.youngs_modulus * self.moment_of_inertia)

    @Attribute
    def deflection_dist(self):
        return 5 * self.force * self.length ** 4 / (384 * self.youngs_modulus * self.moment_of_inertia)

    @Attribute
    def force_per_area(self):  # N/cm2
        return self.force / self.area

    @Attribute
    def force_check(self):
        return self.deflection_dist / self.force_per_area < 10 / 0.88 if self.force_type == "distributed" else self.deflection_point / self.force < 25 / 50

    @Part
    def cyl(self):
        return Box(width= 10, length= 10, height=400,
                        position=Position(Point(1300, 100, 440)))

    @Part
    def cyl2(self):
        return MirroredShape(shape_in=self.cyl, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))

    @Part
    def cyl3(self):
        return Box(width=10, length=10, height=250,
                   position=rotate(rotate(Position(Point(1300, 100, 830)), "y", -65, deg=True),"x", -5, deg=True))

    @Part
    def cyl4(self):
        return MirroredShape(shape_in=self.cyl3, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))

    @Part
    def cyl5(self):
        return Box(width=10, length=10, height=200,
                   position=rotate(Position(Point(1300, 100, 840)), "y", 90, deg=True))

    @Part
    def cyl6(self):
        return MirroredShape(shape_in=self.cyl5, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))

    @Part
    def cyl7(self):
        return Box(width=10, length=10, height=440,
                   position=rotate(rotate(Position(Point(1500, 100, 840)), "y", -77.5, deg=True), "x", -3, deg=True))

    @Part
    def cyl8(self):
        return MirroredShape(shape_in=self.cyl7, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))

    @Part
    def cyl9(self):
        return Box(width=20, length=20, height=40,
                   position=(Position(Point(1500, 95, 820))))

    @Part
    def cyl10(self):
        return MirroredShape(shape_in=self.cyl9, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))

    @Part
    def merged_connector_right(self):
        return FusedSolid(shape_in= self.cyl, tool = [self.cyl3, self.cyl5, self.cyl7, self.cyl9])

    @Part
    def merged_connector_left(self):
        return MirroredShape(shape_in=self.merged_connector_right, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))


if __name__ == '__main__':
    from parapy.gui import display

    obj = Connector(label="Connector")

    display(obj)