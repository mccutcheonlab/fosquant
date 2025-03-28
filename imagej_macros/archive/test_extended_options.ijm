channel = 2;

close("*")

path = "/home/jaime-recent/Data/FT122 40um test/chan3/FT122_1A__s011.tif"
path = "/home/jaime-recent/Data/FT122 40um test/chan2/FT122_1A__s015.tif"

parent = File.getParent(path);
outDir = parent + File.separator + "gpu_options" + File.separator 

open(path)

windowName = getTitle();
run("Split Channels");
selectWindow("C" + channel + "-" + windowName);

makeRectangle(3204, 1540, 372, 360);
run("Duplicate...", "title=crop duplicate");

input = "crop";

run("CLIJ2 Macro Extensions", "cl_device=");
Ext.CLIJ2_clear();
Ext.CLIJ2_push(input);

// set up arrays for radius and sigma
radiusArray = newArray(1.0, 2.0, 3.0, 5.0, 10.0);
sigmaArray = newArray(2.0, 5.0, 10.0, 20.0);


for (r=0; r<5; r++) {
	for (s=0; s<4; s++) {
		radius_x = radiusArray[r];
		radius_y = radiusArray[r];
		sigma = sigmaArray[s];
		output = "ext_" + r + "_" + s;
		
//		Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(input, output, radius_x, radius_y, sigma);
		
		Ext.CLIJ2_pull(output);
		
		saveAs("jpg", outDir + output);
		 
	}
}



