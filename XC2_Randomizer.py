from tkinter import PhotoImage, ttk
import random, subprocess, shutil, os, threading
from tkinter import *
import EnemyRandoLogic, SavedOptions, SeedNames, Helper, JSONParser, SkillTreeAdjustments, CoreCrystalAdjustments, TestingStuff, TutorialShortening
from IDs import *
from Cosmetics import *

root = Tk()
root.title("Xenoblade Chronicles 2 Randomizer 0.1.0")
root.configure(background='#632424')
root.geometry('900x800')
icon = PhotoImage(file="./_internal/Images/XC2Icon.png")
root.iconphoto(True, icon)

CommonBdatInput = ""
JsonOutput = "./_internal/JsonOutputs"
CheckboxStates = []
CheckboxList = []
OptionsRunList = []
OptionInputs = []
rowIncrement = 0
CheckBoxFunctions = []
White = "#ffffff"
Gray = "#D5D5D5"

# The Notebook
MainWindow = ttk.Notebook(root, height=2)

#Frames in the notebook
TabGeneralOuter = Frame(MainWindow) 
TabDriversOuter = Frame(MainWindow) 
TabBladesOuter = Frame(MainWindow) 
TabEnemiesOuter = Frame(MainWindow) 
TabMiscOuter = Frame(MainWindow) 
TabQOLOuter = Frame(MainWindow)
TabCosmeticsOuter = Frame(MainWindow)

# Canvas 
TabGeneralCanvas = Canvas(TabGeneralOuter) 
TabDriversCanvas = Canvas(TabDriversOuter) 
TabBladesCanvas = Canvas(TabBladesOuter)
TabEnemiesCanvas = Canvas(TabEnemiesOuter) 
TabMiscCanvas = Canvas(TabMiscOuter)
TabQOLCanvas = Canvas(TabQOLOuter)
TabCosmeticsCanvas = Canvas(TabCosmeticsOuter)

# Actual Scrollable Content
TabGeneral = Frame(TabGeneralCanvas) 
TabDrivers = Frame(TabDriversCanvas) 
TabBlades = Frame(TabBladesCanvas)
TabEnemies = Frame(TabEnemiesCanvas) 
TabMisc = Frame(TabMiscCanvas)
TabQOL = Frame(TabQOLCanvas)
TabCosmetics = Frame(TabCosmeticsCanvas)


def CreateScrollBars(OuterFrames, Canvases, InnerFrames): # I never want to touch this code again lol what a nightmare
    for i in range(len(Canvases)):
        scrollbar = ttk.Scrollbar(OuterFrames[i], orient="vertical", command=Canvases[i].yview)
        Canvases[i].config(yscrollcommand=scrollbar.set, highlightthickness=0)
        OuterFrames[i].config(highlightthickness=0)
        InnerFrames[i].config(highlightthickness=0)
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

CreateScrollBars([TabGeneralOuter, TabDriversOuter, TabBladesOuter, TabEnemiesOuter, TabMiscOuter, TabQOLOuter, TabCosmeticsOuter],[TabGeneralCanvas, TabDriversCanvas, TabBladesCanvas, TabEnemiesCanvas, TabMiscCanvas, TabQOLCanvas, TabCosmeticsCanvas],[TabGeneral, TabDrivers, TabBlades, TabEnemies, TabMisc, TabQOL, TabCosmetics])


MainWindow.add(TabGeneralOuter, text ='General') 
MainWindow.add(TabDriversOuter, text ='Drivers') 
MainWindow.add(TabBladesOuter, text ='Blades') 
MainWindow.add(TabEnemiesOuter, text ='Enemies') 
MainWindow.add(TabMiscOuter, text ='Misc.') 
MainWindow.add(TabQOLOuter, text = 'Quality of Life')
MainWindow.add(TabCosmeticsOuter, text='Cosmetics')
MainWindow.pack(expand = True, fill ="both", padx=10, pady=10) 


