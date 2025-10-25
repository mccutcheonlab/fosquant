from pathlib import Path
import shutil

IMAGEJPATH = Path("C:/Users/jmc010/AppData/Local/fiji-win64/Fiji.app/macros")

MACROFILES_TO_COPY = [
    "StartupMacros.fiji.ijm",
    "export_hires.ijm",
]

for file in MACROFILES_TO_COPY:
    shutil.copy(file, IMAGEJPATH / file)
    print("Macros copied to ImageJ folder")
