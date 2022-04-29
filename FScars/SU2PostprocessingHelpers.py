import vtk

from vtk.util import numpy_support
import numpy as np
import matplotlib.pyplot as plt


yval = 10
margin = 100

def get_xyzval(file_name, data_type):

	# Read the source file.
	reader = vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName(file_name)
	reader.Update()  # Needed because of GetScalarRange
	output = reader.GetOutput()
	points = numpy_support.vtk_to_numpy(output.GetPoints().GetData())
	datavalues = output.GetPointData().GetArray(data_type)

	datavalues_numpy = numpy_support.vtk_to_numpy(datavalues)

	#print(datavalues_numpy)
	if isinstance(datavalues_numpy[0], np.float32) == False:
		if len(datavalues_numpy[0])>1:
			new_datavalues_numpy = np.zeros(len(datavalues_numpy))
			for j in range(len(datavalues_numpy)):
				datapoint = 0
				for i in range(len(datavalues_numpy[j])):
					datapoint = datapoint + datavalues_numpy[j][i]**2
				new_datavalues_numpy[j] = (datapoint)**0.5

			datavalues_numpy = new_datavalues_numpy

	xarray = np.zeros(len(datavalues_numpy))
	yarray = np.zeros(len(datavalues_numpy))
	zarray = np.zeros(len(datavalues_numpy))
	valarray = np.zeros((len(datavalues_numpy)))

	for i in range(0, len(datavalues_numpy)):
		xarray[i] = points[i][0]
		yarray[i] = points[i][1]
		zarray[i] = points[i][2]
		valarray[i] = datavalues_numpy[i]

	return xarray, yarray, zarray, valarray


def surface_values(data_type):

	xarray, yarray, zarray, valarray = get_xyzval("surface_flow.vtu", data_type)

	fig = plt.figure(figsize= (16,9))
	ax= plt.axes(projection= "3d")

	color_map = plt.get_cmap('spring')

	scatter_plot = ax.scatter3D(xarray, yarray, zarray, c=valarray, cmap=color_map)
	#ax.set_box_aspect([1,1,1])
	ax.set_ylim(0,3*10**3)
	ax.set_xlim(-1*10**3,2*10**3)
	ax.set_zlim(0,3*10**3)

	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	plt.colorbar(scatter_plot)

	plt.show()

	return

def cut_in_y(data_type, yloc, ymargin):
	xarray, yarray, zarray, valarray = get_xyzval("flow.vtu", data_type)
	yval = yloc
	margin = ymargin

	cut_xvals = []
	cut_valvals = []
	cut_zvals = []

	for i in range(len(xarray)):
		if yval + margin > yarray[i] > yval-margin:
			cut_xvals.append(xarray[i])
			cut_valvals.append(valarray[i])
			cut_zvals.append(zarray[i])

	plt.tricontourf(cut_xvals, cut_zvals, cut_valvals, 1000, cmap='jet')

	xarray, yarray, zarray, valarray = get_xyzval("surface_flow.vtu", data_type)

	xmax = -10**4
	xmin = 10**4
	ymax = -10**4
	ymin= 10**4
	zmax= -10**4
	zmin = 10**4

	reader = vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName("surface_flow.vtu")
	reader.Update()  # Needed because of GetScalarRange
	output = reader.GetOutput()
	points = numpy_support.vtk_to_numpy(output.GetPoints().GetData())
	datavalues = output.GetPointData().GetArray(data_type)

	datavalues_numpy = numpy_support.vtk_to_numpy(datavalues)


	for i in range(0, len(datavalues_numpy)):
		if points[i][0] > xmax:
			xmax = points[i][0]
		if points[i][0] < xmin:
			xmin = points[i][0]
		if points[i][1] > ymax:
			ymax = points[i][1]
		if points[i][1] < ymin:
			ymin = points[i][1]
		if points[i][2] > zmax:
			zmax = points[i][2]
		if points[i][2] < zmin:
			zmin = points[i][2]

	cut_xvals = []
	cut_valvals = []
	cut_zvals = []

	for i in range(len(xarray)):
		if yval + margin > yarray[i] > yval-margin:
			if xmax-20 > xarray[i] > xmin:
				if zmax-20 > zarray[i] > zmin+20:
					cut_xvals.append(xarray[i])
					cut_valvals.append(valarray[i]*0.001)
					cut_zvals.append(zarray[i])
	print(data_type)

	if str(data_type) == "Pressure":
		title = str(data_type) + " at y = "+ str(yloc) + " mm given in MPa"
	if str(data_type) == "Velocity":
		title = str(data_type) + " at y = "+ str(yloc) + " mm given in m/s"

	plt.colorbar()
	plt.title(title)
	plt.xlabel("Position in X [mm]")
	plt.ylabel("Position in Z [mm]")
	plt.scatter(cut_xvals, cut_zvals, color = 'black', s=0.3)
	plt.axis('equal')
	savefilename = "ycut_"+str(data_type)+"at"+str(yloc)+"mm.png"
	plt.savefig(savefilename, dpi=300)
	plt.show()

