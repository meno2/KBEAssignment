from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve

class WingElement(Base):
    angleOfIncidence = Input()
    liftCoefficient = Input()
    dragCoefficient = Input()
    span = Input()
    meanChord = Input()
    twistDistribution = Input()
    airfoil_type=Input()

    @Part
    def airfoil(self):
        return Naca4AirfoilCurve(designation=self.airfoil_type)
    