channel = "chan3";

macro "Process user-defined ROIs [P]" {
	
	channelOptions = newArray("chan2", "chan3", "coloc");
	
	Dialog.create("Process user-defined ROIs");
	Dialog.addChoice("Channel", channelOptions, channel);
	Dialog.show();
	
	channel = Dialog.getChoice();
	
	path = File.openDialog("Please pick a file with user-defined ROIs");
	roiScaleFactor = getNumber("Enter scaling factor for ROIs", 2);

	userdefinedDir = File.getParent(path);
	// outputFile = userdefinedDir + File.separator + need to work out path
	parent = File.getParent(userdefinedDir);
	pngFolder = parent + File.separator + channel;
	
	print(pngFolder);

	roiManager("open", path);
	n = roiManager("count");
	
	//
	for (i = 0; i < n; i++) {
		roiManager("Select", i);
//		run("Scale... ", "x=" + roiScaleFactor + " y=" + roiScaleFactor);
//		roiManager("update");
// 		name = Roi.getName;

 		pngs = getFileList(pngFolder);
 		nFiles = 
 		for (j = 0; j < nFiles; j++) {
 			print(pngs[j]);
 			// check if file matches roi name
 			// if it does open the file
 			// count cells in roi
 			// append data to csv file
 			// increase total counter
 			
 		}


 		
 		// increase total counter
	}
	roiManager("show all with labels");
	
	// add total to csv file
	
	print("Hey there");

}