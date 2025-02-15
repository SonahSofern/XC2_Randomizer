import json, random, Options
from Enhancements import *


def EnemyArts(spinbox):
    Arts = {
        "Skin Upgrade": 176,
        "Life Plant": 393,
        "Reset Punch": 50,
        "Element Breaker": 990,
        "Cold Era": 582
    }
    with open("./_internal/JsonOutputs/common/CHR_EnParam.json", 'r+', encoding='utf-8') as EnFile:
        EnData = json.load(EnFile) # Adds a single new art to enemies to art 16
        for en in EnData["rows"]:
            if spinbox < random.randrange(0,100): # Spinbox value check
                continue
            en["ArtsNum16"] = random.choice(list(Arts.values()))
        EnFile.seek(0)
        EnFile.truncate()
        json.dump(EnData, EnFile, indent=2, ensure_ascii=False)  


def EnemyArtAttributes():
    with open("./_internal/JsonOutputs/common/BTL_Arts_En.json", 'r+', encoding='utf-8') as EnArtsFile:
        with open("./_internal/JsonOutputs/common/BTL_Arts_BlSp.json", 'r+', encoding='utf-8') as EnBlArtsFile:
            with open("./_internal/JsonOutputs/common_ms/btl_arts_en_ms.json", 'r+', encoding='utf-8') as EnArtsNamesFile:  
                with open("./_internal/JsonOutputs/common_ms/btl_arts_blsp_ms.json", 'r+', encoding='utf-8') as EnBlArtsNamesFile:  
                    with open("./_internal/JsonOutputs/common_ms/btl_arts_bl_ms.json", 'r+', encoding='utf-8') as BlArtsNamesFile:  
                        with open("./_internal/JsonOutputs/common/BTL_Arts_Bl.json", 'r+', encoding='utf-8') as BlArtsFile:  
                            enArtsData = json.load(EnArtsFile)
                            enBlArtsData = json.load(EnBlArtsFile)
                            enArtsNameData = json.load(EnArtsNamesFile)
                            enBlArtsNameData = json.load(EnBlArtsNamesFile)
                            blArtNameData = json.load(BlArtsNamesFile)
                            blArtsData = json.load(BlArtsFile)
                            
                            ChangeArts(enArtsData, enArtsNameData)
                            ChangeArts(enBlArtsData, enBlArtsNameData)
                            # ChangeArts(blArtsData, blArtNameData, spinBox) # Currently this will change ally and enemy because they use the same files :/
                            
                            BlArtsFile.seek(0)
                            BlArtsFile.truncate()
                            json.dump(blArtsData, BlArtsFile, indent=2, ensure_ascii=False)  
                        BlArtsNamesFile.seek(0)
                        BlArtsNamesFile.truncate()
                        json.dump(blArtNameData, BlArtsNamesFile, indent=2, ensure_ascii=False)  
                    EnBlArtsNamesFile.seek(0)
                    EnBlArtsNamesFile.truncate()
                    json.dump(enBlArtsNameData, EnBlArtsNamesFile, indent=2, ensure_ascii=False)  
                EnArtsNamesFile.seek(0)
                EnArtsNamesFile.truncate()
                json.dump(enArtsNameData, EnArtsNamesFile, indent=2, ensure_ascii=False)  
            EnBlArtsFile.seek(0)
            EnBlArtsFile.truncate()
            json.dump(enBlArtsData, EnBlArtsFile, indent=2, ensure_ascii=False)
        EnArtsFile.seek(0)
        EnArtsFile.truncate()
        json.dump(enArtsData, EnArtsFile, indent=2, ensure_ascii=False)
        
