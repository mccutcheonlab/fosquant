#@ int (label="Section number to start from", description="Starting section", persist=false, value=0) startSection

macro "Load ROIs" {
	// #@ File(label="Select a directory", style="directory", value="D:/Test Data/histology/fostrappilot/") defaultDir
	// path = File.openDialog("Please pick a file with ROIs");
	path = "D:/Test Data/histology/fostrappilot/"
	roiManager("open", path);
}

macro "Rename ROIs" {
	n = roiManager('count');
	print(n);
	if (n = 0) {
		exit("No ROIs to process");
		// maybe run Load ROIs macro here
	}
	lowresDir = getDir("cwd") + "lowres" + File.separator; // need to check whether this works
	if (!File.exists(lowresDir)) {
    	exit("Unable to create directory");
	}
	for (i = 0; i < n; i++) {
		run("Duplicate...", "title=crop");
	    roiManager('select', i);
	    currentSection = startSection + i;
	    if (currentSection < 10) {
	    	sectionNumber = "_s00" + currentSection;
	    } else {
	    	sectionNumber = "_s0" + currentSection;
	    }
	    roiManager("rename", sectionNumber)
	}
}

macro "Save ROIs" {
	print("Hey")
}
