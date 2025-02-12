import json, random
from BladeRandomization import Replacement2Original

# Lists of cosmetics to choose from
ValidDriverCosmetics = []
ValidBladeCosmetics = [] 
ValidArtificialBladeCosmetics = [] 

# List passed to gen the options 
CosmeticsList = []

# Types
Blade = 1
Driver = 2
ArtBlade = 3

# Character Numbers
Rex = "Rex"
Nia = "Nia"
Tora = "Tora"
Morag = "Morag"
Zeke = "Zeke"
Pyra = "Pyra"
Mythra = "Mythra"
Dromarch = "Dromarch"
Poppiα = "Poppiα"
PoppiQT = "PoppiQT"
PoppiQTπ = "PoppiQTπ"
Brighid = "Brighid"
Pandoria = "Pandoria"

class Cosmetic:
    def __init__(self, model: str, characterID: int, characterName:str, cosmeticName:str, type:int):
        self.model = model
        self.characterID = characterID
        self.characterName = characterName
        self.cosmeticName = cosmeticName
        if type == Driver:
            CosmeticsList.extend([self.cosmeticName, [lambda: ValidDriverCosmetics.append(self)]])
        elif type == Blade:
            CosmeticsList.extend([self.cosmeticName, [lambda: ValidBladeCosmetics.append(self)]])
        elif type == ArtBlade:
            CosmeticsList.extend([self.cosmeticName, [lambda: ValidArtificialBladeCosmetics.append(self)]])

# Blades
JadeOrchidBrighid = Cosmetic("bl/bl121001", 1009, Brighid, "Jade Orchid Brighid", Blade)
WaterLilyBrighid = Cosmetic("bl/bl111001", 1009, Brighid, "Water Lily Brighid", Blade)
CrimsonOrchidBrighid = Cosmetic("bl/bl101001", 1009, Brighid, "Crimson Orchid Brighid", Blade)
# DefaultBrighid = Cosmetic("bl/bl001001", 1009, Brighid, "Default Brighid", Blade)

MagicalPinkPandoria = Cosmetic("bl/bl120901", 1010, Pandoria, "Magical Pink Pandoria", Blade)
MermaidBluePandoria = Cosmetic("bl/bl100901", 1010, Pandoria, "Mermaid Blue Pandoria", Blade)
BeachDatePandoria = Cosmetic("bl/bl110901", 1010, Pandoria, "Beach Date Pandoria", Blade)
# DefaultPandoria = Cosmetic("bl/bl000901", 1010, Pandoria, "Default Pandoria", Blade)
ClearGlassesPandoria = Cosmetic("bl/bl000902", 1010, Pandoria, "Clear Glasses Pandoria", Blade)

ObsidianDromarch = Cosmetic("bl/bl120501", 1004, Dromarch, "Obsidian Dromarch", Blade)
SavageDromarch = Cosmetic("bl/bl100501", 1004, Dromarch, "Savage Dromarch", Blade)
# DefaultDromarch = Cosmetic("bl/bl000501", 1004, Dromarch, "Default Dromarch", Blade)

DevotedMarigoldNia = Cosmetic("bl/bl120403", 1011, Nia, "Devoted Marigold Nia", Blade)
SincerePrimroseNia = Cosmetic("bl/bl120402", 1011, Nia, "Sincere Primrose Nia", Blade)
LoyalBellflowerNia = Cosmetic("bl/bl120401", 1011, Nia, "Loyal Bellflower Nia", Blade)
# DefaultBladeNia = Cosmetic("bl/bl000401", 1011, Nia, "Default Nia", Blade)

CarbonMythra = Cosmetic("bl/bl120201", 1002, Mythra, "Carbon Mythra", Blade)
RadiantBeachMythra = Cosmetic("bl/bl110201", 1002, Mythra, "Radiant Beach Mythra", Blade)
PyraStyleMythra = Cosmetic("bl/bl100201", 1002, Mythra, "Pyra Style Mythra", Blade)
# DefaultMythra = Cosmetic("bl/bl000201", 1002, Mythra, "Default Mythra", Blade)