def ChangeArts(artData, artNameData):
    newNameID = 457 # Starting id to add new names to old names file
    
    spinBox = Options.EnemyArtEffectsOption.GetOdds()
    isReactions = Options.EnemyArtEffectsOption_Reactions.GetState()
    isDebuffs = Options.EnemyArtEffectsOption_Debuffs.GetState()
    isBuffs = Options.EnemyArtEffectsOption_Buffs.GetState()
    isEnhancements = Options.EnemyArtEffectsOption_Enhancements.GetState()
    isAOE = Options.EnemyArtEffectsOption_AOE.GetState()
                    
    
    for art in artData["rows"]:
        
        # Needed to target only arts with no camera data because that corresponds with valid enemy blade arts 
        if art.get("Camera1") and art["Camera1"] != 0 and art["Camera2"] != 0 and art["Camera3"] != 0:
            continue

        # Spinbox value check
        if spinBox < random.randrange(0,100): 
            continue
        
         # Avoid changing autoattacks and things with no name
        if art["Name"] == 0:
            continue
        
         # Dont want to overwrite previous behaviour so check what i can change on an art
        validChanges = FindValidChanges(art, isReactions, isDebuffs, isBuffs, isEnhancements, isAOE) 
        
        # Make sure theres at least one valid change to make
        if not validChanges:
            continue
        newNameID += 1

        # choose a change to apply
        myChange = random.choice(validChanges) 
        newNamePrefix = myChange()
        
        # Get the old name 
        for name in artNameData["rows"]:
            if name["$id"] == art["Name"]:
                oldName = name["name"]
                break

        # create new name
        newName = { 
            "$id" : newNameID,
            "style" : 15,
            "name" : f"{newNamePrefix} {oldName}"
        }
        art["Name"] =  newNameID # Set new name id to the art
        artNameData["rows"].append(newName) # add newname
        
def FindValidChanges(art, isReactions, isDebuffs, isBuffs, isEnhancements, isAOE):
    ValidChanges = []
    if isDebuffs and art.get("ArtsDeBuff") != None and art["ArtsDeBuff"] in [0] and art["Target"] == 0: # Only change arts with no debuff and target enemies
        ValidChanges.append(lambda: Debuff(art))           # Debuff
    if isBuffs and art["ArtsBuff"] == 0: # Change arts that dont already do buff stuff (Current AOE is placed only on these things so gotta fix that)
        ValidChanges.append(lambda: Buff(art))
    if isEnhancements and art.get("Enhance") != None and art["Enhance"] == 0 and art["Target"] == 0 and art["ArtsType"] != 4: # Add enhancements only to arts without them and that target enemies
        ValidChanges.append(lambda: Enhancements(art))
    if isAOE and art["RangeType"] == 0 and art["ArtsType"] in [1,2,3]: # Make sure art is single target and a physical ether or healing move
        ValidChanges.append(lambda: AOE(art))
    if isReactions:
        for i in range(1,17): # Check that the art has at least one an empty hit to place a combo into
            if art[f"ReAct{i}"] == 0 and art[f"HitFrm{i}"] != 0:
                ValidChanges.append(lambda: Reaction(art))
                break
    return ValidChanges

ValidSkills = []
class EnemyArtEnhancements(Enhancement):
    def __init__(self, name, enhancement, para1 = [0,0,0,0],para2 = [0,0,0,0]):
        self.name = name
        self.EnhanceEffect = enhancement.EnhanceEffect
        self.Caption = 0
        self.addToList = False
        self.Param1 = para1
        self.Param2 = para2
        ValidSkills.append(self)
    
# backatk = EnemyArtEnhancements("Back↑", BackDamageUp, [40,60,80,100])
frontatk = EnemyArtEnhancements("Front↑", FrontDamageUp, [20,40,60,80])
pierce = EnemyArtEnhancements("Pierce", GuardAnnulAttack, [100,100,100,100])
# lowhpDamage = EnemyArtEnhancements("HP↓Dmg↑", DamageUpWhenHpDown, [10,20,30,40])
transmig = EnemyArtEnhancements("Flip", Transmigration, [100,100,100,100])
vamp = EnemyArtEnhancements("Vamp", ArtDamageHeal, [200,250,300,350])

def Enhancements(art):
    skill:Enhancement = random.choice(ValidSkills)
    skill.RollEnhancement()
    art["Enhance"] = skill.id
    return f"[System:Color name=green]{skill.name}[/System:Color]"

