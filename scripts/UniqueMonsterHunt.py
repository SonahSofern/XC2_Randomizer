import json, random, Helper, IDs, EnemyRandoLogic, RaceMode, math

AllUniqueMonsterDefaultIDs = [611, 612, 705, 706, 707, 708, 709, 710, 711, 712, 713, 715, 736, 738, 808, 809, 810, 811, 812, 814, 815, 816, 817, 819, 890, 891, 892, 893, 894, 895, 896, 898, 899, 926, 929, 953, 954, 955, 957, 958, 1019, 1020, 1023, 1025, 1026, 1101, 1102, 1104, 1106, 1108, 1109, 1111, 1112, 1113, 1114, 1115, 1131, 1132, 1134, 1155, 1156, 1157, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1255, 1256, 1258, 1260, 1261, 1262, 1264, 1265, 1563, 1564, 1566, 1567, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1670, 1774, 1886]

# "Location": [Warp Cutscene, "chgEdID", Map Name, Map ID]
ContinentInfo = {"Gormott": [10035, 10036, "ma05a", 6], "Uraya": [10088, 10079, "ma07a", 9], "Mor Ardain": [10156, 10149, "ma08a", 10], "Leftheria": [10197, 10192, "ma15a", 14], "Temperantia": [10233, 10224, "ma10a", 11], "Tantal": [10270, 10367, "ma13a", 13], "Spirit Crucible": [10325, 10323, "ma16a", 15], "Cliffs of Morytha": [10351, 10345, "ma17a", 16], "Land of Morytha": [10368, 10361, "ma18a", 18], "World Tree": [10399, 10393, "ma20a", 20]}

TotalAreaPool = ["Gormott", "Uraya", "Mor Ardain", "Leftheria", "Temperantia", "Tantal", "Spirit Crucible", "Cliffs of Morytha", "Land of Morytha", "World Tree"]

# "Driver": ["scriptName", "scriptStartID"]
PartyMembersAddScripts = {"Tora": ["chapt02", 7], "Nia": ["chapt02", 9], "Morag": ["chapt05", 7], "Zeke": ["chapt06", 5]}

# Item ID 25489 is the Shop Token!

# TO DO
# all blades unlock skill tree levels by purchasing items in shops?
# need to add custom shops with deeds/other stuff for purchase in each area
# I can just start with all continents having 1 landmark on them, and then just allow the mapON condition to be dependent on the order.
# change font color of "Current Objective", and change it to something like "bounties remaining"

def UMHunt(OptionDictionary):
    if IDs.CurrentSliderOdds != 0:
        SetCount = IDs.CurrentSliderOdds
        ChosenAreaOrder = []
        if IDs.CurrentSliderOdds > 10: #really need to limit the spinbox instead
            SetCount = 10
        #ChosenAreaOrder.extend(["Cliffs of Morytha"])
        ChosenAreaOrder.extend(random.sample(TotalAreaPool, SetCount))
        PartyMemberstoAdd = PartyMemberAddition(SetCount, ChosenAreaOrder)
        AreaUMs, AllAreaMonsters = CustomEnemyRando(ChosenAreaOrder)
        EnemySets = ChosenEnemySets(SetCount, AreaUMs)
        WarpManagement(SetCount, ChosenAreaOrder, PartyMemberstoAdd, EnemySets)
        CHR_EnArrangeAdjustments(AllAreaMonsters, EnemySets, ChosenAreaOrder)
        LandmarkAdjustments(ChosenAreaOrder)
        NoUnintendedRewards(ChosenAreaOrder)
        SpiritCrucibleEntranceRemoval()
        UMRewardDropChanges()
        CoreCrystalIdentification(OptionDictionary)
        CustomShopSetup()
        Cleanup()
        UMHuntMenuTextChanges()

def WarpManagement(SetCount, ChosenAreaOrder, PartyMemberstoAdd, EnemySets): # Main function was getting a bit too cluttered
    EventSetup(SetCount, ChosenAreaOrder, PartyMemberstoAdd)
    EventChangeSetup(SetCount, ChosenAreaOrder)
    QuestListSetup(SetCount, ChosenAreaOrder)
    QuestTaskSetup(SetCount, ChosenAreaOrder, EnemySets)
    FieldQuestBattleSetup(SetCount, ChosenAreaOrder, EnemySets)
    FieldQuestTaskLogSetup(SetCount, ChosenAreaOrder, EnemySets)
    AddQuestConditions(SetCount, ChosenAreaOrder)

