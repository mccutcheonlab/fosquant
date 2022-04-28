series_hires = 8;
path = "C:/Github/fosquant/data/FTP01_A2.vsi";


run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_8 x_coordinate_1=100 y_coordinate_1=100 width_1=1000 height_1=1000");

//
//IJ.run("Bio-Formats Importer", "open=["+origPath+"] color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_1 x_coordinate_1="+str(xPos)+" y_coordinate_1="+str(yPos)+" width_1="+str(width)+" height_1="+str(height)+"")
