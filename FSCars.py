from parapy.core import *
from parapy.geom import *

class FSCar(Base):
    speed=Input()
    rideHeight=Input()

    @Part
    def aerodynamic_device(self):
        return AerodynamicDevice(lift=self.lift,
                                 drag=self.drag)

    @Part
    def imported_geometry(self):
        return ImportedGeometry()