var channel_lowres = 1;

var basename = "";

var roipath = "";

macro "Open TIFF [T]" {
	
	Dialog.create("Choose options");
	Dialog.addNumber("Channel", channel_lowres);
	Dialog.show();
	
	channel_lowres = Dialog.getNumber();
	
	path = File.openDialog("Please pick a .tif file");
	
	parent = File.getParent(path);
	tifName = File.getName(path);
	baseName = replace(tifName, ".tif", "");
	baseName = replace(baseName, ".", "_");
	roipath = parent + File.separator + baseName + "_ROIs.zip";
	newpath = parent + File.separator + baseName + "_edited.tif";
	
	open(path);
	run("Split Channels");
	selectWindow(tifName + " (red)");
	run("8-bit");
	run("Invert LUT");
	run("Enhance Contrast", "saturated=0.35"); // this helps to see but does not change underlying data
	
	roiManager("reset");
	setOption("Show All", true);
	saveAs("TIFF", newpath);
}