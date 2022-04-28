series_hires = 13;
path = "C:/Github/fosquant/data/FTP01_A2.vsi";

xPos=100
yPos=100

width=100;
height=100;

s = 8;

//run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_11 width_11=100 height_11=100");

open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;

run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);

//run("Bio-Formats", "open=[path] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_&series_hires x_coordinate_&series_hires=&xPos y_coordinate_&series_hires=&yPos width_&series_hires=&width height_&series_hires=&height");

//
//IJ.run("Bio-Formats Importer", "open=["+origPath+"] color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_1 x_coordinate_1="+str(xPos)+" y_coordinate_1="+str(yPos)+" width_1="+str(width)+" height_1="+str(height)+"")
