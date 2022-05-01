
macro "focus_image [F]" {
	tStart = getTime();
	path = "/home/jaime/Data/FT122/chan3/FT122_1A__s012.tif";
	
	open(path);
	
	
	
	tEnd = getTime();
	tTaken = (tEnd - tStart) / 1000;
	print("Time taken: ", tTaken, "s");
}

// 7.05 s to open tif
