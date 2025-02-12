import json, random
from Enhancements import *


def RandomizeAuxCoreEnhancements():
    InvalidSkillEnhancements = [ForcedHPPotionOnHit,ArtCancel,HpPotChanceFor2, EyeOfJustice, XStartBattle, YStartBattle, BStartBattle, EvadeDrainHp, EvadeDriverArt,ArtDamageHeal, BladeSwitchDamageUp]

    ValidSkills = [x for x in EnhanceClassList if x not in InvalidSkillEnhancements]

    with open("./_internal/JsonOutputs/common/ITM_OrbEquip.json", 'r+', encoding='utf-8') as file:
        with open("./_internal/JsonOutputs/common_ms/itm_orb.json", 'r+', encoding='utf-8') as auxNames:
            with open("./_internal/JsonOutputs/common/ITM_HanaAssist.json", 'r+', encoding='utf-8') as poppiAuxEnhancements:
                
                
                AuxCategory = 0
                poppiAux = json.load(poppiAuxEnhancements)
                enhanceFile = json.load(file)
                auxNameFile = json.load(auxNames)
                for Aux in enhanceFile["rows"]:
                    Aux["EnhanceCategory"] = AuxCategory # Stops the cannot equip same effect message
                    AuxCategory += 1
                    skillNameID = Aux["Name"]
                    enhancement = random.choice(ValidSkills)
                    enhancement.RollEnhancement()
                    # ValidSkills.remove(enhancement) # Need full pool to remove 
                    for skillName in auxNameFile["rows"]:  
                        if skillName["$id"] == skillNameID:    
                            skillName["name"] = f"{enhancement.name} Core"
                            break
                    Aux["Enhance"] = enhancement.id
                    Aux["Rarity"] = enhancement.Rarity
                    
                    
                poppiAuxEnhancements.seek(0)
                poppiAuxEnhancements.truncate()
                json.dump(poppiAux, poppiAuxEnhancements, indent=2, ensure_ascii=False)
            auxNames.seek(0)
            auxNames.truncate()
            json.dump(auxNameFile, auxNames, indent=2, ensure_ascii=False)
        file.seek(0)
        file.truncate()
        json.dump(enhanceFile, file, indent=2, ensure_ascii=False)