def GenOption(optionName, parentTab, desc, Filename=[], keyWords=[], rangeOfValuesToReplace=[], rangeOfValidReplacements=[],  OptionNameANDIndexValue = [], InvalidTargetIDs =[]):
    global rowIncrement
    global OptionsRunList
    global OptionInputs

    optionPanel = Frame(parentTab, padx=10, pady=10)
    optionPanel.grid(row = rowIncrement, column= 0, sticky="sw")

    if (rowIncrement %2 == 0):
        OptionColor = White
    else:
        OptionColor = Gray
    
    optionPanel.config(background=OptionColor)
    option = Label(optionPanel, text=optionName, background=OptionColor, width=30, anchor="w")
    option.grid(row=rowIncrement, column=0, sticky="sw")

    # Make here a option based on what user wants for their option (they can have multiple EX. A frequency slider AND a checkbox for yes no)
    optionSlider = Scale(optionPanel, from_=0, to=100, orient= HORIZONTAL, sliderlength=10, background=OptionColor, highlightthickness=0)
    OptionInputs.append(optionSlider)
    optionSlider.grid(row=rowIncrement, column=1, sticky='n')

    optionDesc = Label(optionPanel, text=desc, background=OptionColor, width=900, anchor='w')
    optionDesc.grid(row=rowIncrement, column=2, sticky="sw")


    for i in range((len(OptionNameANDIndexValue))//2):
        var = BooleanVar()

        checkFunction = lambda i=i, var=var: Helper.OptionCarveouts(rangeOfValidReplacements, OptionNameANDIndexValue[2*i+1], var)

        box = Checkbutton(optionPanel, background=OptionColor, text=OptionNameANDIndexValue[2*i], variable=var, command = checkFunction, highlightthickness=0)
        
        #HACKY want to fix
        CheckBoxFunctions.append(checkFunction)


        CheckboxStates.append(var)
        CheckboxList.append(OptionNameANDIndexValue[2*i] + " Box")
        box.grid(row=rowIncrement+i+1, column=0, sticky="sw")
        Helper.OptionCarveouts(rangeOfValidReplacements, OptionNameANDIndexValue[2*i+1], var)
    rowIncrement += 1

    if optionName != "Enemies": # make this pass an anonymous function so the genoption calls have the decision of what funciton to run
        OptionsRunList.append(lambda: JSONParser.ChangeJSON(optionName, Filename, keyWords, rangeOfValuesToReplace, optionSlider.get(), rangeOfValidReplacements, InvalidTargetIDs))


GenOption("Pouch Item Shops", TabGeneral, "Randomizes what Pouch Items appear in Pouch Item Shops", ["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), list(set(PouchItems)-set([40007])), PouchItems)
GenOption("Accessory Shops", TabGeneral, "Randomizes what Accessories appear in Accessory Shops", ["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), list(set(Accessories)-set([1])), Accessories + Helper.inclRange(448,455))
GenOption("Weapon Chip Shops", TabGeneral, "Randomizes what Weapon Chips appear in Weapon Chip Shops", ["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), WeaponChips, WeaponChips)

GenOption("Treasure Chests Contents", TabGeneral, "Randomizes the contents of Treasure Chests", Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"), ["itm1ID", "itm2ID", "itm3ID", "itm4ID","itm5ID","itm6ID","itm7ID","itm8ID"], Accessories + WeaponChips + AuxCores + CoreCrystals,[], ["Accessories", Accessories,"Weapon Chips", WeaponChips, "Aux Cores", AuxCores, "Core Crystals", CoreCrystals, "Deeds", Deeds, "Collection Point Materials", CollectionPointMaterials])
GenOption("Collection Points", TabGeneral, "Randomizes the contents of Collection Points", Helper.InsertHelper(2,1,90, "maa_FLD_CollectionPopList.json", "common_gmk/"), ["itm1ID", "itm2ID", "itm3ID", "itm4ID"], list(set(CollectionPointMaterials) - set([30019])), [], ["Accessories", Accessories,"Weapon Chips", WeaponChips, "Aux Cores", AuxCores, "Core Crystals", CoreCrystals, "Deeds", Deeds, "Collection Point Materials", CollectionPointMaterials])

GenOption("Driver Art Debuffs", TabDrivers, "Randomizes a Driver's Art debuff effect", ["common/BTL_Arts_Dr.json"], ["ArtsDeBuff"], ArtDebuffs, ArtDebuffs + ArtBuffs, ["Doom", [21]],  InvalidTargetIDs=AutoAttacks)
# GenOption("Driver Art Distances", TabDrivers, "Randomizes how far away you can cast an art", ["common/BTL_Arts_Dr.json"], ["Distance"], Helper.inclRange(0, 20), Helper.inclRange(1,20)) Nothing wrong with this just kinda niche/silly
GenOption("Driver Skill Trees", TabDrivers, "Randomizes all driver's skill trees", ["common/BTL_Skill_Dr_Table01.json", "common/BTL_Skill_Dr_Table02.json", "common/BTL_Skill_Dr_Table03.json", "common/BTL_Skill_Dr_Table04.json", "common/BTL_Skill_Dr_Table05.json", "common/BTL_Skill_Dr_Table06.json"], ["SkillID"], DriverSkillTrees, DriverSkillTrees)
GenOption("Driver Art Reactions", TabDrivers, "Randomizes each hit of an art to have a random effect such as break, knockback etc.", ["common/BTL_Arts_Dr.json"], Helper.StartsWith("ReAct", 1,16), HitReactions, HitReactions, InvalidTargetIDs=AutoAttacks) # we want id numbers no edit the 1/6 react stuff
GenOption("Driver Animation Speed", TabDrivers, "Randomizes animation speeds", ["common/BTL_Arts_Dr.json"], ["ActSpeed"], Helper.inclRange(0,255), Helper.inclRange(50,255), InvalidTargetIDs=AutoAttacks)
#GenOption("Driver Starting Accessory", TabDrivers, "Randomizes what accessory your drivers begin the game with",["common/CHR_Dr.json"], ["DefAcce"], AllValues, Accessories, ["Remove All Starting Accessories", Accessories] ) only problem is the button on of off changin the values we want

GenOption("Blade Special Reactions", TabBlades, "Randomizes each hit of a blade special to have a random effect such as break, knockback etc.", ["common/BTL_Arts_Bl.json"], Helper.StartsWith("ReAct", 1, 16), HitReactions, HitReactions)
GenOption("Blade Special Damage Types", TabBlades, "Randomizes whether a blade's special deals Physical Damage or Ether Damage", ["common/BTL_Arts_Bl.json"], ["ArtsType"], [1, 2], [1,2])
GenOption("Blade Special Button Challenges", TabBlades, "Randomizes what button a special uses for its button challenge", ["common/MNU_BtnChallenge2.json"], Helper.StartsWith("BtnType", 1, 3), ButtonCombos, ButtonCombos)
GenOption("Blade Elements", TabBlades, "Randomizes what element a blade is", ["common/CHR_Bl.json"],["Atr"], Helper.inclRange(1,8), Helper.inclRange(1,8))
GenOption("Blade Battle Skills", TabBlades, "Randomizes blades battle (yellow) skill tree", ["common/CHR_Bl.json"], Helper.StartsWith("BSkill", 1, 3), BladeBattleSkills, BladeBattleSkills)
GenOption("Blade Green Skills", TabBlades, "Randomizes blades field (green) skill tree", ["common/CHR_Bl.json"], Helper.StartsWith("FSkill", 1, 3), BladeFieldSkills, BladeFieldSkills, ["Field Skill QOL", [1135]], InvalidTargetIDs=[1135])
GenOption("Blade Specials", TabBlades, "Randomizes blades special (red) skill tree", ["common/CHR_Bl.json"], Helper.StartsWith("BArts", 1, 3) + ["BartsEx", "BartsEx2"], BladeSpecials, BladeSpecials)
GenOption("Blade Cooldowns", TabBlades, "Randomizes a blades cooldown", ["common/CHR_Bl.json"], ["CoolTime"], Helper.inclRange(1,1000), Helper.inclRange(1,1000))
GenOption("Blade Arts", TabBlades, "Randomizes your blade's arts", ["common/CHR_Bl.json"], Helper.StartsWith("NArts",1,3), ArtBuffs, ArtBuffs)
GenOption("Blade Aux Core Slots", TabBlades, "Randomizes how many Aux Core slots a Blade gets", ["common/CHR_Bl.json"],["OrbNum"], Helper.inclRange(0,3), Helper.inclRange(0,3))
GenOption("Blade Names", TabBlades, "Randomizes the names of blades",["common/CHR_Bl.json"], ["Name"], Helper.inclRange(0,1000), BladeNames)
GenOption("Blade Defenses", TabBlades, "Randomizes Blade Physical and Ether Defense", ["common/CHR_Bl.json"], ["PArmor", "EArmor"], Helper.inclRange(0,100), BladeDefenseDistribution)
GenOption("Blade Mods", TabBlades, "Randomizes Blade Stat Modifiers", ["common/CHR_Bl.json"], ["HpMaxRev", "StrengthRev", "PowEtherRev", "DexRev", "AgilityRev", "LuckRev"], Helper.inclRange(0,100), BladeModDistribution)
GenOption("Blade Scale", TabBlades, "Randomizes the size of Blades", ["common/CHR_Bl.json"], ["Scale", "WpnScale"], AllValues, Helper.inclRange(1,250) + [1000,16000]) # Make sure these work for common blades

GenOption("Enemy Drops", TabEnemies, "Randomizes enemy drop tables", ["common/BTL_EnDropItem.json"], Helper.StartsWith("ItemID", 1, 8), AuxCores + Accessories + WeaponChips, AuxCores + Accessories + WeaponChips)
GenOption("Enemy Size", TabEnemies, "Randomizes the size of enemies", ["common/CHR_EnArrange.json"], ["Scale"], Helper.inclRange(0, 1000), Helper.inclRange(1, 200) + Helper.inclRange(990,1000))
GenOption("Enemies", TabEnemies, "Randomizes what enemies appear in the world", Helper.InsertHelper(2, 1,90,"maa_FLD_EnemyPop.json", "common_gmk/") + Helper.InsertHelper(2, 1,90,"mac_FLD_EnemyPop.json", "common_gmk/") + Helper.InsertHelper(2, 1,90,"mab_FLD_EnemyPop.json", "common_gmk/"), ["ene1ID", "ene2ID", "ene3ID", "ene4ID"], Helper.inclRange(0,1888), ValidEnemies, ["Story Bosses", [1998], "Quest Enemies", [1999], "Unique Monsters", [2000], "Superbosses", [2001], "Normal Enemies", [2002], "Mix Enemies Between Types", [2003], "Keep All Enemy Levels", [2004], "Keep Quest Enemy Levels", [2005], "Keep Story Boss Levels", [2006], "Core Crystal Changes", [2007], "Arts Cancel on Tier 1", [2008], "Balanced Random Skill Trees", [2009], "Shorter Tutorial", [2010], "Beta Stuff", [2011]])
GenOption("Enemy Move Speed", TabEnemies, "Randomizes how fast enemies move in the overworld", ["common/CHR_EnParam.json"], ["WalkSpeed", "RunSpeed"], Helper.inclRange(0,100), Helper.inclRange(0,100) + Helper.inclRange(250,255))
#GenOption("Enemy Level Ranges", TabEnemies, "Randomizes enemy level ranges", Helper.InsertHelper(2, 1,90,"maa_FLD_EnemyPop.json", "common_gmk/"), ["ene1Lv", "ene2Lv", "ene3Lv", "ene4Lv"], Helper.inclRange(-100,100), Helper.inclRange(-30,30))

GenOption("Music", TabMisc, "Randomizes what music plays where", ["common/RSC_BgmCondition.json"], ["BgmIDA", "BgmIDB", "BgmIDC", "BgmIDD"], BackgroundMusic, BackgroundMusic) # need to change title screen music
GenOption("NPCs", TabMisc, "Randomizes what NPCs appear in the world (still testing)", Helper.InsertHelper(2, 1,90,"maa_FLD_NpcPop.json", "common_gmk/"), ["NpcID"], Helper.inclRange(0,3721), Helper.inclRange(2001,3721))
GenOption("NPCs Size", TabMisc, "Randomizes the size of NPCs", ["common/RSC_NpcList.json"], ["Scale"], Helper.inclRange(1,100), Helper.inclRange(1,250))
#GenOption("Core Crystal Changes", TabMisc, "Removes Gacha System", ["common/ITM_CrystalList.json"], ["BladeID"],)
#GenOption("Funny Faces", TabMisc, "Randomizes Facial Expressions", ["common/EVT_eyetype.json"], ["$id"], Helper.inclRange(0,15), Helper.inclRange(0,15)) # doesnt work yet
GenOption("Menu Colors", TabMisc, "Randomizes Colors in the UI", ["common/MNU_ColorList.json"], ["col_r", "col_g", "col_b"], Helper.inclRange(0,255), Helper.inclRange(0,0))

# this changed animations on text but not in a good way:
# GenOption("Text Effects", TabMisc, "Randomizes text movement", ["common/MNU_ResMotion.json"], ["$id"], Helper.inclRange(1,39), Helper.inclRange(1,39))
# EnemyRandoLogic.ColumnAdjust("./_internal/JsonOutputs/common/MNU_ResMotion.json", ["file"], "sample") 

GenOption("Fix Bad Descriptions", TabQOL, "Fixes some of the bad descriptions in the game") #common_ms/menu_ms
GenOption("Running Speed", TabQOL, "Set your starting run speed bonus")
#GenOption("Freely Engage All Blades", TabQOL, "Allows all blades to be freely engaged", ["common/CHR_Bl.json"], []) # common/CHR_Bl Set Free Engage to true NEED TO FIGURE OUT ACCESS TO FLAGS

GenOption("Rex's Cosmetics", TabCosmetics, "Randomizes Rex's Outfits", ["common/CHR_Dr.json"], ["Model"], [DefaultRex], [], RexCosmetics)
GenOption("Pyra's Cosmetics", TabCosmetics, "Randomizes Pyra's Outfits", ["common/CHR_Bl.json"], ["Model"], [DefaultPyra], [], PyraCosmetics)
GenOption("Mythra's Cosmetics", TabCosmetics, "Randomizes Mythra's Outfits", ["common/CHR_Bl.json"], ["Model"], [DefaultMythra], [], MythraCosmetics)
GenOption("Nia's Cosmetics (Driver)", TabCosmetics, "Randomizes Nia's Driver Outfits", ["common/CHR_Dr.json"], ["Model"], [DefaultDriverNia], [], NiaDriverCosmetics)
GenOption("Nia's Cosmetics (Blade)", TabCosmetics, "Randomizes Nia's Blade Outfits", ["common/CHR_Bl.json"], ["Model"], [DefaultBladeNia], [], NiaBladeCosmetics)
GenOption("Dromarch's Cosmetics", TabCosmetics, "Randomizes Dromarch's Outfits", ["common/CHR_Bl.json"], ["Model"], [DefaultDromarch], [], DromarchCosmetics)
GenOption("Tora's Cosmetics", TabCosmetics, "Randomizes Tora's Outfits", ["common/CHR_Dr.json"], ["Model"], [DefaultTora], [], ToraCosmetics)
GenOption("Morag's Cosmetics", TabCosmetics, "Randomizes Morag's Outfits", ["common/CHR_Dr.json"], ["Model"], [DefaultMorag], [], MoragCosmetics)
GenOption("Brighid's Cosmetics", TabCosmetics, "Randomizes Brighid's Outfits", ["common/CHR_Bl.json"], ["Model"], [DefaultBrighid], [], BrighidCosmetics)
GenOption("Zeke's Cosmetics", TabCosmetics, "Randomizes Zeke's Outfits", ["common/CHR_Dr.json"], ["Model"], [DefaultZeke], [], ZekeCosmetics)
GenOption("Pandoria's Cosmetics", TabCosmetics, "Randomizes Pandoria's Outfits", ["common/CHR_Bl.json"], ["Model"], [DefaultPandoria], [], PandoriaCosmetics)

OptionsRunList.append(lambda: EnemyRandoLogic.EnemyLogic(CheckboxList, CheckboxStates))
OptionsRunList.append(lambda: SkillTreeAdjustments.BalancingSkillTreeRando(CheckboxList, CheckboxStates))
OptionsRunList.append(lambda: CoreCrystalAdjustments.CoreCrystalChanges(CheckboxList, CheckboxStates))
OptionsRunList.append(lambda: TestingStuff.Beta(CheckboxList, CheckboxStates))
OptionsRunList.append(lambda: TutorialShortening.ShortenedTutorial(CheckboxList, CheckboxStates))

def Randomize():
    def ThreadedRandomize():
        global OptionsRunList
        RandomizeButton.config(state=DISABLED)

        random.seed(randoSeedEntry.get())
        print("Seed: " + randoSeedEntry.get())

        subprocess.run(f"./_internal/Toolset/bdat-toolset-win64.exe extract {bdatFilePathEntry.get()}/common.bdat -o {JsonOutput} -f json --pretty")
        subprocess.run(f"./_internal/Toolset/bdat-toolset-win64.exe extract {bdatFilePathEntry.get()}/common_gmk.bdat -o {JsonOutput} -f json --pretty")
        subprocess.run(f"./_internal/Toolset/bdat-toolset-win64.exe extract {bdatFilePathEntry.get()}/gb/common_ms.bdat -o {JsonOutput} -f json --pretty")

        for OptionRun in OptionsRunList:
            OptionRun()

        subprocess.run(f"./_internal/Toolset/bdat-toolset-win64.exe pack {JsonOutput} -o {outDirEntry.get()} -f json")
        os.makedirs(f"{outDirEntry.get()}/gb", exist_ok=True)
        shutil.move(f"{outDirEntry.get()}/common_ms.bdat", f"{outDirEntry.get()}/gb/common_ms.bdat")


        RandomizeButton.config(state=NORMAL)
        print("Done")

    threading.Thread(target=ThreadedRandomize).start()
    
def GenRandomSeed():
    print(Helper.InsertHelper(3,1,8,"itmID", ""))
    #print(Helper.StartsWithHelper("BSkill", 1, 3))
    #Helper.FindBadValuesList("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["Name"], [0], "$id")
    # Helper.FindBadValuesList("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["ParamID"], [1,307,308,285,1261,314,339,1143,350,892,1041,303,942,1153,1015,1016,941,891,317,1258,1250,352,331,281,343, 3, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21,1116,1118,1172, 1178,1179,1134,1135,1136,1154,1194,1195,1196,1197,1199,1200,332, 0, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 0, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 140, 0, 141, 142, 143, 144, 145, 146, 147, 149, 150, 151, 152, 153, 154, 155, 156, 0, 157, 158, 159, 160, 161, 0, 163, 164, 166, 165, 348, 167, 168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 220, 221, 222, 286, 348, 126, 286, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 196, 197, 198, 199, 205, 207, 208, 209, 1052, 1053, 1052, 1055, 1056, 1057, 1058, 1062, 1068, 1070, 1072, 1073, 1077, 1078, 1083, 1084, 1086, 1087, 1089, 1090, 1091, 1092, 1093, 1094, 1096, 1099, 1100, 1109, 1110, 1111, 1113, 1114, 1117, 1119, 1120, 1122, 1124, 1126, 1127, 1133, 1137, 1138, 1144, 1156, 1158, 1164, 1166, 1168, 1175, 1176, 1177, 1181, 1183, 1185, 1187, 1189, 1191, 1198, 1205, 1208, 1209, 1216, 1221, 1223, 1225, 1227, 1228, 1229, 1234, 1236, 1238, 1240, 1242, 1255, 1263, 1265, 1267, 1270, 1272, 1274, 1276, 1278, 1280, 1282, 1283, 1284, 1285, 1286, 1287, 1293, 1295, 1297, 1299, 1301, 1310, 1312, 1330, 1331, 1336, 1338, 1340, 1341, 1342, 1343, 1345, 1346, 1348, 1350, 1351, 1352, 1353, 1355, 1361, 1362, 1370, 1371, 386, 195, 354, 387, 388, 356, 189, 190, 370, 371, 372, 373, 459, 461, 463, 498, 560, 562, 564, 566, 568, 574, 579, 581, 644, 647, 649, 651, 659, 662, 683, 685, 687, 689, 718, 782, 785, 865, 867, 869, 895, 898, 1020, 1022, 1026, 1037, 1038, 1043, 346, 272, 272, 273, 273, 274, 275, 276, 277, 278, 279, 279, 280, 281, 193, 162, 325, 162, 264, 228, 229, 230, 231, 232, 233, 282, 283, 284, 1375, 1377, 210, 212, 213, 214, 215, 217, 218, 219, 272, 279, 281, 392, 1383, 1385, 1387, 1394, 1396, 1399, 1401,1067,1083,1084,181,184,300,1492,457,1173,1184,1190,1182,1188,1180,1186,579, 0, 0, 1413, 1437, 1438, 1439, 0, 0, 0, 0, 0, 0, 0, 1486, 1487, 1488, 1491, 1496, 1499, 1502, 1505, 1506, 1507, 1521, 0, 0, 0, 0, 0, 0, 0, 1584, 1589, 1624, 1639, 1640, 1642, 0, 0, 1660, 0], "$id")
    # FindBadValuesList("./_internal/JsonOutputs/common_gmk/ma05a_FLD_EnemyPop.json", ["ene1ID"], inclRange(0,100000), "ene1ID")
    #print(Helper.InsertHelper(2,1,90, "maa_FLD_CollectionPopList.json", "common_gmk/"))
    # Helper.FindSubOptionValuesList("./_internal/JsonOutputs/common/CHR_EnArrange.json", "Flag", "AlwaysAttack", 1, "$id") 
    #EnemyRandoLogic.FindMatchingInfo
    #Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], Helper.inclRange(1,37), "Blade")
    randoSeedEntry.delete(0, END)
    randoSeedEntry.insert(0,SeedNames.RandomSeedName())


bdatcommonFrame = Frame(root, background='#632424')
bdatcommonFrame.pack(anchor="w", padx=10)
bdatButton = Button(bdatcommonFrame, width=20, text="Choose Input Folder", command= lambda: Helper.DirectoryChoice("Choose your folder containing common.bdat, common_ms.bdat and common_gmk.bdat", bdatFilePathEntry))
bdatButton.pack(side="left", padx=2, pady=2)
bdatFilePathEntry = Entry(bdatcommonFrame, width=500)
bdatFilePathEntry.pack(side="left", padx=2)
OutputDirectoryFrame = Frame(root, background='#632424')
OutputDirectoryFrame.pack(anchor="w", padx=10)
outputDirButton = Button(OutputDirectoryFrame, width = 20, text='Choose Output Folder', command= lambda: Helper.DirectoryChoice("Choose an output folder", outDirEntry))
outputDirButton.pack(side="left", padx=2, pady=2)
outDirEntry = Entry(OutputDirectoryFrame, width=500)
outDirEntry.pack(side="left", padx=2)
SeedFrame = Frame(root, background='#632424')
SeedFrame.pack(anchor="w", padx=10)
seedDesc = Button(SeedFrame, text="Seed", command=GenRandomSeed)
seedDesc.pack(side='left', padx=2, pady=2)
randoSeedEntry = Entry(SeedFrame, width=25)
randoSeedEntry.pack(side='left', padx=2)
RandomizeButton = Button(text='Randomize', command=Randomize)
RandomizeButton.pack(pady=10) 

EveryObjectSave = ([bdatFilePathEntry, outDirEntry, randoSeedEntry] + CheckboxStates + OptionInputs)
SavedOptions.loadData(EveryObjectSave)
#HACKY want to fix 
for boxFunction in CheckBoxFunctions:
    boxFunction()

root.protocol("WM_DELETE_WINDOW", lambda: (SavedOptions.saveData(EveryObjectSave), root.destroy()))
root.mainloop()