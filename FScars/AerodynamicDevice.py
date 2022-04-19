from parapy.core import *
from parapy.geom import *

class AerodynamicDevice(FSCar):
      lift=Input()
      drag=Input()

      @Part
      def rearWing(self):
            RearWing(computeDownForce= self.computeDownForce,
                     computeDrag=self.computeDrag)