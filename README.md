# XC2_Randomizer
A randomizer project for Xenoblade 2 capable of randomizing: Enemies, Accessories, Blades, Drivers, Loot and much more!


# General Description
This program randomizes the BDAT files in Xenoblade Chronicles 2. Tested on the main story of the English Version 2.1.0 + DLC only. The project is still a work in progress, please report bugs or suggestions to our discord so we can make this better!

# Contact Us
Discord: https://discord.gg/h93yqZHG8z

# Known Issues
Race Mode will overwrite some settings. (for example Treasure Chest Contents will be overwritten if race mode is on)\
Torna has not been tested at all, it may or may not work.


# Credits
https://github.com/roccodev/bdat-rs \
https://frontiernav.net/wiki/xenoblade-chronicles-2 \
https://xenobladedata.github.io/ \
https://gitlab.com/damysteryman/XC2SaveNETThingy/-/tags/r6.1 

# Setup

### Requirements:
[Python v3.11.0](https://www.python.org/downloads/release/python-3110/)\
Legal Dump of Xenoblade 2 Switch v2.1.0 + Torna\
Homebrewed Switch or Emulator\
[NXDumpTool](https://github.com/DarkMatterCore/nxdumptool)\
[Xenoblade 2 Set](https://gbatemp.net/threads/xenoblade-chronicles-2-graphics-settings.529436/)

### Console Also Requires:
microSD card (A 32GB minimum exFAT-formatted microSD card is recommended; FAT32 will split up your files and youll have to take an extra step to combine them.)\
Modded Nintendo Switch with Atmosphere


### Process:
Guide adapted from: https://gamebanana.com/tuts/13815 

1. CONSOLE ONLY: Use NXDumpTool to perform a full dump of XC2's RomFS to your microSD card, and put it into your computer.
2. EMULATOR ONLY: Use your emulator's built-in tool to perform a full dump of XC2's RomFS. If given the option, select 0100E95004038000.
3. Locate "bf2.ard" and "bf2.arh"; those are the only two important files.
> **IMPORTANT:** if your sdcard is formatted as fat32, bf2.ard might be split into a folder with multiple files inside. In this case you will have to combine them.\
> Open a command prompt and navigate to your bf2.ard folder\
> Depending on your OS run the following command:\
> **Windows: `copy /b` file1name `+` file2name `+` file3name `bf2.ard`\
> **Mac/Linux: `cat` file1name file2name file3name `> bf2.ard`\
> You should have the combined file now!
4. Download Xenoblade2Set from (https://gbatemp.net/threads/xenoblade-chronicles-2-graphics-settings.529436/), and extract its contents.
5. Copy bf2.ard and bf2.arh to the Xenoblade2Set folder, and run "quickbms_4gb_files.exe".
6. It will ask for a "bms script"; select Xenoblade2ard.bms. It will then ask for "archives/files"; select bf2.arh. For "output folder", go into the empty "modified" folder and press "Save". The files should extract, it may take a bit. NOTE: You can stop the program once all the GB files are finished. The rest is just for the other languages.
7. There should now be a new "bdat" folder inside "modified"; This is the folder that the randomizer program targets as the input folder. The output folder should be\
FOR YUZU: C:/Users/yourName/AppData/Roaming/yuzu/load/0100E95004039001/Randomizer/romfs/bdat\
FOR RYUJINX: C:/Users/yourName/AppData/Roaming/Ryujinx/sdcard/atmosphere/contents/0100e95004039001/romfs/bdat\
FOR CONSOLE: This PC/Nintendo Switch/SD Card/atmosphere/contents/0100E95004039001/romfs/bdat (This is on your microsd card)\
NOTE: You will have to create the 0100E95004039001 folder.
8. Choose your preferred settings, then use the randomizer program to randomize the contents of the game.
9. CONSOLE ONLY: Put your microSD card back into your Switch and Launch the game. Pressing L bypasses the active patches, so if you wish to play the vanilla game again, you can do so in this way.
10. You should be ready to start playing!