MythraStylePyra = Cosmetic("bl/bl100102", 1001, Pyra, "Mythra Style Pyra", Blade)
DisguisedPyra = Cosmetic("bl/bl100101", 1001, Pyra, "Disguised Pyra", Blade)
BlueSkyPyra = Cosmetic("bl/bl120101", 1001, Pyra, "Blue Sky Pyra", Blade)
ProSwimmerPyra = Cosmetic("bl/bl110101", 1001, Pyra, "Pro Swimmer Pyra", Blade)
# DefaultPyra = Cosmetic("bl/bl000101", 1001, Pyra, "Default Pyra", Blade)

# DefaultPoppiα = Cosmetic("bl/bl000601", 1005, Poppiα, "Default Poppiα", ArtBlade)
CornflowerPoppiα = Cosmetic("bl/bl120601", 1005, Poppiα, "Cornflower Poppi α", ArtBlade)
SwimLessonPoppiα = Cosmetic("bl/bl110601", 1005, Poppiα, "Swim Lesson Poppi α", ArtBlade)

# DefaultPoppiQT = Cosmetic("bl/bl000701", 1006, PoppiQT, "Default PoppiQT", ArtBlade)
AntiquePrincessPoppiQT = Cosmetic("bl/bl120701", 1006, PoppiQT, "Antique Princess QT", ArtBlade)

# DefaultPoppiQTπ = Cosmetic("bl/bl000801", 1007, PoppiQTπ, "Default PoppiQTπ", ArtBlade)
NanoOrangeQTπ = Cosmetic("bl/bl120801", 1007, PoppiQTπ, "Nano Orange QTπ", ArtBlade)

# Drivers
CloudSeaKingRex = Cosmetic("pc/pc120101", 1, Rex, "Cloud Sea King Rex", Driver)
CloudSeaSharkRex = Cosmetic("pc/pc110101", 1, Rex, "Cloud Sea Shark Rex", Driver)
PrototypeSuitRex = Cosmetic("pc/pc100101", 1, Rex, "Prototype Suit Rex", Driver)
MasterDriverRex = Cosmetic("pc/pc000103", 1, Rex, "Master Driver Rex", Driver)
HelmetedRex = Cosmetic("pc/pc000102", 1, Rex, "Helmeted Rex", Driver)
# DefaultRex = Cosmetic("pc/pc000101", 1, Rex, "Default Rex", Driver)

ObligatoryLeaveMorag = Cosmetic("pc/pc110601", 6, Morag, "Obligatory Leave Morag", Driver)
DressUniformMorag = Cosmetic("pc/pc100601", 6, Morag, "Dress Uniform Morag", Driver)
ScarletInquisitorMorag = Cosmetic("pc/pc120601", 6, Morag, "Scarlet Inquisitor Morag", Driver)
# DefaultMorag = Cosmetic("pc/pc000601", 6, Morag, "Default Morag", Driver)

SurfinatorZeke = Cosmetic("pc/pc110501", 3, Zeke, "Surfinator Zeke", Driver)
EmbercakeZeke = Cosmetic("pc/pc100501", 3, Zeke, "Embercake Zeke", Driver)
ShiningJusticeZeke = Cosmetic("pc/pc120501", 3, Zeke, "Shining Justice Zeke", Driver)
# DefaultZeke = Cosmetic("pc/pc000501", 3, Zeke, "Default Zeke", Driver)
HoodedZeke = Cosmetic("pc/pc000502", 3, Zeke, "Hooded Zeke", Driver)

BestGirlFanTora = Cosmetic("pc/pc110301", 4, Tora, "Best Girl Fan Tora", Driver)
BusterModeTora = Cosmetic("pc/pc100301", 4, Tora, "Buster Mode Tora", Driver)
SkullfacePunkTora = Cosmetic("pc/pc120301", 4, Tora, "Skullface Punk Tora", Driver)
# DefaultTora = Cosmetic("pc/pc000301", 4, Tora, "Default Tora", Driver)

