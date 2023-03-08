var channel_lowres = 2;
var series_lowres = 13;

var channel_hires = 2;
var series_hires = 9;

var rotation = "180 Degrees";
var invertImage = false;

var parent = "";
var basename = "";

// For load, save, and rename ROIs
var roipath = "";
var roiScaleFactor = 1;
var roiSuffix = "";
var startSection = 0;

// For  export hires options
var channel_1 = false;
var channel_2 = true;
var channel_3 = true;

var	saveJPEG = true;
var	savePNG = false;
var	saveTIFF = false;

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
	
	roiSuffix = getString("Add ROI suffix if required", roiSuffix);
	
	if (roipath == "") {
		path = getInfo("image.directory");
		filename = getInfo("image.filename");
	
		basename = replace(filename, ".vsi", "");
		roipath = path + File.separator + basename + roiSuffix + "_ROIs.zip";
	}
	print(roipath); 
	roiManager("save", roipath);
	showMessage("ROIs saved successfully in " + roipath);
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

macro "Export lowres [E]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
		
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_lowres);
	Dialog.addNumber("Channel", channel_lowres);
	Dialog.addChoice("Rotation", rotationItems);
	Dialog.addCheckbox("Invert", invertImage);
	Dialog.show();

	series_lowres = Dialog.getNumber();
	channel_lowres = Dialog.getNumber();
	rotation = Dialog.getChoice();
	invertImage = Dialog.getCheckbox();
	
//	if (!isOpen("*")) {
//		print("There should not be a file open");
//		path = File.openDialog("Please pick a .vsi file");
//		// path = "C:/Github/fosquant/data/FTP01_A2.vsi";
//		parent = File.getParent(path);
//		vsiName = File.getName(path);
//		basename = replace(vsiName, ".vsi", "");
//		run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series_lowres);
//	}
//	
//	else {
//		print("There should be a file open")
//		parent = getInfo("image.directory");
//	}
	
	currentDir = getInfo("image.directory");
	parent = File.getParent(currentDir)
	vsiName = getInfo("image.filename");
	basename = replace(vsiName, ".vsi", "");
	
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

		savefile = outDir + File.separator + basename + "_lowres" + sectionNumber + ".jpg";
	    saveAs("Jpeg", savefile);
    	close();
	}
	selectImage(id);
	close();
}

