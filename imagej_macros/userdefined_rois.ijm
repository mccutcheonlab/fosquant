
macro "Add and rename ROI [a]" {

	// get region
	regionOptions = newArray("nacshell", "naccore", "piriform", "caudate_put", "pv_thal", "pv_hypo", "arcuate", "lat_hypo", "parabrac", "raphe");
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

	if (File.exists(roiPath)) {
		arg = getString("ROI file exists in this location. Press A to append or O to overwrite", "");
		if (arg == "O") {
			print("Trying to overwrite...");
			if (getBoolean("Are you sure you want to overwrite")) {
				roiManager("save", roiPath);
				print("Saved file as " + roiPath);
			}
			else {
				print("...but no overwrite selected. Exiting");
			}
		}
		else if (arg == "A") {
			print("appending");
			roiManager("Open", roiPath);
			roiManager("Sort");
			roiManager("save", roiPath);
			print("Saved file as " + roiPath);
		}
		else {
			print("Not a valid option. Exiting macro without saving.");
		}
	}
	else {
		roiManager("save", roiPath);
		print("Saved file as " + roiPath);
	}
}
