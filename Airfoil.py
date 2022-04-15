from parapy.core import *
from parapy.geom import *
from kbeutils.geom import Naca4AirfoilCurve

class Airfoil(WingElement):
    airfoil_type=Input()