from tkinter import ttk
import JSONParser, Helper
from IDs import *
from tkinter import *
import _Accessories, _DriverArts, SkillTrees, BladeRandomization, _AuxCores, IDs, _GreenSkills, _WeaponChips, EnemyRandoLogic, _EnemyEnhancements, _EnemyArts, MusicShuffling, TrustBeam, CoreCrystalAdjustments
import TutorialShortening, GachaModifications, FieldSkillAdjustments, Enhancements, BigItems, RaceMode, UniqueMonsterHunt, Cosmetics


# Prio
First = 0
Last = 100

class Option():
    def __init__(self, _name:str, _tab, _desc:str, _commands:list = [], _defState = False, _prio = 50, _hasSpinBox = False, _spinMin = 0, _spinMax = 100, _spinDesc = "% randomized", _spinWidth = 3, _spinIncr = 10):
        # Objects
        self.descObj = None
        self.spinBoxObj = None
        self.spinBoxLabel = None
        self.spinBoxVal = None
        self.checkBox = None
        self.checkBoxVal = None
        self.subOptions:list[SubOption] = []

        # Initial Data
        self.name =  _name
        self.tab = _tab
        self.desc = _desc
        self.hasSpinBox = _hasSpinBox
        self.commands:list = _commands
        self.subDefState = _defState
        self.prio = _prio
        OptionList.append(self)
        
        # Custom Spinboxes
        self.spinBoxMin = _spinMin
        self.spinBoxMax = _spinMax
        self.spinDesc = _spinDesc
        self.spinWidth = _spinWidth
        self.spinIncr = _spinIncr

    def DisplayOption(self, tab):
        self.GenStandardOption(tab)
        self.StateUpdate()
        
    def GenStandardOption(self, parentTab):    # This probably shouldnt be a class function what if we want to make a nonstandard option we could make a carveout and let you call a custom function but how would you set everything with a custom function
        # Variables
        global rowIncrement
        self.spinBoxVal = IntVar(value=100)
        self.checkBoxVal = BooleanVar()
        self.spinBoxObj = ttk.Label()
        self.spinBoxObj = ttk.Spinbox()

        # Parent Frame
        optionPanel = ttk.Frame(parentTab)
        optionPanel.grid(row = rowIncrement, column= 0, sticky="ew")
        
        # Major Option Checkbox
        self.checkBox = ttk.Checkbutton(optionPanel, variable= self.checkBoxVal, text=self.name, width=40, style="midColor.TCheckbutton", command=lambda: self.StateUpdate())
        self.checkBox.grid(row=rowIncrement, column=0, sticky="w")
        
        # Description Label
        self.descObj = ttk.Label(optionPanel, text=self.desc, anchor="w", width=60, wraplength=400)
        self.descObj.grid(row=rowIncrement, column=1, sticky="w", padx=0)
        
        # % Boxes
        if self.hasSpinBox:
            self.spinBoxObj = ttk.Spinbox(optionPanel, from_=self.spinBoxMin, to=self.spinBoxMax, textvariable=self.spinBoxVal, wrap=True, width=self.spinWidth, increment=self.spinIncr)
            self.spinBoxObj.grid(row=rowIncrement, column=2, padx=(15,0))
            self.spinBoxLabel = ttk.Label(optionPanel, text=self.spinDesc, anchor="w")
            self.spinBoxLabel.grid(row=rowIncrement, column=3, sticky="w", padx=0)

        for sub in self.subOptions:
            rowIncrement += 1
            sub.checkBoxVal = BooleanVar(value=sub.defState)
            sub.checkBox = ttk.Checkbutton(optionPanel, text=sub.name, variable=sub.checkBoxVal, width=30)
            sub.checkBox.grid(row=rowIncrement, column=0, sticky="sw")
        rowIncrement += 1

    
    def StateUpdate(self):
        if self.GetState():
            for sub in self.subOptions:
                sub.checkBox.state(["!disabled"])
            self.descObj.state(["!disabled"])
            self.spinBoxObj.state(["!disabled"])
            if self.spinBoxLabel != None: # If we dont have one
                self.spinBoxLabel.state(["!disabled"])
            for sub in self.subOptions: # Handles Dropdown
                sub.checkBox.grid()     
        else:
            for sub in self.subOptions:
                sub.checkBox.state(["disabled"])
            self.descObj.state(["disabled"])
            self.spinBoxObj.state(["disabled"])
            if self.spinBoxLabel != None:
                self.spinBoxLabel.state(["disabled"])
            for sub in self.subOptions: # Handles Dropdown
                sub.checkBox.grid_remove()
    
    def GetOdds(self):
        return self.spinBoxVal.get()
    
    def GetState(self):
        return self.checkBoxVal.get()

