close("*");

run("Blobs (25K)");
run("CLIJ2 Macro Extensions", "cl_device=[GeForce RTX 2080 SUPER]");

print("Working up to here");

// // gaussian blur
// image1 = "blobs.gif";
// run("32-bit");
// Ext.CLIJ2_push(image1);
// image2 = "gaussian_blur1915207998";
// sigma_x = 2.0;
// sigma_y = 2.0;
// Ext.CLIJ2_gaussianBlur2D(image1, image2, sigma_x, sigma_y);
// Ext.CLIJ2_pull(image2);

// Ext.CLIJ2_getGPUProperties(gpu, memory, opencl_version);
// print("GPU: " + gpu);
// print("Memory in GB: " + (memory / 1024 / 1024 / 1024) );
// print("OpenCL version: " + opencl_version);

// Ext.CLIJ2_clear();

// setBatchMode(false);