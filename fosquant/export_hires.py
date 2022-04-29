# %% 
import imagej
# ij = imagej.init('sc.fiji:fiji:2.1.1')
ij = imagej.init()
ij.getVersion()

# %%
macro = """

    series_hires = 11
    channel_hires = 2
	path = "C:/Github/fosquant/data/FTP01_A2.vsi";
	parent = File.getParent(path);
	vsiName = File.getName(path);
	basename = replace(vsiName, ".vsi", "");
	
	Dialog.create("Choose options");
	Dialog.addNumber("Series", series_hires);
	Dialog.addNumber("Channel", channel_hires);
	Dialog.show();
	
	outDir = parent + File.separator + "chan" + channel_hires;
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "chan" + channel_hires);
	}
	
	series_hires = Dialog.getNumber();
	channel_hires = Dialog.getNumber();
	
	scaleFactor = pow(2, (13 - series_hires));
	s = series_hires;
	
	roiManager("List");
	n = roiManager("count");
	
	for (i = 0; i < n; i++) {	
		roiName = getResultString("Name", i);
		xPos = getResult("X", i) * scaleFactor;
		yPos = getResult("Y", i) * scaleFactor;
		width = getResult("Width", i) * scaleFactor;
		height = getResult("Height", i) * scaleFactor;
		
		open_string = " series_" + s + " x_coordinate_" + s + "=" + xPos + " y_coordinate_" + s + "=" + yPos + " width_" + s + "=" + width + " height_" + s + "=" + height;
		run("Bio-Formats", "open=[path] autoscale color_mode=Default crop rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT" + open_string);
		
		Stack.setChannel(channel_hires);
		run("Rotate 90 Degrees Right");
		saveAs("jpg", outDir + File.separator + basename + "_" +roiName);
		close();

"""
# %%
ij.py.run_macro(macro)
# %%
