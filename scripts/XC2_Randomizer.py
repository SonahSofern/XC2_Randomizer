from tkinter import PhotoImage, ttk
import random, subprocess, shutil, os, threading, traceback, time, sys
from tkinter import *
import EnemyRandoLogic, SavedOptions, SeedNames, JSONParser, SkillTreeAdjustments, FieldSkillAdjustments, CoreCrystalAdjustments, RaceMode, TutorialShortening, IDs, MusicShuffling, DebugLog, CustomArts, PermalinkManagement, Helper, SkillTrees, Enhancements, BigItems, _EnemyEnhancements, CameraFixes, UniqueMonsterHunt
import GUISettings, TrustBeam
import _WeaponChips as WPChips
import _AuxCores as AuxCr
import _Accessories as Accs
from IDs import *
from Cosmetics import *
from UI_Colors import *
from tkinter.font import Font

Version = "1.2.0"
CommonBdatInput = ""
JsonOutput = "./_internal/JsonOutputs"
OptionDictionary = {}
rowIncrement = 0
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
defFontSizeVar = tk.IntVar(value=16)
defGUIThemeVar = tk.StringVar(value="Light Mode")
loadData([defFontVar, defFontSizeVar, defGUIThemeVar], "GUISavedOptions.txt")


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
TabRaceModeOuter = ttk.Frame(MainWindow)
TabFunnyOuter = ttk.Frame(MainWindow)

# Canvas 
TabGeneralCanvas = Canvas(TabGeneralOuter) 
TabDriversCanvas = Canvas(TabDriversOuter) 
TabBladesCanvas = Canvas(TabBladesOuter)
TabEnemiesCanvas = Canvas(TabEnemiesOuter) 
TabMiscCanvas = Canvas(TabMiscOuter)
TabQOLCanvas = Canvas(TabQOLOuter)
TabCosmeticsCanvas = Canvas(TabCosmeticsOuter)
TabRaceModeCanvas = Canvas(TabRaceModeOuter)
TabFunnyCanvas = Canvas(TabFunnyOuter)

# Actual Scrollable Content
TabGeneral = ttk.Frame(TabGeneralCanvas) 
TabDrivers = ttk.Frame(TabDriversCanvas) 
TabBlades = ttk.Frame(TabBladesCanvas)
TabEnemies = ttk.Frame(TabEnemiesCanvas) 
TabMisc = ttk.Frame(TabMiscCanvas)
TabQOL = ttk.Frame(TabQOLCanvas)
TabCosmetics = ttk.Frame(TabCosmeticsCanvas)
TabRaceMode = ttk.Frame(TabRaceModeCanvas)
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

CreateScrollBars([TabGeneralOuter, TabDriversOuter, TabBladesOuter, TabEnemiesOuter, TabMiscOuter, TabQOLOuter, TabCosmeticsOuter, TabRaceModeOuter, TabFunnyOuter],[TabGeneralCanvas, TabDriversCanvas, TabBladesCanvas, TabEnemiesCanvas, TabMiscCanvas, TabQOLCanvas, TabCosmeticsCanvas, TabRaceModeCanvas, TabFunnyCanvas],[TabGeneral, TabDrivers, TabBlades, TabEnemies, TabMisc, TabQOL, TabCosmetics, TabRaceMode, TabFunny])

# Tabs
MainWindow.add(TabGeneralOuter, text ='General') 
MainWindow.add(TabDriversOuter, text ='Drivers') 
MainWindow.add(TabBladesOuter, text ='Blades') 
MainWindow.add(TabEnemiesOuter, text ='Enemies') 
MainWindow.add(TabCosmeticsOuter, text='Cosmetics')
MainWindow.add(TabQOLOuter, text = 'Quality of Life')
MainWindow.add(TabRaceModeOuter, text='Race Mode')
MainWindow.add(TabFunnyOuter, text='Funny')
MainWindow.add(TabMiscOuter, text ='Misc.') 
MainWindow.pack(expand = True, fill ="both", padx=10, pady=10) 

def ShowTitleScreenText():
    JSONParser.ChangeJSONLine(["common_ms/menu_ms.json"],[132], ["name"], [f"Randomizer v{Version}"]) # Change Title Version to Randomizer v0.1.0