def Cleanup():
    with open("./_internal/JsonOutputs/common/FLD_QuestList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if (row["PRTQuestID"] != 0) and (row["$id"] >= 25):
                row["PRTQuestID"] = 6
            if row["$id"] == 15: # Talking to Spraine
                row["NextQuestA"] = 234
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/EVT_listBf.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10013:
                row["nextID"] = 10464
                row["scenarioFlag"] = 10009
                row["nextIDtheater"] = 10464
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def QuestListSetup(SetCount, ChosenAreaOrder): # Adjusting the quest list
    with open("./_internal/JsonOutputs/common/FLD_QuestList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, SetCount):
            if i != SetCount - 1:
                for row in data["rows"]:
                    if row["$id"] == 235 + i:
                        row["Talker"] = 1001
                        row["FlagCLD"] = 832 + i
                        row["PurposeID"] = 249 + i
                        row["CountCancel"] = 0
                        row["NextQuestA"] = row["$id"] + 1
                        row["CallEventA"] = ContinentInfo[ChosenAreaOrder[i+1]][0]
                        break
            else:
                for row in data["rows"]:
                    if row["$id"] == 235 + i:
                        row["Talker"] = 1001
                        row["FlagCLD"] = 832 + i
                        row["PurposeID"] = 249 + i
                        row["CountCancel"] = 0
                        row["NextQuestA"] = 30000
                        row["CallEventA"] = 10503
                        break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def EventSetup(SetCount, ChosenAreaOrder, PartyMemberstoAdd): # Adjusting the initial area warp events
    with open("./_internal/JsonOutputs/common/EVT_listBf.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10465:
                row["nextID"] = ContinentInfo[ChosenAreaOrder[0]][0]
                row["nextIDtheater"] = row["nextID"]
                break
        for i in range(0, SetCount):
            for row in data["rows"]:
                if row["$id"] == ContinentInfo[ChosenAreaOrder[i]][0]:
                    row["scenarioFlag"] = 10010 + i
                    row["chapID"] = 10
                    row["linkID"] = 0
                    row["nextID"] = 0
                    row["nextIDtheater"] = 0
                    if PartyMemberstoAdd[i] != 0:
                        row["scriptName"] = PartyMembersAddScripts[PartyMemberstoAdd[i]][0]
                        row["scriptStartId"] = PartyMembersAddScripts[PartyMemberstoAdd[i]][1]
                    else:
                        row["scriptName"] = ""
                        row["scriptStartId"] = 0
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def EventChangeSetup(SetCount, ChosenAreaOrder): # Adjusting the warp event endings that change scenario flags
    with open("./_internal/JsonOutputs/common/EVT_chgBf01.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, SetCount):
            for row in data["rows"]:
                if row["$id"] == ContinentInfo[ChosenAreaOrder[i]][1]:
                    row["id"] = 10010 + i
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def PartyMemberAddition(SetCount, ChosenAreaOrder): # Adds new party members
    ChosenPartyMemberOrder = []
    FirstPartyMember = []
    ChosenPartyMemberOrder.extend(random.sample(["Tora", "Zeke", "Nia", "Morag"], min(SetCount, 4)))
    FirstPartyMember.append(ChosenPartyMemberOrder[0]) # We want to guarantee getting 1 teammate minimum to start with
    ChosenPartyMemberOrder.pop(0)
    while len(ChosenPartyMemberOrder) < SetCount - 1:
        ChosenPartyMemberOrder.append(0)
    random.shuffle(ChosenPartyMemberOrder)
    FirstPartyMember.extend(ChosenPartyMemberOrder)
    RNGAdjustedChosenPartyMemberOrder = FirstPartyMember
    return RNGAdjustedChosenPartyMemberOrder

def QuestTaskSetup(SetCount, ChosenAreaOrder, EnemySets): # Adds the new quest tasks
    with open("./_internal/JsonOutputs/common/FLD_QuestTask.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, SetCount):
            if len(EnemySets[i]) == 4:
                data["rows"].append({"$id": 249 + i, "PreCondition": 0, "TaskType1": 1, "TaskID1": 777 + i*4, "Branch1": 0, "TaskLog1": 278 + i*4, "TaskUI1": 0, "TaskCondition1": 0, "TaskType2": 1, "TaskID2": 777 + i*4 + 1, "Branch2": 0, "TaskLog2": 278 + i*4 + 1, "TaskUI2": 0, "TaskCondition2": 0, "TaskType3": 1, "TaskID3": 777 + i*4 + 2, "Branch3": 0, "TaskLog3": 278 + i*4 + 2, "TaskUI3": 0, "TaskCondition3": 0, "TaskType4": 1, "TaskID4": 777 + i*4 + 3, "Branch4": 0, "TaskLog4": 278 + i*4 + 3, "TaskUI4": 0, "TaskCondition4": 0}) 
            else:
                data["rows"].append({"$id": 249 + i, "PreCondition": 0, "TaskType1": 1, "TaskID1": 777 + i*4, "Branch1": 0, "TaskLog1": 278 + i*4, "TaskUI1": 0, "TaskCondition1": 0, "TaskType2": 1, "TaskID2": 777 + i*4 + 1, "Branch2": 0, "TaskLog2": 278 + i*4 + 1, "TaskUI2": 0, "TaskCondition2": 0, "TaskType3": 1, "TaskID3": 777 + i*4 + 2, "Branch3": 0, "TaskLog3": 278 + i*4 + 2, "TaskUI3": 0, "TaskCondition3": 0, "TaskType4": 0, "TaskID4": 0, "Branch4": 0, "TaskLog4": 0, "TaskUI4": 0, "TaskCondition4": 0}) 
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def FieldQuestBattleSetup(SetCount, ChosenAreaOrder, EnemySets): # Adds new rows in FLD_QuestBattle accordingly
    with open("./_internal/JsonOutputs/common/FLD_QuestBattle.json", 'r+', encoding='utf-8') as file:
        LastRow = 777
        LastFlag = 795
        data = json.load(file)
        for i in range(0, SetCount):
            for j in range(0, len(EnemySets[i])):
                data["rows"].append({"$id": LastRow, "Refer": 1, "EnemyID": EnemySets[i][j], "EnemyGroupID": 0, "EnemySpeciesID": 0, "EnemyRaceID": 0, "Count": 1, "CountFlag": LastFlag, "DeadAll": 0, "TimeCount": 0, "TimeCountFlag": 0, "ReduceEnemyHP": 0, "ReducePCHP": 0, "TargetOff": 0}) 
                LastRow = LastRow + 1
                LastFlag = LastFlag + 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def FieldQuestTaskLogSetup(SetCount, ChosenAreaOrder, EnemySets): # Adds the task logs for the field quests
    AllEnemySetNames = []
    AllEnemySetNameIDs = []
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: # add level scaling here
        data = json.load(file)
        for i in range(0, len(EnemySets)):
            CurrEnemySetNameIDs = []
            for j in range(0, len(EnemySets[i])):
                for row in data["rows"]:
                    if row["$id"] == EnemySets[i][j]:
                        CurrEnemySetNameIDs.append(row["Name"])
                        row["Lv"] = 5 + 10*i # Sets level of enemy equal to 5 min, then for each set after, the level goes up by 10 more
                        break
            AllEnemySetNameIDs.append(CurrEnemySetNameIDs)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_enemyname.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(EnemySets)):
            CurrEnemySetNames = []
            for j in range(0, len(EnemySets[i])):
                for row in data["rows"]:
                    if row["$id"] == AllEnemySetNameIDs[i][j]:
                        CurrEnemySetNames.append(row["name"])
                        break
            AllEnemySetNames.append(CurrEnemySetNames)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_quest.json", 'r+', encoding='utf-8') as file:
        StartRow = 278 # makes things easier to get the correct row
        data = json.load(file)
        for i in range(0, len(EnemySets)):
            for j in range(0, len(EnemySets[i])):
                data["rows"].append({"$id": StartRow, "style": 62, "name": f"Defeat [System:Color name=tutorial]{AllEnemySetNames[i][j]}[/System:Color]"})
                StartRow = StartRow + 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ChosenEnemySets(SetCount, AreaUMs): # Figuring out what enemies to turn into a set
    EnemySets = []
    for i in range(0, SetCount):
        if len(AreaUMs[i]) >= 4:
            EnemySets.append(random.sample(AreaUMs[i], 4))
        else:
            EnemySets.append(random.sample(AreaUMs[i], len(AreaUMs[i])))
    return EnemySets

def CustomEnemyRando(ChosenAreaOrder): # Custom shuffling of enemies
    AllAreaUMs = []
    AllAreaMonsters = []
    AllOriginalUMIDs = []
    ShuffledUniqueEnemyIDs = AllUniqueMonsterDefaultIDs.copy()
    random.shuffle(ShuffledUniqueEnemyIDs)
    for k in range(0, len(ChosenAreaOrder)):
        for i in range(0, len(IDs.ValidEnemyPopFileNames)):
            if ContinentInfo[ChosenAreaOrder[k]][2] in IDs.ValidEnemyPopFileNames[i]:
                CurrentAreaUMs = []
                CurrentAreaMonsters = []
                CurrentAreaOriginalUMIDs = []
                enemypopfile = "./_internal/JsonOutputs/common_gmk/" + IDs.ValidEnemyPopFileNames[i]
                with open(enemypopfile, 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data["rows"]:
                        if row["name"][:3] != "bos":
                            for j in range(0, len(ShuffledUniqueEnemyIDs)):
                                if row["ene1ID"] == AllUniqueMonsterDefaultIDs[j]: # only care about the first slot
                                    CurrentAreaOriginalUMIDs.append(row["ene1ID"])
                                    row["ene1ID"] = ShuffledUniqueEnemyIDs[j]
                                    row["Condition"] = row["ScenarioFlagMax"] = row["ScenarioFlagMin"] = row["QuestFlag"] = row["QuestFlagMin"] = row["QuestFlagMax"] = row["muteki_QuestFlag"] = row["muteki_QuestFlagMin"] = row["muteki_QuestFlagMax"] = row["muteki_Condition"] = 0
                                    row["POP_TIME"] = 256
                                    row["popWeather"] = 255
                                    CurrentAreaUMs.append(row["ene1ID"])
                                    break
                        CurrentAreaMonsters.extend([row["ene1ID"], row["ene2ID"], row["ene3ID"], row["ene4ID"]])
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
                CurrentAreaMonsters = [x for x in CurrentAreaMonsters if x != 0]
                CurrentAreaMonsters = list(set(CurrentAreaMonsters))
                AllOriginalUMIDs.append(CurrentAreaOriginalUMIDs)
                AllAreaUMs.append(CurrentAreaUMs)
                AllAreaMonsters.append(CurrentAreaMonsters)
    EnemyRandoLogic.FlyingEnemyFix(AllOriginalUMIDs, AllAreaUMs)
    EnemyRandoLogic.SwimmingEnemyFix(AllOriginalUMIDs, AllAreaUMs)
    EnemyRandoLogic.FishFix()
    EnemyRandoLogic.BigEnemyCollisionFix()
    EnemyRandoLogic.SummonsLevelAdjustment()
    return AllAreaUMs, AllAreaMonsters
    
def CHR_EnArrangeAdjustments(AllAreaMonsters, EnemySets, ChosenAreaOrder): # adjusts aggro + drops of all enemies
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["ExpRev", "GoldRev", "WPRev", "SPRev", "DropTableID", "DropTableID2", "DropTableID3", "PreciousID"], 0)         
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(AllAreaMonsters)):
            for row in data["rows"]:
                if row["$id"] in AllAreaMonsters[i]:
                    row["Lv"] = 5 + 12*i # Sets level of enemy equal to 5 min, then for each set after, the level goes up by 12 more, so eventually the enemies outscale you
        for i in range(0, len(EnemySets)):
            for j in range(0, len(EnemySets[i])):
                for row in data["rows"]:
                    if row["$id"] == EnemySets[i][j]:
                        row["PreciousID"] = 25479 + i
                        row["ZoneID"] = ContinentInfo[ChosenAreaOrder[i]][3]
                        break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def LandmarkAdjustments(ChosenAreaOrder): # removes xp and sp gains from landmarks, except for the first one
    for i in range(0, len(ChosenAreaOrder)):
        landmarkpopfile = "./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_LandmarkPop.json"
        with open(landmarkpopfile, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                row["getEXP"] = 0
                row["getSP"] = 0
                row["developZone"] = 0
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def AddQuestConditions(SetCount, ChosenAreaOrder): # Adding conditions for each area's warp to be unlocked + 1 to allow me to disable all other stuff (salvage points are the big one atm)
    # First, need to replace any conditions
    with open("./_internal/JsonOutputs/common/FLD_ConditionScenario.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["ScenarioMax"] > 10009:
                row["ScenarioMax"] = 10009
            if row["NotScenarioMin"] < 10009:
                row["NotScenarioMin"] = 10009
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    for i in range(0, len(ChosenAreaOrder)):
        eventpopfile = "./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_EventPop.json"
        with open(eventpopfile, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                if row["ScenarioFlagMax"] > 10009:
                    row["ScenarioFlagMax"] = 10009
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    # Condition 3903 Disables Stuff when applied to it.
    with open("./_internal/JsonOutputs/common/FLD_ConditionScenario.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["rows"].append({"$id": 322, "ScenarioMin": 1001, "ScenarioMax": 1002, "NotScenarioMin": 0, "NotScenarioMax": 0})
        for i in range(0, SetCount):
            data["rows"].append({"$id": 323 + i, "ScenarioMin": 10010 + i, "ScenarioMax": 10048, "NotScenarioMin": 0, "NotScenarioMax": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["rows"].append({"$id": 3903, "Premise": 0, "ConditionType1": 1, "Condition1": 322, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        for i in range(0, SetCount):
            data["rows"].append({"$id": 3904 + i, "Premise": 0, "ConditionType1": 1, "Condition1": 323 + i, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    OrderedMapIDs = []
    with open("./_internal/JsonOutputs/common/FLD_maplist.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(ChosenAreaOrder)):
            for row in data["rows"]:
                if row["select"] == ContinentInfo[ChosenAreaOrder[i]][2]:
                    OrderedMapIDs.append(row["$id"])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_WorldMapCond.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] <= len(ChosenAreaOrder):
                row["mapId"] = ContinentInfo[ChosenAreaOrder[row["$id"] - 1]][3]
                row["cond1"] = 3903 + row["$id"]
                row["pos1"] = row["$id"]
            elif row["$id"] == len(ChosenAreaOrder) + 1:
                row["mapId"] = 3
                row["cond1"] = 1
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_MapInfoFile.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] <= len(ChosenAreaOrder):
                row["file_name"] = ContinentInfo[ChosenAreaOrder[row["$id"] - 1]][2]
            else:
                row["file_name"] = ""
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)  

def NoUnintendedRewards(ChosenAreaOrder): # Removes any cheese you can do by doing sidequests, selling Collection Point items
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/FLD_QuestReward.json", ["Gold", "EXP", "Sp", "Coin", "DevelopZone", "DevelopPoint", "TrustPoint", "MercenariesPoint", "IdeaCategory", "IdeaValue", "ItemID1", "ItemNumber1", "ItemID2", "ItemNumber2", "ItemID3", "ItemNumber3", "ItemID4", "ItemNumber4"], 0) # doing quests don't reward you
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/ITM_CollectionList.json", ["Price"], 0) # collectables sell for 0
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_SalvagePointList.json", ["Condition"], 3903) # salvaging is disabled
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2", "EnemyExp"], ['252']) # It costs 252 xp to level up, regardless of level
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_GravePopList.json", ["en_popID"], 0) # Keeps you from respawning a UM.
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/ma02a_FLD_TboxPop.json", ["Condition"], 3903) # removes drops from chests in argentum
    for area in ChosenAreaOrder:
        Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/" + ContinentInfo[area][2] + "_FLD_TboxPop.json", ["Condition"], 3903) # removes drops from chests
   
def SpiritCrucibleEntranceRemoval(): # Exiting or Entering Spirit Crucible has problems with resetting the quest condition. So we remove that by warping the player back to the original landmark in that area.
    with open("./_internal/JsonOutputs/common_gmk/FLD_MapJump.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 3: # Leftherian Entrance to Spirit Crucible
                row["MapJumpId"] = 166 # get pranked lmao
            if row["$id"] == 4: # Spirit Crucible Entrance to Leftheria
                row["MapJumpId"] = 167 # get pranked lmao
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def UMHuntMenuTextChanges():
    seedhashcomplete = random.choice(IDs.SeedHashAdj) + " " + random.choice(IDs.SeedHashNoun) 
    with open("./_internal/JsonOutputs/common_ms/menu_ms.json", 'r+', encoding='utf-8') as file: #puts the seed hash text on the main menu and on the save game screen
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 128:
                row["name"] = f"Seed Hash: {seedhashcomplete}"
                row["style"] = 166
            if row["$id"] == 129:
                row["name"] = "[System:Color name=tutorial]Unique Monster Hunt[/System:Color]"
            if row["$id"] in [983, 1227]:
                row["name"] = "Bounties"
            if row["$id"] == 1644:
                row["name"] = f"{seedhashcomplete}"
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def UMRewardDropChanges(): #Changes text for the UM drops we want
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in Helper.InclRange(25479, 25489):
                row["ValueMax"] = 99
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for i in range(1, 11):
            for row in data["rows"]:
                if row["$id"] == 962 + i:
                    row["name"] = f"[System:Color name=green]Bounty Token Lv{i}[/System:Color]"
                if row["$id"] == 978 + i:
                    row["name"] = "Can be traded at the \nBounty Token Exchange for upgrades."
        for row in data["rows"]:
            if row["$id"] == 973:
                row["name"] = "[System:Color name=tutorial]Shop Token[/System:Color]"
            if row["$id"] == 989:
                row["name"] = "Can be traded at shops for upgrades."
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def IdentifyDLCBladeCrystals(CrystalList):
    DLCBladeCrystalList = []
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: # Adds the exchange tasks
        data = json.load(file)
        for i in range(0, len(CrystalList)):
            for row in data["rows"]:
                if (row["$id"] == CrystalList[i]) and (row["BladeID"] in [1105, 1106, 1107, 1108, 1109, 1111]):
                    DLCBladeCrystalList.append(row["$id"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    return DLCBladeCrystalList

def IdentifyClassBladeCrystals(CrystalList): # go from ITM_CrystalList $id->bladeID-> CHR_Bl $id->WeaponType-> ITM_PcWpnType $id->Role
    CrystalBladeIDList = []
    CrystalWeaponTypeIDList = []
    CrystalWeaponRoleList = []
    AttackerList = []
    HealerList = []
    TankList = []
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: # Getting BladeIDs for a Crystal $id
        data = json.load(file)
        for i in range(0, len(CrystalList)):
            for row in data["rows"]:
                if row["$id"] == CrystalList[i]:
                    CrystalBladeIDList.append(row["BladeID"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/CHR_Bl.json", 'r+', encoding='utf-8') as file: # Getting WeaponType for a Blade $id
        data = json.load(file)
        for i in range(0, len(CrystalBladeIDList)):
            for row in data["rows"]:
                if row["$id"] == CrystalBladeIDList[i]:
                    CrystalWeaponTypeIDList.append(row["WeaponType"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_PcWpnType.json", 'r+', encoding='utf-8') as file: # Getting Role for a WeaponType $id
        data = json.load(file)
        for i in range(0, len(CrystalWeaponTypeIDList)):
            for row in data["rows"]:
                if row["$id"] == CrystalWeaponTypeIDList[i]:
                    CrystalWeaponRoleList.append(row["Role"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    for i in range(0, len(CrystalList)):
        if CrystalWeaponRoleList[i] == 1: # Tank
            TankList.append(CrystalList[i])
        elif CrystalWeaponRoleList[i] == 2: # Attacker
            AttackerList.append(CrystalList[i])
        else: # Healer
            HealerList.append(CrystalList[i])
    return TankList, AttackerList, HealerList

def CoreCrystalIdentification(OptionsRunDict): # Figuring out the groups that each Core Crystal Belongs to, then picking items from each group for the shop
    ShuffleCoreCrystals()
    AllBladeCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    NGPlusBladeCrystalIDs = RaceMode.DetermineNGPlusBladeCrystalIDs(OptionsRunDict)
    RemainingBladeCrystalIDs = [x for x in AllBladeCrystalIDs if x not in NGPlusBladeCrystalIDs]
    DLCBladeCrystalIDs = IdentifyDLCBladeCrystals(RemainingBladeCrystalIDs)
    RemainingBladeCrystalIDs = [x for x in RemainingBladeCrystalIDs if x not in DLCBladeCrystalIDs]
    TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs = IdentifyClassBladeCrystals(RemainingBladeCrystalIDs)
    CoreCrystalGroupCreation(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs)

def ShuffleCoreCrystals(): # first we need to shuffle the blade ids into the core crystal pool
    AllBladeCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    BladeIDs = [1008, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1050, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1104, 1108, 1109, 1105, 1106, 1107, 1111]
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        RandomBlades = BladeIDs.copy()
        random.shuffle(RandomBlades)
        for i in range(0, len(AllBladeCrystalIDs)):
            for row in data["rows"]:
                if row["$id"] == AllBladeCrystalIDs[i]:
                    row["BladeID"] = RandomBlades[i]
                    row["ValueMax"] = 1
                    row["NoMultiple"] = i + 11
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def CoreCrystalGroupCreation(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs):
    Item1IDs, Item2IDs, Item3IDs, Item4IDs = [], [], Helper.ExtendListtoLength([], 16, "0"), Helper.ExtendListtoLength([], 16, "0")
    ChosenAtkBlades, ChosenTnkBlades, ChosenHlrBlades = random.sample(AttackerBladeCrystalIDs, min(8, len(AttackerBladeCrystalIDs))), random.sample(TankBladeCrystalIDs, min(6, len(TankBladeCrystalIDs))), random.sample(HealerBladeCrystalIDs, min(6, len(HealerBladeCrystalIDs)))
    ChosenAtkBlades = Helper.ExtendListtoLength(ChosenAtkBlades, 8 , "0")
    ChosenTnkBlades = Helper.ExtendListtoLength(ChosenTnkBlades, 6 , "0")
    ChosenHlrBlades = Helper.ExtendListtoLength(ChosenHlrBlades, 6 , "0")
    ChosenNGPlusBladeCrystalIDs = random.sample(NGPlusBladeCrystalIDs, min(3, len(NGPlusBladeCrystalIDs)))
    ChosenDLCBladeCrystalIDs = random.sample(DLCBladeCrystalIDs, min(3, len(DLCBladeCrystalIDs)))
    ChosenNGPlusBladeCrystalIDs = Helper.ExtendListtoLength(ChosenNGPlusBladeCrystalIDs, 3, "0")
    ChosenDLCBladeCrystalIDs = Helper.ExtendListtoLength(ChosenDLCBladeCrystalIDs, 3, "0")
    Item1IDs.extend(ChosenAtkBlades[:4])
    Item1IDs.extend(ChosenTnkBlades[:3])
    Item1IDs.extend(ChosenHlrBlades[:3])
    Item1IDs.extend(ChosenDLCBladeCrystalIDs[:3])
    Item1IDs.extend(ChosenNGPlusBladeCrystalIDs[:3])
    Item2IDs.extend(ChosenAtkBlades[-4:])
    Item2IDs.extend(ChosenTnkBlades[-3:])
    Item2IDs.extend(ChosenHlrBlades[-3:])
    Item2IDs = Helper.ExtendListtoLength(Item2IDs, 16, "0")
    global OutputCrystalGroupItemIDs
    OutputCrystalGroupItemIDs = [Item1IDs, Item2IDs, Item3IDs, Item4IDs]
    RenameCrystals(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs)
    # Output should be [16, 16, 16, 16] format, with last 2 entries being 0

def RenameCrystals(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs):    
    AllBladeCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/ITM_CrystalList.json", ["Condition", "CommonID", "CommonWPN", "CommonAtr", "Price", "RareTableProb", "RareBladeRev", "AssureP"], 0)
    with open("./_internal/JsonOutputs/common_ms/itm_crystal.json", "r+", encoding='utf-8') as file: # Now we want to rename crystals according to their category
        IDNumbers = Helper.InclRange(16, 20)
        CrystalCategoryNames = ["NG+ Core Crystal", "DLC Core Crystal", "TNK Core Crystal", "ATK Core Crystal", "HLR Core Crystal"]
        data = json.load(file)
        for i in range(0, len(IDNumbers)):
            data["rows"].append({"$id": IDNumbers[i], "style": 36, "name": CrystalCategoryNames[i]})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in NGPlusBladeCrystalIDs:
                row["Name"] = 16
            elif row["$id"] in DLCBladeCrystalIDs:
                row["Name"] = 17
            elif row["$id"] in TankBladeCrystalIDs:
                row["Name"] = 18
            elif row["$id"] in AttackerBladeCrystalIDs:
                row["Name"] = 19
            elif row["$id"] in HealerBladeCrystalIDs:
                row["Name"] = 20
            else:
                row["Name"] = 12
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def CustomShopSetup(): # Sets up the custom shops with loot
    # Sanity Checks: The number of items in InputTaskIDs should always be 16
    # The number of SetItem1IDs, RewardIDs, RewardNames, RewardSP, and RewardXP should all be the same, and also equal to the number of non-zero InputTaskIDs
    # Reward IDs, RewardQtys should have same number of values in each list as SetItem1IDs, however, each list should be made up of 4 lists, 1 for each item slot that a reward can be
    ArgentumShopNPCIDs = [2079, 2080, 2085, 2087, 2088, 2092, 2097, 2182, 2313, 2398]
    ArgentumShopEventIDs = [40045, 40054, 40051, 40048, 40052, 40056, 40050, 40058, 40055]
    OriginalShopIDs = [18, 17, 24, 21, 26, 13, 23, 16, 183, 28]
    OriginalShopNames = [9, 8, 16, 13, 17, 3, 15, 7, 188, 19]
    CoreCrystalCostDistribution = [1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 8, 10, 12, 25, 35, 45]
    TokenFillerList = Helper.ExtendListtoLength([], 10, "0") # This gets used so much, I'd rather not screw up typing it out, also by initializing it here, it doesn't calculate the value every time in the dictionary
    FullFillerList = Helper.ExtendListtoLength([], 16, "0") # Empty list of full size
    TokenExchangeShop = {
        "NPCID": 2079, # ma02a_FLD_NpcPop $id
        "ShopIcon": 420, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 18, # MNU_ShopList $id
        "ShopNametoReplace": 9, # fld_shopname $id
        "ShopEventID": 40045, # ma02a_FLD_NpcPop EventID
        "Name": "[System:Color name=green]Bounty Token[/System:Color] Exchange", # fld_shopname name
        "InputTaskIDs": Helper.ExtendListtoLength(Helper.InclRange(917, 926), 16, "0"), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([1,1], 8, "0"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.InclRange(25479, 25488), TokenFillerList, TokenFillerList, TokenFillerList, TokenFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [Helper.ExtendListtoLength([], 10, "1"), TokenFillerList, TokenFillerList, TokenFillerList, TokenFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1282, 1291), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": [Helper.ExtendListtoLength([], 10, "25489"), TokenFillerList, TokenFillerList, TokenFillerList], # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [[1,2,3,4,5,6,7,8,9,10], TokenFillerList, TokenFillerList, TokenFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["Shop Token", "Shop Token (x2)", "Shop Token (x3)", "Shop Token (x4)", "Shop Token (x5)", "Shop Token (x6)", "Shop Token (x7)", "Shop Token (x8)", "Shop Token (x9)", "Shop Token (x10)"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": [625, 1250, 1875, 2500, 3125, 3750, 4375, 5000, 5625, 6250], #FLD_QuestReward Sp
        "RewardXP": [630, 630, 630, 630, 630, 630, 630, 630, 630, 630] # FLD_QuestReward EXP
    }
    CoreCrystalShop = {
        "NPCID": 2080, # ma02a_FLD_NpcPop $id
        "ShopIcon": 427, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 17, # MNU_ShopList $id
        "ShopNametoReplace": 8, # fld_shopname $id
        "ShopEventID": 40054, # ma02a_FLD_NpcPop EventID
        "Name": "Core Crystal Cache", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(927, 942), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), FullFillerList, FullFillerList, FullFillerList, FullFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [CoreCrystalCostDistribution, FullFillerList, FullFillerList, FullFillerList, FullFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1292, 1307), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": OutputCrystalGroupItemIDs, # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [Helper.ExtendListtoLength([], 16, "1"), Helper.ExtendListtoLength([], 16, "1"), FullFillerList, FullFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["ATK Blade Bundle", "ATK Blade Bundle", "ATK Blade Bundle", "ATK Blade Bundle", "TNK Blade Bundle", "TNK Blade Bundle", "TNK Blade Bundle", "HLR Blade Bundle", "HLR Blade Bundle", "HLR Blade Bundle", "DLC Core Crystal", "DLC Core Crystal", "DLC Core Crystal", "NG+ Core Crystal", "NG+ Core Crystal", "NG+ Core Crystal"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": FullFillerList, #FLD_QuestReward Sp
        "RewardXP": FullFillerList # FLD_QuestReward EXP
    }

    ShopList = [TokenExchangeShop, CoreCrystalShop]
    with open("./_internal/JsonOutputs/common/MNU_ShopChange.json", 'r+', encoding='utf-8') as file: # Adds the exchange tasks
        data = json.load(file)
        ShopChangeStartRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChange.json", "$id") + 1 # used in MNU_ShopList for "TableID"
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChange.json", "$id") + 1
        for shop in ShopList:
            data["rows"].append({"$id": CurrRow, "DefTaskSet1": shop["InputTaskIDs"][0], "DefTaskSet2": shop["InputTaskIDs"][1], "DefTaskSet3": shop["InputTaskIDs"][2], "DefTaskSet4": shop["InputTaskIDs"][3], "DefTaskSet5": shop["InputTaskIDs"][4], "DefTaskSet6": shop["InputTaskIDs"][5], "DefTaskSet7": shop["InputTaskIDs"][6], "DefTaskSet8": shop["InputTaskIDs"][7], "AddTaskSet1": shop["InputTaskIDs"][8], "AddCondition1": shop["AddTaskConditions"][0], "AddTaskSet2": shop["InputTaskIDs"][9], "AddCondition2": shop["AddTaskConditions"][1], "AddTaskSet3": shop["InputTaskIDs"][10], "AddCondition3": shop["AddTaskConditions"][2], "AddTaskSet4": shop["InputTaskIDs"][11], "AddCondition4": shop["AddTaskConditions"][3], "AddTaskSet5": shop["InputTaskIDs"][12], "AddCondition5": shop["AddTaskConditions"][4], "AddTaskSet6": shop["InputTaskIDs"][13], "AddCondition6": shop["AddTaskConditions"][5], "AddTaskSet7": shop["InputTaskIDs"][14], "AddCondition7": shop["AddTaskConditions"][6], "AddTaskSet8": shop["InputTaskIDs"][15], "AddCondition8": shop["AddTaskConditions"][7], "LinkQuestTask": 0, "LinkQuestTaskID": 0, "UnitText": 0})
            CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_shopchange.json", 'r+', encoding='utf-8') as file: # Changes the reward name for the token shop
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopchange.json", "$id") + 1
        StartingShopChangeNameRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopchange.json", "$id") + 1 # Used in MNU_ShopChangeTask for "Name"
        for shop in ShopList:
            for reward in shop["RewardNames"]:
                data["rows"].append({"$id": CurrRow, "style": 36, "name": reward})
                CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_ShopChangeTask.json", 'r+', encoding='utf-8') as file: # Now we define what each task does
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChangeTask.json", "$id") + 1
        for shop in ShopList:
            for i in range(0, len(shop["SetItemIDs"][0])):
                data["rows"].append({"$id": CurrRow, "Name": StartingShopChangeNameRow, "SetItem1": shop["SetItemIDs"][0][i], "SetNumber1": shop["SetItemQtys"][0][i], "SetItem2": shop["SetItemIDs"][1][i], "SetNumber2": shop["SetItemQtys"][1][i], "SetItem3": shop["SetItemIDs"][2][i], "SetNumber3": shop["SetItemQtys"][2][i], "SetItem4": shop["SetItemIDs"][3][i], "SetNumber4": shop["SetItemQtys"][3][i], "SetItem5": shop["SetItemIDs"][4][i], "SetNumber5": shop["SetItemQtys"][4][i], "HideReward": 0, "Reward": shop["RewardIDs"][i], "HideRewardFlag": 0, "AddFlagValue": 0, "forcequit": 0, "IraCraftIndex": 0})
                CurrRow += 1
                StartingShopChangeNameRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_QuestReward.json", 'r+', encoding='utf-8') as file: # Sets the reward for each task
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_QuestReward.json", "$id") + 1
        for shop in ShopList:
            for i in range(0, len(shop["RewardIDs"])):
                data["rows"].append({"$id": CurrRow, "Gold": 0, "EXP": shop["RewardXP"][i], "Sp": shop["RewardSP"][i], "Coin": 0, "DevelopZone": 0, "DevelopPoint": 0, "TrustPoint": 0, "MercenariesPoint": 0, "IdeaCategory": 0, "IdeaValue": 0, "ItemID1": shop["RewardItemIDs"][0][i], "ItemNumber1": shop["RewardQtys"][0][i], "ItemID2": shop["RewardItemIDs"][1][i], "ItemNumber2": shop["RewardQtys"][1][i], "ItemID3": shop["RewardItemIDs"][2][i], "ItemNumber3": shop["RewardQtys"][2][i], "ItemID4": shop["RewardItemIDs"][3][i], "ItemNumber4": shop["RewardQtys"][3][i]})
                CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_shopname.json", 'r+', encoding='utf-8') as file: # Adds new shop name to list 
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopname.json", "$id") + 1
        ShopNameStartingRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopname.json", "$id") + 1 # used in MNU_ShopList for "Name"
        for i in range(0, len(ShopList)):
            data["rows"].append({"$id": CurrRow, "style": 70, "name": ShopList[i]["Name"]})
            CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_ShopList.json", 'r+', encoding='utf-8') as file: # Changes existing shop to match what we want
        data = json.load(file)
        for i in range(0, len(ShopList)):
            for row in data["rows"]:
                if row["$id"] == ShopList[i]["ShopIDtoReplace"]:
                    row["Name"] = ShopNameStartingRow
                    row["ShopIcon"] = ShopList[i]["ShopIcon"]
                    row["TableID"] = ShopChangeStartRow
                    row["Discount1"] = row["Discount2"] = row["Discount3"] = row["Discount4"] = row["Discount5"] = 0
                    row["ShopType"] = 1
                    ShopChangeStartRow += 1
                    ShopNameStartingRow += 1
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_gmk/ma02a_FLD_NpcPop.json", 'r+', encoding='utf-8') as file: # Lets you rest in the Argentum Trade Guild Inn, but removes all other shops (we're adding them back after)
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] != 2096: # keeps only the inn as a shop in Argentum
                row["ShopID"] = 0
                row["flag"]["Talkable"] = 0
                row["EventID"] = 0
        for i in range(0, len(ShopList)): # gives a specific npc the shop we want
            for row in data["rows"]:
                if row["$id"] == ShopList[i]["NPCID"]:
                    row["ScenarioFlagMin"] = row["QuestFlag"] = row["QuestFlagMin"] = row["QuestFlagMax"] = row["TimeRange"] = row["Condition"] = row["Mot"] = row["QuestID"] = 0
                    row["ScenarioFlagMax"] = 10048
                    row["flag"]["Talkable"] = 1
                    row["EventID"] = ShopList[i]["ShopEventID"]
                    row["ShopID"] = ShopList[i]["ShopIDtoReplace"]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
