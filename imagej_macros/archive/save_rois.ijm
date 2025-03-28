
var roipath = "";
var roiSuffix = "";

macro "Save ROIs [S]" {
	
	roiSuffix = getString("Add ROI suffix if required", roiSuffix);
	
	if (roipath == "") {
		path = getInfo("image.directory");
		filename = getInfo("image.filename");
	
		basename = replace(filename, ".vsi", "");
		basename = replace(basename, ".tif", "");
		roipath = path + File.separator + basename + roiSuffix + "_ROIs.zip";
	}
	print(roipath); 
	roiManager("save", roipath);
	showMessage("ROIs saved successfully in " + roipath);
}