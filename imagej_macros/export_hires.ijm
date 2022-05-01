var parent = "";
var basename = "";

var series_hires = 11;
var channel_hires = 2;

var rotation = "180 Degrees";

macro "Export hires [H]" {
	setBatchMode(true);
	// test if there is an open image and ROIs and if ROIs are named correctly
	// add dialog for channel and invert and rotate

	path = File.openDialog("Please pick a .vsi file");
//	path = "C:/Github/fosquant/data/FTP01_A2.vsi";
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_hires);
	Dialog.addNumber("Channel", channel_hires);
	Dialog.addChoice("Rotation", rotationItems); 
	Dialog.show();
	
	series_hires = Dialog.getNumber();
	channel_hires = Dialog.getNumber();
	rotation = Dialog.getChoice();
	
	outDir = parent + File.separator + "chan" + channel_hires;
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "chan" + channel_hires);
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

//		windowName = getTitle();
//		run("Split Channels");
//		selectWindow("C" + channel_hires + "-" + windowName);
//
//		run("EDF Easy mode", "quality='4' topology='1' show-topology='off' show-view='off'");
//			
//		while (nImages <= 3) {
//			// Waits for plugin to complete
//		}
//		
//		selectWindow("Output");		
//						
//		run("Z Project...", "projection=[Max Intensity]");
		
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
		
//		saveAs("jpg", outDir + File.separator + basename + "_" +roiName);
		save(outDir + File.separator + basename + "_" +roiName);

		close("*");
		tEnd = getTime();
		tTaken = (tEnd - tStart) / 1000;
		print("Time taken", tTaken);
	}

	close("*");
	close("Overlay Elements of CROPPED_ROI Manager");
//	close("ROI Manager");

setBatchMode(false);
}
