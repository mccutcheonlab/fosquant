# fosquant
 Code for quantifiying and colocalising Fos and trapped neurons


## STEP 1 (project prep and splitting into sections (ROIs))
Put .vsi and associated folders for a single mouse into their own folder

Macro - Load VSI
Run macro 1 to open .vsi, ask which channel to use, enhance contrast etc
 - Maybe macro 1 also makes folder structure although could check whether folders were there first. Probably not though, maybe better to make folders as they are needed, e.g. lowres folder when saving lowres.


Draw ROIs on slides - add to ROI manager using CTRL-T.

Macro - Rename ROIs
When finished drawing ROIs run rename_and_save macro - rename macro asks what section number to start then renames ROIs, saves ROIs to file with stubname from .vsi, makes a new folder, and saves lowres images.

Macro - Save Lo-Res
Loads ROIs if not already loaded




## STEP 2 (prepare hi-res images for cell counts) (maybe do on server for speed)

Macro - Save Hi_Res

Current instructions - 
(work out what scaling factor, lowres series should be, currently lowres=10, hires=9, scale=2 but could change in future)
Load ROI file (choose scaling factor 2)
Run Export Hires macro (not from macro set but from edit macro window).
Check options, probably select 180 degree turn
Make sure output jpegs look good

In future, auto select ROI file and scale factors etc by looking at dimensions


Run macro to load ROIs - ask for folder, search for ROI files, ask about series #, ask about scaling factor (but have defaults set), then open .vsi of appropriate resolution, then make new directory and save hi-res sections for cell counts

make sure it saves or displays a picture showing ROIs before confirming the save/export

to decide...
maybe do two channels separately - two different folders and then make grayscale - images probably smaller? TODO TEST whether the section that didn't work will work if it is a one channel file?

think about using slightly lower res, one level now

## STEP 3 (develop cellpose models using cropped images for speed) [optional]



## STEP 4 (do cell counts)
Copy hi-res folder to GPU machine
Run cellpose with appropriate trained models

[earlier step, develop models with cropped images]

For files that cause cellpose to fail, move into separate folder (e.g. "big") and try running using run_cellpose.py (need to move it into the folder with remaining images, adjust model and diameter in script)

Attn! Not working with fos diameter set to 7.87 - works with 10 but not sure how accurate it will be

## STEP 5 (atlas alignment)

Linnea has a protocol set up and working


## STEP 6 (nutil counts)
Use export_for_nutil.ijm (imageJ macro) to convert PNGs to binary for Nutil

STEP 6 ()

## Ideas
start to time steps on server, laptop, GPU
save a couple of sections already opened and cropped from bioformats (as TIFFs) for testing


## Useful sites
For using GPU and extended depth of focus in ImageJ
https://forum.image.sc/t/patchy-extend-depth-of-focus-using-clij/65090/4




