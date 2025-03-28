
var roipath = "";
var roiScaleFactor = 1;

macro "Load ROIs [L]" {
	path = File.openDialog("Please pick a file with ROIs");
	roiScaleFactor = getNumber("Enter scaling factor for ROIs", 1);

	roiManager("open", path);
	
	n = roiManager("count");
	for (i = 0; i < n; i++) {
		roiManager("Select", i);
		run("Scale... ", "x=" + roiScaleFactor + " y=" + roiScaleFactor);
		roiManager("update");
	}
	roiManager("show all with labels");
}