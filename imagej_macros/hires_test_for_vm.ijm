
selectWindow("FT104_1A__s000.tif");
run("Duplicate...", "duplicate");
selectWindow("FT104_1A__s000-1.tif");

windowName = getTitle();
run("Split Channels");

input = "C" + 2 + "-" + windowName;

run("CLIJ2 Macro Extensions", "cl_device=");
Ext.CLIJ2_clear();
Ext.CLIJ2_push(input);

output = "ext2";
radius_x = 2.0;
radius_y = 2.0;
sigma = 10.0;

Ext.CLIJ2_extendedDepthOfFocusVarianceProjection(input, output, radius_x, radius_y, sigma);

Ext.CLIJ2_pull(output);

Ext.CLIJ2_clear();
    