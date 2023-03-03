macro "user crops [u]" {
	run("Duplicate...", " ");
	
	folder = File.directory;
	filename = File.name;
	
	new_filename = folder + "crop_" + filename;
	print(new_filename);
	saveAs("PNG", new_filename);
}
