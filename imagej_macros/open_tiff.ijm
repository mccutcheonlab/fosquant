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
	basename = replace(tifName, ".tif", "");
	roipath = parent + File.separator + basename + "_ROIs.zip";
	newpath = parent + File.separator + basename + "_edited.tif";
	
	open(path);
	run("8-bit");
	run("Invert LUT");
	run("Enhance Contrast", "saturated=0.35");
	
	roiManager("reset");
	setOption("Show All", true);
	save(newpath)
}