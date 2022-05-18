
macro "Make Colocalized Images [M]" {
	
	chan1Dir = getDirectory("Please pick a directory with masked PNGs for first channel.");
	chan2Dir = getDirectory("Please pick a directory with masked PNGs for second channel.");
	
	parent = File.getParent(chan1Dir);
	colocDir = parent + File.separator + "coloc";
			if (!File.exists(colocDir)) {
				File.makeDirectory(colocDir);
			}

	chan1Files = getFileList(chan1Dir);
	chan2Files = getFileList(chan2Dir);
	
	print(chan1Files.length);
	
	if (chan1Files.length != chan2Files.length) {
		exit("Different numbers of files in each folder. Exiting macro.");
	}

	for (i=0; i<chan1Files.length; i++) {
		currentSectionNumber = getSectionNumber(chan1Files[i]);
		for (j=0; j<chan2Files.length; j++) {
			chan2SectionNumber = getSectionNumber(chan2Files[j]);
			if (chan2SectionNumber == currentSectionNumber) {
				print(currentSectionNumber, "is go go go");
				open(chan1Files[i]);
				chan1Img = getImageID();
				open(chan2Files[j]);
				chan2Img = getImageID();
				imageCalculator("AND create", chan1Img, chan2Img);
				run("Analyze Particles...", "size=10-Infinity circularity=0.20-1.00 show=Masks display clear include composite");
				maskImg = getImageID();
				saveAs("png", chan1Dir + File.separator + "coloc_s" + currentSectionNumber);
			}
		}
//		open(chan1Files[i]);
//		currentFilename = File.nameWithoutExtension;
//		section = split(currentFilename, "(_s)");
//		getSectionNumber(chan1Files[i]);
//		print(i, chan1Files[i]);
	}
	
	close("*");
	
}

function getSectionNumber(filename) {
	filenameWithoutExtension = replace(filename, ".png", "");
	section = split(filenameWithoutExtension, "(_s)");
	sectionNumber = section[1];
	return sectionNumber;
}
