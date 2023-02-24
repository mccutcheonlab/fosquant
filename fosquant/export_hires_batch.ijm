t0=getTime()

print("Running macro to export ROIs as HIRES tiff images");

argString = getArgument();
args = split(argString, "(, )");

// // these lines need to be changed to reflect args in...
vsipath = args[0];
roispath = args[1];

series_rois = parseInt(args[2]);
series_hires = parseInt(args[3]);

rotation = args[7];

// setBatchMode(true);

// current = File.getParent(vsipath);
// parent = File.getParent(current) + File.separator + "hires";
// File.makeDirectory(parent);

// vsiName = File.getName(vsipath);
// basename = replace(vsiName, ".vsi", "");

// scaleFactor = pow(2, (series_rois - series_hires));
// s = series_hires;

// print(scaleFactor);

// roiManager("open", roispath);
// n = roiManager("count");
// print(n);
// roiManager("List");

for (i = 0; i < n; i++) {
    tStart = getTime();
    roiName = getResultString("Name", i);
    xPos = getResult("X", i) * scaleFactor;
    yPos = getResult("Y", i) * scaleFactor;
    width = getResult("Width", i) * scaleFactor;
    height = getResult("Height", i) * scaleFactor;
    print("Dimensions are: ", width, "x", height);
    
    open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
    
    run("Bio-Formats", "open=" + vsipath + " autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
    
    if (rotation == "upsidedown") {
        run("Rotate 90 Degrees Left");
        run("Rotate 90 Degrees Left");
    }
    else if (rotation == "anticlockwise") {
        run("Rotate 90 Degrees Left");
    }
    else if (rotation == "clockwise") {
        run("Rotate 90 Degrees Right");
    }

    tiffDir = parent + File.separator + "raw_tifs";
    if (!File.exists(tiffDir)) {
        File.makeDirectory(tiffDir);
    }
    save(tiffDir + File.separator + basename + "_" +roiName);
    close("*");
}
close("Overlay Elements of CROPPED_ROI Manager");
close("ROI Manager");

print("Finished running!");
    
// //     windowName = getTitle();
// //     run("Split Channels");
    
// //     for (c=0; c<3; c++) {
// //         if (channelArray[c] == true) {
            
// //             workingChannel = c + 1;
// //             print("Analyzing", basename, "channel", workingChannel, "blaaaaah!");
                            
// //             outDir = parent + File.separator + "chan" + workingChannel;
// //             File.makeDirectory(outDir);
// //             print("Saving to", outDir);
            
// //             input = "C" + workingChannel + "-" + windowName;

// //             run("CLIJ2 Macro Extensions", "cl_device=");
// //             Ext.CLIJ2_clear();
// //             Ext.CLIJ2_push(input);

// //             output = "ext" + workingChannel;
// //             radius_x = 2.0;
// //             radius_y = 2.0;
// //             sigma = 10.0;
            
// //             Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(input, output, radius_x, radius_y, sigma);
            
// //             Ext.CLIJ2_pull(output);

// //             Ext.CLIJ2_clear();
    
// //             selectWindow(output);
            
// //             if (rotation == "upsidedown") {
// //                 run("Rotate 90 Degrees Left");
// //                 run("Rotate 90 Degrees Left");
// //             }
// //             else if (rotation == "anticlockwise") {
// //                 run("Rotate 90 Degrees Left");
// //             }
// //             else if (rotation == "clockwise") {
// //                 run("Rotate 90 Degrees Right");
// //             }
            
// //             newName = basename + "_chan" + workingChannel + "_" + roiName;
                        
// //             tEnd = getTime();
// //             tTaken = (tEnd - tStart) / 1000;
// //             print("Time taken", tTaken);
// //         }
// //     }


// // setBatchMode(false);
