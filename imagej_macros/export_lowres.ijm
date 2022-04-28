var parent = ""
var basename = ""

macro "Export lowres [L]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
	// add dialog for channel and invert and rotate
	
	if (basename == "") {
		parent = getInfo("image.directory");
		filename = getInfo("image.filename");
		basename = replace(filename, ".vsi", "");
	}
	
	lowresDir = parent + File.separator + "lowres"; // need to check whether this works
	if (!File.exists(lowresDir)) {
    	exit("Unable to create directory");
	}
	
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
		savefile = lowresDir + File.separator + basename + "_lowres" + sectionNumber + ".jpg";
		print(savefile);
	    saveAs("Jpeg", savefile);
    	close();
	}
	selectImage(id);
	close();
}
