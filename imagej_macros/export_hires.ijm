var parent = "";
var basename = "";

var series_hires = 8;
var channel = 1;

macro "Export hires [H]" {
	// test if there is an open image and ROIs and if ROIs are named correctly
	// add dialog for channel and invert and rotate
	
//	if (basename == "") {
//		parent = getInfo("image.directory");
//		filename = getInfo("image.filename");
//		basename = replace(filename, ".vsi", "");
//	}
	path = File.openDialog("Please pick a .vsi file");
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series_hires);
	
//	Stack.setChannel(channel);
//	scaleFactor = pow(2, (13 - series_hires));
//
//	n = roiManager("count");
//	for (i = 0; i < n; i++) {
//		roiManager("select", i);
//		run("Scale... ", "x=&scaleFactor y=&scaleFactor");
//		roiManager("update");
//	}
//	
//	array = newArray(n);
//	  for (i=0; i<array.length; i++) {
//	      array[i] = i;
//	  }
//	
//	OutDir = "C:/Github/fosquant/data/lowresmulti/";
//	roiManager("Select", array);
//	RoiManager.multiCrop(OutDir, " show");
//	roiManager("List");
//	
//	for (i = 0; i < n; i++) {
//		ROIName=getResultString("Name", i, "Overlay Elements of CROPPED_ROI Manager");
//		selectWindow("CROPPED_ROI Manager");
//		setSlice(i+1);
//		run("Duplicate...", "title="+basename+"_"+ROIName);
//		saveAs("jpg", OutDir+basename+"_"+ROIName);
//		close();
//	}
//	
//	close("*");
//	close("Overlay Elements of CROPPED_ROI Manager");
//	close("ROI Manager");



//	hiresDir = parent + File.separator + "lowres"; // need to check whether this works
//	if (!File.exists(hiresDir)) {
//    	exit("Unable to create directory");
//	}


}
