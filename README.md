# BetaExtractor9000
Scripts to extract and compare new images and other texts from beta cache files. If you have git download with that, if not you can download a zip file ("Code" > "Download ZIP") and extract that.

# How To Use (Executable):

* Update "config.ini" (open in any text editor) with newest data and your options
* Start "run.exe", important that it's in the same folder as "config.ini"

# How To Use (Python):

* Install python (any recent python 3 version should work fine, using 3.8 mysef but that shouldn't be important)
* (Recommended, but Optional) Install "Virtual Studio Code", it will make working with the python scripts easier :)
* Install required libraries:
    * Open a terminal in this directory, then execute command:
    * py -m pip install -r requirements.txt

You can now either run the main program with "py run.py", or if you want to edit the code you can edit any of the scripts in scripts folder, then either use "py run.py" again, or you can use "py scripts/compare.py" for example. It's important that you keep the file structure as it is, and that when running the scripts in the scripts folder individually, you're starting them from the main folder. 