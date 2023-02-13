t0=getTime()

print("Running macro to export ROIs as hires images");

argString = getArgument();
args = split(argString, "(, )");

// these lines need to be changed to reflect args in...
filename = args[0];
outputDir = args[1];
proj = args[2];
framesPerChunk = args[3];
z = args[4];