def AOE(art):
    CircleAroundTarget = 1
    ConeAhead = 2
    CircleAroundUser = 5
    RangeType = random.choice([CircleAroundTarget, ConeAhead, CircleAroundUser])
    RandomRadius = random.randrange(8,16)
    RandomLength = random.randrange(2,17,4)
    
    
    art["RangeType"] = RangeType
    art["Radius"] =  RandomRadius # Not sure what makes a good radius
    art["Length"] = RandomLength
    return f"[System:Color name=green]AOE[/System:Color]"


def Reaction(art):
    ValidReactions = {
        "Orb↓": [46],
        "BlCombo↓": [34,40,45],
        "Element": [17, 35],
        # "Elem Ref": [20], not satifying to deal with
    }
    Flames = {
        "Flames": [38], # Needs circle id 1-6
    }
    SelfTargetReactions = {
        "Enrage": [19,39,37], # Type 10 art or Range type 1, also make sure enemy actually has an enrage form
    }
    EnemyTargetReactions = {
        "Combo" : [1,2,3,4],
        "KB": [5,6,7,8,9],
        "BD": [10,11,12,13,14],
        "Aff↓": [21,22,23,24,25], 
    }
    
    if art["Target"] == 1:
        ValidReactions.update(SelfTargetReactions) # Add self targeting
    elif art["Target"] == 0:
        ValidReactions.update(EnemyTargetReactions) # Add enemy targeting
    if art.get("CircleID") and art["CircleID"] == 0 and art["Target"] == 0:
            ValidReactions.update(Flames) # Add flames 
        
    name,values = random.choice(list(ValidReactions.items()))
    
    # Special Cases that need more changes
    if name == "Flames":
        art["CircleID"] = 1
    elif name == "Combo":
        art["Flag"]["Fcombo"] = 1 # Forces combos to work even if out of order
        
        
    for i in range(1,17):
        if art[f"HitFrm{i}"] == 0: # Make sure there is a hit
            break
        if art[f"ReAct{i}"] != 0: # Make sure it doesnt already have a reaction 
            continue
        art[f"ReAct{i}"] =  random.choice(values)
    return f"[System:Color name=tutorial]{name}[/System:Color]"


def Buff(art):
    Buffs = {
        "Evade": 2,
        "Block": 3,
        "Counter": 6,
        "↑Counter": 7,
        "Rflct": 5,
        "Inv": 4,
        "Absorb":  17,
    }
    CD = {
        "CD↓": 0, # Special case its not really a buff but I dont want to give it its own category, I think it makes sense as a buff, this causes the problem that only arts with no buff can have their cd reduced which is fine maybe
    }
    
    if art.get("Recast") and art["Recast"] != 0:
        Buffs.update(CD)
    
    name,value = random.choice(list(Buffs.items()))
    if name == "CD↓": # Checks to be sure recast exists some dont have it
        art["Recast"] //= random.choice([2,4,6])
    elif name == "Loop":
        art["LoopNum"] = random.choice([1,1,1,1,2,2,2,3,3,4])
    else:
        art["ArtsBuff"] = value
    return f"[System:Color name=green]{name}[/System:Color]"

def Debuff(art): 
    Debuffs = {
        "Taunt" : 11,
        "Stench": 12,
        "NlHeal": 15,
        "Shackle": 14,
        "Def↓": 23,
        "EDef↓": 24,
        "Res↓": 25,
        # "Rage": 35, # We just resist rage strike?? even on BOC and enemy is enraged
        # "Fire": 33 Already have fire this might just be a different buff even though its only on brighids confining flames
    }
    SingleTarget = {
        "Shackle": 13,
        "Doom": 21,
    }
    if art["RangeType"] == 0: # Ensures single target
        Debuffs.update(SingleTarget)
    name,value = random.choice(list(Debuffs.items()))
    art["ArtsDeBuff"] = value
    return f"[System:Color name=red]{name}[/System:Color]"
    
