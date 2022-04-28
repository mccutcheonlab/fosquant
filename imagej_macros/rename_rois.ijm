var startSection = 0;

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

//	lowresDir = getDir("cwd") + "lowres" + File.separator; // need to check whether this works
//	if (!File.exists(lowresDir)) {
//    	exit("Unable to create directory");
// 		run("Duplicate...", "title=crop");