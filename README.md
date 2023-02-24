# fosquant
 Code for quantifiying and colocalising Fos and trapped neurons

## STEP 0 (Installation)
Get fosquant repository from Git and install macros in ImageJ


## STEP 1 (project prep and splitting into sections (ROIs))
Put .vsi and associated folders for a single mouse into their own folder

Macro - Load VSI
Run macro 1 to open .vsi, ask which channel to use, enhance contrast etc
 - Maybe macro 1 also makes folder structure although could check whether folders were there first. Probably not though, maybe better to make folders as they are needed, e.g. lowres folder when saving lowres.


Draw ROIs on slides - add to ROI manager using CTRL-T.

Macro - Rename ROIs
When finished drawing ROIs run rename_and_save macro - rename macro asks what section number to start then renames ROIs, saves ROIs to file with stubname from .vsi, makes a new folder, and saves lowres images.

Macros - Save ROIs
suffix option

Macros - Load ROIs [optional]
If you have just completed the previous steaps (e.g. opened a .vsi file, drawn and renamed ROIs) then this step should not be necessary. But reasons for loading previous ROIs before are exporting include, wanting the lowres images to be higher resolution (e.g. can draw ROIs in 'series 13', which is lowest resolution, but then can export lowres from 'series 11', which will make it easier to do atlas registration). You could also choose to invert or manipulate the .vsi file in other ways which may help with atlas registration. 

Macro - Export Lo-Res
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

**plan is to do this in two steps - export multichannel, multi-Z tifs first (imageJ subprocess because of reading vsi files) and then do EDF with python script**
 

## STEP 3 (develop cellpose models using cropped images for speed) [optional]



## STEP 4 (do cell counts)
Copy hi-res folder to GPU machine
Run cellpose with appropriate trained models

[earlier step, develop models with cropped images]

Get binary masks for all three required channels (fos, trap and colocalized)

issues with running out of RAM so ran on server put without GPU so was slow. Wrote script to split images in two and then re-merge which can be used if not installed on server by the time needed

## STEP 5 (atlas alignment)

Linnea has a protocol set up and working


## STEP 6 (nutil counts)
Prepare Nutil config files (.nut) for all three channels (fos, trap, and coloc)

Run all .nut files in a folder using CLI for nutil by navigating to folder where nutil program lives and running the following:

process...

Can specify number of threads.

Because this is CPU - not GPU-based - runs faster with more cores and so is best run on server if possible.

Could set up a unix bash script to run many files (or just move all .nut files into a single folder)


## STEP 7 (optional; user-defined regions)
- make user-defined ROIs folder (do at start when setting up folder structure)
- for all sections with region of interest:
- - open file (e.g. lowres)
- - trace ROIs (using whichever tool is preferred)
- - add ROI to ROI manager (ctrl-alt-T)
- - when both added run user-defined macro to rename them, [U]
- - when all sections traced run Save user-defined ROIs [P]

- then to count
- - ask for channel to count (options chan2, chan3, coloc, or all)
- - ask for ROI file
- - macro should make separate output file for each channel
- - loop through ROIs, find and open masked png section, count particles, write number to file, with section number, maybe have cellcounter
- - at end, write total number


## Ideas
start to time steps on server, laptop, GPU
save a couple of sections already opened and cropped from bioformats (as TIFFs) for testing


## Useful sites
For using GPU and extended depth of focus in ImageJ
https://forum.image.sc/t/patchy-extend-depth-of-focus-using-clij/65090/4




