var channel_lores = 1;
var series_lores = 13;

var basename = "";

var roipath = "";

macro "Open vsi [O]" {
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_lores);
	Dialog.addNumber("Channel", channel_lores);
	Dialog.show();
	
	series_lores = Dialog.getNumber();
	channel_lores = Dialog.getNumber();
	
	path = File.openDialog("Please pick a .vsi file");
	
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	roipath = parent + File.separator + basename + "_ROIs.zip";
	
	run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series_lores);
	// work out how to select channel
	// run("Split Channels");
	// selectWindow("C" + channel "-" vsiName + " - " + vsiName + " #" + series);
	run("Enhance Contrast", "saturated=0.35");
	// invert as well
	
	roiManager("reset");
	setOption("Show All", true);
}