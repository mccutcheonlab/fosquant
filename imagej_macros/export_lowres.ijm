var parent = "";
var basename = "";

var rotation = "180 Degrees";

var series_lowres = 11;
var channel_lowres = 2;

macro "Export lowres [L]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
	// add dialog for channel and invert and rotate
		
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_lowres);
	Dialog.addNumber("Channel", channel_lowres);
	Dialog.addChoice("Rotation", rotationItems); 
	Dialog.show();

	series_lowres = Dialog.getNumber();
	channel_lowres = Dialog.getNumber();
	rotation = Dialog.getChoice();
	
	outDir = parent + File.separator + "lowres";
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "lowres");
	}
	
	if (basename == "") {
		//	path = File.openDialog("Please pick a .vsi file");
		path = "C:/Github/fosquant/data/FTP01_A2.vsi";
		parent = File.getParent(path);
		vsiName = File.getName(path);
		basename = replace(vsiName, ".vsi", "");
		run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series_lowres);
	}
	
	Stack.setChannel(channel_lowres);
	run("Duplicate...", "title=inverted");
	run("8-bit");
	run("Invert LUT");
	
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
