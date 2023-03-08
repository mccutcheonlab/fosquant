import subprocess
import os

imagej_path = "~/Fiji.app/ImageJ-linux64"
macro_name = "blobs_gputest.ijm"

path_to_macro = os.path.join(os.path.dirname(os.getcwd()), "imagej_macros", macro_name)
subprocess.call("cp {} ~/Fiji.app/macros/".format(path_to_macro), shell=True)


subprocess.call("{} -macro {} -batch".format(imagej_path, macro_name), shell=True)