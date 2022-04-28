#@ Integer (label="Please choose channel to use for low res", description="Channel", persist=false, min=1, max=3, value=1) channel
#@ Integer (label="Please choose series to load for low res", description="Series", persist=false, value=5) series
#@ File(label="Select a directory", style="directory", value="D:/Test Data/histology/fostrappilot/") defaultDir

macro "Export lowres" {
	path = File.openDialog("Please pick a .vsi file");
	parent = File.getParent(path);
	vsiName = File.getName(path);
	baseName = replace(vsiName, ".vsi", "");
	
	run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_5");
	// work out how to select channel
	
	roiFile = parent + File.separator + "RoiSet_" + baseName + ".zip";
	
	roiManager("open", roiFile);
	n = roiManager('count');
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
	    run("Crop");
	    run("Rotate 90 Degrees Right");
	    run("8-bit");
		run("Invert LUT");
	    saveAs("Jpeg", parent + File.separator + baseName + "_lowres" + sectionNumber + ".jpg");
    	close();
}
