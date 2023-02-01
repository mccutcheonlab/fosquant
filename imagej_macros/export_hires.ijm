var parent = "";
var basename = "";

var series_lores = 10;
var series_hires = 9;

var rotation = "180 Degrees";

var channel_1 = false;
var channel_2 = true;
var channel_3 = true;

var	saveJPEG = true;
var	savePNG = false;
var	saveTIFF = false;

macro "Export hires [H]" {
	setBatchMode(true);

	path = File.openDialog("Please pick a .vsi file");

	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	saveOptions = newArray("TIFF", "PNG", "JPG");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series for lores", series_lores);
	Dialog.addNumber("Series for hires", series_hires);
	Dialog.addCheckbox("Channel 1", channel_1);
	Dialog.addCheckbox("Channel 2", channel_2);
	Dialog.addCheckbox("Channel 3", channel_3);
	Dialog.addChoice("Rotation", rotationItems);
	
	Dialog.addMessage("File formats to save as");
	Dialog.addCheckbox("JPEG", saveJPEG);
	Dialog.addCheckbox("PNG", savePNG);
	Dialog.addCheckbox("TIFF", saveTIFF);
	Dialog.show();
	
	series_lores = Dialog.getNumber();
	series_hires = Dialog.getNumber();
	channel_1 = Dialog.getCheckbox();
	channel_2 = Dialog.getCheckbox();
	channel_3 = Dialog.getCheckbox();
	rotation = Dialog.getChoice();
	
	saveJPEG = Dialog.getCheckbox();
	savePNG = Dialog.getCheckbox();
	saveTIFF = Dialog.getCheckbox();
	
	channelArray = newArray(channel_1, channel_2, channel_3);
	for (c=0; c<3; c++) {
		if (channelArray[c] == true) {
			workingChannel = c+1;
			outDir = parent + File.separator + "chan" + workingChannel;
			if (!File.exists(outDir)) {
				File.makeDirectory(parent + File.separator + "chan" + workingChannel);
			}
		}
	}

	scaleFactor = pow(2, (series_lores - series_hires));
	s = series_hires;
	
	roiManager("List");
	n = roiManager("count");
	
	for (i = 0; i < n; i++) {
		tStart = getTime();
		roiName = getResultString("Name", i);
		xPos = getResult("X", i) * scaleFactor;
		yPos = getResult("Y", i) * scaleFactor;
		width = getResult("Width", i) * scaleFactor;
		height = getResult("Height", i) * scaleFactor;
		print("Dimensions are: ", width, "x", height);
		
		open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
		run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
		
		if (saveTIFF == true) {
			tiffDir = parent + File.separator + "raw_tiffs";
			if (!File.exists(tiffDir)) {
				File.makeDirectory(tiffDir);
			}
			save(tiffDir + File.separator + basename + "_" +roiName);
		}
		
		windowName = getTitle();
		run("Split Channels");
		
		for (c=0; c<3; c++) {
			if (channelArray[c] == true) {
				
				workingChannel = c + 1;
				print("Analyzing", basename, "channel", workingChannel, "blaaaaah!");
								
				outDir = parent + File.separator + "chan" + workingChannel;
				print("Saving to", outDir);
				
				input = "C" + workingChannel + "-" + windowName;

				run("CLIJ2 Macro Extensions", "cl_device=");
				Ext.CLIJ2_clear();
				Ext.CLIJ2_push(input);

				output = "ext" + workingChannel;
				radius_x = 2.0;
				radius_y = 2.0;
				sigma = 10.0;
				
				Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(input, output, radius_x, radius_y, sigma);
				
				Ext.CLIJ2_pull(output);
	
				Ext.CLIJ2_clear();
		
				selectWindow(output);
				
				if (rotation == "180 Degrees") {
					run("Rotate 90 Degrees Left");
					run("Rotate 90 Degrees Left");
				}
				else if (rotation == "Rotate 90 Degrees Left") {
					run("Rotate 90 Degrees Left");
				}
				else if (rotation == "Rotate 90 Degrees Right") {
					run("Rotate 90 Degrees Right");
				}
				
				newName = basename + "_chan" + workingChannel + "_" + roiName;
				
				if (saveJPEG == true) {
					saveAs("jpg", outDir + File.separator + newName);
				}
				if (savePNG == true) {
					saveAs("png", outDir + File.separator + newName);
				}
				
				tEnd = getTime();
				tTaken = (tEnd - tStart) / 1000;
				print("Time taken", tTaken);
			}
		}
	close("*");
	}
	close("Overlay Elements of CROPPED_ROI Manager");
	close("ROI Manager");
	
	print("Finished running!");

setBatchMode(false);
}
// time taken to open and save as tiff on GPU machine, series 9 = 72 s
