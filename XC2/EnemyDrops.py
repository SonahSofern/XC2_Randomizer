import Options, IDs, json, random
from scripts import Helper
def RandoEnemyDrops():
    ValidReplacements = []
    if Options.EnemyDropOption_Accessories.GetState():
        ValidReplacements.append(IDs.Accessories)
    if Options.EnemyDropOption_TornaAccessories.GetState():
        ValidReplacements.append(IDs.TornaAccessories)
    if Options.EnemyDropOption_WeaponChips.GetState():
        ValidReplacements.append(IDs.WeaponChips)
    if Options.EnemyDropOption_AuxCores.GetState():
        ValidReplacements.append(IDs.AuxCores)
    if Options.EnemyDropOption_RefinedAuxCores.GetState():
        ValidReplacements.append(IDs.RefinedAuxCores)
    if Options.EnemyDropOption_CoreCrystals.GetState():
        ValidReplacements.append(IDs.CoreCrystals)
    if Options.EnemyDropOption_Deeds.GetState():
        ValidReplacements.append(IDs.Deeds)
    if Options.EnemyDropOption_CollectionPointMaterials.GetState():
        ValidReplacements.append(IDs.CollectionPointMaterials)
    odds = Options.EnemyDropOption.GetOdds()

    
    if ValidReplacements == []: # In case they dont select anything
        return
    


    with open(f"./_internal/JsonOutputs/common/BTL_EnDropItem.json", 'r+', encoding='utf-8') as enDropFile:
        enDropData = json.load(enDropFile)
        for drop in enDropData["rows"]:
            for i in range(1,9):
                if not Helper.OddsCheck(odds): # Check spinbox
                    continue
                if drop[f"ItemID{i}"] == 0: # Ignore empty spots in points
                    continue
                drop[f"ItemID{i}"] = random.choice(ValidReplacements) # Make our selection
        enDropFile.seek(0)
        enDropFile.truncate()
        json.dump(enDropData, enDropFile, indent=2, ensure_ascii=False)

# EnemyDropOption = Option("Enemy Drops", Enemies, "Randomizes enemy drops/loot", [lambda: JSONParser.ChangeJSONFile(["common/BTL_EnDropItem.json"], Helper.StartsWith("ItemID", 1, 8), AuxCores+ RefinedAuxCores + IDs.Accessories + WeaponChips, [])], _hasSpinBox = True)
