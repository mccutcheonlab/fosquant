series_hires = 13;
path = "C:/Github/fosquant/data/FTP01_A2.vsi";

xPos=100;
yPos=100;

width=100;
height=100;

s = 12;

open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;

run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
