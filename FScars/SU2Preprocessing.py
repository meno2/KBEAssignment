
def preprocessing(filename, tags):
	f = open(filename, "r")
	lines= f.readlines()

	foundtags = 0
	for lineid in range(len(lines)):
		line = lines[lineid]
		if line.find("TAG") > -1:
			#print(line)
			#print(str(line[:line.find("=")+2]) + tags[foundtags] + "\n")

			lines[lineid] = str(line[:line.find("=")+2]) + tags[foundtags] + "\n"
			foundtags = foundtags+1

	filename2 = "edited_"+filename
	f = open(filename2, "w")
	f.writelines(lines)
	f.close()
	print("Succesfully preprocessed!")

def changevelocity(velocity):
	f = open("SU2_config.cfg", "r")
	lines = f.readlines()

	for lineid in range(len(lines)):
		line = lines[lineid]
		if line.find("VELOCITY_INIT") > -1:
			#print(line)
			newline = "INC_VELOCITY_INIT= ( "+ str(velocity)+", 0.0, 0.0 )\n"
			#print(newline)
			lines[lineid] = newline

	f=open("SU2_config.cfg", "w")
	f.writelines(lines)
	f.close()

#preprocessing("RearWingGrid.su2", ["Front", "Right", "Top", "Left", "Bottom", "Rear", "Wall"])
