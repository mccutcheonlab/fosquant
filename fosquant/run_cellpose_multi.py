# %%
# 


import os
import shutil

folders = [
           
           
           "/home/jaime/Data/FT133/chan2/",
           "/home/jaime/Data/FT136/chan2/",]


for folder in folders:

    # # make temp directory
    try:
        os.mkdir(folder + "temp/")
    except FileExistsError:
        print("temp folder already exists. Continuing...")

    try:
        os.mkdir(folder + "big/")
    except FileExistsError:
        print("big folder already exists. Continuing...")

    try:
        os.mkdir(folder + "complete/")
    except FileExistsError:
        print("complete folder already exists. Continuing...")

    tempdir = folder + "temp/"
    completedir = folder + "complete/"
    bigdir = folder + "big/"

    # # make complete directory 
    # os.mkdir("./complete")
    # os.mkdir("")

    list_of_files = os.listdir(folder)

    print(list_of_files)

    for file in list_of_files:
        if ".jpg" in file:
            shutil.move(folder+file, tempdir + file)
            try:
                os.system("python -m cellpose --dir {} --pretrained_model ~/Data/cellpose_models/CP_20220504_fos --chan 0 --chan2 0 --save_png --verbose --use_gpu --diameter 7.87".format(tempdir))
                processed_files = os.listdir(tempdir)
                print(processed_files)
                for proc_file in processed_files:
                    if (".npy" in proc_file) or (".png" in proc_file) or (".jpg" in proc_file):
                        shutil.move(tempdir+proc_file, completedir + proc_file)
            except:
                print("{} could not be processed this time")
                for big_file in os.listdir(tempdir):
                    if ".jpg" in big_file:
                        shutil.move(tempdir+big_file, bigdir+big_file)




# %%
