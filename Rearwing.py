from parapy.core import *
from parapy.geom import *

class RearWing(AerodynamicDevice):

    @Attribute
    def compute_downforce(self):
        return

    @Attribute
    def compute_drag(self):
        return

    @Part
    def connector(self):
        return Connector(stiffness=self.stiffness,
                         material= self.material)
    @Part
    def wing_element(self):
        return WingElement(angleOfIncidence=self.angleOfIncidence,
                           liftCoefficient= self.liftCoefficient,
                           dragCoefficient= self.dragCoefficient,
                           span=self.span,
                           meanChord=self.meanChord,
                           twistDistribution=self.twistDistribution)
    @Part
    def end_plates(self):
        return EndPlates(height=self.height,
                         width=self.width,
                         depth=self.depth)