def GenHeader(headerName, parentTab, backgroundColor):
    global rowIncrement
    
    Header = ttk.Label(parentTab, text=headerName, padx=10, pady=10, background=backgroundColor, font=(defaultFont), width=MaxWidth, anchor="w")
    Header.grid(row=rowIncrement, column=0, sticky="w")

    rowIncrement += 1


stateSetList = []    

def StateUpdate(button, textList):
    if button.get():
        for item in textList:
            item.state(["!disabled"])       
    else:
        for item in textList:
            item.state(["disabled"])
            
def InteractableStateSet():
    for item in stateSetList:
        item()
        

def GenStandardOption(optionName, parentTab, description, commandList = [], subOptionName_subCommandList = [], optionType = Checkbutton):   
    # Variables
    global OptionDictionary
    global rowIncrement
    spinBoxVar = IntVar(value=100)
    var = BooleanVar()
    spinDesc = ttk.Label()
    spinBoxObj = ttk.Spinbox()
    StateSet = lambda: StateUpdate(checkButtonVar, [optionDesc, spinDesc, spinBoxObj] + checkBoxList)

    # Parent Frame
    optionPanel = ttk.Frame(parentTab)
    optionPanel.grid(row = rowIncrement, column= 0, sticky="ew")
    
    # Major Option Checkbox

    checkButtonObj = ttk.Checkbutton(optionPanel, variable= var, text=optionName, width=40, style="midColor.TCheckbutton",command= StateSet)
    checkButtonObj.grid(row=rowIncrement, column=0, sticky="e")
    checkButtonVar = var
    
    # Description Label
    optionDesc = ttk.Label(optionPanel, text=description, anchor="w", width=60, wraplength=650)
    optionDesc.grid(row=rowIncrement, column=1, sticky="w", padx=0)
    
    # % Boxes
    if (optionType == Spinbox):
        spinBoxObj = ttk.Spinbox(optionPanel, from_=0, to=100, textvariable=spinBoxVar, wrap=True, width=3, increment=10)
        spinBoxObj.grid(row=rowIncrement, column=2, padx=(15,0))
        spinDesc = ttk.Label(optionPanel, text="% randomized", anchor="w")
        spinDesc.grid(row=rowIncrement, column=3, sticky="w", padx=0)


    # Create Main Option Dictionary Entry
    OptionDictionary[optionName]={
        "name": optionName,
        "optionTypeVal": checkButtonVar,
        "spinBoxVal": spinBoxVar,
        "commandList": commandList,
        "subOptionObjects": {},
    }
    checkBoxList = []
    # Create Suboptions Dictionary Entry
    for i in range((len(subOptionName_subCommandList))//2):
        var = BooleanVar()
        checkBox = ttk.Checkbutton(optionPanel, text=subOptionName_subCommandList[2*i], variable=var, width=35)
        checkBox.grid(row=rowIncrement+i+1, column=0, sticky="sw")
        checkBoxList.append(checkBox)
        OptionDictionary[optionName]["subOptionObjects"][subOptionName_subCommandList[2*i]] = {
        "subName": subOptionName_subCommandList[2*i],
        "subOptionTypeVal": var,
        "subCommandList": subOptionName_subCommandList[2*i+1],
        }
    rowIncrement += 1
    # Variable to help set initial states of interactables
    stateSetList.append(StateSet)
    
    
def Options():
    # DebugLog.CreateDebugLog(OptionDictionary, Version, randoSeedEntry.get())
    
    # General
    GenStandardOption("Pouch Item Shops", TabGeneral, "Randomizes Pouch Items in Pouch Item Shops", [lambda: JSONParser.ChangeJSONFile(["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), list(set(PouchItems)-set([40007])), PouchItems)])
    GenStandardOption("Accessory Shops", TabGeneral, "Randomizes Accessories in Accessory Shops", [lambda: JSONParser.ChangeJSONFile(["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), list(set(IDs.Accessories)-set([1])),IDs.Accessories)])
    GenStandardOption("Weapon Chip Shops", TabGeneral, "Randomizes Weapon Chips in Weapon Chip Shops", [lambda: JSONParser.ChangeJSONFile(["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), WeaponChips, WeaponChips)])
    GenStandardOption("Treasure Chests Contents", TabGeneral, "Randomizes the contents of Treasure Chests", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"), ["itm1ID", "itm2ID", "itm3ID", "itm4ID","itm5ID","itm6ID","itm7ID","itm8ID"], Accessories + Boosters + WeaponChips + AuxCores + CoreCrystals + RefinedAuxCores,[])], ["Accessories", [lambda: IDs.ValidReplacements.extend(IDs.Accessories)] ,"Weapon Chips", [lambda: IDs.ValidReplacements.extend(WeaponChips)], "Aux Cores", [lambda: IDs.ValidReplacements.extend(AuxCores)], "Refined Aux Cores", [lambda: IDs.ValidReplacements.extend(RefinedAuxCores)], "Core Crystals", [lambda: IDs.ValidReplacements.extend(CoreCrystals)], "Deeds", [lambda: IDs.ValidReplacements.extend(Deeds)], "Collection Point Materials", [lambda: IDs.ValidReplacements.extend(CollectionPointMaterials)]])
    GenStandardOption("Collection Points", TabGeneral, "Randomizes the contents of Collection Points", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_CollectionPopList.json", "common_gmk/"), ["itm1ID", "itm2ID", "itm3ID", "itm4ID"], list(set(CollectionPointMaterials) - set([30019])), [])], ["Accessories", [lambda: IDs.ValidReplacements.extend(IDs.Accessories)] ,"Weapon Chips", [lambda: IDs.ValidReplacements.extend(WeaponChips)], "Aux Cores", [lambda: IDs.ValidReplacements.extend(AuxCores)],"Refined Aux Cores", [lambda: IDs.ValidReplacements.extend(RefinedAuxCores)], "Core Crystals", [lambda: IDs.ValidReplacements.extend(CoreCrystals)], "Deeds", [lambda: IDs.ValidReplacements.extend(Deeds)], "Collection Point Materials", [lambda: IDs.ValidReplacements.extend(CollectionPointMaterials)]])

    # Drivers
    GenStandardOption("Driver Skill Trees", TabDrivers, "Randomizes driver's skill trees",[lambda: SkillTrees.RandomizeSkillEnhancements(OptionDictionary),lambda: SkillTrees.FirstSlotCost()],["Nonstandard Skills", []])
    GenStandardOption("Driver Accessories", TabDrivers, "Randomizes effects of Accessories", [lambda: Accs.RandomizeAccessoryEnhancements()])
    GenStandardOption("Art Reactions", TabDrivers, "Randomizes art reactions (break, blowdown etc.)",[lambda: CustomArts.RandomArtReactions(OptionDictionary)], ["Clear Vanilla Reactions", [lambda: Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", Helper.StartsWith("ReAct", 1,16), 0)],"Multiple Reactions", []], optionType=Spinbox)
    GenStandardOption("Art Debuffs", TabDrivers, "Randomizes a Driver's Art debuff effect", [lambda: JSONParser.ChangeJSONFile(["common/BTL_Arts_Dr.json"], ["ArtsDeBuff"], ArtDebuffs, [], InvalidTargetIDs=AutoAttacks)],["Debuffs", [lambda: IDs.ValidReplacements.extend(list(set(ArtDebuffs)-set([21,35,16,17])))],"Buffs",[lambda: IDs.ValidReplacements.extend(ArtBuffs)], "Doom", [lambda: IDs.ValidReplacements.extend([21])], "Monado Armor", [lambda: IDs.ValidReplacements.extend([16])], "Superstrength", [lambda: IDs.ValidReplacements.extend([17])]], Spinbox)
    GenStandardOption("Driver Arts", TabDrivers, "Randomizes effects of driver arts", [lambda: CustomArts.GenCustomArtDescriptions()], ["Cooldown", [lambda: CustomArts.RandomArtCooldowns()], "Damage", [lambda: CustomArts.RandomArtDamageRatios()], "Enhancements", [lambda: CustomArts.RandomArtEnhancements()], "Animation Speed", [lambda: JSONParser.ChangeJSONFile(["common/BTL_Arts_Dr.json"], ["ActSpeed"], Helper.InclRange(0,255), Helper.InclRange(50,255), InvalidTargetIDs=AutoAttacks)]], optionType = Spinbox)
       
    # Blades
    GenStandardOption("Blade Aux Cores", TabBlades, "Randomizes a Blade's Aux Core enhancement", [lambda: AuxCr.RandomizeAuxCoreEnhancements()])
    GenStandardOption("Blade Aux Core Slots", TabBlades, "Randomizes a Blade's maximum Aux Core Slots", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"],["OrbNum"], Helper.InclRange(0,3), IDs.BladeAuxCoreSlotDistribution)])
    GenStandardOption("Blade Arts", TabBlades, "Randomizes a Blade's arts", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("NArts",1,3), BladeArts, BladeArts)])
    GenStandardOption("Blade Battle Skills", TabBlades, "Randomizes a Blade's battle (yellow) skill tree", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("BSkill", 1, 3), list(set(BladeBattleSkills) - set([268, 8, 9])), list(set(BladeBattleSkills) - set([268, 267,266,265,144,142,143, 8, 9])) )])
    GenStandardOption("Blade Cooldowns", TabBlades, "Randomizes a Blade's swap cooldown", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["CoolTime"], Helper.InclRange(1,1000), Helper.InclRange(1,1000))])
    GenStandardOption("Blade Defenses", TabBlades, "Randomizes a Blade's Physical and Ether Defense", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["PArmor", "EArmor"], Helper.InclRange(0,100), BladeDefenseDistribution)],optionType=Spinbox)
    GenStandardOption("Blade Elements", TabBlades, "Randomizes a Blade's element", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"],["Atr"], Helper.InclRange(1,8), Helper.InclRange(1,8))],optionType=Spinbox)
    GenStandardOption("Blade Field Skills", TabBlades, "Randomizes a Blade's field (green) skill tree", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("FSkill", 1, 3), BladeFieldSkills, list(set(BladeFieldSkills) - set([1,6])),[1001], IgnoreID_AND_Key=[[1005, "FSkill3"], [1008, "FSkill2"]]) ])
    GenStandardOption("Blade Mods", TabBlades, "Randomizes a Blade's Stat Modifiers", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["HpMaxRev", "StrengthRev", "PowEtherRev", "DexRev", "AgilityRev", "LuckRev"], Helper.InclRange(1,100), BladeModDistribution)])
    GenStandardOption("Blade Special Buttons", TabBlades, "Randomizes what button a special uses for its button challenge", [lambda: JSONParser.ChangeJSONFile(["common/MNU_BtnChallenge2.json"], Helper.StartsWith("BtnType", 1, 3), ButtonCombos, ButtonCombos)])
    GenStandardOption("Blade Special Reactions", TabBlades, "Randomizes each hit of a blade special to have a random effect such as break, knockback etc.", [lambda: JSONParser.ChangeJSONFile(["common/BTL_Arts_Bl.json"], Helper.StartsWith("ReAct", 1, 16), HitReactions, HitReactions)], optionType=Spinbox)
    # GenStandardOption("Blade Specials", TabBlades, "Randomizes blades special (red) skill tree", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("BArts", 1, 3) + ["BartsEx", "BartsEx2"], BladeSpecials,  list(set(BladeSpecials) - set([215])))]) works okay, but animations dont connect feels mid
    GenStandardOption("Blade Weapon Class", TabBlades, "Randomizes which role a weapon type counts as (ATK, TNK, HLR)", [lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpnType.json"], ["Role"], Helper.InclRange(1,3), WeaponTypeRoles)])
    GenStandardOption("Blade Weapons", TabBlades, "Randomizes a Blade's Weapons stats from chips", [],["Auto Attack",[lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpn.json"],["Damage"],Helper.InclRange(0,1298), Helper.InclRange(1,900) + Helper.InclRange(1000,1100) + Helper.InclRange(1250,1300))],"Crit Rate",[lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpn.json"],["CriRate"],Helper.InclRange(0,100), Helper.InclRange(1,50))],"Guard Rate",[lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpn.json"],["GuardRate"],Helper.InclRange(0,100), Helper.InclRange(1,60))],"Enhancements",[lambda: WPChips.RandomizeWeaponEnhancements(OptionDictionary["Blade Weapons"]["spinBoxVal"])]], optionType= Spinbox)
        
    # Enemies
    GenStandardOption("Enemies", TabEnemies, "Randomizes what enemies appear in the world", [lambda: EnemyRandoLogic.EnemyLogic(OptionDictionary)],["Story Bosses", [], "Quest Enemies", [], "Unique Monsters", [], "Superbosses", [], "Normal Enemies", [], "Mix Enemies Between Types", [], "Keep All Enemy Levels", [], "Keep Story Boss Levels", [], "Keep Quest Enemy Levels", []])
    GenStandardOption("Enemy Enhancements", TabEnemies, "Gives enemies a random enhancement; displayed by their name", [lambda: _EnemyEnhancements.EnemyStats(OptionDictionary["Enemy Enhancements"]["spinBoxVal"].get())],optionType=Spinbox)
    GenStandardOption("Enemy Drops", TabEnemies, "Randomizes enemy drops", [lambda: JSONParser.ChangeJSONFile(["common/BTL_EnDropItem.json"], Helper.StartsWith("ItemID", 1, 8), AuxCores+ RefinedAuxCores + IDs.Accessories + WeaponChips, [])], ["Accessories", [lambda: IDs.ValidReplacements.extend(IDs.Accessories)] ,"Weapon Chips", [lambda: IDs.ValidReplacements.extend(WeaponChips)], "Aux Cores", [lambda: IDs.ValidReplacements.extend(AuxCores)],"Refined Aux Cores", [lambda: IDs.ValidReplacements.extend(RefinedAuxCores)], "Core Crystals", [lambda: IDs.ValidReplacements.extend(CoreCrystals)], "Deeds", [lambda: IDs.ValidReplacements.extend(Deeds)], "Collection Point Materials", [lambda: IDs.ValidReplacements.extend(CollectionPointMaterials)]], optionType=Spinbox)
    GenStandardOption("Enemy Aggro", TabEnemies, "The percentage of all non-boss and non-quest enemies that will aggro the player", [lambda: EnemyRandoLogic.EnemyAggroProportion(OptionDictionary)],optionType=Spinbox)
    GenStandardOption("Enemy Move Speed", TabEnemies, "Randomizes how fast enemies move in the overworld", [lambda: JSONParser.ChangeJSONFile(["common/CHR_EnParam.json"], ["WalkSpeed", "RunSpeed"], Helper.InclRange(0,100), Helper.InclRange(0,100) + Helper.InclRange(250,255))],optionType=Spinbox)
    # GenStandardOption("Enemy Rage", TabEnemies, "Randomizes the effects of enemy enraged states", ["common/BTL_Aura"])

    # Misc
    GenStandardOption("Music", TabMisc, "Randomizes Music", [lambda: MusicShuffling.MusicShuffle(OptionDictionary)], ["Seperate Battle and \nEnvironment Themes", []]) # need to change title screen music
    GenStandardOption("Trust Lines", TabMisc, "Randomizes blade trust lines in battle (colors, power, etc.)", [lambda: TrustBeam.BeamRandomizer()])
    GenStandardOption("Custom Core Crystals", TabMisc, "Adds Core Crystals with guaranteed Rare Blades to Treasure Chests.", [lambda: CoreCrystalAdjustments.CoreCrystalChanges(OptionDictionary)], optionType=Spinbox) # The slider shouldnt do anything tbh the other things have sliders like enemy drop rando, chest rando etc. All this should do is add custom crystals to the crystal file. 

    
    
    # GenDictionary("NPCs", TabMisc, "Randomizes what NPCs appear in the world (still testing)", [lambda: JSONParser.ChangeJSON(Helper.InsertHelper(2, 1,90,"maa_FLD_NpcPop.json", "common_gmk/"), ["NpcID"], Helper.InclRange(0,3721), Helper.InclRange(2001,3721))])
    # GenOption("Funny Faces", TabMisc, "Randomizes Facial Expressions", ["common/EVT_eyetype.json"], ["$id"], Helper.inclRange(0,15), Helper.inclRange(0,15)) # doesnt work yet
    # GenDictionary("Menu Colors", TabMisc, "Randomizes Colors in the UI", [lambda: JSONParser.ChangeJSON(["common/MNU_ColorList.json"], ["col_r", "col_g", "col_b"], Helper.InclRange(0,255), Helper.InclRange(0,0))])

    # QOL
    GenStandardOption("Shortened Tutorial", TabQOL, "Shortens/removes tutorials", [lambda: TutorialShortening.ShortenedTutorial(OptionDictionary)])
    # GenStandardOption("Fast Skill Trees", TabQOL, "Makes Blade Skill Trees easy to complete", [lambda: CoreCrystalAdjustments.FieldSkillLevelAdjustment()])
    GenStandardOption("Freely Engage Blades", TabQOL, "Allows blades to be freely engaged by all valid drivers", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["FreeEngage"], [0], [1], [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1075, 1076, 1103])])
    GenStandardOption("Easy Field Skill Trees", TabQOL, "Maxes out all Blade field skills",  [lambda: CoreCrystalAdjustments.FieldSkillLevelAdjustment()])
    GenStandardOption("Treasure Chest Visibility", TabQOL, "Increases the range you can see treasure chests from", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"), ["msgVisible", "msgdigVisible"], Helper.InclRange(0,200), [255])])
    GenStandardOption("Remove Story Field Skills", TabQOL, "Removes field skill checks",  [lambda: FieldSkillAdjustments.RemoveFieldSkills(OptionDictionary)], ["Remove All Field Skills", []])
    GenStandardOption("Everlasting Pouch Items", TabQOL, "Makes Pouch Items last forever", [lambda: JSONParser.ChangeJSONFile(["common/ITM_FavoriteList.json"],["Time"], Helper.InclRange(0,255), [6099])])
    GenStandardOption("Condense Gold Loot", TabQOL, "Condenses gold in chests so you can see other items", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"),["goldPopMin", "goldPopMax"], Helper.InclRange(0,100000), [1])])
    GenStandardOption("Mute Popups", TabQOL, "Stops blade skill and pouch item refill popups", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[89], ["sheet06"], [""])],["Landmarks", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[85], ["sheet04"], [""])]])
    # GenStandardOption("Less UI", TabQOL, "Removes some of the unneccessary on screen UI (Blade Swap and Current Objective)", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[88], ["sheet05", "sheet03"], [""])])
    GenStandardOption("Screenshot Mode", TabQOL, "Removes most UI for screenshots", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[88], ["sheet05", "sheet03", "sheet04"], ""), lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[86], ["sheet02", "sheet03"], "")])
    # GenStandardOption("Enhancement Proc Tags", TabQOL, "Shows when enhancements proc like hunter's chemistry for example", [])
    GenStandardOption("Blade Weapon Cosmetics", TabQOL, "Keeps all blades default weapon models regardless of chips", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["OnlyWpn"], [0], [1])])
    GenStandardOption("Enhancement Display", TabQOL, "Shows when enhancements activate such as Hunter's Chemistry", [lambda: Enhancements.SearchAndSetDisplayIDs()])
    
    
    # Funny
    GenStandardOption("Projectile Treasure Chests", TabFunny, "Launches your items from chests", [lambda: JSONParser.ChangeJSONFile(["common/RSC_TboxList.json"], ["box_distance"], [0,0.5,1], [15])])
    GenStandardOption("Blade Size", TabFunny, "Randomizes the size of Blades", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["Scale", "WpnScale"], [], Helper.InclRange(1,250) + [1000,16000])], optionType= Spinbox) # Make sure these work for common blades
    GenStandardOption("NPCs Size", TabFunny, "Randomizes the size of NPCs", [lambda: JSONParser.ChangeJSONFile(["common/RSC_NpcList.json"], ["Scale"], Helper.InclRange(1,100), Helper.InclRange(30,250))], optionType=Spinbox)
    GenStandardOption("Enemy Size", TabFunny, "Randomizes the size of enemies", [lambda: JSONParser.ChangeJSONFile(["common/CHR_EnArrange.json"], ["Scale"], Helper.InclRange(0, 1000), Helper.InclRange(1, 200) + Helper.InclRange(990,1000))], optionType=Spinbox)
    GenStandardOption("Field Item Size and Spin", TabFunny, "Randomizes the size and spin rate of items from chests and collection points", [lambda: BigItems.BigItemsRando()])

    # Cosmetics
    GenStandardOption("Cosmetics", TabCosmetics, "Randomizes Cosmetics on Accessories and Aux Cores", [lambda: Cosmetics(OptionDictionary)], RexCosmetics + NiaDriverCosmetics + ToraCosmetics + MoragCosmetics + ZekeCosmetics + PyraCosmetics + MythraCosmetics + DromarchCosmetics + BrighidCosmetics + PandoriaCosmetics + NiaBladeCosmetics + PoppiαCosmetics + PoppiQTCosmetics + PoppiQTπCosmetics, Spinbox)
    
    # Race Mode
    GenStandardOption("Race Mode", TabRaceMode, "Enables Race Mode (see the Race Mode README)", [lambda: RaceMode.RaceModeChanging(OptionDictionary), RaceMode.SeedHash], ["Zohar Fragment Hunt", [], "Less Grinding", [], "Shop Changes", [], "Enemy Drop Changes", [], "DLC Item Removal", [], "Custom Loot", []])
    GenStandardOption("Chest Type Matches Contents", TabQOL, "Chest model and label changes depending on tier of loot", [lambda: RaceMode.ChestTypeMatching(OptionDictionary)])
    
    GenStandardOption("Unique Monster Hunt", TabRaceMode, "Experimental Mode", [lambda: UniqueMonsterHunt.UMHunt()], optionType=Spinbox)

    # Blade Names (moved so that blade name rando doesn't mess up Race Mode getting blade IDs)
    GenStandardOption("Blade Names", TabBlades, "Randomizes a Blade's name", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["Name"], Helper.InclRange(0,1000), BladeNames)])

