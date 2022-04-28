
var roipath = "";

macro "Save ROIs [S]" {
	
	if (roipath == "") {
		path = getInfo("image.directory");
		filename = getInfo("image.filename");
	
		basename = replace(filename, ".vsi", "");
		roipath = path + File.separator + basename + "_ROIs.zip";
	}
	print(roipath); 
	roiManager("save", roipath);
	showMessage("ROIs saved successfully in " + roipath);
}