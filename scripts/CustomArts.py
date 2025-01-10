import json
import random
from IDs import Lv1ArtCDs, Lv1DamageRatios, EnhancementSets, ValidArtIDs, EvasionEnhancementIDs, SpecialEffectArtIDs, ArtDebuffs, AutoAttacks, ArtBuffs, HitReactions, HitReactionDistribution, OriginalAOECaptionIDs, ArtRandoCompleteness
import JSONParser
import Helper
import IDs

def DriverArtRando(OptionsRunDict): # We want custom descriptions for the driver arts, so we need to check the status of all options that affect it before randomizing. The last option that messes with the descriptions should also make the custom descriptions as well.
    if IDs.ArtRandoCompleteness == 0:
        DebuffRando = OptionsRunDict["Driver Art Debuffs"]["optionTypeVal"].get()
        ReactionRando = OptionsRunDict["Driver Art Reaction"]["optionTypeVal"].get()
        CooldownRando = OptionsRunDict["Driver Art Cooldowns"]["optionTypeVal"].get()
        DamageRatioRando = OptionsRunDict["Driver Art Damage Ratio"]["optionTypeVal"].get()
        EnhancementRando = OptionsRunDict["Driver Art Enhancements"]["optionTypeVal"].get()

        DebuffSliderOdds = OptionsRunDict["Driver Art Debuffs"]["spinBoxVal"].get()
        ReactionSliderOdds = OptionsRunDict["Driver Art Reaction"]["spinBoxVal"].get()

        ReplaceWithDebuffs = OptionsRunDict["Driver Art Debuffs"]["subOptionObjects"]["Debuffs"]["subOptionTypeVal"].get()
        ReplaceWithBuffs = OptionsRunDict["Driver Art Debuffs"]["subOptionObjects"]["Buffs"]["subOptionTypeVal"].get()
        ReplaceWithDoom = OptionsRunDict["Driver Art Debuffs"]["subOptionObjects"]["Doom"]["subOptionTypeVal"].get()
        ClearVanillaReactions = OptionsRunDict["Driver Art Reaction"]["subOptionObjects"]["Clear Vanilla Reactions"]["subOptionTypeVal"].get()

        if DebuffRando:
            ValidDebuffReplacements = []
            if ReplaceWithDebuffs:
                ValidDebuffReplacements.extend(list(set(ArtDebuffs)-set([21,35])))
            if ReplaceWithBuffs:
                ValidDebuffReplacements.extend(ArtBuffs)
            if ReplaceWithDoom:
                ValidDebuffReplacements.extend([21])
            ValidDebuffReplacements = list(set(ValidDebuffReplacements))
            ChangeJSONFileArtsRando(["common/BTL_Arts_Dr.json"], ["ArtsDeBuff"], ArtDebuffs, ValidDebuffReplacements, AutoAttacks, DebuffSliderOdds)
        if ReactionRando:
            if ClearVanillaReactions:
                Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", Helper.StartsWith("ReAct", 1,16), 0)    
            JSONParser.ChangeJSONFile(["common/BTL_Arts_Dr.json"], Helper.StartsWith("ReAct", 1,16), HitReactions, HitReactionDistribution, AutoAttacks, ReactionSliderOdds)
        if CooldownRando:
            RandomArtCooldowns()
        if DamageRatioRando:
            RandomArtDamageRatios()
        if EnhancementRando:
            RandomArtEnhancements()
        CustomArtDescriptionGenerator()
        IDs.ArtRandoCompleteness = 1

