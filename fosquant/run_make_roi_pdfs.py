import sys
import getopt
from pathlib import Path
import os
import io
import base64

import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from read_roi import read_roi_zip

# get and parse options
def parse_args(argv):
    args_dict = {}
    args_dict["animals"] = ""

    try:
        opts, args = getopt.getopt(argv[1:], "a:")
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-a", "--animals"):
            args_dict["animals"] = arg
        
    print("Arguments parsed successfully")
    
    return args_dict

def get_sections(folder):
    
    contents = os.listdir(folder / "lowres")
    
    sections = [f.split("_")[3].split(".")[0] for f in contents if f.endswith(".jpg")]
    return sections

def parse_roi_name(roiname):
    
    section = roiname.split("_")[0]
    region = "".join(roiname.split("_")[1:]).split("-")[0]
    
    return section, region

def get_rois(roidata):
    
    regions = []
    for roi in roidata:
        _, region = parse_roi_name(roi)
        regions.append(region)
        
    return list(set(regions))

def get_lowres_image(folder, section):
    
    lowresimages = [f for f in os.listdir(folder / "lowres") if f.endswith("{}.jpg".format(section))]
    
    if len(lowresimages) != 1:
        print("Problem finding correct lowres image")
    else:
        im = imread(folder / "lowres" / lowresimages[0])
    
    return im

def make_figure(im, roidata):

    f, ax = plt.subplots()
    ax.imshow(im)
    for key, roi in roidata.items():
        try:
            ax.plot(roi["x"], roi["y"], color="red")
        except KeyError:
            print(key)
    
    img = io.BytesIO()
    f.savefig(img, format='png')
    
    img.seek(0)
    f_base64 = base64.b64encode(img.getvalue()).decode()
    
    return f_base64

def make_section_html(section, figure):
    
    return f"""
    <html>
      <body>
        <h1>{section}</h1>
        <img src="data:image/png;base64,{figure}" alt="Matplotlib Plot" class="blog-image">
      </body>
    </html>
    """

args_dict = parse_args(sys.argv)
args_dict["prefix"] = "FT"

PROJECT_DIR = Path("C:/Users/jmc010/Data/fostrap/")
ROI_FILE_SUFFIX = "_cleaned"

print(args_dict)

if args_dict["animals"] == "all":
    args_dict["animals"] = [d for d in os.listdir(PROJECT_DIR) if args_dict["prefix"] in d]
elif args_dict["animals"] == "":
    print("No animals given. Exiting")
    sys.exit(2)
else:
    args_dict["animals"] = args_dict["animals"].split()

for animal in args_dict["animals"]:
    print("\n******************")
    print("Making PDFs for", animal)
    folder = PROJECT_DIR / animal
    print(folder)

    try:
        sections = get_sections(folder)
        roipath = folder / "lowres" / "{}_userdefined_ROIs_cleaned.zip".format(folder.name)
        roidata = read_roi_zip(roipath)
    except FileNotFoundError:
        print(f"Cannot find files for {animal}. Ignoring and moving on.")
        continue

    rois = get_rois(roidata)

    sections_and_rois = {}
    for section in sections:
        sections_and_rois[section] = {}
        for key, val in roidata.items():
            if section in key:
                sections_and_rois[section][key] = val

    html_all = f"""
    <html>
    <head>
        <title>{animal}</title>
    </head>
    </html>
    """

    for key, val in sections_and_rois.items():
        if len(val.keys()) == 0:
            continue
            
        im = get_lowres_image(folder, key)       
        f_base64 = make_figure(im, val)
        html_all = html_all + make_section_html(key, f_base64)

    html_file = f"{animal}.html"
    with open(folder / html_file, "w") as f:
        f.write(html_all)