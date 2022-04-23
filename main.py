import os
#os.system("%SU2_RUN%SU2_CFD Configv2.cfg")

stream = os.popen("%SU2_RUN%SU2_CFD Configv2.cfg")
output = stream.read()
output