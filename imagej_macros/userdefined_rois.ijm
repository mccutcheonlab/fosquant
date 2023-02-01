macro "User ROIs [U]" {

	imageFilename = getInfo("Image.title");
	tempString = split(imageFilename, "(_s)");
	sectionNumber = replace(tempString[1], ".jpg", "");

	n = roiManager("count");
	print(n);
	if (n == 0) {
		exit("No ROIs to process");
	}
	
	counter=1;
	
	for (i = 0; i < n; i++) {
	    roiManager("select", i);
	    name = Roi.getName;
	    if (startsWith(name, "s")) {
	    	continue;
	    }
	    else {
	    	roiManager("rename", "s" + sectionNumber + "_n" + counter);
	    	counter = counter + 1;
	    	
	    }
	}	
}

macro "Save user-defined ROIs [D]" {
		
	region = getString("Add name for brain region", "");
	
	path = getInfo("image.directory");
	parent = File.getParent(path);

	roipath = parent + File.separator + "userdefined_rois" + File.separator + region + "_ROIs.zip";

	print(roipath); 
	roiManager("save", roipath);
	showMessage("ROIs saved successfully in " + roipath);
}

