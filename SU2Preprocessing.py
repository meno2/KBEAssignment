
def preprocessing(filename, tags):
	f = open(filename, "r")
	lines= f.readlines()

	foundtags = 0
	for lineid in range(len(lines)):
		line = lines[lineid]
		if line.find("TAG") > -1:
			print(line)
			print(str(line[:line.find("=")+2]) + tags[foundtags] + "\n")

			lines[lineid] = str(line[:line.find("=")+2]) + tags[foundtags] + "\n"
			foundtags = foundtags+1

	filename2 = "edited_"+filename
	f = open(filename2, "w")
	f.writelines(lines)
	f.close()

preprocessing("RearWingGrid.su2", ["Front", "Right", "Top", "Left", "Bottom", "Rear", "Wall"])