macro "Export hires [H]" {
	setBatchMode(true);

	path = File.openDialog("Please pick a .vsi file");

	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	saveOptions = newArray("TIFF", "PNG", "JPG");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_hires);
	Dialog.addCheckbox("Channel 1", channel_1);
	Dialog.addCheckbox("Channel 2", channel_2);
	Dialog.addCheckbox("Channel 3", channel_3);
	Dialog.addChoice("Rotation", rotationItems);
	
	Dialog.addMessage("File formats to save as");
	Dialog.addCheckbox("JPEG", saveJPEG);
	Dialog.addCheckbox("PNG", savePNG);
	Dialog.addCheckbox("TIFF", saveTIFF);
	Dialog.show();
	
	series_hires = Dialog.getNumber();
	channel_1 = Dialog.getCheckbox();
	channel_2 = Dialog.getCheckbox();
	channel_3 = Dialog.getCheckbox();
	rotation = Dialog.getChoice();
	
	saveJPEG = Dialog.getCheckbox();
	savePNG = Dialog.getCheckbox();
	saveTIFF = Dialog.getCheckbox();
	
	channelArray = newArray(channel_1, channel_2, channel_3);
	for (c=0; c<3; c++) {
		if (channelArray[c] == true) {
			workingChannel = c+1;
			outDir = parent + File.separator + "chan" + workingChannel;
			if (!File.exists(outDir)) {
				File.makeDirectory(parent + File.separator + "chan" + workingChannel);
			}
		}
	}

	scaleFactor = pow(2, (13 - series_hires));
	s = series_hires;
	
	roiManager("List");
	n = roiManager("count");
	
	for (i = 0; i < n; i++) {
		tStart = getTime();
		roiName = getResultString("Name", i);
		xPos = getResult("X", i) * scaleFactor;
		yPos = getResult("Y", i) * scaleFactor;
		width = getResult("Width", i) * scaleFactor;
		height = getResult("Height", i) * scaleFactor;
		print("Dimensions are: ", width, "x", height);
		
		open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
		run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
		
		if (saveTIFF == true) {
			tiffDir = parent + File.separator + "raw_tiffs";
			if (!File.exists(tiffDir)) {
				File.makeDirectory(tiffDir);
			}
			save(tiffDir + File.separator + basename + "_" +roiName);
		}
		
		windowName = getTitle();
		run("Split Channels");
		
		for (c=0; c<3; c++) {
			if (channelArray[c] == true) {
				
				workingChannel = c + 1;
				print("Analyzing", basename, "channel", workingChannel, "blaaaaah!");
								
				outDir = parent + File.separator + "chan" + workingChannel;
				print("Saving to", outDir);
				
				input = "C" + workingChannel + "-" + windowName;

				run("CLIJ2 Macro Extensions", "cl_device=");
				Ext.CLIJ2_clear();
				Ext.CLIJ2_push(input);

				output = "ext" + workingChannel;
				radius_x = 2.0;
				radius_y = 2.0;
				sigma = 10.0; 
				
				Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(input, output, radius_x, radius_y, sigma);
				
				Ext.CLIJ2_pull(output);
	
				Ext.CLIJ2_clear();
		
				selectWindow(output);
				
				if (rotation == "180 Degrees") {
					run("Rotate 90 Degrees Left");
					run("Rotate 90 Degrees Left");
				}
				else if (rotation == "Rotate 90 Degrees Left") {
					run("Rotate 90 Degrees Left");
				}
				else if (rotation == "Rotate 90 Degrees Right") {
					run("Rotate 90 Degrees Right");
				}
				
				newName = basename + "_chan" + workingChannel + "_" + roiName;
				
				if (saveJPEG == true) {
					saveAs("jpg", outDir + File.separator + newName);
				}
				if (savePNG == true) {
					saveAs("png", outDir + File.separator + newName);
				}
				
				tEnd = getTime();
				tTaken = (tEnd - tStart) / 1000;
				print("Time taken", tTaken);
			}
		}
	close("*");
	}
	close("Overlay Elements of CROPPED_ROI Manager");
	close("ROI Manager");

setBatchMode(false);
}

var num = 3;
var width = 250;
var height = 250;
var channel = 1;
var seed = 101279;

macro "Make crops [M]" {
	
	Dialog.create("Choose options");
	Dialog.addNumber("Number", num);
	Dialog.addNumber("Width (px)", width);
	Dialog.addNumber("Height (px)", height);
	Dialog.addNumber("Channel", channel);
	Dialog.addNumber("Random seed", seed);
	Dialog.show();

	num = Dialog.getNumber();
	width = Dialog.getNumber();
	height = Dialog.getNumber();
	channel = Dialog.getNumber();
	seed = Dialog.getNumber();
	
	parent = getDirectory("Please pick a directory with images.");
	
	outDir = parent + File.separator + "crops";
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "crops");
	}
	
	files = getFileList(parent);
	nFiles = files.length;
	
	random("seed", seed);
	
	for (i=0; i<num; i++) {
		shuffle(files);
		file = parent + files[0];
		open(file);

		w = getWidth();
		h = getHeight();
		
		xPos = randomInt(w - width);
		yPos = randomInt(h - height);
		
		makeRectangle(xPos, yPos, width, height);
		run("Crop");
		saveAs("jpg", outDir + File.separator + seed + "_" + i);
		close();
	}

function shuffle(array) {
   n = array.length;  // The number of items left to shuffle (loop invariant).
   while (n > 1) {
      k = randomInt(n);     // 0 <= k < n.
      n--;                  // n is now the last pertinent index;
      temp = array[n];  // swap array[n] with array[k] (does nothing if k==n).
      array[n] = array[k];
      array[k] = temp;
   }
}

// returns a random number, 0 <= k < n
function randomInt(n) {
   return n * random();
}

}
