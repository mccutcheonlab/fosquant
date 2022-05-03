var parent = "";
var basename = "";

var channel_1 = false;
var channel_2 = true;
var channel_3 = false;

var rotation = "180 Degrees";

macro "Export hires [H]" {
	setBatchMode(true);

	parent = getDirectory("Please pick a directory with tifs.");
	
	rotationItems = newArray("None", "Rotate 90 Degrees Left", "Rotate 90 Degrees Right", "180 Degrees");
	
	Dialog.create("Choose options");
	Dialog.addCheckbox("Channel 1", channel_1);
	Dialog.addCheckbox("Channel 2", channel_2);
	Dialog.addCheckbox("Channel 3", channel_3);
	Dialog.addChoice("Rotation", rotationItems); 
	Dialog.show();

	channel_1 = Dialog.getCheckbox();
	channel_2 = Dialog.getCheckbox();
	channel_3 = Dialog.getCheckbox();
	rotation = Dialog.getChoice();
	
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

	files = getFileList(parent);
	nFiles = files.length;
	
	for (i = 0; i < nFiles; i++) {

		if (endsWith(files[i], ".tif")) {
			tifFile = files[i];
			basename = replace(tifFile, ".tif", "");
			
			tStart = getTime();
			open(parent + File.separator + tifFile);
	
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
					bn = split(basename, "_");
					newName = bn[0] + "_" + bn[1] + "_chan" + workingChannel + "_" + bn[2];
					
					saveAs("jpg", outDir + File.separator + newName);
	
					tEnd = getTime();
					tTaken = (tEnd - tStart) / 1000;
					print("Time taken", tTaken);
				}
			}
	close("*");
		}
	}

setBatchMode(false);
}

// time taken to open and save as tiff on GPU machine, series 9 = 72 s
