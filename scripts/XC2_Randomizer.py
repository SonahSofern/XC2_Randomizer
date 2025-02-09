from tkinter import PhotoImage, ttk
import random, subprocess, shutil, os, threading, traceback, time, sys
from tkinter import *
import EnemyRandoLogic, SavedOptions, SeedNames, JSONParser, FieldSkillAdjustments, CoreCrystalAdjustments, RaceMode, TutorialShortening, IDs, MusicShuffling, DebugLog, _DriverArts, PermalinkManagement, Helper, SkillTrees, Enhancements, BigItems, _EnemyEnhancements, CameraFixes, UniqueMonsterHunt
import GUISettings, TrustBeam, _EnemyArts, _BladeWeapons, BladeRandomization, GachaModifications, _GreenSkills
import _WeaponChips as WPChips
import _AuxCores as AuxCr
import _Accessories as Accs
from Options import *
from IDs import *
from Cosmetics import *
from UI_Colors import *
from tkinter.font import Font


Version = "1.3.0"
CommonBdatInput = ""
JsonOutput = "./_internal/JsonOutputs"
MaxWidth = 1000
windowWidth = "1550"
windowHeight = "900"
OptionColorLight = White
OptionColorDark = Gray
SavedOptionsFileName = f"SavedOptionsv{Version}.txt"
if getattr(sys, 'frozen', False):  # If the app is running as a bundled executable
    isOnefile = True
else:
    isOnefile = False
    
root = Tk()
defFontVar = tk.StringVar(value="Arial")
defFontSizeVar = tk.IntVar(value=13)
defGUIThemeVar = tk.StringVar(value="Dark Mode")
# loadData([defFontVar, defFontSizeVar, defGUIThemeVar], "GUISavedOptions.txt")


RootsForStyling.append(root)
defaultFont = Font(family=defFontVar.get(), size=defFontSizeVar.get())

root.title(f"Xenoblade Chronicles 2 Randomizer v{Version}")
root.option_add("*Font", defaultFont)
root.geometry(f'{windowWidth}x{windowHeight}')

if isOnefile:
    bdat_path = os.path.join(sys._MEIPASS, 'Toolset', 'bdat-toolset-win64.exe')
else:
    bdat_path = "./_internal/Toolset/bdat-toolset-win64.exe"

if isOnefile: 
    icon_path = os.path.join(sys._MEIPASS, 'Images', 'XC2Icon.png')
else:
    icon_path = "./_internal/Images/XC2Icon.png"
icon = PhotoImage(file=icon_path)
root.iconphoto(True, icon)


# The Notebook
MainWindow = ttk.Notebook(root, height=5)
# Frames in the notebook
TabGeneralOuter = ttk.Frame(MainWindow) 
TabDriversOuter = ttk.Frame(MainWindow) 
TabBladesOuter = ttk.Frame(MainWindow) 
TabEnemiesOuter = ttk.Frame(MainWindow) 
TabMiscOuter = ttk.Frame(MainWindow) 
TabQOLOuter = ttk.Frame(MainWindow)
TabCosmeticsOuter = ttk.Frame(MainWindow)
TabGameModeOuter = ttk.Frame(MainWindow)
TabFunnyOuter = ttk.Frame(MainWindow)

# Canvas 
TabGeneralCanvas = Canvas(TabGeneralOuter) 
TabDriversCanvas = Canvas(TabDriversOuter) 
TabBladesCanvas = Canvas(TabBladesOuter)
TabEnemiesCanvas = Canvas(TabEnemiesOuter) 
TabMiscCanvas = Canvas(TabMiscOuter)
TabQOLCanvas = Canvas(TabQOLOuter)
TabCosmeticsCanvas = Canvas(TabCosmeticsOuter)
TabGameModeCanvas = Canvas(TabGameModeOuter)
TabFunnyCanvas = Canvas(TabFunnyOuter)

