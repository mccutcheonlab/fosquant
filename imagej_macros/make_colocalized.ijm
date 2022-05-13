
macro "Make Colocalized Images [M]" {
	
	chan1Dir = getDirectory("Please pick a directory with masked PNGs for first channel.");
	chan2Dir = getDirectory("Please pick a directory with masked PNGs for second channel.");
	
	chan1Files = getFileList(chan1Dir);
	chan2Files = getFileList(chan2Dir);
	
	if (chan1Files.length != chan2Files.length) {
		exit("Different numbers of files in each folder. Exiting macro.");
	}

	for (i=0; i<chan1Files.length; i++) {
		open(chan1Files[i]);
		print(i, chan1Files[i]);
	}
	
}