def cut_in_z(data_type, yloc, ymargin):
	xarray, zarray, yarray, valarray = get_xyzval("flow.vtu", data_type)
	yval = yloc
	margin = ymargin

	cut_xvals = []
	cut_valvals = []
	cut_zvals = []

	for i in range(len(xarray)):
		if yval + margin > yarray[i] > yval-margin:
			cut_xvals.append(xarray[i])
			cut_valvals.append(valarray[i])
			cut_zvals.append(zarray[i])

	inverted_cutzvals = []
	for i in cut_zvals:
		inverted_cutzvals.append(-i)
	plt.tricontourf(cut_xvals, inverted_cutzvals, cut_valvals, 1000, cmap='jet')
	plt.tricontourf(cut_xvals, cut_zvals, cut_valvals, 1000, cmap='jet')

	xarray, zarray, yarray, valarray = get_xyzval("surface_flow.vtu", data_type)

	xmax = -10**4
	xmin = 10**4
	ymax = -10**4
	ymin= 10**4
	zmax= -10**4
	zmin = 10**4

	reader = vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName("surface_flow.vtu")
	reader.Update()  # Needed because of GetScalarRange
	output = reader.GetOutput()
	points = numpy_support.vtk_to_numpy(output.GetPoints().GetData())
	datavalues = output.GetPointData().GetArray(data_type)

	datavalues_numpy = numpy_support.vtk_to_numpy(datavalues)


	for i in range(0, len(datavalues_numpy)):
		if points[i][0] > xmax:
			xmax = points[i][0]
		if points[i][0] < xmin:
			xmin = points[i][0]
		if points[i][1] > ymax:
			ymax = points[i][1]
		if points[i][1] < ymin:
			ymin = points[i][1]
		if points[i][2] > zmax:
			zmax = points[i][2]
		if points[i][2] < zmin:
			zmin = points[i][2]

	cut_xvals = []
	cut_valvals = []
	cut_zvals = []

	for i in range(len(xarray)):
		if yval + margin > yarray[i] > yval-margin:
			if xmax-20 > xarray[i] > xmin:
				if zmax-20 > zarray[i] > zmin+20:
					cut_xvals.append(xarray[i])
					cut_valvals.append(valarray[i]*0.001)
					cut_zvals.append(zarray[i])
	print(data_type)

	if str(data_type) == "Pressure":
		title = str(data_type) + " at z = "+ str(yloc) + " mm given in MPa"
	if str(data_type) == "Velocity":
		title = str(data_type) + " at z = "+ str(yloc) + " mm given in m/s"

	plt.colorbar()
	plt.title(title)
	plt.xlabel("Position in X [mm]")
	plt.ylabel("Position in Y [mm]")
	plt.scatter(cut_xvals, cut_zvals, color = 'black', s=0.3)

	inverted_cutzvals = []
	for i in cut_zvals:
		inverted_cutzvals.append(-i)
	plt.scatter(cut_xvals, inverted_cutzvals, color = 'black', s=0.3)

	plt.axis('equal')
	savefilename = "zcut"+str(data_type)+"at"+str(yloc)+"mm.png"
	plt.savefig(savefilename, dpi=300)
	plt.show()



