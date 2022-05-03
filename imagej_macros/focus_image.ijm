
var channel_hires=3;

macro "focus_image [F]" {
	tStart = getTime();
//	path = "/home/jaime/Data/FT122/chan3/FT122_1A__s012.tif";
	path = "D:/Test Data/histology/demo_FT122/chan2/FT122_1A__s012.tif";
	open(path);

	windowName = getTitle();
	
	print("Opened", windowName);
	
	run("Split Channels");
	selectWindow("C" + channel_hires + "-" + windowName);
	
	// To try with GPU acceleration
	makeRectangle(10960, 1280, 1072, 1024);
	run("Duplicate...", "title=crop duplicate");
	
//	run("CLIJ2 Macro Extensions", "cl_device=");
//	Ext.CLIJ2_clear();
//	
//	input = getTitle();
//	
//	time = getTime();
//	Ext.CLIJ2_push(input);
//	print("Pushing one image to the GPU took " + (getTime() - time) + " msec");
//	
//	// clean up ImageJ
//	run("Close All");
//	
//	Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(input, output, 3, 3, 5);
//
//	Ext.CLIJ2_getGPUProperties(gpu, memory, opencl_version);
//	print("GPU: " + gpu);
//	print("Memory in GB: " + (memory / 1024 / 1024 / 1024) );
//	print("OpenCL version: " + opencl_version);
//
//	Ext.CLIJ2_clear();
	
// extended depth of focus tenengrad projection
//image1 = "CLIJ2 Image of crop";
//Ext.CLIJ2_push(image1);
//image2 = "extended_depth_of_focus_tenengrad_projection427575626";
//sigma = 10.0;
//Ext.CLIJ2_extendedDepthOfFocusTenengradProjection(image1, image2, sigma);
//Ext.CLIJ2_pull(image2);
//selectWindow("CLIJ2 Image of crop");
//
//// extended depth of focus variance projection
//Ext.CLIJ2_push(image1);
//image3 = "extended_depth_of_focus_variance_projection1975025239";
//radius_x = 2.0;
//radius_y = 2.0;
//sigma = 10.0;
//Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(image1, image3, radius_x, radius_y, sigma);
//Ext.CLIJ2_pull(image3);
//selectWindow("CLIJ2 Image of crop");
//
//// extended depth of focus sobel projection
//Ext.CLIJ2_push(image1);
//image4 = "extended_depth_of_focus_sobel_projection1900342545";
//sigma = 10.0;
//Ext.CLIJ2_extendedDepthOfFocusSobelProjection(image1, image4, sigma


//	run("EDF Easy mode", "quality='1' topology='1' show-topology='off' show-view='off'");
//		
//	while (nImages <= 3) {
//		// Waits for plugin to complete
//	}

	tEnd = getTime();
	tTaken = (tEnd - tStart) / 1000;
	print("Time taken: ", tTaken, "s");
}

// 7.05 s to open 5GB tif on server
// 3.1 s to open 1.3GB tif on laptop

// 63 s to open and process tif on laptop - series 9, quality 1
// 717 s as above but quality 4

// 337 s to open and process tif on laptop - series 8, quality 1
