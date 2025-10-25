var channel_lowres = 1;
var basename = "";
var roipath = "";

macro "Install Startup Macros [M]" {
    run("Install...", "install=C:/Users/jmc010/AppData/Local/fiji-win64/Fiji.app/macros/StartupMacros.fiji.ijm");
}

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
	sectionpath = parent + File.separator + baseName + "_sections.zip";
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

var startSection = 0;

macro "Rename Section ROIs [R]" {
	
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
	    	sectionNumber = "s00" + currentSection;
	    } else {
	    	sectionNumber = "s0" + currentSection;
	    }
	    roiManager("rename", sectionNumber)
	}
}

var sectionpath = "";
var sectionSuffix = "";

macro "Save Section ROIs [S]" {
	
	sectionSuffix = getString("Add section ROI suffix if required", sectionSuffix);
	
	if (roipath == "") {
		path = getInfo("image.directory");
		filename = getInfo("image.filename");
	
		basename = replace(filename, ".vsi", "");
		basename = replace(basename, ".tif", "");
		sectionpath = path + File.separator + basename + sectionSuffix + "_sections.zip";
	}
	print(sectionpath); 
	roiManager("save", sectionpath);
	showMessage("Section ROIs saved successfully in " + sectionpath);
}

macro "Load ROIs [L]" {
	
	path = File.openDialog("Please pick a file with ROIs");
	roiScaleFactor = getNumber("Enter scaling factor for ROIs", 1);

	roiManager("open", path);
	
	n = roiManager("count");
	for (i = 0; i < n; i++) {
		roiManager("Select", i);
		run("Scale... ", "x=" + roiScaleFactor + " y=" + roiScaleFactor);
		roiManager("update");
	}
	roiManager("show all with labels");
}

var rotation = "180 Degrees";
var invertImage = false;

var parent = "";
var basename = "";

macro "Export lowres [E]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
		
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Channel", channel_lowres);
	Dialog.addChoice("Rotation", rotationItems);
	Dialog.addCheckbox("Invert", invertImage);
	Dialog.show();

	channel_lowres = Dialog.getNumber();
	rotation = Dialog.getChoice();
	invertImage = Dialog.getCheckbox();
	
//	if (!isOpen("*")) {
//		print("There should not be a file open");
//		path = File.openDialog("Please pick the raw tiff file");
//		// path = "C:/Github/fosquant/data/FTP01_A2.vsi";
//		parent = File.getParent(path);
//		tifName = File.getName(path);
//		basename = replace(tifName, ".tif", "");
//		open(path);
//	}
//	
//	else {
//		print("There should be a file open")
//		parent = getInfo("image.directory");
//	}
	
	currentDir = getInfo("image.directory");
	parent = File.getParent(currentDir)
	tifName = getInfo("image.filename");
	basename = replace(tifName, ".tif", "");
	
	outDir = parent + File.separator + "lowres";
	print(outDir);
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "lowres");
	}
	
	run("Select None");
	
	Stack.setChannel(channel_lowres);
	run("Duplicate...", "title=inverted");
	run("8-bit");
	
	if (invertImage == true) {
		run("Invert LUT");
	}
	
	id = getImageID();
	
	n = roiManager("count");
	for (i = 0; i < n; i++) {
		selectImage(id);
		run("Duplicate...", "title=crop");
	    roiManager("select", i);
	    sectionNumber = Roi.getName();
	    
	    run("Crop");
	    
	    if (rotation == "180 Degrees") {
			run("Rotate 90 Degrees Left");
			run("Rotate 90 Degrees Left");
		}
		else if (rotation == "Rotate 90 Degrees Left") {
			run("Rotate 90 Degrees Left");
		}
		else if (rotation == "Rotate 90 Degrees Right") {
			run("Rotate 90 Degrees Right")
		}

		savefile = outDir + File.separator + basename + "_lowres_" + sectionNumber + ".jpg";
	    saveAs("Jpeg", savefile);
    	close();
	}
	selectImage(id);
	close();
}

// User-defined ROI macros

macro "Add and rename ROI [a]" {

	// get region
	regionOptions = newArray("motorctx", "sensoryctx", "insulactx", "nacshell", "naccore", "piriform", "caudate_put", "pv_thal", "pv_hypo", "arcuate", "lat_hypo", "parabrac", "raphe");
	Dialog.create("Choose region");
	Dialog.addChoice("Region", regionOptions);
	Dialog.show();
	region = Dialog.getChoice();
	
	// get section number
	imageFilename = getInfo("Image.title");
	tempString = split(imageFilename, "(_s)");
	sectionNumber = replace(tempString[1], ".jpg", "");
	
	// add and select ROI
	roiManager("Add");
	n = roiManager("count");
	roiManager("Select", n-1);
	
	// rename ROI
	roiName = "s" + sectionNumber + "_" + region;
	roiManager("rename", roiName);
	
	// Add overlay
	run("Add Selection...");
	run("Overlay Options...", "stroke=red width=10 fill=none set apply");
}

macro "Save all ROIs [s]" {
	
	imageFilename = getInfo("Image.title");
	tempString = split(imageFilename, "_");
	mouseID = tempString[0];
	
	path = getInfo("image.directory");
	
	roiPath = path + mouseID + "_userdefined_ROIs.zip";

	if (File.exists(roiPath)) {
		arg = getString("ROI file exists in this location. Press A to append or O to overwrite", "");
		if (arg == "O") {
			print("Trying to overwrite...");
			if (getBoolean("Are you sure you want to overwrite")) {
				roiManager("save", roiPath);
				print("Saved file as " + roiPath);
			}
			else {
				print("...but no overwrite selected. Exiting");
			}
		}
		else if (arg == "A") {
			print("appending");
			roiManager("Open", roiPath);
			roiManager("Sort");
			roiManager("save", roiPath);
			print("Saved file as " + roiPath);
		}
		else {
			print("Not a valid option. Exiting macro without saving.")
;
		}
	}
	else {
		roiManager("save", roiPath);
		print("Saved file as " + roiPath);
	}
}

