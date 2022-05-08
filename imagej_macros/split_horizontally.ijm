macro "split horizontally" {
original = getImageID;
title = getTitle;
height = getHeight;
width = getWidth;
halfWidth = width / 2;
makeRectangle(0, 0, halfWidth, height);
run("Duplicate...", "title=left_"+title+" duplicate");
selectImage(original);
makeRectangle(halfWidth+1, 0, halfWidth, height);
run("Crop");
rename("right_"+title);
}