# Actual Scrollable Content
TabGeneral = ttk.Frame(TabGeneralCanvas) 
TabDrivers = ttk.Frame(TabDriversCanvas) 
TabBlades = ttk.Frame(TabBladesCanvas)
TabEnemies = ttk.Frame(TabEnemiesCanvas) 
TabMisc = ttk.Frame(TabMiscCanvas)
TabQOL = ttk.Frame(TabQOLCanvas)
TabCosmetics = ttk.Frame(TabCosmeticsCanvas)
TabGameMode = ttk.Frame(TabGameModeCanvas)
TabFunny = ttk.Frame(TabFunnyCanvas)

def CreateScrollBars(OuterFrames, Canvases, InnerFrames): # I never want to touch this code again lol what a nightmare
    for i in range(len(Canvases)):
        scrollbar = ttk.Scrollbar(OuterFrames[i], orient="vertical", command=Canvases[i].yview)
        Canvases[i].config(yscrollcommand=scrollbar.set, borderwidth=0, relief="flat", highlightthickness=0)
        CanvasesForStyling.append(Canvases[i])
        # OuterFrames[i].config(borderwidth=0, relief="flat")
        InnerFrames[i].bind("<Configure>", lambda e, canvas=Canvases[i]: canvas.configure(scrollregion=canvas.bbox("all")))

        OuterFrames[i].pack_propagate(False)
        Canvases[i].create_window((0, 0), window=InnerFrames[i], anchor="nw")
        Canvases[i].pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event, canvas=Canvases[i]):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        Canvases[i].bind("<Enter>", lambda e, canvas=Canvases[i]: canvas.bind_all("<MouseWheel>", lambda event: _on_mousewheel(event, canvas)))
        Canvases[i].bind("<Leave>", lambda e, canvas=Canvases[i]: canvas.unbind_all("<MouseWheel>"))
        OuterFrames[i].pack(expand=True, fill="both")

CreateScrollBars([TabGeneralOuter, TabDriversOuter, TabBladesOuter, TabEnemiesOuter, TabMiscOuter, TabQOLOuter, TabCosmeticsOuter, TabGameModeOuter, TabFunnyOuter],[TabGeneralCanvas, TabDriversCanvas, TabBladesCanvas, TabEnemiesCanvas, TabMiscCanvas, TabQOLCanvas, TabCosmeticsCanvas, TabGameModeCanvas, TabFunnyCanvas],[TabGeneral, TabDrivers, TabBlades, TabEnemies, TabMisc, TabQOL, TabCosmetics, TabGameMode, TabFunny])

# Tabs
MainWindow.add(TabGeneralOuter, text ='General') 
MainWindow.add(TabDriversOuter, text ='Drivers') 
MainWindow.add(TabBladesOuter, text ='Blades') 
MainWindow.add(TabEnemiesOuter, text ='Enemies') 
MainWindow.add(TabCosmeticsOuter, text='Cosmetics')
MainWindow.add(TabQOLOuter, text = 'Quality of Life')
MainWindow.add(TabGameModeOuter, text='Game Modes')
MainWindow.add(TabFunnyOuter, text='Funny')
MainWindow.add(TabMiscOuter, text ='Misc.') 
MainWindow.pack(expand = True, fill ="both", padx=10, pady=10) 


for opt in OptionList:
    if opt.tab == General:
        opt.DisplayOption(TabGeneral)
    elif opt.tab == Driver:
        opt.DisplayOption(TabDrivers)


def ShowTitleScreenText():
    JSONParser.ChangeJSONLine(["common_ms/menu_ms.json"],[132], ["name"], [f"Randomizer v{Version}"]) # Change Title Version to Randomizer vX.x.x

