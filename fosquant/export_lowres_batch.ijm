t0=getTime()

print("Running macro to export ROIs as lowres images");

argString = getArgument();
args = split(argString, "(, )");

// // these lines need to be changed to reflect args in...
vsipath = args[0];
roispath = args[1];
series_lowres = args[2];
channel_lowres = args[3];
rotation = args[4]; // ensure to pass correct option, include possibilities in .py help

if (args[5] == "invertOn") {
    print("Inverting");
    invertImage = true;
}
else {
    invertImage = false;
}

roiScaleFactor = 4;

print(args[0]);
print("Next line");

roiManager("open", roispath);

run("Bio-Formats", "open=" + vsipath + " autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_" + series_lowres);
	
currentDir = getInfo("image.directory");
parent = File.getParent(currentDir);
vsiName = getInfo("image.filename");
basename = replace(vsiName, ".vsi", "");
	
outDir = parent + File.separator + "lowres";
print(outDir);
if (!File.exists(outDir)) {
    File.makeDirectory(parent + File.separator + "lowres");
}

run("Select None");
	
Stack.setChannel(channel_lowres);
run("Duplicate...", "title=inverted");
run("8-bit");
	
if (invertImage == true) {
    run("Invert LUT");
}
	
id = getImageID();
	
n = roiManager("count");

for (i = 0; i < n; i++) {
    selectImage(id);
    run("Duplicate...", "title=crop");

    roiManager("select", i);
    run("Scale... ", "x=" + roiScaleFactor + " y=" + roiScaleFactor);
    roiManager("update");
    sectionNumber = Roi.getName();
    
    run("Crop");
    run("Gamma...", "value=0.50");

    if (rotation == "upsidedown") {
        run("Rotate 90 Degrees Left");
        run("Rotate 90 Degrees Left");
    }
    else if (rotation == "anticlockwise") {
        run("Rotate 90 Degrees Left");
    }
    else if (rotation == "clockwise") {
        run("Rotate 90 Degrees Right")
    }

    savefile = outDir + File.separator + basename + "_lowres" + sectionNumber + ".jpg";
    saveAs("Jpeg", savefile);
    close();
}
selectImage(id);
close();

