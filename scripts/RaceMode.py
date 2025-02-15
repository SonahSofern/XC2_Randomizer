import Helper as Helper
import json
import EnemyRandoLogic as EnemyRandoLogic
import random
from IDs import AllRaceModeItemTypeIDs, RaceModeAuxCoreIDs, A1RaceModeCoreChipIDs, A2RaceModeCoreChipIDs, A3RaceModeCoreChipIDs, A4RaceModeCoreChipIDs, SeedHashAdj, SeedHashNoun, ValidTboxMapNames, AllCoreCrystals, InvalidTreasureBoxIDs, PreciousItems, Accessories, WeaponChips, AuxCores, RefinedAuxCores, CollectionPointMaterials, TornaAccessories
import time
import JSONParser
import DebugLog
import CoreCrystalAdjustments
import math, Options

AllMapIDs = [["Gormott", "ma05a"], ["Uraya", "ma07a"], ["Mor Ardain","ma08a"], ["Leftherian Archipelago", "ma15a"], ["Indoline Praetorium", "ma11a"], ["Tantal", "ma13a"], ["Spirit Crucible Elpys", "ma16a"], ["Cliffs of Morytha", "ma17a"], ["World Tree", "ma20a"], ["Final Stretch", "ma21a"]] #that we care about lol

