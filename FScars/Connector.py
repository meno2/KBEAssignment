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
        return Cylinder(radius= 10, height=350,
                        position=Position(Point(1350, 50, 500)))

    @Part
    def cyl2(self):
        return MirroredShape(shape_in=self.cyl, reference_point=self.position,
                             vector1=(1, 0, 0),
                             vector2=(0, 0, 1))



if __name__ == '__main__':
    from parapy.gui import display

    obj = Connector(label="Connector")

    display(obj)