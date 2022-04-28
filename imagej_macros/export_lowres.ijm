var parent = "";
var basename = "";

channel_lowres = 1;

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