# Default Level-Based Modifiers for EXP, Damage Taken/Given, Accuracy, and Odds of getting a reaction (on an enemy?) (break/topple/launch/smash)
ExpRevHigh = [105, 110, 117, 124, 134, 145, 157, 170, 184, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
ExpRevLow = [95, 86, 77, 69, 62, 56, 50, 45, 41, 37, 33, 30, 27, 24, 22, 20, 18, 16, 14, 13]
ExpRevLow2 = [100, 95, 88, 81, 75, 69, 64, 56, 49, 43, 38, 33, 29, 25, 22, 20, 18, 16, 14, 13]
DamageRevHigh = [100, 100, 100, 105, 110, 125, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
DamageRevLow = [100, 100, 100, 98, 96, 94, 92, 90, 88, 86, 84, 82, 80, 78, 76, 74, 72, 70, 68, 66]
HitRevLow = [110, 115, 122, 129, 138, 147, 158, 169, 182, 195, 210, 225, 242, 259, 278, 297, 318, 339, 362, 385]
ReactRevHigh = [0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 40, 60, 80, 100, 100, 100, 100, 100, 100, 100]

def RaceModeChanging(): 
    print("Setting Up Race Mode")    
    #Helper.ColumnAdjust("./_internal/JsonOutputs/common/MNU_WorldMapCond.json", ["cond1"], 1850) #unlocks the world maps
    #Helper.ColumnAdjust("./_internal/JsonOutputs/common/FLD_maplist.json", ["mapON_cndID"], 1850) #unlocks the world maps

    AreaList1 = [41, 68] #41, 68
    AreaList2 = [99, 152] #99, 152
    AreaList3 = [125, 133, 168] #125, 133, 168
    AreaList4 = [175, 187] #175, 187

    RaceModeDungeons = []
    RaceModeDungeons.append(random.choice(AreaList1))
    RaceModeDungeons.append(random.choice(AreaList2))
    RaceModeDungeons.append(random.choice(AreaList3))
    RaceModeDungeons.append(random.choice(AreaList4))
    RaceModeDungeons.append(200)

    # common/FLD_QuestList
    # [Gormott, Uraya, Mor Ardain, Leftherian Archipelago, Temperantia + Indoline Praetorium, Tantal, Spirit Crucible Elpys, Cliffs of Morytha + Land of Morytha, World Tree, Final Stretch]

    ContinentWarpCutscenes = [10035, 10088, 10156, 10197, 10213, 10270, 10325, 10350, 10399, 10476] # We want to call these after the boss fight cutscenes
    FinalContinentCutscenes = [10079, 10130, 10189, 10212, 10266, 10304, 10345, 10392, 10451, 30000]
    NextQuestAList = [27, 56, 100, 128, 136, 163, 184, 195, 215, 238]
    LastQuestAList = [50, 81, 125, 135, 161, 177, 191, 211, 227, 270]
    ScenarioFlagLists = [2001, 3005, 4025, 5005, 5021, 6028, 7018, 7043, 8031, 10026]
    LevelAtStartofArea = [5, 20, 29, 35, 38, 42, 46, 51, 59, 68] #Level going to: # Level(ish) of the first boss of the current area (so you want to be around this level after warping)
    LevelAtEndofArea = [15, 26, 34, 35, 42, 46, 46, 59, 68, 70]  #Level going from: # Level the last boss of the previous area was (so you should be around the same level before warping to new area)

    # The Save File is set up in a way that it is level 5 already to start with.
    # XP needed to reach a given level, formatted in [Given Level, Total XP Needed]
    XPNeededToReachLv = [[5, 390], [15, 9100], [20, 21360], [26, 44520], [29, 59820], [34, 91320], [35, 98580], [38, 122520], [42, 160080], [46, 205140], [51, 274640], [59, 428120], [68, 682040], [70, 789920]]
    global ChosenIndices
    ChosenIndices = []

    RaceModeMapJumpIDs = [41, 68, 99, 152, 125, 133, 168, 175, 187, 200]

    for i in range(0, len(RaceModeDungeons)): # Defines the chosen indices that we're using from the list of race-mode locations
        for j in range(0, len(RaceModeMapJumpIDs)):
            if RaceModeDungeons[i] == RaceModeMapJumpIDs[j]:
                ChosenIndices.append(j)
    ExpBefore = [0] * 5
    ExpAfter = [0] * 5
    ExpDiff = [0] * 5

    for i in range(0, len(ChosenIndices)): # Defines the EXP difference we need to give to the first landmark in a race-mode location    
        for j in range(0, len(XPNeededToReachLv)):
            if i == 0:
                ExpBefore[i] = 390
                if LevelAtStartofArea[ChosenIndices[i]] == XPNeededToReachLv[j][0]:    
                    ExpAfter[i] = XPNeededToReachLv[j][1]
                    break
            if i < 4:
                if LevelAtEndofArea[ChosenIndices[i-1]] == XPNeededToReachLv[j][0]:
                    ExpBefore[i] = XPNeededToReachLv[j][1]
                if LevelAtStartofArea[ChosenIndices[i]] == XPNeededToReachLv[j][0]:
                    ExpAfter[i] = XPNeededToReachLv[j][1]
            if i == 4:
                ExpAfter[i] = 682040
                if LevelAtEndofArea[ChosenIndices[i-1]] == XPNeededToReachLv[j][0]:
                    ExpBefore[i] = XPNeededToReachLv[j][1]
                    break
                
        ExpDiff[i] = ExpAfter[i] - ExpBefore[i]

    MapSpecificIDs = [501, 701, 832, 1501, 1101, 1301, 1601, 1701, 2012, 2103]
    FileStart = "./_internal/JsonOutputs/common_gmk/"
    FileEnd = "_FLD_LandmarkPop.json"
    global LandmarkFilestoTarget
    LandmarkFilestoTarget = [] 
    LandmarkMapSpecificIDstoTarget = []
    
    for i in range(0, len(ChosenIndices)): # Defines what files we want to target and what map ids in that file we want to target  
        LandmarkFilestoTarget.append(FileStart + AllMapIDs[ChosenIndices[i]][1] + FileEnd)
        LandmarkMapSpecificIDstoTarget.append(MapSpecificIDs[ChosenIndices[i]])

    for i in range(0, len(LandmarkFilestoTarget)):  # Adjusts the EXP gained from the first landmark in every other race-mode location      
            with open(LandmarkFilestoTarget[i], 'r+', encoding='utf-8') as file:
                data = json.load(file)
                for row in data["rows"]:
                    if row["$id"] == LandmarkMapSpecificIDstoTarget[i]:
                        row["getEXP"] = ExpDiff[i]
                        if (i+2) % 2 == 0: 
                            row["getSP"] = 1500 + 6800 * ChosenIndices[i] #This allows me to award some sp for gormott area 1, which feels barren at the moment.
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=2, ensure_ascii=False)
    
    with open("./_internal/JsonOutputs/common/FLD_QuestList.json", 'r+', encoding='utf-8') as file: #race mode implementation #these just adjust the quest markers as far as I can tell
        data = json.load(file)
        for row in data["rows"]:
            if (row["PRTQuestID"] != 0) and (row["$id"] >= 25):
                row["PRTQuestID"] = 6
            if row["$id"] == 15: # Talking to Spraine
                row["NextQuestA"] = NextQuestAList[ChosenIndices[0]]
        for i in range(0, len(ChosenIndices) - 1):
            for row in data["rows"]:
                if row["$id"] == LastQuestAList[ChosenIndices[i]]:
                    row["NextQuestA"] = NextQuestAList[ChosenIndices[i+1]]
                    break
        for row in data["rows"]: # because cliffs and land are together, the chapter cutscene sets the current quest cleared id to something that is not 6, causing issues with the way I did things.
            if row["$id"] == 200:
                row["NextQuestA"] = 202
            if row["$id"] == 261: # same thing for indol and temperantia
                row["NextQuestA"] = 150
            if row["$id"] == 220: # world tree chapter transition fix
                row["NextQuestA"] = 222
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    if ChosenIndices[3] == 8:
        with open("./_internal/JsonOutputs/common_gmk/ma20a_FLD_LandmarkPop.json", 'r+', encoding='utf-8') as file: # Turning World Tree Mizar Floor into another landmark
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] == 2001:
                    row["menuPriority"] = 10
                if row["$id"] == 2012:
                    row["category"] = 0
                    row["MAPJUMPID"] = 187
                    row["menuPriority"] = 20
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/EVT_listBf.json", 'r+', encoding='utf-8') as file: # adjust story events, changing scenario flag
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10013:
                if ChosenIndices[0] == 0:
                    # Gormott
                    row["nextID"] = 10035
                    row["scenarioFlag"] = 2002
                    row["nextIDtheater"] = 10035
                if ChosenIndices[0] == 1:
                    # Uraya
                    row["nextID"] = 10088
                    row["scenarioFlag"] = 3005
                    row["nextIDtheater"] = 10088
        for i in range(0, len(ChosenIndices) - 1):
            for row in data["rows"]:
                if row["$id"] == FinalContinentCutscenes[ChosenIndices[i]]:
                    row["nextID"] = ContinentWarpCutscenes[ChosenIndices[i+1]]
                    row["nextIDtheater"] = ContinentWarpCutscenes[ChosenIndices[i+1]]
                    row["scenarioFlag"] = ScenarioFlagLists[ChosenIndices[i+1]]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common_gmk/FLD_ElevatorGimmick.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 17: # Think this patches skipping zohar fragments by just walking to end of game lol
                row["tgt_liftswitchMSG_ID"] = 0
                row["liftnameRadius"] = 0
                row["lift_offsetID"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    ScriptAdjustments()
    NGPlusBladeCrystalIDs = DetermineNGPlusBladeCrystalIDs()
    PickupRadiusDeedStart()
    DifficultyChanges()
    XPDownScaling()
    DriverLvandSPFix()
    LandmarkConditions()
    GimmickAdjustments()
    HideMapAreas(ScenarioFlagLists)
    print("Filling Chests with Custom Loot")
    RaceModeLootChanges(NGPlusBladeCrystalIDs)
    StackableCoreCrystalsandKeyItems()
    FindtheBladeNames()
    print("Reducing amount of grinding")
    LessGrinding()
    if NGPlusBladeCrystalIDs != None:
        ChangeBladeLevelUnlockReqs(NGPlusBladeCrystalIDs)
        ReduceBladeReqTrustVals()
    SecondSkillTreeCostReduc()
    DriverArtUpgradeCostChange()
    BladeTreeMaxRewardChange()
    PoppiswapCostReductions()   
    print("Changing Shops")
    ShyniniSaveUs()
    ShopRemovals()
    WeaponChipShopPowerLevelIncrease()
    MovespeedDeedChanges()
    PouchItemCarryCapacityIncrease()
    print("Removing enemy drops")
    EnemyDropRemoval()
    EnemyRandoLogic.KeyItemsReAdd()
    CoreCrystalAdjustments.FieldSkillLevelAdjustment()
    if Options.RaceModeOption_DLC.GetState():
        print("Nerfing Corvin and Crossette")
        DLCItemChanges()

def PoppiswapCostReductions(): # reduces cost of poppiswap stuff
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/ITM_HanaArtsEnh.json","./_internal/JsonOutputs/common/ITM_HanaAssist.json", "./_internal/JsonOutputs/common/ITM_HanaAtr.json", "./_internal/JsonOutputs/common/ITM_HanaNArtsSet.json", "./_internal/JsonOutputs/common/ITM_HanaRole.json"], ["NeedEther", "DustEther"], ['row[key] // 2'])
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_HanaPower.json"], ["EtherNum1", "EtherNum2", "EtherNum3"], ['row[key] // 2'])
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_HanaBase.json"], ["Circuit4Num", "Circuit5Num", "Circuit6Num"], ['row[key] // 5'])

def LessGrinding(): #adjusting level based exp gains, and debuffs while underleveled to make it less grindy
    with open("./_internal/JsonOutputs/common/BTL_Lv_Rev.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            row["ExpRevHigh"] = 210 + 20 * row["$id"]
            row["ExpRevLow"] = 100
            if row["$id"] >= 10:
                row["DamageRevHigh"] = 250
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def DetermineNGPlusBladeCrystalIDs():
    NGPlusBladeIDs = [1043, 1044, 1045, 1046, 1047, 1048, 1049]
    NGPlusBladeCrystalIDs = []
    if (Options.CustomCoreCrystalOption.GetState()) or (Options.UMHuntOption.GetState()):
        with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for i in range(0, len(NGPlusBladeIDs)):
                for row in data["rows"]:
                    if row["BladeID"] == NGPlusBladeIDs[i]:
                        NGPlusBladeCrystalIDs.append(row["$id"])
                        break
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
        return NGPlusBladeCrystalIDs

def ChangeBladeLevelUnlockReqs(NGPlusBladeCrystalIDs): # changes the blade trust/skill unlock requirements to the same condition as reaching the 2nd and 4th race mode areas
    KeyAchievementIDs = [15, 25, 0, 35, 45, 55, 65, 75, 85, 95, 105, 0, 0, 115, 125, 135, 145, 375, 385, 155, 185, 165, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295, 305, 315, 325, 335, 345, 195, 355, 365, 395, 0, 415, 425, 465, 455, 445, 435, 405, 175, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 95, 405, 455, 455, 445, 435, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 365, 85, 1668, 1678, 1648, 1658, 1739, 1749, 0, 1759, 1739, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 325, 325, 325, 1679, 1689, 1699, 1709, 1719, 1729]
    KeyAchievementIDs = list(set([x for x in KeyAchievementIDs if x != 0]))
    RelevantChosenIndices = [x for x in ChosenIndices if x != 9]
    RelevantLocation = [501, 701, 832, 1501, 1101, 1301, 1601, 1701, 2012]
    MapIDs = [6, 9, 10, 14, 12, 13, 15, 16, 20]
    TaskIDs = [143, 309, 147, 285]
    TaskLogIDs = [659, 660, 661, 662]
    LocationNames = ["Gormott", "Uraya", "Mor Ardain", "Leftheria", "Indol", "Tantal", "Spirit Crucible Elpys", "the Cliffs of Morytha", "the World Tree"]

    StarterBladeTrustSetAppearance = [16, 12, 16, 14, 16] #rank 1
    A1TrustSetAppearance = [16, 12, 16, 14, 16] # rank 1
    A2TrustSetAppearance = [16, 16, 16, 14, 16] # rank 3
    A3TrustSetAppearance = [16, 16, 16, 14, 16] # rank 3
    A4TrustSetAppearance = [16, 16, 16, 16, 16] # rank 5

    AllTrustSetAppearances = [StarterBladeTrustSetAppearance, A1TrustSetAppearance, A2TrustSetAppearance, A3TrustSetAppearance, A4TrustSetAppearance]

    StarterBladeIDs = [1001, 1002, 1004, 1005, 1006, 1007, 1009, 1010]
    A1BladeIDs = []
    A2BladeIDs = []
    A3BladeIDs = []
    A4BladeIDs = [1043, 1044, 1045, 1046, 1047, 1048, 1049, 1011]

    ValidCrystalListIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    ValidCrystalListIDs = [x for x in ValidCrystalListIDs if x not in NGPlusBladeCrystalIDs]
    CorrespondingBladeIDs = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/ITM_CrystalList.json",["$id"], ValidCrystalListIDs, "BladeID")
    A1BladeIDs = CorrespondingBladeIDs[:12]
    del CorrespondingBladeIDs[:12]
    A2BladeIDs = CorrespondingBladeIDs[:12]
    del CorrespondingBladeIDs[:12]
    A3BladeIDs = CorrespondingBladeIDs
    AllBladeIDs = [StarterBladeIDs, A1BladeIDs, A2BladeIDs, A3BladeIDs, A4BladeIDs]

    ArtandSkillCols = ["ArtsAchievement1", "ArtsAchievement2", "ArtsAchievement3", "SkillAchievement1", "SkillAchievement2", "SkillAchievement3"]
    TrustCol = "KeyAchievement"

    ArtandSkillIDs = [[0], [0], [0], [0], [0]]
    TrustIDs = [[0], [0], [0], [0], [0]]

    for g in range(0, 5): # need to find the area each id belongs to
        for i in range(0, len(ArtandSkillCols)):
            ArtandSkillIDs[g] = ArtandSkillIDs[g] + Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/CHR_Bl.json", ["$id"], AllBladeIDs[g], ArtandSkillCols[i])
            ArtandSkillIDs[g] = list(set(ArtandSkillIDs[g])- set([0]))
        TrustIDs[g] = TrustIDs[g] + Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/CHR_Bl.json", ["$id"], AllBladeIDs[g], TrustCol)
        TrustIDs[g] = list(set(TrustIDs[g]) - set([0]))

    with open("./_internal/JsonOutputs/common/FLD_AchievementSet.json", 'r+', encoding='utf-8') as file: # now we need to modify corresponding set ids
        data = json.load(file)
        for i in range(0, len(ArtandSkillIDs)):
            for row in data["rows"]:
                if row["$id"] in ArtandSkillIDs[i]:
                    for j in range(1, 6):
                        if (row[f"AchievementID{j}"] != 0):
                            row[f"AchievementID{j}"] = 16
                if row["$id"] in TrustIDs[i]: 
                    for j in range(1,6):
                        row[f"AchievementID{j}"] = AllTrustSetAppearances[i][j-1]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_Achievement.json", 'r+', encoding='utf-8') as file: #we need to change FLD_Achievement ID 1 to walk 1 step total
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1:
                    row["StatsID"] = 60
                    row["Count"] = 1
                    row["DebugName"] = "WALK_TOTAL"
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_QuestTaskAchievement.json", 'r+', encoding='utf-8') as file: #now we need to modify the FLD_QuestTaskAchievement
        data = json.load(file)
        for i in range(0, 4):
            for row in data["rows"]:
                if row["$id"] <= 7004:
                    row["TaskType1"] = 5
                    row["TaskID1"] = TaskIDs[row["$id"]-7001]
                    row["TaskCondition1"] = 0
                if row["$id"] == 7005:
                    row["TaskType1"] = 12
                    row["TaskID1"] = 1
                    row["TaskCondition1"] = 0
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_QuestReach.json", 'r+', encoding='utf-8') as file:  #modifying the tasks where you need to reach a certain location
        data = json.load(file)
        for i in range(0, 4):
            for row in data["rows"]:
                if row["$id"] == TaskIDs[i]:
                    row["Category"] = 2
                    row["MapID"] = MapIDs[RelevantChosenIndices[i]]
                    row["PlaceID"] = RelevantLocation[RelevantChosenIndices[i]]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common_ms/fld_quest_achievement.json", 'r+', encoding='utf-8') as file: #modifying the text files that describe what you need to do to unlock the node
        data = json.load(file)
        for i in range(0, 4):
            for row in data["rows"]:
                if row["$id"] == TaskLogIDs[i]:
                    row["name"] = f"Reach {LocationNames[RelevantChosenIndices[i]]}"
                    break
            for row in data["rows"]:
                if row["$id"] == 663:
                    row["name"] = "Unlocked once you unlock the \n corresponding Trust Level."
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def RaceModeLootChanges(NGPlusBladeCrystalIDs):
    if NGPlusBladeCrystalIDs == None:
        A1CoreCrystalIDs, A2CoreCrystalIDs, A3CoreCrystalIDs, A4CoreCrystalIDs = [], [], [], []
    if NGPlusBladeCrystalIDs != None:
        NonNGPlusCoreCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
        NonNGPlusCoreCrystalIDs = [x for x in NonNGPlusCoreCrystalIDs if x not in NGPlusBladeCrystalIDs]
        NonNGPlusCoreCrystalIDs.sort()
        A1CoreCrystalIDs = (NonNGPlusCoreCrystalIDs[:12])
        del NonNGPlusCoreCrystalIDs[:12]
        A2CoreCrystalIDs = (NonNGPlusCoreCrystalIDs[:12])
        del NonNGPlusCoreCrystalIDs[:12]
        A3CoreCrystalIDs = (NonNGPlusCoreCrystalIDs)
        A4CoreCrystalIDs = NGPlusBladeCrystalIDs
    A1Equip, A2Equip, A3Equip, A4Equip = [], [], [], []
    DriverAccesEnh = Options.DriverAccessoriesOption.GetState()
    AuxCoreEnh = Options.BladeAuxCoresOption.GetState()
    if DriverAccesEnh: # If we have the wacky enhancements:
        CommonDAcc, RareDAcc, LegDAcc = Helper.FindValues("./_internal/JsonOutputs/common/ITM_PcEquip.json", ["Rarity"], [0], "$id"), Helper.FindValues("./_internal/JsonOutputs/common/ITM_PcEquip.json", ["Rarity"], [1], "$id"), Helper.FindValues("./_internal/JsonOutputs/common/ITM_PcEquip.json", ["Rarity"], [2], "$id")
        CommonDAcc, RareDAcc, LegDAcc = [x for x in CommonDAcc if x in Accessories], [x for x in RareDAcc if x in Accessories], [x for x in LegDAcc if x in Accessories]
        CommonDAcc, RareDAcc, LegDAcc = [x for x in CommonDAcc if x not in TornaAccessories], [x for x in RareDAcc if x not in TornaAccessories], [x for x in LegDAcc if x not in TornaAccessories]
        random.shuffle(CommonDAcc)
        random.shuffle(RareDAcc)
        random.shuffle(LegDAcc)
        for i in range(0, len(CommonDAcc) // 4):
            A1Equip.append(CommonDAcc[i])
        for i in range(len(CommonDAcc) // 4, len(CommonDAcc) // 2):
            A2Equip.append(CommonDAcc[i])
        for i in range(0, len(RareDAcc) // 3):
            A3Equip.append(RareDAcc[i])
        for i in range(0, len(LegDAcc) // 3):
            A4Equip.append(LegDAcc[i])
    else:
        for i in range(0, len(AllRaceModeItemTypeIDs)):
            A1Num = random.randint(1,3) - 1
            A2Num = random.randint(4,6) - 1
            A3Num = random.randint(7,9) - 1
            A4Num = random.randint(10,12) - 1
            A1Equip.append(AllRaceModeItemTypeIDs[i][A1Num]) 
            A2Equip.append(AllRaceModeItemTypeIDs[i][A2Num])
            A3Equip.append(AllRaceModeItemTypeIDs[i][A3Num])
            A4Equip.append(AllRaceModeItemTypeIDs[i][A4Num])
    if AuxCoreEnh: # with wacky aux cores
        CommonAux, RareAux, LegAux = Helper.FindValues("./_internal/JsonOutputs/common/ITM_OrbEquip.json", ["Rarity"], [0], "$id"), Helper.FindValues("./_internal/JsonOutputs/common/ITM_OrbEquip.json", ["Rarity"], [1], "$id"), Helper.FindValues("./_internal/JsonOutputs/common/ITM_OrbEquip.json", ["Rarity"], [2], "$id")
        random.shuffle(CommonAux)
        random.shuffle(RareAux)
        random.shuffle(LegAux)
        for i in range(0, len(CommonAux) // 2):
            A1Equip.append(CommonAux[i])
        for i in range(len(CommonAux) // 2, (len(CommonAux) * 3) // 4):
            A2Equip.append(CommonAux[i])
        for i in range(0, len(RareAux) // 2):
            A3Equip.append(RareAux[i])
        for i in range(0, len(LegAux) // 2):
            A4Equip.append(LegAux[i])
    else:
        for i in range(0, len(RaceModeAuxCoreIDs)):
            A1Num = random.randint(1,3) - 1
            A2Num = random.randint(4,6) - 1
            A3Num = random.randint(7,9) - 1
            A4Num = random.randint(10,12) - 1
            A1Equip.append(RaceModeAuxCoreIDs[i][A1Num]) 
            A2Equip.append(RaceModeAuxCoreIDs[i][A2Num])
            A3Equip.append(RaceModeAuxCoreIDs[i][A3Num])
            A4Equip.append(RaceModeAuxCoreIDs[i][A4Num])
    AllEquipIDs = [A1Equip, A2Equip, A3Equip, A4Equip]
    Area1ShopDeedIDs, Area2ShopDeedIDs, Area3ShopDeedIDs, Area4ShopDeedIDs = [], [], [], []
    Area1ShopDeedIDs, Area2ShopDeedIDs, Area3ShopDeedIDs, Area4ShopDeedIDs = Helper.InclRange(25249, 25264), Helper.InclRange(25265, 25280), Helper.InclRange(25281, 25291), Helper.InclRange(25292, 25299)
    Area1LootIDs = A1CoreCrystalIDs * 2 + [25305] * 3 + Area1ShopDeedIDs * 2 + [25450] * 3 + A1Equip + [25408] * 5 + [25218, 25218, 25218, 25219, 25219, 25219] + A1RaceModeCoreChipIDs * 2 + [25407] * 10
    if ChosenIndices[1] == 3: # Leftherian Archipelago (30ish chests)
        Area2LootIDs = A2CoreCrystalIDs + [25305] * 2 + Area2ShopDeedIDs + [25450] * 2 + A2Equip + [25408] * 3 + [25220, 25220] + A2RaceModeCoreChipIDs + [25407] * 5
    else: # Mor Ardain (70 ish chests)
        Area2LootIDs = A2CoreCrystalIDs * 2 + [25305] * 3 + Area2ShopDeedIDs * 2 + [25450] * 3 + A2Equip + [25408] * 5 + [25220, 25220, 25220] + A2RaceModeCoreChipIDs * 2 + [25407] * 10
    # adjusting the loot pool depending on dungeon size
    if ChosenIndices[2] == 5: # tantal (52 chests)
        Area3LootIDs = A3CoreCrystalIDs * 2 + [25305] * 3 + Area3ShopDeedIDs * 2 + [25450] * 3 + A3Equip + [25408] * 5 + [25221, 25221, 25221] + A3RaceModeCoreChipIDs * 2 + [25407] * 10    
    else: # (25 chests for these locations more or less)
        Area3LootIDs = A3CoreCrystalIDs + [25305] * 2 + Area3ShopDeedIDs + [25450] * 2 + A3Equip + [25408] * 3 + [25221, 25221] + A3RaceModeCoreChipIDs + [25407] * 5
    Area4LootIDs = A4CoreCrystalIDs + [25305] * 2 + Area4ShopDeedIDs + [25450] * 2 + A4Equip + [25408] * 3 + [25222, 25222] + A4RaceModeCoreChipIDs + [25407] * 5
    random.shuffle(Area1LootIDs)
    random.shuffle(Area2LootIDs)
    random.shuffle(Area3LootIDs)
    random.shuffle(Area4LootIDs)
    AllAreaLootIDs = [Area1LootIDs, Area2LootIDs, Area3LootIDs, Area4LootIDs]
    TBoxFiles = [[0,0], [0,0], [0,0], [0,0]] # this needs to be changed to a for loop if i change the number of race mode dungeons (append [0,0])
    FileStart = "./_internal/JsonOutputs/common_gmk/"
    FileEnd = "_FLD_TboxPop.json"
    StartingPreciousIDs = Helper.InclRange(25001, 25499)
    ExcludePreciousIDs = Helper.InclRange(25218, 25222) + [25305] + [25408] + [25450] + [25405] + [25406] + [25407] + Helper.InclRange(25249, 25300) + [25067, 25160] # We are ok with replacing these, since they're in the pool of items to pull from anyways or a debug item
    FinalPreciousIDs = [x for x in StartingPreciousIDs if x not in ExcludePreciousIDs] # We do not want to replace these, these are quest/key items
    for i in range(0, len(ChosenIndices) - 1): # Defines what files we want to target and what map ids in that file we want to target  
        if (ChosenIndices[i] != 4) & (ChosenIndices[i] != 7):
            TBoxFiles[i][0] = FileStart + AllMapIDs[ChosenIndices[i]][1] + FileEnd
    BoxestoRandomizePerMap = [0] * (len(ChosenIndices) - 1)
    TBoxName = ""
    for i in range(0, len(ChosenIndices)):
        if ChosenIndices[i] == 4:
            TBoxFiles[i][0] = "./_internal/JsonOutputs/common_gmk/ma10a_FLD_TboxPop.json"
            TBoxFiles[i][1] = "./_internal/JsonOutputs/common_gmk/ma11a_FLD_TboxPop.json"
        if ChosenIndices[i] == 7:
            TBoxFiles[i][0] = "./_internal/JsonOutputs/common_gmk/ma17a_FLD_TboxPop.json"
            TBoxFiles[i][1] = "./_internal/JsonOutputs/common_gmk/ma18a_FLD_TboxPop.json"
    global ListTboxFiles
    ListTboxFiles = []
    for i in range(0, 4):
        for j in range(0, 2):
            if TBoxFiles[i][j] != 0:
                ListTboxFiles.append(TBoxFiles[i][j])
    AllOtherMapIDs = [x for x in ValidTboxMapNames if x not in ListTboxFiles]
    for i in range(0, len(AllOtherMapIDs)):
        Helper.ColumnAdjust(AllOtherMapIDs[i], ["Condition", "itm1Num", "itm2Num", "itm3Num", "itm4Num", "itm5Num", "itm6Num", "itm7Num", "itm8Num", "itm1ID", "itm2ID", "itm3ID", "itm4ID", "itm5ID", "itm6ID", "itm7ID", "itm8ID"], 0)
    for i in range(0, len(ListTboxFiles)):
        Helper.ColumnAdjust(ListTboxFiles[i], ["Condition"], 0)
    for i in range(0, len(TBoxFiles)):
        for l in range(0, len(TBoxFiles[i])):
            if TBoxFiles[i][l] != 0:
                with open(TBoxFiles[i][l], 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data["rows"]:
                        if row["$id"] not in InvalidTreasureBoxIDs: 
                            BoxestoRandomizePerMap[i] = BoxestoRandomizePerMap[i] + 1
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
    ItemsPerBox = []
    for i in range(0, len(AllAreaLootIDs)):
        ItemsPerBox.append(int(math.ceil(len(AllAreaLootIDs[i])/BoxestoRandomizePerMap[i])))
        if ItemsPerBox[i] > 7:
            ItemsPerBox[i] = 7
        else:
            ItemtoChestDifference = int(math.ceil(len(AllAreaLootIDs[i])/BoxestoRandomizePerMap[i])) * BoxestoRandomizePerMap[i] - len(AllAreaLootIDs[i])
            for j in range(0, ItemtoChestDifference):
                AllAreaLootIDs[i].append(random.choice(AllEquipIDs[i])) # fill the rest with a random loot item from the relevant equipment pool
            random.shuffle(AllAreaLootIDs[i])
    k = 0
    for i in range(0, len(TBoxFiles)):
        k = 0
        for l in range(0, len(TBoxFiles[i])):
            if TBoxFiles[i][l] != 0:
                with open(TBoxFiles[i][l], 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data["rows"]: # We want to double the gold per chest to compensate that we're not getting enemy drops
                        row["goldMin"] = 2 * row["goldMin"]
                        row["goldMax"] = 2 * row["goldMax"]
                    for row in data["rows"]:
                        if k > len(AllAreaLootIDs[i]): #If k ever exceeds the size of the loot ids we're shuffling, then we can stop going through the files
                            file.seek(0)
                            file.truncate()
                            json.dump(data, file, indent=2, ensure_ascii=False)
                            break
                        if row["$id"] not in InvalidTreasureBoxIDs:
                            for j in range(0, 8):
                                if row[f"itm{j+1}ID"] not in FinalPreciousIDs:
                                    row[f"itm{j+1}ID"] = 0
                                    row[f"itm{j+1}Num"] = 0
                                    row[f"itm{j+1}Per"] = 0 # don't know if this is used at all, but better safe than sorry
                            for h in range(0, ItemsPerBox[i]):
                                if row[f"itm{h+1}ID"] not in FinalPreciousIDs:
                                    row[f"itm{h+1}ID"] = AllAreaLootIDs[i][k]
                                    row[f"itm{h+1}Num"] = 1
                                    k = k + 1
                                elif ItemsPerBox[i] < 7: # should help ensure items get placed if there's extra room
                                        row["itm7ID"] = AllAreaLootIDs[i][k]
                                        row["itm7Num"] = 1
                                        k = k + 1
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
    if Options.RaceModeOption_Zohar.GetState(): 
        print("Shuffling in Zohar Fragments")
        ZoharFragmentHunt(TBoxFiles, BoxestoRandomizePerMap)
        
def ShyniniSaveUs(): # Just in case we don't get good blade field skills, we can rely on Shynini to always sell core crystals :D
    with open("./_internal/JsonOutputs/common/MNU_ShopNormal.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 6:
                row["DefItem7"] = 45011
                row["DefItem8"] = 45012
                row["DefItem9"] = 45013
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ShopRemovals(): # Removes the Expensive Core Crystal from the shop, as well as the shop deeds
    ShopDeedIDs = Helper.InclRange(25249, 25300)
    with open("./_internal/JsonOutputs/common/MNU_ShopNormal.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["PrivilegeItem"] in ShopDeedIDs:
                row["PrivilegeItem"] = 0
            if row["$id"] == 33:
                row["Addtem2"] = 0
                row["AddCondition2"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def MovespeedDeedChanges(): #Replaces all other deed effects with movespeed, makes the max movespeed bonus 250% instead of 25%
    DeedTypeIDValues = Helper.InclRange(1, 51)
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # Changes caption and name
        data = json.load(file)
        for row in data["rows"]:
            if row["Type"] in DeedTypeIDValues:
                row["Caption"] = 603 # Increases running speed by 5%
    with open("./_internal/JsonOutputs/common/FLD_OwnerBonus.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in DeedTypeIDValues:
                row["Value"] = 5
                row["Type"] = 1
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_OwnerBonusParam.json", 'r+', encoding='utf-8') as file: # Changes max movespeed bonus to 250%
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1:
                row["Max"] = 150
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # Changes name of deed
        data = json.load(file)
        for row in data["rows"]:
            if (row["$id"] >= 25249) & (row["$id"] <= 25299):
                row["Caption"] = 603
            if row["$id"] > 25299:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for row in data["rows"]:
            if (row["$id"] >= 491) & (row["$id"] < 542):
                row["name"] = "Movespeed Deed"
            if row["$id"] == 542:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def PickupRadiusDeedStart(): # Start with a Pickup Radius Up Deed, to account for items falling in gaps between chests and walls and despawning.
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # Changes caption and name
        data = json.load(file)
        for row in data["rows"]:
            if row["Type"] == 52: # Adding 1 Custom Deed to increase pickup range, due to some issues where loot would drop from a chest that ended up stuck behind it with no way to pick it up before the loot despawned.
                row["Caption"] = 612 # Increases item drop collection range by 150cm
    with open("./_internal/JsonOutputs/common/FLD_OwnerBonus.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 52:
                row["Value"] = 150
                row["Type"] = 10
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # Changes name of deed
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 25300:
                row["Caption"] = 612
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 542:
                row["name"] = "Pickup Radius Deed"
            if row["$id"] == 612:
                row["name"] = "Increases item drop collection\nrange by 150cm."
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)        

def DLCItemChanges(): # Changes all DLC gifts to 1 gold except for poppy crystals
    DLCIDRowsWithItems = Helper.InclRange(1,7) + [9, 10] + Helper.InclRange(16, 21) + [23,24] + [30] + [36, 37] + Helper.InclRange(43, 55)
    with open("./_internal/JsonOutputs/common/MNU_DlcGift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in DLCIDRowsWithItems:
                row["item_id"] = 0
                row["category"] = 2
                row["value"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def DifficultyChanges(): # Makes Easy difficulty the same as Normal
    with open("./_internal/JsonOutputs/common/BTL_DifSetting.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for row in data["rows"]:
            row["Easy"] = row["Normal"]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def SeedHash():
    seedhashcomplete = random.choice(SeedHashAdj) + " " + random.choice(SeedHashNoun) 
    with open("./_internal/JsonOutputs/common_ms/menu_ms.json", 'r+', encoding='utf-8') as file: #puts the seed hash text on the main menu and on the save game screen
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 128:
                row["name"] = f"Seed Hash: {seedhashcomplete}"
                row["style"] = 166
            if row["$id"] == 129:
                row["name"] = "Race Mode Start"
            if row["$id"] == 1644:
                row["name"] = f"{seedhashcomplete}"
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    # DebugLog.AppendSeedHash(seedhashcomplete)
    
def ReduceBladeReqTrustVals(): # Sets required Trust Values to 0.5x the vanilla values
    with open("./_internal/JsonOutputs/common/FLD_ConditionIdea.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            row["TrustPoint"] = int(0.5 * row["TrustPoint"])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def SecondSkillTreeCostReduc(): # Reduces the cost of the hidden driver skill tree by 80% for race mode
    FilePaths = ["./_internal/JsonOutputs/common/BTL_Skill_Dr_Table01.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table02.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table03.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table04.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table05.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table06.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table17.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table18.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table19.json"]
    for i in range(0, len(FilePaths)):
        with open(FilePaths[i], 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] > 15:
                    row["NeedSp"] = int(row["NeedSp"] / 5)
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def EnemyDropRemoval(): # Removes all enemy drops, to avoid getting powerful equipment out of logic.
    for i in range(1, 9):
        Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_EnDropItem.json", [f"ItemID{i}", f"DropProb{i}", f"NoGetByEnh{i}", f"FirstNamed{i}"] , 0)

def ZoharFragmentHunt(TBoxFiles, BoxestoRandomizePerMap): # Experimental Mode to make players go out and find chests.
    ZoharFragPreciousIDs = [25135, 25136, 25137, 25138] # for now fixed at 4, but if we change # of race mode dungeons or give the player that option, will need to change this
    FragmentNameIDs = [191, 192, 193, 194]
    CaptionIDs = [197, 199, 201, 206]
    NumberofFragsPerArea = [0] * len(TBoxFiles)
    for i in range(0, len(TBoxFiles)): #variable number of fragments per map, depending on the number of chests available in the area
        NumberofFragsPerArea[i] = int(BoxestoRandomizePerMap[i] // 10)
        if NumberofFragsPerArea[i] < 3:
            NumberofFragsPerArea[i] = 3
        if NumberofFragsPerArea[i] > 6:
            NumberofFragsPerArea[i] = 6
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # makes them stackable
        data = json.load(file)
        for i in range(0, len(TBoxFiles)):
            for row in data["rows"]:
                if row["$id"] == ZoharFragPreciousIDs[i]:
                    row["ValueMax"] = 99
                    row["ClearNewGame"] = 0
                    row["Name"] = FragmentNameIDs[i]
                    row["Caption"] = CaptionIDs[i]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    NameTexts = ["[System:Color name=tutorial]Zohar Fragment A[/System:Color]", "[System:Color name=tutorial]Zohar Fragment B[/System:Color]", "[System:Color name=tutorial]Zohar Fragment C[/System:Color]", "[System:Color name=tutorial]Zohar Fragment D[/System:Color]"]
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # renaming the fragments in menus
        data = json.load(file)
        for i in range(0, len(TBoxFiles)):
            for row in data["rows"]:
                if row["$id"] == FragmentNameIDs[i]:
                    row["name"] = NameTexts[i]
                    break
        for i in range(0, len(TBoxFiles)):
            for row in data["rows"]:
                if row["$id"] == CaptionIDs[i]:
                    row["name"] = f"{NumberofFragsPerArea[i]} of these are needed to\nprogress to the next area."
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    QuestCollectIDs = [27, 50, 68, 69]
    with open("./_internal/JsonOutputs/common/FLD_QuestCollect.json", 'r+', encoding='utf-8') as file: # Making Quest Collect Entries for each of them
        data = json.load(file)
        for i in range(0, len(TBoxFiles)):
            for row in data["rows"]:
                if row["$id"] == QuestCollectIDs[i]:
                    row["Refer"] = 4
                    row["Count"] = NumberofFragsPerArea[i]
                    row["Deduct"] = 0
                    row["ItemID"] = 25135 + i
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)   
    LastQuestPurposeIDs = [48, 78, 121, 130, 155, 171, 184, 203, 218]
    IDNumbers = Helper.InclRange(278, 281)
    with open("./_internal/JsonOutputs/common/FLD_QuestTask.json", 'r+', encoding='utf-8') as file: # Adding the Quest Requirement to the final quest of the area
        data = json.load(file)
        for i in range(0, len(ChosenIndices) - 1):
            for row in data["rows"]:
                if row["$id"] == LastQuestPurposeIDs[ChosenIndices[i]]:
                    row["TaskType2"] = 3
                    row["TaskID2"] = QuestCollectIDs[i]
                    row["TaskLog2"] = IDNumbers[i]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_quest.json", "r+", encoding='utf-8') as file: # the quest objective now says the name of the custom part
        AreaLetters = ["A", "B", "C", "D"]
        data = json.load(file)
        for i in range(0, len(IDNumbers)):
            data["rows"].append({"$id": IDNumbers[i], "style": 62, "name": f"Find {NumberofFragsPerArea[i]} Zohar Fragment {AreaLetters[i]}."})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    BlankstoShuffle = [0] * (len(ChosenIndices) - 1)
    PartstoShuffle = [0] * (len(ChosenIndices) - 1)
    for i in range(0, len(PartstoShuffle)):
        PartstoShuffle[i] = int(BoxestoRandomizePerMap[i] // 3) # 1/3rd of all chests have a Zohar Fragment
        if PartstoShuffle[i] < 5:
            PartstoShuffle[i] = 5
        BlankstoShuffle[i] = BoxestoRandomizePerMap[i] - PartstoShuffle[i]
    Area1ZoharLocations = [0] * BlankstoShuffle[0] + [25135] * PartstoShuffle[0]
    random.shuffle(Area1ZoharLocations)
    Area2ZoharLocations = [0] * BlankstoShuffle[1] + [25136] * PartstoShuffle[1]
    random.shuffle(Area2ZoharLocations)
    Area3ZoharLocations = [0] * BlankstoShuffle[2] + [25137] * PartstoShuffle[2]
    random.shuffle(Area3ZoharLocations)
    Area4ZoharLocations = [0] * BlankstoShuffle[3] + [25138] * PartstoShuffle[3]
    random.shuffle(Area4ZoharLocations)
    AllZoharLocations = [Area1ZoharLocations, Area2ZoharLocations, Area3ZoharLocations, Area4ZoharLocations]
    ACurBox = 0
    ZoharChestIDs = []
    for i in range(0, len(TBoxFiles)): # Shuffling the Zohar fragments into the treasure chests
        ACurBox = 0
        for l in range(0, len(TBoxFiles[i])):
            if TBoxFiles[i][l] != 0:
                with open(TBoxFiles[i][l], 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data["rows"]:
                        if row["$id"] not in InvalidTreasureBoxIDs:
                            if AllZoharLocations[i][ACurBox] != 0:
                                row["itm8ID"] = AllZoharLocations[i][ACurBox]
                                row["itm8Num"] = 1
                                ZoharChestIDs.append(row["$id"])
                            ACurBox = ACurBox + 1
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
    # DebugLog.DebugZoharLocations(ZoharChestIDs)

def DriverLvandSPFix():
    with open("./_internal/JsonOutputs/common/CHR_Dr.json", 'r+', encoding='utf-8') as file: # Maybe fixing XP dupe
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] <= 6:
                row["DefLv"] = 1
                row["DefLvType"] = 1
                row["DefWPType"] = 1
                row["DefWP"] = 0
                row["DefSPType"] = 0
                row["DefSP"] = 0
                row["DefAcce"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def StackableCoreCrystalsandKeyItems(): # Allows us to shuffle more than 1 copy of a key item or core crystal into the pool
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in Helper.InclRange(25218, 25222):
                row["ValueMax"] = 3
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def FindtheBladeNames():
    if Options.CustomCoreCrystalOption.GetState():
        ValidCrystalListIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
        CorrespondingBladeIDs = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/ITM_CrystalList.json",["$id"], ValidCrystalListIDs, "BladeID")
        CorrespondingBladeNameIDs = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/CHR_Bl.json", ["$id"], CorrespondingBladeIDs, "Name")
        CorrespondingBladeNames = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_ms/chr_bl_ms.json", ["$id"], CorrespondingBladeNameIDs, "name")
        # DebugLog.DebugCoreCrystalAddition(ValidCrystalListIDs, CorrespondingBladeNames)
        ITMCrystalAdditions(CorrespondingBladeNames, CorrespondingBladeIDs)

def ITMCrystalAdditions(BladeNames, CorrespondingBladeIDs):
    with open("./_internal/JsonOutputs/common_ms/itm_crystal.json", "r+", encoding='utf-8') as file:     
        IDNumbers = Helper.InclRange(16, 58)
        data = json.load(file)
        for i in range(0, len(IDNumbers)):
            data["rows"].append({"$id": IDNumbers[i], "style": 36, "name": f"{BladeNames[i]}\'s Core Crystal"})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            for i in range(0, len(CorrespondingBladeIDs)):
                if row["BladeID"] == CorrespondingBladeIDs[i]:
                    row["Name"] = IDNumbers[i]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def PouchItemCarryCapacityIncrease(): # Set the max carry capacity of pouch items to 10 for all items
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/ITM_FavoriteList.json", ["ValueMax"], 10)

def DriverArtUpgradeCostChange(): # to reduce the amount of time spent menuing, a single manual should be enough to upgrade an art to level 5
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP2"], 250)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP3"], 500)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP4"], 1000)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP5"], 2000)
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 25407:
                row["Type"] = 3750 # Changed the amount of WP it gives 
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
def BladeTreeMaxRewardChange(): # When a blade skill tree completes, rewards that I already add to the item pool get given to the player, so I just replace the rewards with nothing.
    with open("./_internal/JsonOutputs/common/FLD_QuestReward.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in Helper.InclRange(911, 931):
                row["ItemID1"] = 0
                row["ItemNumber1"] = 0
                row["ItemID2"] = 0
                row["ItemNumber2"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def LandmarkConditions(): # Makes Cliffs of Morytha and Spirit Crucible Elpys available on map if they're rolled as a race mode dungeon, we start with a second landmark unlocked in their area, but you can't open the menu to skip travel to it until you get a minimum scenario flag matching the area. 
    ExtraConditionIDs = []
    with open("./_internal/JsonOutputs/common/FLD_ConditionScenario.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        data["rows"].append({"$id": 322, "ScenarioMin": 1001, "ScenarioMax": 7018, "NotScenarioMin": 0, "NotScenarioMax": 0})
        data["rows"].append({"$id": 323, "ScenarioMin": 1001, "ScenarioMax": 7043, "NotScenarioMin": 0, "NotScenarioMax": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    ExtraConditionIDs.append(322)
    ExtraConditionIDs.append(323)
    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        ExtraScenarioIDs = [3903, 3904]
        for i in range(0, len(ExtraConditionIDs)):
            data["rows"].append({"$id": ExtraScenarioIDs[i], "Premise": 0, "ConditionType1": 1, "Condition1": ExtraConditionIDs[i], "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0 , "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    if ChosenIndices[2] == 6: # Spirit Crucible Chosen
        with open("./_internal/JsonOutputs/common_gmk/ma16a_FLD_LandmarkPop.json", 'r+', encoding='utf-8') as file: # Turning Canyon of Husks into a second Landmark that warps you to Spirit Crucible Entrance
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] == 1601:
                    row["menuPriority"] = 10
                if row["$id"] == 1609:
                    row["category"] = 0
                    row["MAPJUMPID"] = 168
                    row["menuPriority"] = 20
                    row["stoff_cndID"] = 3903 # only unlock if we have min scenario flag corresponding to reaching the area
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    if ChosenIndices[3] == 7: # Cliffs selected
        with open("./_internal/JsonOutputs/common_gmk/ma17a_FLD_LandmarkPop.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] == 1701:
                    row["menuPriority"] = 10
                if row["$id"] == 1706:
                    row["stoff_cndID"] = 3904 #only unlock if we have min scenario flag corresponding to reaching the area
                    row["menuPriority"] = 20
                    row["category"] = 0
                    row["MAPJUMPID"] = 175
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def WeaponChipShopPowerLevelIncrease(): # Common issue at start of run is first boss is a slog to fight if they're high level, so we want to give some chips around the average power level of the first area we're going to.
    with open("./_internal/JsonOutputs/common/MNU_ShopNormal.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 7:
                if ChosenIndices[0] == 0: # Gormott
                    row["DefItem1"] = 10003
                    row["DefItem2"] = 10011
                else: # Uraya
                    row["DefItem1"] = 10017
                    row["DefItem2"] = 10018
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ChestTypeMatching():  # Chest type matches Contents
    RaceModeOn = Options.RaceModeOption.GetState()
    ZoharFragOn = Options.RaceModeOption_Zohar.GetState()
    CoreCrystalRandoOn = Options.CustomCoreCrystalOption.GetState()
    ZoharFragItemIDs = [25135, 25136, 25137, 25138]
    CoreCrystalIDs = AllCoreCrystals
    MovespeedDeedIDs = Helper.InclRange(25249, 25300)
    RareItemIDs = [25305, 25450, 25408, 25218, 25219, 25220, 25221, 25222, 25407]
    ChestTierListIDs = [0, 0, 0, 0, 0]
    ChestTierListItemNames = ["","","","",""]
    ZoharFragChests = []
    CoreCrystalChests = []
    MovespeedDeedChests = []
    RareItemChests = []
    EquipmentGoldChests = []
    if RaceModeOn:
        if ZoharFragOn:
            ChestTierListIDs[0] = 3
            ChestTierListItemNames[0] = "[System:Color name=tutorial]Zohar Fragment[/System:Color]"
        if CoreCrystalRandoOn:
            ChestTierListIDs[1] = 5
            ChestTierListItemNames[1] = "Core Crystal"   
        ChestTierListIDs[2] = 2
        ChestTierListItemNames[2] = "Movespeed Deed"
        ChestTierListIDs[3] = 1
        ChestTierListIDs[4] = 4
        ChestTierListItemNames[3] = "Rare Item"
        ChestTierListItemNames[4] = "Equipment/Gold"        
        for i in range(0, len(ListTboxFiles)):
            with open(ListTboxFiles[i], 'r+', encoding='utf-8') as file: 
                data = json.load(file)
                for row in data["rows"]:
                    rowcatfound = False
                    if ZoharFragOn:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in ZoharFragItemIDs:
                                row["RSC_ID"] = ChestTierListIDs[0]
                                rowcatfound = True
                                ZoharFragChests.append(row["$id"])
                                break
                    if CoreCrystalRandoOn:
                        if not rowcatfound:
                            for j in range(1, 9):
                                if row[f"itm{j}ID"] in CoreCrystalIDs:
                                    row["RSC_ID"] = ChestTierListIDs[1]
                                    rowcatfound = True
                                    CoreCrystalChests.append(row["$id"])
                                    break
                    if not rowcatfound:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in MovespeedDeedIDs:
                                row["RSC_ID"] = ChestTierListIDs[2]
                                rowcatfound = True
                                MovespeedDeedChests.append(row["$id"])
                                break
                    if not rowcatfound:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in RareItemIDs:
                                row["RSC_ID"] = ChestTierListIDs[3]
                                rowcatfound = True
                                RareItemChests.append(row["$id"])
                                break
                    if not rowcatfound:
                        row["RSC_ID"] = ChestTierListIDs[4]
                        rowcatfound = True
                        EquipmentGoldChests.append(row["$id"])
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=2, ensure_ascii=False)
        for i in range(0, len(ValidTboxMapNames)):
            if ValidTboxMapNames[i] not in ListTboxFiles:
                with open(ValidTboxMapNames[i], 'r+', encoding='utf-8') as file: 
                    data = json.load(file)
                    for row in data["rows"]:
                        if row["RSC_ID"] in [1,2,3,4,5,6,8,9,11,12,13,14]:
                            row["RSC_ID"] = 11
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
        with open("./_internal/JsonOutputs/common_ms/fld_gmkname.json", 'r+', encoding='utf-8') as file:
            data = json.load(file)
            newgmkIDs = [154, 155, 156, 157, 158]
            for i in range(0, 5):
                data["rows"].append({"$id": newgmkIDs[i], "style": 36, "name": ChestTierListItemNames[i]})
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    else:
        ChestTierListIDs = [3,5,2,1,4,11]
        ChestTierListItemNames = ["Key Item/Quest Item", "Core Crystal", "Shop Deed", "Equipment", "Collection Materials", "Gold"]
        for i in range(0, len(ValidTboxMapNames)):
            with open(ValidTboxMapNames[i], 'r+', encoding='utf-8') as file: 
                data = json.load(file)
                for row in data["rows"]:
                    rowcatfound = False
                    for j in range(1, 9):
                        if (row[f"itm{j}ID"] in PreciousItems) and not (row[f"itm{j}ID"] in MovespeedDeedIDs):
                            row["RSC_ID"] = ChestTierListIDs[0]
                            rowcatfound = True
                            break
                    if not rowcatfound:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in CoreCrystalIDs:
                                row["RSC_ID"] = ChestTierListIDs[1]
                                rowcatfound = True
                                break
                    if not rowcatfound:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in MovespeedDeedIDs:
                                row["RSC_ID"] = ChestTierListIDs[2]
                                rowcatfound = True
                                break
                    if not rowcatfound:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in Accessories + WeaponChips + AuxCores + RefinedAuxCores:
                                row["RSC_ID"] = ChestTierListIDs[3]
                                rowcatfound = True
                                break
                    if not rowcatfound:
                        for j in range(1, 9):
                            if row[f"itm{j}ID"] in CollectionPointMaterials:
                                row["RSC_ID"] = ChestTierListIDs[4]
                                rowcatfound = True
                                break
                        if not rowcatfound:
                            row["RSC_ID"] = ChestTierListIDs[5]
                            rowcatfound = True
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=2, ensure_ascii=False)
        with open("./_internal/JsonOutputs/common_ms/fld_gmkname.json", 'r+', encoding='utf-8') as file:
            data = json.load(file)
            newgmkIDs = [154, 155, 156, 157, 158, 159]
            for i in range(0, len(newgmkIDs)):
                data["rows"].append({"$id": newgmkIDs[i], "style": 36, "name": ChestTierListItemNames[i]})
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/RSC_TboxList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            for i in range(0, len(ChestTierListItemNames)):
                if row["$id"] == ChestTierListIDs[i]:
                    row["MSG_ID"] = newgmkIDs[i]
            row["initWaitTimeRand"] = 0.1 # reduces wait time for chest down to 0.1 sec
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def HideMapAreas(ScenarioFlagLists): # Adding conditions for each area's map to be unlocked
    MapIDsforRaceModeAreas = [[4],[5],[6],[10],[7,8],[9],[11],[12,13],[14],[15]]
    with open("./_internal/JsonOutputs/common/FLD_ConditionScenario.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(ChosenIndices)):
            data["rows"].append({"$id": 324 + i, "ScenarioMin": ScenarioFlagLists[ChosenIndices[i]], "ScenarioMax": 10048, "NotScenarioMin": 0, "NotScenarioMax": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(ChosenIndices)):
            data["rows"].append({"$id": 3905 + i, "Premise": 0, "ConditionType1": 1, "Condition1": 324 + i, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_WorldMapCond.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] >= 4:
                for i in range(0, len(ChosenIndices)):
                    for j in range(0, len(MapIDsforRaceModeAreas[ChosenIndices[i]])):
                        if row["$id"] == MapIDsforRaceModeAreas[ChosenIndices[i]][j]:
                            row["cond1"] = 3905 + i
                            break
                if row["cond1"] <= 3000:
                    row["cond1"] = 3472   
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ScriptAdjustments(): # For individual script changes
    with open("./_internal/JsonOutputs/common/EVT_listBf.json", 'r+', encoding='utf-8') as file: # adjust story events, changing scenario flag
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10034: # this lets us start at the start of gormott but not have the broken objective pointer
                row["chgEdID"] = 0
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10036: # this lets us start at the start of gormott but not have the broken objective pointer
                row["nextID"] = 10034
                row["nextIDtheater"] = 10034
            if row["$id"] == 10189:
                row["linkID"] = 0
                row["envSeam"] = 0
            if row["$id"] == 10094: # script that causes Vandham to join is name chapt03 startid 5
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10096: #
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10107: # script for the second time Vandham joins
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10129: # script for when Vandham dies (fixes bug where Roc on Rex gets deleted when Vandham dies)
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10211: # script that removes morag
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10213: # script that readds morag
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10240: # need to hard code the chapter transition for indol and temperantia section because I break some stuff to make warping between continents work.
                row["scenarioFlag"] = 6001
                row["nextID"] = 10244
                row["nextIDtheater"] = 10244
                row["linkID"] = 0
            if row["$id"] == 10260: #removing script that removes morag
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10269: #removing script that removes morag
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10304:
                row["linkID"] = 0
            if row["$id"] == 10366: # need to hard code the leap between cliffs and land of morytha because I break some stuff to make warping between continents work.
                row["scenarioFlag"] = 8001
                row["nextID"] = 10369
                row["nextIDtheater"] = 10369
            if row["$id"] == 10370:
                row["scriptName"] = "chapt08"
                row["scriptStartId"] = 6
            if row["$id"] == 10371:
                row["scriptName"] = ""
                row["scriptStartId"] = 0
            if row["$id"] == 10411: # fix for world tree chapter 9 transition
                row["nextID"] = 10427
                row["nextIDtheater"] = 10427
                row["linkID"] = 0
                row["scenarioFlag"] = 9008
            if row["$id"] == 10451: # end of world tree
                row["linkID"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/EVT_listFev01.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in [30034, 30036]: # Removing more scripts that remove morag from party
                row["scriptName"] = ""
                row["scriptStartId"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def XPDownScaling(): # Scales the amount of XP per level and xp gained dramatically, to allow me to level the user up quickly
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2", "EnemyExp"], ['max(row[key] // 10,1)'])
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/FLD_QuestReward.json"], ["EXP"], ['max(row[key] // 10,1)'])
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common_gmk/ma02a_FLD_LandmarkPop.json"] + LandmarkFilestoTarget, ["getEXP"], ['max(row[key] // 10,1)'])

def GimmickAdjustments(): # removes requirements for specific gimmicks
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_MapGimmick.json", ["Condition"], 0)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_EffectPop.json", ["Condition", "QuestFlagMin", "QuestFlagMax"], 0)
