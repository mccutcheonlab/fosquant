
macro "Export for Nutil [N]" {
	setBatchMode(true);

	parent = getDirectory("Please pick a directory with masked PNGs.");
	
	outDir = parent + File.separator + "nutil";
			if (!File.exists(outDir)) {
				File.makeDirectory(outDir);
			}
	
	files = getFileList(parent);
	nFiles = files.length;
	
	for (i = 0; i<nFiles; i++) {
		if (endsWith(files[i], "cp_masks.png")) {
			open(files[i]);
			setOption("BlackBackground", true);
			setThreshold(1, 65535, "raw");
			run("Convert to Mask");
			run("8-bit");
			basename = split(File.nameWithoutExtension, "(_cp)");
			saveAs("PNG", outDir + File.separator + "nutil_" + basename[0]);
			close("*");
		}
	}
	setBatchMode(false);
}
	