def Randomize():
    def ThreadedRandomize():
        # Disable Repeated Button Click
        RandomizeButton.config(state=DISABLED)

        # Showing Progress Diplay 
        randoProgressDisplay.pack(side='left', anchor='w', pady=10, padx=10)
        randoProgressDisplay.config(text="Unpacking BDATs")

        random.seed(permalinkVar.get())
        print("Seed: " + randoSeedEntry.get())
        print("Permalink: "+  permalinkVar.get())

        try:
        # Unpacks BDATs
            subprocess.run([bdat_path, "extract", f"{fileEntryVar.get().strip()}/common.bdat", "-o", JsonOutput, "-f", "json", "--pretty"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run([bdat_path, "extract", f"{fileEntryVar.get().strip()}/common_gmk.bdat", "-o", JsonOutput, "-f", "json", "--pretty"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run([bdat_path, "extract", f"{fileEntryVar.get().strip()}/gb/common_ms.bdat", "-o", JsonOutput, "-f", "json", "--pretty"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            print(f"{traceback.format_exc()}") # shows the full error
            randoProgressDisplay.config(text="Invalid Input Directory")
            time.sleep(3)
            randoProgressDisplay.config(text="")
            RandomizeButton.config(state=NORMAL)
            return

        # Runs all randomization
        # RunOptions()
        randoProgressDisplay.config(text="Packing BDATs")
        
        try:
            # Packs BDATs
            subprocess.run(f"{bdat_path} pack {JsonOutput} -o {outputDirVar.get().strip()} -f json", check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Outputs common_ms in the correct file structure
            os.makedirs(f"{outputDirVar.get().strip()}/gb", exist_ok=True)
            shutil.move(f"{outputDirVar.get().strip()}/common_ms.bdat", f"{outputDirVar.get().strip()}/gb/common_ms.bdat")

            # Displays Done and Clears Text
            randoProgressDisplay.config(text="Done")
            time.sleep(1.5)
            randoProgressDisplay.config(text="")
            randoProgressDisplay.pack_forget()
            
            print("Done")
        except:
            print(f"{traceback.format_exc()}") # shows the full error
            randoProgressDisplay.config(text="Invalid Output Directory")

        
        # Re-Enables Randomize Button
        RandomizeButton.config(state=NORMAL)

    threading.Thread(target=ThreadedRandomize).start()

def RunOptions():
    
    OptionList.sort(key=lambda x: x.prio) # Sort main options by priority
    
    for opt in OptionList:
        if not opt.GetCheckBox(): # Checks state
            continue
        
        opt.subOptions.sort(key= lambda x: x.prio) # Sort suboptions by priority
        IDs.CurrentSliderOdds = opt.GetSpinBox()
        
        for sub in opt.subOptions:
            if not sub.checkBoxVal.get(): # Checks state
                continue
            try:
                for command in sub.commands:
                    command()
            except Exception as error:
                print(f"ERROR: {opt.name}: {sub.name} | {error}")
                print(f"{traceback.format_exc()}") # shows the full error
                
        randoProgressDisplay.config(text=opt.name)
        for command in opt.commands:
            try:
                command()
            except Exception as error:
                print(f"ERROR: {opt.name} | {error}")
                print(f"{traceback.format_exc()}") # shows the full error
    
    # Nonstandard Options
    ShowTitleScreenText()
    Enhancements.AddCustomEnhancements() # Figure out how to not run this here just dont have time rn


def GenRandomSeed(randoSeedEntryVar):
    randoSeedEntryVar.set(SeedNames.RandomSeedName())

bdatcommonFrame = ttk.Frame(root, style="NoBackground.TFrame")
bdatcommonFrame.pack(anchor="w", padx=10)
bdatButton = ttk.Button(bdatcommonFrame, width=20, text="Choose Input Folder", command= lambda: Helper.DirectoryChoice("Choose your folder containing common.bdat, common_ms.bdat and common_gmk.bdat", bdatFilePathEntry))
bdatButton.pack(side="left", padx=2, pady=2)
fileEntryVar = StringVar()
bdatFilePathEntry = ttk.Entry(bdatcommonFrame, width=MaxWidth, textvariable=fileEntryVar)
bdatFilePathEntry.pack(side="left", padx=2)
OutputDirectoryFrame = ttk.Frame(root, style="NoBackground.TFrame")
OutputDirectoryFrame.pack(anchor="w", padx=10)
outputDirButton = ttk.Button(OutputDirectoryFrame, width = 20, text='Choose Output Folder', command= lambda: Helper.DirectoryChoice("Choose an output folder", outDirEntry))
outputDirButton.pack(side="left", padx=2, pady=2)
outputDirVar = StringVar()
outDirEntry = ttk.Entry(OutputDirectoryFrame, width=MaxWidth, textvariable=outputDirVar)
outDirEntry.pack(side="left", padx=2)
SeedFrame = ttk.Frame(root, style="NoBackground.TFrame")
SeedFrame.pack(anchor="w", padx=10)
seedDesc = ttk.Button(SeedFrame, text="Seed", command=lambda: GenRandomSeed(seedEntryVar))

seedDesc.pack(side='left', padx=2, pady=2)

RootsForStyling.append(bdatcommonFrame)

# Seed entry box
seedEntryVar = StringVar()
GenRandomSeed(seedEntryVar) # Gen a random seed if you have no save data 
randoSeedEntry = ttk.Entry(SeedFrame, width=30, textvariable=seedEntryVar)
randoSeedEntry.pack(side='left', padx=2)

permalinkVar = StringVar()

class SavedEntry:
    def __init__(self, _name, _val):
        self.name =_name
        self.checkBoxVal = _val # Polymorphism with the Option Class
        self.subOptions = []
        
fileEnt = SavedEntry("Input Bdats",fileEntryVar)
fileOut = SavedEntry("Output Bdats", outputDirVar)
permLink = SavedEntry("Permalink", permalinkVar)
seedVar = SavedEntry("Seed", seedEntryVar)

# Save and Load Last Options
EntriesToSave = ([fileEnt, fileOut, permLink, seedVar])
SavedOptions.loadData(EntriesToSave + OptionList, SavedOptionsFileName)
UpdateAllStates()

# # Permalink Options/Variables
# permalinkFrame = ttk.Frame(root,style="NoBackground.TFrame")
# permalinkEntry = ttk.Entry(permalinkFrame, width=MaxWidth, textvariable=permalinkVar)
# CompressedPermalink = PermalinkManagement.GenerateCompressedPermalink(randoSeedEntry.get(), EveryObjectToSaveAndLoad, Version)
# permalinkVar.set(CompressedPermalink)
# permalinkButton = ttk.Button(permalinkFrame, text="Settings")
# permalinkButton.state(["disabled"])
# permalinkFrame.pack(padx=10, pady=2, anchor="w")
# permalinkButton.pack(side="left", padx=2)
# permalinkEntry.pack(side='left', padx=2)
# PermalinkManagement.AddPermalinkTrace(EveryObjectToSaveAndLoad, permalinkVar, seedEntryVar, Version, lambda:InteractableStateSet())


# Bottom Left Progress Display Text
randoProgressDisplay = ttk.Label(text="", anchor="e", padding=2, style="BorderlessLabel.TLabel")

# Randomize Button
RandomizeButton = ttk.Button(text='Randomize', command=Randomize)
RandomizeButton.place(relx=0.5, rely=1, y= -10, anchor="s")
RandomizeButton.config(padding=5)

# Options Cog
if isOnefile:  # If the app is running as a bundled executable
    icon_path = os.path.join(sys._MEIPASS, 'Images', 'SmallSettingsCog.png')
else:  # If running as a script (not bundled)
    icon_path = "./_internal/Images/SmallSettingsCog.png"
Cog = PhotoImage(file=icon_path)
SettingsButton = ttk.Button(image=Cog, command=lambda: GUISettings.OpenSettingsWindow(root, defaultFont, defGUIThemeVar))
SettingsButton.pack(pady=10, padx=10, side='right', anchor='e') 

root.protocol("WM_DELETE_WINDOW", lambda: (SavedOptions.saveData(EntriesToSave + OptionList, SavedOptionsFileName), root.destroy()))
GUISettings.LoadTheme(defaultFont, defGUIThemeVar.get())


root.mainloop()

