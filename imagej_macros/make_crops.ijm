var num = 20;
var width = 250;
var height = 250;
var seed = 201279;

macro "Make crops [M]" {
	
	Dialog.create("Choose options");
	Dialog.addNumber("Number", num);
	Dialog.addNumber("Width (px)", width);
	Dialog.addNumber("Height (px)", height);
	Dialog.addNumber("Random seed", seed);
	Dialog.show();

	num = Dialog.getNumber();
	width = Dialog.getNumber();
	height = Dialog.getNumber();
	seed = Dialog.getNumber();
	
	parent = getDirectory("Please pick a directory with images.");
//	parent = "C:/Github/fosquant/data/lowresmulti/";
	
	outDir = parent + File.separator + "crops";
	if (!File.exists(outDir)) {
		File.makeDirectory(parent + File.separator + "crops");
	}
	
	files = getFileList(parent);
	nFiles = files.length;
	
	random("seed", seed);
	
	for (i=0; i<num; i++) {
		shuffle(files);
		file = parent + files[0];
		open(file);

		w = getWidth();
		h = getHeight();
		
		xPos = randomInt(w - width);
		yPos = randomInt(h - height);
		
		makeRectangle(xPos, yPos, width, height);
		run("Crop");
		saveAs("jpg", outDir + File.separator + seed + "_" + i);
		close();
	}

function shuffle(array) {
   n = array.length;  // The number of items left to shuffle (loop invariant).
   while (n > 1) {
      k = randomInt(n);     // 0 <= k < n.
      n--;                  // n is now the last pertinent index;
      temp = array[n];  // swap array[n] with array[k] (does nothing if k==n).
      array[n] = array[k];
      array[k] = temp;
   }
}

// returns a random number, 0 <= k < n
function randomInt(n) {
   return n * random();
}

}