def RandomArtCooldowns(): # randomizes art cooldowns
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in ValidArtIDs:
                row["Recast1"] = random.choice(Lv1ArtCDs)
                for j in range(2, 7):
                    row[f"Recast{j}"] = row[f"Recast{j-1}"] - random.choice([0, 0, 0, 1, 1, 2])
                    if row[f"Recast{j}"] < 1:
                        row[f"Recast{j}"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def RandomArtDamageRatios(): # randomizes damage ratios
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in ValidArtIDs:
                row["DmgMgn1"] = random.choice(Lv1DamageRatios)
                for j in range(2, 7):
                    row[f"DmgMgn{j}"] = row[f"DmgMgn{j-1}"] + random.choice([20, 20, 30, 30, 30, 30, 30, 30, 40, 40, 40, 50, 50])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def RandomArtEnhancements(): # randomizes art enhancements
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in ValidArtIDs:
                if row["$id"] not in SpecialEffectArtIDs:
                    row["ArtsBuff"] = 0
                SelectedEnhancementList = random.choice(EnhancementSets)
                for j in range(1, 7):
                    row[f"Enhance{j}"] = SelectedEnhancementList[j-1]
                if row["Enhance1"] in EvasionEnhancementIDs: # Evasion Art Enhancement
                    row["ArtsBuff"] = 2
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ChangeJSONFileArtsRando(Filename, keyWords, rangeofValuesToReplace = [], rangeValidReplacements = [], InvalidTargetIDs = [], SliderOdds = 100, IgnoreID_AND_Key = [["",""]]):
    for name in Filename:
        filePath = "./_internal/JsonOutputs/" + name
        with open(filePath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for item in data['rows']:
                if not item["$id"] in InvalidTargetIDs:
                    for key in item:  
                        if ([item["$id"], key] not in IgnoreID_AND_Key):       
                            if key in keyWords:
                                if (((rangeofValuesToReplace == []) or (item[key] in rangeofValuesToReplace)) and (SliderOdds > random.randint(0,100))):
                                    item[key] = random.choice(rangeValidReplacements)
                            elif key == "Flag":
                                for flag, flagVal in item[key].items():
                                    if flag in keyWords:
                                        if ((flagVal in rangeofValuesToReplace) and (SliderOdds > random.randint(0,100))):
                                            item[key][flag] = random.choice(rangeValidReplacements)                                
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def CustomArtDescriptionGenerator(): # With all the changes to arts, we want custom descriptions for them
    RandomizedArtType = []
    RandomizedArtBuffs = []
    RandomizedArtDebuffs = []
    RandomizedArtReactions = []
    RandomizedArtEnhancements = []
    AOEofArt = []
    CurrentArtReactions = []
    CurrentArtDescription = ["", "", "", "", ""]
    TotalArtDescription = ""
    FirstDescriptionMod = -1
    LastDescriptionMod = -1
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", "r+", encoding='utf-8') as file:     
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in ValidArtIDs:
                RandomizedArtType.extend([row["ArtsType"]])
                RandomizedArtBuffs.extend([row["ArtsBuff"]])
                RandomizedArtDebuffs.extend([row["ArtsDeBuff"]])
                RandomizedArtEnhancements.extend([row["Enhance1"]])   
                for j in range(1, 17):
                    if row[f"ReAct{j}"] != 0:
                        CurrentArtReactions.extend([row[f"ReAct{j}"]])
                if CurrentArtReactions == []:
                    CurrentArtReactions = [0]
                RandomizedArtReactions.append(CurrentArtReactions)
                if row["Caption"] in OriginalAOECaptionIDs:
                    AOEofArt.extend([1])
                else:
                    AOEofArt.extend([0])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/btl_arts_dr_cap.json", "r+", encoding='utf-8') as file:     
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] <= 400:
                TotalArtDescription = ""
                CurrentArtDescription = ["", "", "", "", ""]
                if AOEofArt[row["$id"] - 1] == 1:
                    CurrentArtDescription[0] += "AOE"
                if RandomizedArtType[row["$id"] - 1] == 3:
                    CurrentArtDescription[1] += "Heal party"
                elif RandomizedArtType[row["$id"] - 1] == 11:
                    CurrentArtDescription[1] += "Defense"
                if RandomizedArtEnhancements[row["$id"] - 1] in [2830, 2835]:
                    CurrentArtDescription[2] += "Aggro Down"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2850, 2873]:
                    CurrentArtDescription[2] += "Aggro Up"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2795:
                    CurrentArtDescription[2] += "Aggroed↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2705:
                    CurrentArtDescription[2] += "Aquatic↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2760, 2755]:
                    CurrentArtDescription[2] += "Back atk↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2810:
                    CurrentArtDescription[2] += "Cancel atk↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2975:
                    CurrentArtDescription[2] += "Crit boost"  
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2840:
                    CurrentArtDescription[2] += "Crit recharge"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2866, 2872]:
                    CurrentArtDescription[2] += "Evasion"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2700:
                    CurrentArtDescription[2] += "Flying↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2740:
                    CurrentArtDescription[2] += "Front atk↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2735, 2878]:
                    CurrentArtDescription[2] += "Atk+Heal"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2845:
                    CurrentArtDescription[2] += "Atk+Heal Party"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2800, 2805]:
                    CurrentArtDescription[2] += "High HP↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2825:
                    CurrentArtDescription[2] += "-HP +Evasion"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2815, 2860]:
                    CurrentArtDescription[2] += "HP Potion"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2685:
                    CurrentArtDescription[2] += "Insects↑"                                                                                                                                        
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2780, 2775]:
                    CurrentArtDescription[2] += "Launched↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2790, 2785]:
                    CurrentArtDescription[2] += "Low HP↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2730, 2725]:
                    CurrentArtDescription[2] += "Machines↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2861:
                    CurrentArtDescription[2] += "Pierce"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2746, 2745, 2750]:
                    CurrentArtDescription[2] += "Side atk↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] in [2770, 2765]:
                    CurrentArtDescription[2] += "Toppled↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2680:
                    CurrentArtDescription[2] += "Beasts↑"
                elif RandomizedArtEnhancements[row["$id"] - 1] == 2715:
                    CurrentArtDescription[2] += "Humanoids↑"
                CurrentArtDescription[3] += "" # just for now, until the stuff gets merged to find the last hit of an art
                if RandomizedArtDebuffs[row["$id"] - 1] == 1:
                    CurrentArtDescription[4] += "Foe Crit Up"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 2:
                    CurrentArtDescription[4] += "Foe Acc Up"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 3:
                    CurrentArtDescription[4] += "Foe Art↑"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 4:
                    CurrentArtDescription[4] += "Foe CDs Down"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 5:
                    CurrentArtDescription[4] += "Foe HP Shield"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 6:
                    CurrentArtDescription[4] += "Foe Null React"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 7:
                    CurrentArtDescription[4] += "Foe -Debuff"                                                            
                elif RandomizedArtDebuffs[row["$id"] - 1] == 8:
                    CurrentArtDescription[4] += "Foe Back Atk↑"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 9:
                    CurrentArtDescription[4] += "Foe Draw Aggro"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 16:
                    CurrentArtDescription[4] += "Foe Armor↑"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 17:
                    CurrentArtDescription[4] += "Foe Atk↑"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 11:
                    CurrentArtDescription[4] += "Taunt"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 12:
                    CurrentArtDescription[4] += "Stench"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 13:
                    CurrentArtDescription[4] += "Shackle Driver"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 14:
                    CurrentArtDescription[4] += "Shackle Blade"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 15:
                    CurrentArtDescription[4] += "Null Heal"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 21:
                    CurrentArtDescription[4] += "Doom"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 23:
                    CurrentArtDescription[4] += "Phys Def Down"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 24:
                    CurrentArtDescription[4] += "Ether Def Down"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 25:
                    CurrentArtDescription[4] += "Res Down"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 30:
                    CurrentArtDescription[4] += "Freeze"
                elif RandomizedArtDebuffs[row["$id"] - 1] == 35:
                    CurrentArtDescription[4] += "Enrage"                 
                for i in range(0, len(CurrentArtDescription)):
                    if CurrentArtDescription[i] != "":
                        FirstDescriptionMod = i
                        break
                for i in range(len(CurrentArtDescription) - 1, 0, -1):
                    if CurrentArtDescription[i] != "":
                        LastDescriptionMod = i
                        break
                TotalArtDescription += CurrentArtDescription[FirstDescriptionMod]
                if FirstDescriptionMod != LastDescriptionMod:
                    for i in range(FirstDescriptionMod + 1, LastDescriptionMod + 1):
                        if CurrentArtDescription[i] != "":
                            TotalArtDescription += " / "
                            TotalArtDescription += CurrentArtDescription[i]
                row["name"] = TotalArtDescription
                row["style"] = 16
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", "r+", encoding='utf-8') as file:     
        data = json.load(file)
        for row in data["rows"]:
            for i in range(0, len(ValidArtIDs)):
                if row["$id"] == ValidArtIDs[i]:
                    row["Caption"] = i + 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)