Options()

def Randomize():
    def ThreadedRandomize():
        # Variables
        global OptionDictionary
        
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
            subprocess.run(f"{bdat_path} extract {fileEntryVar.get().strip()}/common.bdat -o {JsonOutput} -f json --pretty", check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f"{bdat_path} extract {fileEntryVar.get().strip()}/common_gmk.bdat -o {JsonOutput} -f json --pretty", check= True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f"{bdat_path} extract {fileEntryVar.get().strip()}/gb/common_ms.bdat -o {JsonOutput} -f json --pretty", check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            print(f"{traceback.format_exc()}") # shows the full error
            randoProgressDisplay.config(text="Invalid Input Directory")
            time.sleep(3)
            randoProgressDisplay.config(text="")
            RandomizeButton.config(state=NORMAL)
            return

        # Runs all randomization
        RunOptions()
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
    for option in OptionDictionary.values():
        if (option["optionTypeVal"].get()): # checks main option input
            IDs.CurrentSliderOdds = option["spinBoxVal"].get()
            for subOption in option["subOptionObjects"].values():
                if (subOption["subOptionTypeVal"].get()): # checks subOption input
                    for subCommand in subOption["subCommandList"]:
                        try:
                            subCommand()
                        except Exception as error:
                            print(f"ERROR: {option['name']}: {subOption['subName']} | {error}")
                            print(f"{traceback.format_exc()}") # shows the full error
            randoProgressDisplay.config(text=f"{option['name']}")
            for command in option["commandList"]:
                try:
                    command()
                except Exception as error:
                    print(f"ERROR: {option['name']} | {error}")
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
randoSeedEntry = ttk.Entry(SeedFrame, width=30, textvariable=seedEntryVar)
randoSeedEntry.pack(side='left', padx=2)

permalinkVar = StringVar()

# Save and Load Last Options
EveryObjectToSaveAndLoad = ([fileEntryVar, outputDirVar, permalinkVar, seedEntryVar,] + [option["optionTypeVal"] for option in OptionDictionary.values()] + [subOption["subOptionTypeVal"] for option in OptionDictionary.values() for subOption in option["subOptionObjects"].values()] + [option["spinBoxVal"] for option in OptionDictionary.values()])

SavedOptions.loadData(EveryObjectToSaveAndLoad, SavedOptionsFileName)

InteractableStateSet()

# Permalink Options/Variables
permalinkFrame = ttk.Frame(root,style="NoBackground.TFrame")
permalinkEntry = ttk.Entry(permalinkFrame, width=MaxWidth, textvariable=permalinkVar)
CompressedPermalink = PermalinkManagement.GenerateCompressedPermalink(randoSeedEntry.get(), EveryObjectToSaveAndLoad, Version)
permalinkVar.set(CompressedPermalink)
permalinkButton = ttk.Button(permalinkFrame, text="Settings")
permalinkButton.state(["disabled"])
permalinkFrame.pack(padx=10, pady=2, anchor="w")
permalinkButton.pack(side="left", padx=2)
permalinkEntry.pack(side='left', padx=2) 
PermalinkManagement.AddPermalinkTrace(EveryObjectToSaveAndLoad, permalinkVar, seedEntryVar, Version, lambda:InteractableStateSet())


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



root.protocol("WM_DELETE_WINDOW", lambda: (SavedOptions.saveData(EveryObjectToSaveAndLoad, SavedOptionsFileName), root.destroy()))
GUISettings.LoadTheme(defaultFont, defGUIThemeVar.get())

root.mainloop()

