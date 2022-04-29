var channel_lores = 1;
var series_lores = 13;

var channel_hires = 2;
var series_hires = 11;

var parent = "";
var basename = "";

var roipath = "";

var startSection = 0;

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

macro "Rename ROIs [R]" {
	
	startSection = getNumber("Number of first section", startSection);
	
	n = roiManager("count");
	print(n);
	if (n == 0) {
		exit("No ROIs to process");
		// maybe run Load ROIs macro here
	}

	for (i = 0; i < n; i++) {
	    roiManager("select", i);
	    currentSection = startSection + i;
	    if (currentSection < 10) {
	    	sectionNumber = "_s00" + currentSection;
	    } else {
	    	sectionNumber = "_s0" + currentSection;
	    }
	    roiManager("rename", sectionNumber)
	}
}

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

macro "Load ROIs [L]" {
	// could add command to automatically load if an ROI file can be found
	path = File.openDialog("Please pick a file with ROIs");
	roiManager("open", path);
	roiManager("show all with labels");
	
}

macro "Export lowres [L]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
	// add dialog for channel and invert and rotate
	
	if (basename == "") {
		parent = getInfo("image.directory");
		filename = getInfo("image.filename");
		basename = replace(filename, ".vsi", "");
	}
	
	channel_lowres = getNumber("Channel", 1);
	
	outDir = parent + File.separator + "lowres";
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "lowres");
	}
	
	Stack.setChannel(channel_lowres);
	run("Duplicate...", "title=inverted");
	run("8-bit");
	run("Invert LUT");
	
	id = getImageID();
	print(id);
	
	n = roiManager("count");
	for (i = 0; i < n; i++) {
		selectImage(id);
		run("Select None");
		run("Duplicate...", "title=crop");
	    roiManager("select", i);
	    sectionNumber = Roi.getName();
	    
	    run("Crop");
	    run("Rotate 90 Degrees Right");
		savefile = outDir + File.separator + basename + "_lowres" + sectionNumber + ".jpg";
	    saveAs("Jpeg", savefile);
    	close();
	}
	selectImage(id);
	close();
}

macro "Export hires [H]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
	// add dialog for channel and invert and rotate

	path = File.openDialog("Please pick a .vsi file");
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_hires);
	Dialog.addNumber("Channel", channel_hires);
	Dialog.show();
	
	outDir = parent + File.separator + "chan" + channel_hires;
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "chan" + channel_hires);
	}
	
	series_hires = Dialog.getNumber();
	channel_hires = Dialog.getNumber();
	
	scaleFactor = pow(2, (13 - series_hires));
	s = series_hires;
	
	roiManager("List");
	n = roiManager("count");
	
	for (i = 0; i < n; i++) {	
		roiName = getResultString("Name", i);
		xPos = getResult("X", i) * scaleFactor;
		yPos = getResult("Y", i) * scaleFactor;
		width = getResult("Width", i) * scaleFactor;
		height = getResult("Height", i) * scaleFactor;
		
		open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
		run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
		
		Stack.setChannel(channel_hires);
		run("Rotate 90 Degrees Right");
		saveAs("jpg", outDir + File.separator + basename + "_" +roiName);
		close();
	}

}