FancySundressNia = Cosmetic("pc/pc110201", 2, Nia, "Fancy Sundress Nia", Driver)
CandyStripeNia = Cosmetic("pc/pc100201", 2, Nia, "Candy Stripe Nia", Driver)
BloodWitchNia = Cosmetic("pc/pc120201", 2, Nia, "Blood Witch Nia", Driver)
# DefaultDriverNia = Cosmetic("pc/pc000201", 2, Nia, "Default Nia", Driver)


def CosmeticPairs(nameData, itmData,odds, charKeyWord, cosmeticsList, optionDict):
    pairs = {}
    for Acc in itmData["rows"]:
        if (odds > random.randint(0,99)):
            cosm:Cosmetic = random.choice(cosmeticsList)
            
            # Keep pairing since we cant make more names
            if Acc["Name"] in pairs:
                cosm = pairs[Acc["Name"]]["cosm"]
            else:
                pairs[Acc["Name"]] = {"cosm": cosm}
            
            
            for _Acc in nameData["rows"]: # Set name
                if _Acc["$id"] == Acc["Name"]:
                    oldName = _Acc["name"]
                    oldNameList = oldName.split()
                    firstWord = oldNameList[0]
                    _Acc["name"] = f"{firstWord} {cosm.characterName}"  
                    # print(_Acc["name"])
                    break
                
            Acc["Model"] = cosm.model
            if optionDict["Blades"]["optionTypeVal"].get() and cosm.characterID in Replacement2Original:
                Acc[f"{charKeyWord}"] = Replacement2Original[cosm.characterID]
            else:
                Acc[f"{charKeyWord}"] = cosm.characterID
            
def Cosmetics(optionDict):
    # Slider
    odds = optionDict["Character Outfits"]["spinBoxVal"].get()
    
    # Drivers
    with open("./_internal/JsonOutputs/common/ITM_PcEquip.json", 'r+', encoding='utf-8') as file:
        with open("./_internal/JsonOutputs/common_ms/itm_pcequip.json", 'r+', encoding='utf-8') as nameFile:  
            eqData = json.load(file)
            accNameData = json.load(nameFile)
            
            CosmeticPairs(accNameData, eqData, odds, "Driver", ValidDriverCosmetics, optionDict)
            
            nameFile.seek(0)
            nameFile.truncate()
            json.dump(accNameData, nameFile, indent=2, ensure_ascii=False)
        file.seek(0)
        file.truncate()
        json.dump(eqData, file, indent=2, ensure_ascii=False)
        
    # Blades
    with open("./_internal/JsonOutputs/common/ITM_OrbEquip.json", 'r+', encoding='utf-8') as orbFile:
        with open("./_internal/JsonOutputs/common_ms/itm_orb.json", 'r+', encoding='utf-8') as nameFile:
            orbData = json.load(orbFile)
            nameData = json.load(nameFile)
            
            CosmeticPairs(nameData,orbData,odds,"Blade", ValidBladeCosmetics, optionDict)
            
            nameFile.seek(0)
            nameFile.truncate()
            json.dump(nameData, nameFile, indent=2, ensure_ascii=False)
        orbFile.seek(0)
        orbFile.truncate()
        json.dump(orbData, orbFile, indent=2, ensure_ascii=False)
        
    # ArtificialBlades 
    with open("./_internal/JsonOutputs/common/ITM_HanaAssist.json", 'r+', encoding='utf-8') as file:
        eqData = json.load(file)
        for Acc in eqData["rows"]:
            if (odds > random.randint(0,99)):
                cosm:Cosmetic = random.choice(ValidArtificialBladeCosmetics) # these names are shared with regular ones so its not going to work to put poppi names on them when most cant equip those anyway
                Acc["Model"] = cosm.model
                if optionDict["Blades"]["optionTypeVal"].get() and cosm.characterID in Replacement2Original:
                    Acc["Blade"] = Replacement2Original[cosm.characterID]
                else:
                    Acc["Blade"] = cosm.characterID
        file.seek(0)
        file.truncate()
        json.dump(eqData, file, indent=2, ensure_ascii=False)
        
    # Clear globals
    ValidDriverCosmetics.clear()
    ValidBladeCosmetics.clear()
    ValidArtificialBladeCosmetics.clear()
