t0=getTime()

print("Running macro to export ROIs as HIRES tiff images");

argString = getArgument();
args = split(argString, "(, )");

// // these lines need to be changed to reflect args in...
vsipath = args[0];
roispath = args[1];

series_rois = parseInt(args[2]);
series_hires = parseInt(args[3]);

rotation = args[4];

print("Done.");

setBatchMode(true);

current = File.getParent(vsipath);
parent = File.getParent(current) + File.separator + "hires";
if (!File.exists(parent)) {
    File.makeDirectory(parent);
}

vsiName = File.getName(vsipath);
basename = replace(vsiName, ".vsi", "");

scaleFactor = pow(2, (series_rois - series_hires));
s = series_hires;

print(scaleFactor);

roiManager("open", roispath);
n = roiManager("count");
print(n);
roiManager("List");

// for (i = 0; i < n; i++) {
//     tStart = getTime();
//     roiName = getResultString("Name", i);
//     xPos = getResult("X", i) * scaleFactor;
//     yPos = getResult("Y", i) * scaleFactor;
//     width = getResult("Width", i) * scaleFactor;
//     height = getResult("Height", i) * scaleFactor;
//     print("Dimensions are: ", width, "x", height);
    
//     open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
    
//     run("Bio-Formats", "open=" + vsipath + " autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
    
//     if (rotation == "upsidedown") {
//         run("Rotate 90 Degrees Left");
//         run("Rotate 90 Degrees Left");
//     }
//     else if (rotation == "anticlockwise") {
//         run("Rotate 90 Degrees Left");
//     }
//     else if (rotation == "clockwise") {
//         run("Rotate 90 Degrees Right");
//     }

//     tifDir = parent + File.separator + "raw_tifs";
//     if (!File.exists(tifDir)) {
//         File.makeDirectory(tifDir);
//     }
//     save(tifDir + File.separator + basename + "_" +roiName);
//     close("*");
//     tEnd = getTime();
//     tTaken = (tEnd - tStart) / 1000;
//     print("Time taken for", roiName, ":", tTaken);
// }
close("Overlay Elements of CROPPED_ROI Manager");
close("ROI Manager");

print("Finished running!");
    
setBatchMode(false);
run("Quit");

