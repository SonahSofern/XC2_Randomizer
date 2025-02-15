import json, random, Options
def RandomizeFieldSkills(): # Make logic to have all skills in the game
    # Drivers
    with open("./_internal/JsonOutputs/common/CHR_Bl.json", 'r+', encoding='utf-8') as bladeFile:
        bladeData = json.load(bladeFile)
        
        # Base 
        BaseSkillPool = [17, 22, 38, 11, 3, 23, 20, 24, 21, 18, 25, 4, 19, 23, 2, 13, 18, 10, 19, 7, 14, 18, 6, 11, 2, 25, 11, 23, 20, 21, 12, 22, 16, 20, 16, 38, 7, 19, 19, 25, 24, 9, 24, 4, 38, 11, 9, 15, 22, 24, 15, 23, 38, 14, 18, 16, 3, 6, 25, 21, 9, 12, 6, 38, 18, 2, 25, 13, 19, 14, 22, 13, 21, 20, 5, 20, 3, 12, 17, 18, 14, 21, 2, 15, 14, 4, 19, 12, 18, 22, 16, 9, 23, 14, 20, 6, 10, 7, 25, 12, 24, 3, 13, 21, 5, 24, 7, 23, 4, 6, 9, 2, 7, 6, 7, 10, 4, 6, 9, 2, 3, 10, 4, 6, 9, 2, 7, 6, 7, 10, 11, 20, 23, 4, 19, 22, 10, 22, 14, 18, 6, 13, 21, 5, 14, 20, 6, 14, 20, 6, 10, 7, 25, 12, 24, 3, 4, 6, 9, 2, 7, 4, 6, 9, 2, 7, 2, 3, 10, 4, 6, 9, 11, 20, 23, 4, 6, 9, 2, 7, 4, 6, 9, 2, 7, 2, 3, 10, 4, 6, 9, 11, 20, 23, 14, 21, 10, 19, 7, 16, 9, 20, 5, 9, 21, 9, 19, 23, 6, 25, 24, 17, 2, 23, 4, 25, 19, 22, 18, 17, 2, 23]
        BaseGameBladeIDs = [1001,1002,1004,1005,1006,1007,1008,1009,1010,1011,1014,1015,1017,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1034,1035,1037,1038,1039,1040,1041,1043,1044,1045,1046,1047,1048,1049,1050,1073,1077,1104,1105,1106,1107,1108,1109,1110,1111]
        
        # Torna
        TornaSkillPool = [72, 58, 66, 68, 59, 65, 67, 60, 73, 70, 63, 69, 64, 71, 62, 61]
        TornaBladeIDs = [1124,1125,1126,1127,1128,1129,1130,1131,1132]

        InvalidBladeIDs = [1012, 1013, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1074, 1003, 1103, 1112, 1081, 1102, 1078, 1079, 1076, 1080, 1075, 1042, 1012, 1018, 1033, 1016, 1036, 1072, 1067, 1068, 1065, 1071, 1070, 1066, 1069, 1060, 1061, 1058, 1064, 1063, 1059, 1062, 1053, 1054, 1051, 1057, 1056, 1052, 1055]
        
        ShuffleQuestSkills = Options.BladeFieldSkillsOption_QuestSkills.GetState()
        QuestSkillPool = [74, 73, 31, 35, 46, 33,37,39,26,43,44,57,34,40,51,29,30,45,47,36,28,32,42,50,48,58,41,49]     

        # Carveouts to make sure the story is completeable
        KeepVanilla = {
            1001: ["FSkill1","FSkill2", "FSkill3"], # Pyra needs all her skills
            1008: ["FSkill2"], # Roc Miasma
            
        }
        Slots = ["FSkill1","FSkill2", "FSkill3"]
        
        if ShuffleQuestSkills: # Add in our quest skills
            BaseSkillPool.extend(QuestSkillPool) 
        
        
        for blade in bladeData["rows"]:     
            
            BladeId = blade["$id"]
            
            if BladeId in InvalidBladeIDs: # Ignore bad blades
                continue
               
            if BladeId in BaseGameBladeIDs: # Decide which pool Torna or Original Game
                Pool = BaseSkillPool
            elif BladeId in TornaBladeIDs:
                Pool = TornaSkillPool
                
            for slot in Slots:
                
                if not ShuffleQuestSkills and (blade[slot] in QuestSkillPool): # Keep unique skills on that blade
                    continue
                
                if (KeepVanilla.get(BladeId) and slot in KeepVanilla[BladeId]): # Ignore special blades to make sure story is completeable
                    continue
                  
                if blade[slot] == 0: # Only replace skillslots that have one (dagas needs this for his weak form)
                    continue
                  
                Skill = random.choice(Pool) # Choose and Set a skill
                Pool.remove(Skill)
                blade[slot] = Skill

        bladeFile.seek(0)
        bladeFile.truncate()
        json.dump(bladeData, bladeFile, indent=2, ensure_ascii=False)
    
    


# Match element of blade to element mastery

 #   GenStandardOption("Blade Field Skills", TabBlades, "Randomizes a Blade's field (green) skill tree", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("FSkill", 1, 3), BladeFieldSkills, BladeFieldSkills,[1001], IgnoreID_AND_Key=[[1005, "FSkill3"], [1008, "FSkill2"]])])
            # if blade["$id"] not in [1124,1125,1126,1127,1128,1129,1130,1131,1132]:
            #     for i in range(1,4):
            #         Skill = blade[f"FSkill{i}"]
            #         if Skill != 0:
            #             print(Skill, end=",")