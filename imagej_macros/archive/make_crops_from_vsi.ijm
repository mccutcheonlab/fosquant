var num = 3;
var width = 500;
var height = 500;
var series_crop = 8;
var channel_crop = 3;
var seed = 101279;

macro "Make crops from .vsi [V]" {
	
	Dialog.create("Choose options");
	Dialog.addNumber("Number", num);
	Dialog.addNumber("Width (px)", width);
	Dialog.addNumber("Height (px)", height);
	Dialog.addNumber("Series", series_crop);
	Dialog.addNumber("Channel", channel_crop);
	Dialog.addNumber("Random seed", seed);
	Dialog.show();

	num = Dialog.getNumber();
	width = Dialog.getNumber();
	height = Dialog.getNumber();
	series_crop = Dialog.getNumber();
	channel_crop = Dialog.getNumber();
	seed = Dialog.getNumber();
	
  	path = File.openDialog("Please pick a .vsi file");
	//path = "C:/Github/fosquant/data/FTP01_A2.vsi";
	
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	outDir = parent + File.separator + "crops";
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "crops");
	}
	
	random("seed", seed);
	
	run("Bio-Formats", "open=[path] autoscale color_mode=Default display_metadata rois_import=[ROI manager] view=[Metadata only] stack_order=XYCZT");

	// These are the row numbers for 10x size (X and Y)
	imageWidth = getResult("Value", 8);
	imageHeight = getResult("Value", 9);
	
	s = series_crop;
	
	for (i=0; i<num; i++) {

		xPos = randomInt(imageWidth - width);
		yPos = randomInt(imageHeight - height);
		
		print(xPos, yPos);
		
		open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
		run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
		
		windowName = getTitle();
		run("Split Channels");
		selectWindow("C" + channel_crop + "-" + windowName);
		
		run("EDF Easy mode", "quality='4' topology='1' show-topology='off' show-view='off'");
		while (nImages <= 3) {
			
		}

		selectWindow("Output");
		saveAs("jpg", outDir + File.separator + seed + "_" + i);
		close("*");
	}
close("Original Metadata - " + vsiName);

// returns a random number, 0 <= k < n
function randomInt(n) {
   return n * random();
}

}
