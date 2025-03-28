print("Starting test...");
run("CLIJ2 Macro Extensions", "cl_device=");
Ext.CLIJ2_getGPUProperties(gpu, memory, opencl_version);
print("GPU: " + gpu);
print("Finished test.");