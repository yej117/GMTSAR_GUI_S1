# GMTSAR_GUI
This python3 program is for reducing time to create batch file for processing Sentinel-1 IW data by GMTSAR.
In Ubuntu, the default python program would be python2; as the result, remember to execute it by python3.  

There are four tabs for different purpose as followings: 
* Info: choose the directories of S-1 scenes and orbit files; and the paths of DEM file, config file [and s1a-aux-cal.xml]. 
* Step 0: choose the S-1 scenes (from date), and their polarization and sub-swath. 
* Step 1: link the files to raw & topo directories and create data.in and *.csh for preprocessing step. 
* Step 2: select the day interval for interferometric pairs and it would help automatically create the intf.in file. 

After these steps, there would be 01_prep.sh and 02_proc.sh, and run them by csh.

# Create an execute file
pyinstaller --onefile GMTSAR_GUI__v3.py
