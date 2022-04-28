
var roipath = ""

macro "Load ROIs [L]" {
	// could add command to automatically load if an ROI file can be found
	path = File.openDialog("Please pick a file with ROIs");
	roiManager("open", path);
	roiManager("show all with labels");
	
}