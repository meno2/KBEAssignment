from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve

class Airfoil(GeomBase):
    airfoil_name = Input()
    chord = Input()

    @Part#(in_tree=False)
    def airfoil1(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name)

    @Part  # (in_tree=False)
    def airfoil2(self):
        return Naca4AirfoilCurve(designation=self.airfoil_name)

    @Part
    def curve(self):
        return ScaledCurve(curve_in=self.airfoil,
                           reference_point=self.position.point,
                           factor=self.chord)



if __name__ == '__main__':
    from parapy.gui import display

    obj = Airfoil(airfoil_name="2412",
                  chord=2,
                  label="wing section",
                  )
    display(obj)

