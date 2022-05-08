var channel_lowres = 1;
var series_lowres = 13;

var basename = "";

var roipath = "";

macro "Open vsi [O]" {
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_lowres);
	Dialog.addNumber("Channel", channel_lowres);
	Dialog.show();
	
	series_lowres = Dialog.getNumber();
	channel_lowres = Dialog.getNumber();
	
	path = File.openDialog("Please pick a .vsi file");
	
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	roipath = parent + File.separator + basename + "_ROIs.zip";
	
	run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series_lowres);
	run("Enhance Contrast", "saturated=0.35");
	
	roiManager("reset");
	setOption("Show All", true);
}