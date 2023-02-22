
macro "Add and rename ROI [a]" {

	// get region
	regionOptions = newArray("nacshell", "naccore", "piriform", "pvn");
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

macro "Save all ROIs [S]" {
	
	imageFilename = getInfo("Image.title");
	tempString = split(imageFilename, "_");
	mouseID = tempString[0];
	
	path = getInfo("image.directory");
	
	roiPath = path + mouseID + "_userdefined_ROIs.zip";
	print("Saved file as " + roiPath);
	roiManager("save", roiPath);
}