class SubOption():
    def __init__(self, _name, _parent:Option, _commands = [], _defState = True, _prio = 0):
        self.name = _name
        self.checkBoxVal = None
        self.checkBox:ttk.Checkbutton = None
        self.commands = _commands    
        self.defState = _defState
        self.prio = _prio
        self.parent = _parent
        _parent.subOptions.append(self)

    def GetState(self):
        return self.checkBoxVal.get()
rowIncrement = 0   
OptionList:list[Option] = []

General = 1
Driver  = 2
Blade = 3
Enemies = 4
Misce = 5
QOL = 6
Funny = 7
CosmeticsTab = 8
GameModeTab = 9

# General
AccessoryShopsOption = Option("Accessory Shops", General, "Randomizes the contents of Accessory Shops", [lambda: JSONParser.ChangeJSONFile(["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), list(set(Accessories)-set([1])),[])], _defState=True, _hasSpinBox = True)
AccessoryShopsOption_Accessories = SubOption("Accessories", AccessoryShopsOption, [lambda: ValidReplacements.extend(Accessories)])
AccessoryShopsOption_TornaAccessories = SubOption("Torna Accessories", AccessoryShopsOption, [lambda: ValidReplacements.extend(TornaAccessories)])
AccessoryShopsOption_WeaponChips = SubOption("Weapon Chips", AccessoryShopsOption, [lambda: ValidReplacements.extend(WeaponChips)])
AccessoryShopsOption_AuxCores = SubOption("Aux Cores", AccessoryShopsOption, [lambda: ValidReplacements.extend(AuxCores)])
AccessoryShopsOption_RefinedAuxCores = SubOption("Refined Aux Cores", AccessoryShopsOption, [lambda: ValidReplacements.extend(RefinedAuxCores)])
AccessoryShopsOption_CoreCrystals = SubOption("Core Crystals", AccessoryShopsOption, [lambda: ValidReplacements.extend(CoreCrystals)])
AccessoryShopsOption_Deeds = SubOption("Shop Deeds", AccessoryShopsOption, [lambda: ValidReplacements.extend(Deeds)])
AccessoryShopsOption_CollectionPointMaterials = SubOption("Collection Point Materials", AccessoryShopsOption, [lambda: ValidReplacements.extend(CollectionPointMaterials)])
AccessoryShopsOption_PouchItems = SubOption("Pouch Items", AccessoryShopsOption, [lambda: ValidReplacements.extend(PouchItems)])
CollectionPointsOption = Option("Collection Points", General, "Randomizes the contents of Collection Points", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_CollectionPopList.json", "common_gmk/"), ["itm1ID", "itm2ID", "itm3ID", "itm4ID"], list(set(CollectionPointMaterials) - set([30019])), [])], _defState=True, _hasSpinBox = True)
CollectionPointsOption_Accessories = SubOption("Accessories", CollectionPointsOption, [lambda: ValidReplacements.extend(Accessories)])
CollectionPointsOption_TornaAccessories = SubOption("Torna Accessories", CollectionPointsOption, [lambda: ValidReplacements.extend(TornaAccessories)])
CollectionPointsOption_WeaponChips = SubOption("Weapon Chips", CollectionPointsOption, [lambda: ValidReplacements.extend(WeaponChips)])
CollectionPointsOption_AuxCores = SubOption("Aux Cores", CollectionPointsOption, [lambda: ValidReplacements.extend(AuxCores)])
CollectionPointsOption_RefinedAuxCores = SubOption("Refined Aux Cores", CollectionPointsOption, [lambda: ValidReplacements.extend(RefinedAuxCores)])
CollectionPointsOption_CoreCrystals = SubOption("Core Crystals", CollectionPointsOption, [lambda: ValidReplacements.extend(CoreCrystals)])
CollectionPointsOption_Deeds = SubOption("Shop Deeds", CollectionPointsOption, [lambda: ValidReplacements.extend(Deeds)])
CollectionPointsOption_CollectionPointMaterials = SubOption("Collection Point Materials", CollectionPointsOption, [lambda: ValidReplacements.extend(CollectionPointMaterials)])
PouchItemShopOption = Option("Pouch Item Shops", General, "Randomizes the contents of Pouch Item Shops", [lambda: JSONParser.ChangeJSONFile(["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), list(set(PouchItems)-set([40007])), [])], _hasSpinBox = True)
PouchShopOption_Accessories = SubOption("Accessories", PouchItemShopOption, [lambda: ValidReplacements.extend(Accessories)])
PouchShopOption_TornaAccessories = SubOption("Torna Accessories", PouchItemShopOption, [lambda: ValidReplacements.extend(TornaAccessories)])
PouchShopOption_WeaponChips = SubOption("Weapon Chips", PouchItemShopOption, [lambda: ValidReplacements.extend(WeaponChips)])
PouchShopOption_AuxCores = SubOption("Aux Cores", PouchItemShopOption, [lambda: ValidReplacements.extend(AuxCores)])
PouchShopOption_RefinedAuxCores = SubOption("Refined Aux Cores", PouchItemShopOption, [lambda: ValidReplacements.extend(RefinedAuxCores)])
PouchShopOption_CoreCrystals = SubOption("Core Crystals", PouchItemShopOption, [lambda: ValidReplacements.extend(CoreCrystals)])
PouchShopOption_Deeds = SubOption("Shop Deeds", PouchItemShopOption, [lambda: ValidReplacements.extend(Deeds)])
PouchShopOption_CollectionPointMaterials = SubOption("Collection Point Materials", PouchItemShopOption, [lambda: ValidReplacements.extend(CollectionPointMaterials)])
PouchShopOption_PouchItems = SubOption("Pouch Items", PouchItemShopOption, [lambda: ValidReplacements.extend(PouchItems)])
TreasureChestOption = Option("Treasure Chests", General, "Randomizes the contents of Treasure Chests", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"), ["itm1ID", "itm2ID", "itm3ID", "itm4ID","itm5ID","itm6ID","itm7ID","itm8ID"], Accessories + Boosters + WeaponChips + AuxCores + CoreCrystals + RefinedAuxCores,[])], _hasSpinBox = True)
TreasureChestOption_Accessories = SubOption("Accessories", TreasureChestOption, [lambda: ValidReplacements.extend(Accessories)])
TreasureChestOption_TornaAccessories = SubOption("Torna Accessories", TreasureChestOption, [lambda: ValidReplacements.extend(TornaAccessories)])
TreasureChestOption_WeaponChips = SubOption("Weapon Chips", TreasureChestOption, [lambda: ValidReplacements.extend(WeaponChips)])
TreasureChestOption_AuxCores = SubOption("Aux Cores", TreasureChestOption, [lambda: ValidReplacements.extend(AuxCores)])
TreasureChestOption_RefinedAuxCores = SubOption("Refined Aux Cores", TreasureChestOption, [lambda: ValidReplacements.extend(RefinedAuxCores)])
TreasureChestOption_CoreCrystals = SubOption("Core Crystals", TreasureChestOption, [lambda: ValidReplacements.extend(CoreCrystals)])
TreasureChestOption_Deeds = SubOption("Shop Deeds", TreasureChestOption, [lambda: ValidReplacements.extend(Deeds)])
TreasureChestOption_CollectionPointMaterials = SubOption("Collection Point Materials", TreasureChestOption, [lambda: ValidReplacements.extend(CollectionPointMaterials)])
WeaponChipShopOption = Option("Weapon Chip Shops", General, "Randomizes Weapon Chips in Weapon Chip Shops", [lambda: JSONParser.ChangeJSONFile(["common/MNU_ShopNormal.json"], Helper.StartsWith("DefItem", 1, 10), WeaponChips, WeaponChips)] , _hasSpinBox = True)

# Drivers
DriverAccessoriesOption = Option("Driver Accessories", Driver, "Randomizes effects of Accessories", [lambda: _Accessories.RandomizeAccessoryEnhancements()])
DriverArtsOption = Option("Driver Arts", Driver, "Randomizes effects of all driver arts", [lambda: _DriverArts.DriverArtRandomizer(), lambda: _DriverArts.GenCustomArtDescriptions()], _hasSpinBox = True)
DriverArtsOption_AutoAttacks = SubOption("Auto Attacks", DriverArtsOption, [], _defState = False)
DriverArtsOption_SingleReaction = SubOption("Single Reaction", DriverArtsOption, [])
DriverArtsOption_MultipleReactions = SubOption("Multiple Reactions", DriverArtsOption, [])
DriverArtsOption_Debuffs = SubOption("Debuffs", DriverArtsOption, [])
DriverArtsOption_Buffs = SubOption("Buffs", DriverArtsOption, [])
DriverArtsOption_Cooldown = SubOption("Cooldown", DriverArtsOption, [])
DriverArtsOption_Damage = SubOption("Damage", DriverArtsOption, [])
DriverArtsOption_Enhancements = SubOption("Enhancements", DriverArtsOption, [])
DriverArtsOption_AnimationSpeed = SubOption("Animation Speed", DriverArtsOption, [])
DriverArtsOption_AOE= SubOption("AOE", DriverArtsOption, [])
DriverSkillTreesOption = Option("Driver Skill Trees", Driver, "Randomizes driver's skill trees", [lambda: SkillTrees.RandomizeSkillEnhancements()])
DriverSkillTreesOption_NonstandardSkills = SubOption("Nonstandard Skills", DriverSkillTreesOption)
DriverSkillTreesOption_EarlyArtsCancel = SubOption("Early Arts Cancel", DriverSkillTreesOption)
DriverSkillTreesOption_EarlyXYBAttack = SubOption("Early XYB Attack", DriverSkillTreesOption)

# Blades
BladesOption = Option("Blades", Blade, "Randomizes when blades appear in the story", [lambda: BladeRandomization.BladeRandomization()], _hasSpinBox = True)
BladesOption_Dromarch = SubOption("Randomize Dromarch", BladesOption)
BladesOption_Healer = SubOption("Guaranteed Healer", BladesOption)
BladeAuxCoresOption = Option("Blade Aux Cores", Blade, "Randomizes the effects of Aux Cores", [lambda: _AuxCores.RandomizeAuxCoreEnhancements()])
BladeAuxCoreSlotsOption = Option("Blade Aux Core Slots", Blade, "Randomizes a Blade's maximum Aux Core Slots", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"],["OrbNum"], Helper.InclRange(0,3), IDs.BladeAuxCoreSlotDistribution)])
BladeArtsOption = Option("Blade Arts", Blade, "Randomizes a Blade's combat arts", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("NArts",1,3), BladeArts, BladeArts)])
BladeBattleSkillsOption = Option("Blade Battle Skills", Blade, "Randomizes a Blade's battle (yellow) skill tree", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("BSkill", 1, 3), list(set(BladeBattleSkills) - set([268, 8, 9])), list(set(BladeBattleSkills) - set([268, 267,266,265,144,142,143, 8, 9])) )], _hasSpinBox = True)
BladeFieldSkillsOption = Option("Blade Field Skills", Blade, "Randomizes a Blade's field (green) skill tree", [lambda: _GreenSkills.RandomizeFieldSkills()])
BladeFieldSkillsOption_QuestSkills = SubOption("Quest Skills", BladeFieldSkillsOption)
BladeCooldownOption = Option("Blade Cooldowns", Blade, "Randomizes a Blade's swap cooldown", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["CoolTime"], Helper.InclRange(1,1000), Helper.InclRange(1,1000))], _hasSpinBox = True)
BladeDefensesOption = Option("Blade Defenses", Blade, "Randomizes a Blade's Physical and Ether Defense", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["PArmor", "EArmor"], Helper.InclRange(0,100), BladeDefenseDistribution)], _hasSpinBox = True)
BladeElementsOption = Option("Blade Elements", Blade, "Randomizes a Blade's element", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"],["Atr"], Helper.InclRange(1,8), Helper.InclRange(1,8))], _hasSpinBox = True)
BladeModsOption = Option("Blade Stat Mods", Blade, "Randomizes a Blade's Stat Modifiers", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["HpMaxRev", "StrengthRev", "PowEtherRev", "DexRev", "AgilityRev", "LuckRev"], Helper.InclRange(1,100), BladeModDistribution)], _hasSpinBox = True)
BladeSpecialButtonsOption = Option("Blade Button Combos", Blade, "Randomizes what button a special uses for its button challenge", [lambda: JSONParser.ChangeJSONFile(["common/MNU_BtnChallenge2.json"], Helper.StartsWith("BtnType", 1, 3), ButtonCombos, [])])
BladeSpecialButtonsOption_A = SubOption("A", BladeSpecialButtonsOption, [lambda: ValidReplacements.append(1)])
BladeSpecialButtonsOption_B = SubOption("B", BladeSpecialButtonsOption, [lambda: ValidReplacements.append(2)])
BladeSpecialButtonsOption_X = SubOption("X", BladeSpecialButtonsOption, [lambda: ValidReplacements.append(3)])
BladeSpecialButtonsOption_Y = SubOption("Y", BladeSpecialButtonsOption, [lambda: ValidReplacements.append(4)])
BladeSpecialButtonsOption_Mystery = SubOption("?", BladeSpecialButtonsOption, [lambda: ValidReplacements.append(5)])
BladeSpecialReactionsOption = Option("Blade Special Reactions", Blade, "Randomizes each hit of a blade special to have a random effect such as break, knockback etc.", [lambda: JSONParser.ChangeJSONFile(["common/BTL_Arts_Bl.json"], Helper.StartsWith("ReAct", 1, 16), HitReactions, HitReactions)], _hasSpinBox = True)
BladeWeaponChipsOption = Option("Blade Weapon Chips", Blade, "Randomizes the effects of weapon chips")
BladeWeaponChipsOption_AutoAtk = SubOption("Auto Attacks", BladeWeaponChipsOption, [lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpn.json"],["Damage"],Helper.InclRange(0,1298), Helper.InclRange(1,900) + Helper.InclRange(1000,1100) + Helper.InclRange(1250,1300))], _defState= True)
BladeWeaponChipsOption_CritRate = SubOption("Crit Rate", BladeWeaponChipsOption, [lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpn.json"],["CriRate"],Helper.InclRange(0,100), BladeWeaponCritDistribution)],_defState= True)
BladeWeaponChipsOption_GuardRate = SubOption("Guard Rate", BladeWeaponChipsOption, [lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpn.json"],["GuardRate"],Helper.InclRange(0,100), BladeWeaponGuardDistribution)],_defState= True)
BladeWeaponChipsOption_Enhancement = SubOption("Enhancements", BladeWeaponChipsOption, [lambda: _WeaponChips.RandomizeWeaponEnhancements()],_defState= True)
BladeWeaponClassOption = Option("Blade Weapon Class", Blade, "Randomizes weapon roles (ATK, TNK, HLR)", [lambda: JSONParser.ChangeJSONFile(["common/ITM_PcWpnType.json"], ["Role"], Helper.InclRange(1,3), WeaponTypeRoles)])

# Enemies
EnemiesOption = Option("Enemies", Enemies, "Randomizes what enemies appear in the world", [lambda: EnemyRandoLogic.EnemyLogic()])
EnemiesOption_Bosses = SubOption("Bosses", EnemiesOption)
EnemiesOption_QuestEnemies = SubOption("Quest Enemies", EnemiesOption)
EnemiesOption_UniqueMonsters = SubOption("Unique Monsters", EnemiesOption)
EnemiesOption_Superbosses = SubOption("Superbosses", EnemiesOption)
EnemiesOption_NormalEnemies = SubOption("Normal Enemies", EnemiesOption)
EnemiesOption_MixedTypes = SubOption("Mix Enemies Between Types", EnemiesOption)
EnemiesOption_BalancedLevels = SubOption("Balanced Levels", EnemiesOption)
# EnemiesOption_Bosses = SubOption("Bosses", EnemiesOption) removed cause i dont want these options but it broke last time i tried to remove
# EnemiesOption_Bosses = SubOption("Bosses", EnemiesOption)
EnemyEnhancementsOption = Option("Enemy Enhancements", Enemies, "Gives enemies a random enhancement; displayed by their name", [lambda: _EnemyEnhancements.EnemyEnhances()], _hasSpinBox = True)
EnemyArtEffectsOption = Option("Enemy Art Effects", Enemies, "Gives enemies a random bonus effect to their arts; displayed by their art's name", [lambda: _EnemyArts.EnemyArtAttributes()], _hasSpinBox = True)
EnemyArtEffectsOption_Reactions = SubOption("Reactions", EnemyArtEffectsOption)
EnemyArtEffectsOption_AOE = SubOption("AOE", EnemyArtEffectsOption)
EnemyArtEffectsOption_Buffs = SubOption("Buffs", EnemyArtEffectsOption)
EnemyArtEffectsOption_Debuffs = SubOption("Debuffs", EnemyArtEffectsOption)
EnemyArtEffectsOption_Enhancements = SubOption("Enhancements", EnemyArtEffectsOption)
EnemyDropOption = Option("Enemy Drops", Enemies, "Randomizes enemy drops/loot", [lambda: JSONParser.ChangeJSONFile(["common/BTL_EnDropItem.json"], Helper.StartsWith("ItemID", 1, 8), AuxCores+ RefinedAuxCores + IDs.Accessories + WeaponChips, [])], _hasSpinBox = True)
EnemyDropOption_Accessories = SubOption("Accessories", EnemyDropOption, [lambda: ValidReplacements.extend(Accessories)])
EnemyDropOption_TornaAccessories = SubOption("Torna Accessories", EnemyDropOption, [lambda: ValidReplacements.extend(TornaAccessories)])
EnemyDropOption_WeaponChips = SubOption("Weapon Chips", EnemyDropOption, [lambda: ValidReplacements.extend(WeaponChips)])
EnemyDropOption_AuxCores = SubOption("Aux Cores", EnemyDropOption, [lambda: ValidReplacements.extend(AuxCores)])
EnemyDropOption_RefinedAuxCores = SubOption("Refined Aux Cores", EnemyDropOption, [lambda: ValidReplacements.extend(RefinedAuxCores)])
EnemyDropOption_CoreCrystals = SubOption("Core Crystals", EnemyDropOption, [lambda: ValidReplacements.extend(CoreCrystals)])
EnemyDropOption_Deeds = SubOption("Shop Deeds", EnemyDropOption, [lambda: ValidReplacements.extend(Deeds)])
EnemyDropOption_CollectionPointMaterials = SubOption("Collection Point Materials", EnemyDropOption, [lambda: ValidReplacements.extend(CollectionPointMaterials)])
EnemyAggroOption = Option("Enemy Aggro", Enemies, "The percentage of all non-boss and non-quest enemies that will aggro the player", [lambda: EnemyRandoLogic.EnemyAggroProportion()], _hasSpinBox = True)
EnemyMovespeedOption = Option("Enemy Movespeed", Enemies, "Randomizes how fast enemies move in the overworld", [lambda: JSONParser.ChangeJSONFile(["common/CHR_EnParam.json"], ["WalkSpeed", "RunSpeed"], Helper.InclRange(0,100), Helper.InclRange(0,100) + Helper.InclRange(250,255))], _hasSpinBox = True)

# Misc
MusicOption = Option("Music", Misce, "Randomizes Music", [lambda: MusicShuffling.MusicShuffle()])
MusicOption_MixBattleAndEnv = SubOption("Mix Battle and Environment Themes", MusicOption, _defState = False)
TrustLineOption = Option("Trust Lines", Misce, "Randomizes blade trust lines in battle (colors, power, etc.)", [lambda: TrustBeam.BeamRandomizer()])
CustomCoreCrystalOption = Option("Custom Core Crystals", Misce, "Adds Core Crystals with guaranteed Rare Blades to Treasure Chests", [lambda: CoreCrystalAdjustments.CoreCrystalChanges()], _hasSpinBox = True)
DifficultyOption = Option("Difficulty", Misce, "Forces this difficulty, regardless of what is chosen in the options menu")
DifficultyOption_Easy = SubOption("Easy", DifficultyOption)
DifficultyOption_Normal = SubOption("Normal", DifficultyOption)
DifficultyOption_BOC = SubOption("Bringer of Chaos", DifficultyOption)
DifficultyOption_Ultimate = SubOption("Ultimate", DifficultyOption)

# QOL
ShortenTutorialOption = Option("Shorten Tutorial", QOL, "Shortens/removes tutorials", [lambda: TutorialShortening.ShortenedTutorial()])
NewGamePlusBladesOption = Option("NG+ Blades", QOL, "Allows all blades to be accessible in a fresh playthrough", [lambda: GachaModifications.UnlockNGPlusBlades()])
FreelyEngageBladesOption = Option("Freely Engage Blades", QOL, "Allows blades to be freely engaged by all valid drivers", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["FreeEngage"], [0], [1], [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1075, 1076, 1103])])
CTMCOption = Option("Chest Type Matches Contents", QOL, "Chest model and label changes depending on tier of loot", [lambda: RaceMode.ChestTypeMatching()], _prio = 95)
TreasureChestVisOption =  Option("Treasure Chest Visibility", QOL, "Increases the range you can see treasure chests from", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"), ["msgVisible", "msgdigVisible"], Helper.InclRange(0,200), [255])])
RemoveFieldSkillsOption = Option("Remove Story Field Skills", QOL, "Removes field skill checks", [lambda: FieldSkillAdjustments.RemoveFieldSkills()], ["Remove All Field Skills", []])
RemoveFieldSkillsOption_AllFieldSkills = SubOption("Remove All Field Skills", RemoveFieldSkillsOption)
EverlastingPouchItemsOption = Option("Everlasting Pouch Items", QOL, "Makes Pouch Items last as long as possible", [lambda: JSONParser.ChangeJSONFile(["common/ITM_FavoriteList.json"],["Time"], Helper.InclRange(0,255), [6099])])
CondenseGoldOption = Option("Condense Gold Loot", QOL, "Condenses gold in chests so you can see other items", [lambda: JSONParser.ChangeJSONFile(Helper.InsertHelper(2,1,90, "maa_FLD_TboxPop.json", "common_gmk/"),["goldPopMin", "goldPopMax"], Helper.InclRange(0,100000), [1])])
MutePopupsOption = Option("Mute Popups", QOL, "Stops blade skill and pouch item refill popups", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[89], ["sheet06"], [""])])
MutePopupsOption_Landmarks = SubOption("Landmarks", MutePopupsOption, [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[85], ["sheet04"], [""])])
EnhancementDisplay = Option("Enhancement Display", QOL, "Shows when enhancements activate in battle", [lambda: Enhancements.SearchAndSetDisplayIDs()])
EasySkillTreesOption = Option("Fast Blade Skill Trees", QOL, "Makes trust the only condition for levelling up a blade's skill tree", [lambda: SkillTrees.BladeSkillTreeShortening()])
FasterDriverSkillTrees = Option("Fast Driver Skill Trees", QOL, "Decreases SP required for each node")
FasterDriverSkillTrees_8 = SubOption("8x", FasterDriverSkillTrees, [lambda: Helper.MathmaticalColumnAdjust(Helper.StartsWith("./_internal/JsonOutputs/common/BTL_Skill_Dr_Table0", 1, 6, addJson=True) + ["./_internal/JsonOutputs/common/BTL_Skill_Dr_Table17.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table18.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table19.json"], ["NeedSp"], ['row[key] // 8'])], _defState = False)
FasterDriverSkillTrees_2 = SubOption("2x", FasterDriverSkillTrees, [lambda: Helper.MathmaticalColumnAdjust(Helper.StartsWith("./_internal/JsonOutputs/common/BTL_Skill_Dr_Table0", 1, 6, addJson=True) + ["./_internal/JsonOutputs/common/BTL_Skill_Dr_Table17.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table18.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table19.json"], ["NeedSp"], ['row[key] // 2'])], _defState = False)
FasterDriverSkillTrees_4 = SubOption("4x", FasterDriverSkillTrees, [lambda: Helper.MathmaticalColumnAdjust(Helper.StartsWith("./_internal/JsonOutputs/common/BTL_Skill_Dr_Table0", 1, 6, addJson=True) + ["./_internal/JsonOutputs/common/BTL_Skill_Dr_Table17.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table18.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table19.json"], ["NeedSp"], ['row[key] // 4'])], _defState = False)
FasterDriverSkillTrees_16 = SubOption("16x", FasterDriverSkillTrees, [lambda: Helper.MathmaticalColumnAdjust(Helper.StartsWith("./_internal/JsonOutputs/common/BTL_Skill_Dr_Table0", 1, 6, addJson=True) + ["./_internal/JsonOutputs/common/BTL_Skill_Dr_Table17.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table18.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table19.json"], ["NeedSp"], ['row[key] // 16'])], _defState = False)
FasterDriverSkillTrees_32 = SubOption("32x", FasterDriverSkillTrees, [lambda: Helper.MathmaticalColumnAdjust(Helper.StartsWith("./_internal/JsonOutputs/common/BTL_Skill_Dr_Table0", 1, 6, addJson=True) + ["./_internal/JsonOutputs/common/BTL_Skill_Dr_Table17.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table18.json", "./_internal/JsonOutputs/common/BTL_Skill_Dr_Table19.json"], ["NeedSp"], ['row[key] // 32'])], _defState = False)

FasterLevelsOption = Option("Faster Levels", QOL, "Decreases EXP required for each levelup")
FasterLevelsOption_2 = SubOption("2x", FasterLevelsOption, [lambda: Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2"], ['row[key] // 2'])])
FasterLevelsOption_4 = SubOption("4x", FasterLevelsOption, [lambda: Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2"], ['row[key] // 4'])])
FasterLevelsOption_8 = SubOption("8x", FasterLevelsOption, [lambda: Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2"], ['row[key] // 8'])])
FasterLevelsOption_16 = SubOption("16x", FasterLevelsOption, [lambda: Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2"], ['row[key] // 16'])])
FasterLevelsOption_32 = SubOption("32x", FasterLevelsOption, [lambda: Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2"], ['row[key] // 32'])])


# Funny
ProjTreasureChestOption = Option("Projectile Treasure Chests", Funny, "Launches your items from chests",[lambda: JSONParser.ChangeJSONFile(["common/RSC_TboxList.json"], ["box_distance"], [0,0.5,1], [15])])
BladeSizeOption = Option("Blade Size", Funny, "Randomizes the size of Blades", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["Scale", "WpnScale"], [], BladeScales)], _hasSpinBox = True)
NPCSizeOption = Option("NPC Size", Funny, "Randomizes the size of NPCs", [lambda: JSONParser.ChangeJSONFile(["common/RSC_NpcList.json"], ["Scale"],[], NPCScales)], _hasSpinBox = True)
EnemySizeOption = Option("Enemy Size", Funny, "Randomizes the size of enemies", [lambda: JSONParser.ChangeJSONFile(["common/CHR_EnArrange.json"], ["Scale"], [], EnemyScales)], _hasSpinBox = True)
FieldItemOption = Option("Field Item Size", Funny, "Randomizes the size and spin rate of items from chests and collection points", [lambda: BigItems.BigItemsRando()])

# Cosmetics
BladeWeaponCosmeticsOption = Option("Blade Weapon Cosmetics", CosmeticsTab, "Keeps all default weapon models regardless of chips", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["OnlyWpn"], [0], [1])])
CosmeticsOption = Option("Character Outfits", CosmeticsTab, "Randomizes Cosmetics on Accessories and Aux Cores", [lambda: Cosmetics.Cosmetics()],_prio=51, _hasSpinBox = True) # Sub are created by another class
for opt in Cosmetics.CosmeticsList: # To gen these since listing them here would be annoying
    opt.CreateSubOptions(CosmeticsOption)

# Game Modes
RaceModeOption = Option("Race Mode", GameModeTab, "Enables Race Mode (see the Race Mode README)", [lambda: RaceMode.RaceModeChanging(), RaceMode.SeedHash])
RaceModeOption_Zohar = SubOption("Zohar Fragment Hunt", RaceModeOption)
RaceModeOption_DLC = SubOption("DLC Item Removal", RaceModeOption)
UMHuntOption = Option("Unique Monster Hunt", GameModeTab, "Experimental Mode", [lambda: UniqueMonsterHunt.UMHunt()], _hasSpinBox = True, _spinMin = 1, _spinMax = 10, _spinIncr = 1, _spinDesc = "Round(s)", _spinWidth = 2)
UMHuntOption_SuperbossWave = SubOption("Superboss Wave", UMHuntOption)

# Currently Disabled for Various Reasons
# Blade Names (moved so that blade name rando doesn't mess up Race Mode getting blade IDs)
# GenStandardOption("Blade Names", TabBlades, "Randomizes a Blade's name", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["Name"], Helper.InclRange(0,1000), BladeNames)])
# GenStandardOption("Less UI", TabQOL, "Removes some of the unneccessary on screen UI (Blade Swap and Current Objective)", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[88], ["sheet05", "sheet03"], [""])])
# GenStandardOption("Screenshot Mode", TabQOL, "Removes most UI for screenshots", [lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[88], ["sheet05", "sheet03", "sheet04"], ""), lambda: JSONParser.ChangeJSONLine(["common/MNU_Layer.json"],[86], ["sheet02", "sheet03"], "")])
# CTMC (has to run after Race Mode in current iteration, needs to know what chests have what loot)
# GenDictionary("NPCs", TabMisc, "Randomizes what NPCs appear in the world (still testing)", [lambda: JSONParser.ChangeJSON(Helper.InsertHelper(2, 1,90,"maa_FLD_NpcPop.json", "common_gmk/"), ["NpcID"], Helper.InclRange(0,3721), Helper.InclRange(2001,3721))])
# GenOption("Funny Faces", TabMisc, "Randomizes Facial Expressions", ["common/EVT_eyetype.json"], ["$id"], Helper.inclRange(0,15), Helper.inclRange(0,15)) # doesnt work yet
# GenDictionary("Menu Colors", TabMisc, "Randomizes Colors in the UI", [lambda: JSONParser.ChangeJSON(["common/MNU_ColorList.json"], ["col_r", "col_g", "col_b"], Helper.InclRange(0,255), Helper.InclRange(0,0))])
# GenStandardOption("Blade Weapons", TabBlades, "Randomizes a Blade Weapon type, for example Pyra can now be a Knuckle Claws user", [lambda: _BladeWeapons.WepRando()])
# GenStandardOption("Blade Specials", TabBlades, "Randomizes blades special (red) skill tree", [lambda: JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("BArts", 1, 3) + ["BartsEx", "BartsEx2"], BladeSpecials,  list(set(BladeSpecials) - set([215])))]) works okay, but animations dont connect feels mid
# DebugLog.CreateDebugLog(OptionDictionary, Version, randoSeedEntry.get())
# GenStandardOption("Enemy Arts", TabEnemies, "Gives enemies new arts", [lambda: _EnemyArts.EnemyArts(OptionDictionary["Enemy Arts"]["spinBoxVal"].get())],optionType=Spinbox)
# GenStandardOption("Enemy Rage", TabEnemies, "Randomizes the effects of enemy enraged states", ["common/BTL_Aura"])   

def UpdateAllStates():
    for opt in OptionList:
        opt.StateUpdate()