def cut_in_x(data_type, yloc, ymargin):
	yarray, xarray, zarray, valarray = get_xyzval("flow.vtu", data_type)
	yval = yloc
	margin = ymargin

	cut_xvals = []
	cut_valvals = []
	cut_zvals = []

	for i in range(len(xarray)):
		if yval + margin > yarray[i] > yval-margin:
			cut_xvals.append(xarray[i])
			cut_valvals.append(valarray[i])
			cut_zvals.append(zarray[i])


	inverted_cutxvals = []
	for i in cut_xvals:
		inverted_cutxvals.append(-i)
	plt.tricontourf(inverted_cutxvals, cut_zvals, cut_valvals, 1000, cmap='jet')
	plt.tricontourf(cut_xvals, cut_zvals, cut_valvals, 1000, cmap='jet')


	yarray, xarray, zarray, valarray = get_xyzval("surface_flow.vtu", data_type)

	xmax = -10**4
	xmin = 10**4
	ymax = -10**4
	ymin= 10**4
	zmax= -10**4
	zmin = 10**4

	reader = vtk.vtkXMLUnstructuredGridReader()
	reader.SetFileName("surface_flow.vtu")
	reader.Update()  # Needed because of GetScalarRange
	output = reader.GetOutput()
	points = numpy_support.vtk_to_numpy(output.GetPoints().GetData())
	datavalues = output.GetPointData().GetArray(data_type)

	datavalues_numpy = numpy_support.vtk_to_numpy(datavalues)


	for i in range(0, len(datavalues_numpy)):
		if points[i][0] > xmax:
			xmax = points[i][0]
		if points[i][0] < xmin:
			xmin = points[i][0]
		if points[i][1] > ymax:
			ymax = points[i][1]
		if points[i][1] < ymin:
			ymin = points[i][1]
		if points[i][2] > zmax:
			zmax = points[i][2]
		if points[i][2] < zmin:
			zmin = points[i][2]

	cut_xvals = []
	cut_valvals = []
	cut_zvals = []

	for i in range(len(xarray)):
		if yval + margin > yarray[i] > yval-margin:
			if xmax-20 > xarray[i] > xmin:
				if zmax-20 > zarray[i] > zmin+20:
					cut_xvals.append(xarray[i])
					cut_valvals.append(valarray[i]*0.001)
					cut_zvals.append(zarray[i])

	if str(data_type) == "Pressure":
		title = str(data_type) + " at x = "+ str(yloc) + " mm given in MPa"
	if str(data_type) == "Velocity":
		title = str(data_type) + " at x = "+ str(yloc) + " mm given in m/s"

	plt.colorbar()
	plt.title(title)
	plt.xlabel("Position in Y [mm]")
	plt.ylabel("Position in Z [mm]")
	plt.scatter(cut_xvals, cut_zvals, color = 'black', s=0.3)

	inverted_cutxvals = []
	for i in cut_xvals:
		inverted_cutxvals.append(-i)

	plt.scatter(inverted_cutxvals, cut_zvals, color = 'black', s=0.3)

	plt.axis('equal')
	savefilename = "xcut_"+str(data_type)+"at"+str(yloc)+"mm.png"
	plt.savefig(savefilename, dpi=300)
	plt.show()




#
# #surface_values("Pressure")
# cut_in_z("Velocity", 20, 10)
# cut_in_z("Pressure", 20, 10)
#
#
# cut_in_z("Velocity", 30, 20)
# cut_in_z("Pressure", 30, 20)
#
# cut_in_z("Velocity", 100, 20)
# cut_in_z("Pressure", 100, 20)
#
# cut_in_z("Velocity", 500, 20)
# cut_in_z("Pressure", 500, 20)
#
# cut_in_y("Velocity", 30, 20)
# cut_in_y("Pressure", 30, 20)
#
# cut_in_y("Velocity", 200, 20)
# cut_in_y("Pressure", 200, 20)

#
# cut_in_x("Velocity", 2100, 20)
# cut_in_x("Pressure", 2100, 20)

# cut_in_x("Velocity", 100, 20)
# cut_in_x("Pressure", 100, 20)
#
# cut_in_x("Velocity", 300, 20)
# cut_in_x("Pressure", 300, 20)

#
# file_name = "flow.vtu"
#
# reader = vtk.vtkXMLUnstructuredGridReader()
# reader.SetFileName(file_name)
# reader.Update()  # Needed because of GetScalarRange
# output = reader.GetOutput()
# points = numpy_support.vtk_to_numpy(output.GetPoints().GetData())
#
# print(output)
