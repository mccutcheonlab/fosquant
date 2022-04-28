// #@ Integer (label="Please choose channel to use for low res", description="Channel", persist=false, min=1, max=3, value=1) channel
// #@ Integer (label="Please choose series to load for low res", description="Series", persist=false, value=13) series
// #@ File(label="Select a directory", style="directory", value="D:/Test Data/histology/fostrappilot/") defaultDir

var defaultDir = "D:/Test Data/histology/fostrappilot2/";
var channel = 1;
var series = 13;

macro "Open vsi [O]" {

	// work out how to make directory or do it in python project setup script
	// defaultDir = "D:/Test Data/histology/fostrappilot/"
	
	File.setDefaultDir(defaultDir);
	path = File.openDialog("Please pick a .vsi file");
	parent = File.getParent(path);
	vsiName = File.getName(path);
	baseName = replace(vsiName, ".vsi", "");

	// series=13 // need to work out how to add this as default
	
	run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series);
	// work out how to select channel
	// run("Split Channels");
	// selectWindow("C" + channel "-" vsiName + " - " + vsiName + " #" + series);
	run("Enhance Contrast", "saturated=0.35");
	// invert as well
}