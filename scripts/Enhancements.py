import JSONParser, Helper, random


Baby = [1,2,4,5]
Mini = [1,7,14,20]
Small = [10,20,35,50]
Medium = [20,40,70,100]
Large = [30,100,200,300]
Mega = [60,200,400,600]
Massive = [300,600,1000,1500]
Giga = [1000,1700,2500,3000]

Common = 0
Rare = 1
Legendary = 2

EnhanceEffectsList = []
EnhanceClassList = []


class Enhancement: 
    id = 0
    name = ""
    EnhanceEffect = 0
    Param1 =   0
    Param2 =  0
    Caption = 0
    Caption2 = 0
    Description = ""
    Rarity = Common
    ReverseOdds = False
    def __init__(self,Name, Enhancement, Caption = 0,  Param1 = [0,0,0,0], Param2 = [0,0,0,0], Description = "", ReverseOdds = False):
        self.name = Name
        self.EnhanceEffect = Enhancement
        self.Caption = Caption
        self.Caption2 = Caption
        self.Param1 = Param1
        self.Param2 = Param2
        self.Description = Description
        self.ReverseOdds = ReverseOdds
        EnhanceClassList.append(self)
    def RollEnhancement(self,ID):
        self.Rarity = random.choice([Common, Rare, Legendary])
        self.id = ID
        def SetParams(ParameterChoices):
            if ParameterChoices == Baby:
                Pstep = 1
            else:
                Pstep = 5
            if len(ParameterChoices) == 1:
                Parameter = ParameterChoices[0]
            else:
                try:
                    if self.ReverseOdds:
                        Common = 2
                        Rare = 1
                        Legendary = 0
                    else:
                        Common = 0
                        Rare = 1
                        Legendary = 2
                    if self.Rarity == Common:
                        Parameter = random.randrange(ParameterChoices[0],ParameterChoices[1]+1,Pstep)
                    elif self.Rarity == Rare:
                        Parameter = random.randrange(ParameterChoices[1],ParameterChoices[2]+1,Pstep)
                    elif self.Rarity == Legendary:
                        Parameter = random.randrange(ParameterChoices[2],ParameterChoices[3]+1,Pstep)
                except:
                    Parameter = 0
            return Parameter


        if self.Description != "":
            JSONParser.ChangeJSONLine(["common_ms/btl_enhance_cap.json"],[self.name], ["name"], self.Description)

        EnhanceEffectsDict = {
            "$id": ID,
            "EnhanceEffect": self.EnhanceEffect,
            "Param1": SetParams(self.Param1),
            "Param2": SetParams(self.Param2),
            "Caption": self.Caption,
            "Caption2": self.Caption
        }
        EnhanceEffectsList.append([EnhanceEffectsDict])
        
def RunCustomEnhancements():
    ID = 3896 # Starting ID for custom enhancements
    for enhancement in EnhanceClassList:
        enhancement.RollEnhancement(ID)
        ID +=1
    JSONParser.ChangeJSONFile(["common/BTL_EnhanceEff.json"],["Param"], Helper.InclRange(1,1000), [9999])
    JSONParser.ChangeJSONLine(["common/BTL_EnhanceEff.json"],[45], ["Param"], random.randrange(1,51)) # Battle damage up after a certain time uses nonstandard parameter this fixes it
    JSONParser.ChangeJSONLine(["common/BTL_EnhanceEff.json"],[181], ["Param"], random.randrange(30,71)) # Healing with low HP
    JSONParser.ChangeJSONLine(["common/BTL_EnhanceEff.json"],[90], ["Param"], random.randrange(10,61)) # Healing with low HP
    JSONParser.ExtendJSONFile("common/BTL_Enhance.json",  EnhanceEffectsList)


HPBoost =       Enhancement("Health",1,1, Small)
StrengthBoost = Enhancement("Strength", 2,2, Small)
EtherBoost = Enhancement("Ether", 3,3, Small)
DexBoost = Enhancement("Dexterity",4,4, Small)
AgiBoost = Enhancement("Agility",5,5, Small)
LuckBoost = Enhancement("Lucky",6,6, Small)
CritBoost = Enhancement("Critical",7,7, Medium)
PhysDefBoost = Enhancement("Phys Def",8,8, Medium)
EthDefBoost = Enhancement("Ether Def",9,9, Medium)
BlockBoost = Enhancement("Block",10,10, Medium)
FlatHPBoost = Enhancement("Health",11,11, Massive)
FlatStrengthBoost = Enhancement("Strength",12,12, Medium)
FlatEtherBoost = Enhancement("Ether",13,13, Medium)
FlatDexBoost = Enhancement("Dexterity",14,14, Large)
FlatAgiBoost = Enhancement("Agility",15,15, Small)
FlatLuckBoost =Enhancement("Luck",16,16, Medium)
FlatCritBoost = Enhancement("Critical",17,17, Small)
FlatDefBoost = Enhancement("Phys Def",18,18, Mini)
FlatEthDefBoost = Enhancement("Eth Def",19,19,Mini)
FlatBlockBoost = Enhancement("Block",20,20,Mini)
TitanDamageUp = Enhancement("Titan",21,222,[6], Mega)
MachineDamageUp = Enhancement("Machine",21, 221, [5], Large)
HumanoidDamageUp = Enhancement("Humanoid",21, 220, [4], Large)
AquaticDamageUp = Enhancement("Aquatic",21, 219, [3], Mega)
AerialDamageUp = Enhancement("Aerial",21, 218, [2], Large)
InsectDamageUp = Enhancement("Insect",21, 217, [1], Large)
BeastDamageUp = Enhancement("Beast",21, 216, [0], Large)
TitanExecute = Enhancement("Titan",22, 229, [6], Baby)
MachineExecute = Enhancement("Machine",22, 228, [5], Baby)
HumanoidExecute = Enhancement("Humanoid",22, 227, [4], Baby)
AquaticExecute = Enhancement("Aquatic",22, 226, [3], Baby)
AerialExecute = Enhancement("Aerial",22, 225, [2], Baby)
InsectExecute = Enhancement("Insect",22, 224, [1], Baby)
BeastExecute = Enhancement("Beast",22, 223, [0], Baby)
BladeComboDamUp = Enhancement("Bl Combo",23,21, Large)
FusionComboDamUp = Enhancement("Fus Combo",24,22, Large)
EtherCounter = Enhancement("Eth Counter",25,23, Giga)
PhysCounter = Enhancement("Phys Counter",26,24, Giga)
AutoAttackHeal = Enhancement("Auto Vamp",27,26, Mini)
SpecialANDArtHeal = Enhancement("Omnivamp",28,27, Baby, Description="Restores [ML:Enhance kind=Param1 ]% HP of damage dealt when\n a Special or Art connects.")
ArtDamageHeal = Enhancement("Omnivamp",28, 28, Small) # This goes on arts only or else it will heal from special and arts
EnemyKillHeal = Enhancement("Scavenger",29,30, Medium)
CritHeal = Enhancement("Crit Vamp",30,31, Small)
CritDamageUp = Enhancement("Crit Damage",31,32, Medium)
PercentDoubleAuto = Enhancement("Doublestrike",32,33, Medium)
FrontDamageUp = Enhancement("Front",33,34, Large)
SideDamageUp = Enhancement("Side",34,35, Large)
BackDamageUp = Enhancement("Back",35,36, Large)
SurpriseAttackUp = Enhancement("Suprise",36,37, Giga)
ToppleDamageUp = Enhancement("Topple",37,38, Large)
LaunchDamageUp = Enhancement("Launch",38,39, Large)
SmashDamageUp = Enhancement("Smash",39,40, Mega)
HigherLVEnemyDamageUp = Enhancement("Underdog",40,41, Large)
AllyDownDamageUp = Enhancement("Comeback",41,42, Mega)
GuardAnnulAttack = Enhancement("Pierce",42,43, Medium)
AnnulReflect = Enhancement("Phase",43,44, Medium)
DamageUpWhenHpDown = Enhancement("Desperation",44,45, Small, Large)
BattleDurationDamageUp = Enhancement("Delayed",45,46, Large) # Uses weird parameter see above
DamageUpOnEnemyKill = Enhancement("Massacre",46,47, Medium)
BreakDurationUp = Enhancement("B Duration",47,48, Medium)
ToppleDurationUp = Enhancement("T Duration",48,49, Medium)
LaunchDurationUp = Enhancement("L Duration",49,50, Medium)
AutoAttackDamageUp = Enhancement("Automatic",50,51, Mega)
AggroedEnemyDamageUp = Enhancement("Self Defense",51,52, Large)
IndoorsDamageUp = Enhancement("Indoor",52,53, Medium)
OutdoorsDamageUp = Enhancement("Outdoor",53,54, Small)
BladeSwitchDamageUp = Enhancement("Switchup",54,55, Small)
OppositeGenderBladeDamageUp = Enhancement("Counterpart",55,56, Medium)
ReduceEnemyToppleResist = Enhancement("Toppler",56,57, Medium)
ReduceEnemyLaunchResist = Enhancement("Breaker",57,58, Medium)
OnBlockNullDamage = Enhancement("Guardian",59, 59, Small)
HPLowEvasion = Enhancement("Sway",62, 60, Small, Medium)
EvasionWhileMoving = Enhancement("Agile",63, 61, Medium)
HPLowBlockRate = Enhancement("Block",64, 62, Small, Medium)
ReduceDamageFromNearbyEnemies = Enhancement("Aura",65, 63, Small)
ReduceDamageOnLowHP = Enhancement("Everlasting",66,64, Small, Small)
HighHPDamageUp = Enhancement("Confidence",67,65, Medium,Large, ReverseOdds=True )
ReduceSpikeDamage =Enhancement("Spike Breaker",68,66, Medium)
BreakResistUp = Enhancement("Fluid",69, 67, Medium)
ToppleResistUp = Enhancement("Lithe",70, 68, Medium)
LaunchResistUp = Enhancement("Heavyweight",71, 69, Medium)
SmashResistUp = Enhancement("Unsmashable",72, 70, Medium)
BlowdownResistUp = Enhancement("Steady",73, 71, Medium)
KnockbackResistUp = Enhancement("Steady",74, 72, Medium)
DefenseAnnulResistUp = Enhancement("Unpierceable",75, 73, Medium)
AutoAttackAggroDown = Enhancement("Aggro Down",77, 75, Large)
AutoAttackAggroUp = Enhancement("Aggro Up",78, 76, Large)
SpecialAndArtsAggroDown = Enhancement("Aggro Down",79, 77, Medium)
SpecialAggroDown = Enhancement("Aggro Down",79, 79, Medium) # For Specials only 
SpecialAndArtsAggroUp = Enhancement("Aggro Up",80, 81, Medium)
AggroReductionUp = Enhancement("Friendly",81, 85, Small)
AggroEverySecond = Enhancement("Provocative",82, 86, Small, Description="Increases aggro every second by [ML:Enhance kind=Param1 ]")
StartBattleAggro = Enhancement("Irksome",83, 92, Giga)
RevivalHP = Enhancement("Revival",84, 96, Large)
RevivalHPTeammate = Enhancement("Revival",85, 97, Large)
HealingArtsUp = Enhancement("Support",88, 98, Small)
IncreaseSelfHeal = Enhancement("Lively",89,99, Medium)
SpecialRechargeCancelling = Enhancement("Special",92, 100, Medium)
AutoAttackCancelDamageUp = Enhancement("Full Auto",93, 101, Medium)
Unbeatable = Enhancement("Unbeatable",94, 102, Medium)
NightAccuracy = Enhancement("Nocturnal",95, 103, Large)
DayAccuracy = Enhancement("Diurnal",96, 104, Large)
ExpEnemiesBoost = Enhancement("Wisdom",97, 105, Medium)
WPEnemiesBoost = Enhancement("Expert",98, 106, Large)
PartyGaugeExcellentFill = Enhancement("Party",101, 109, Small, Description="Fills the Party Gauge when an\n\"Excellent\" is scored during a Special by [ML:Enhance kind=Param1 ].")
PartyGaugeCritFill = Enhancement("Party",102, 112, Mini, Description="Fills the Party Gauge for\neach critical hit delivered by [ML:Enhance kind=Param1 ].")
PartyGaugeDriverArtFill = Enhancement("Party",103, 115, Baby)
DamageUpEnemyNumber = Enhancement("Underdog",104, 116, Medium)
ReflectDamageUp = Enhancement("Reflection",105, 117, Large)
CritDuringChain = Enhancement("Critical",107, 118, Medium)
ChainAttackHeal = Enhancement("Chain Heal",108, 119, Medium)
DriverReviveChainAttack = Enhancement("Resurrection",109, 120)
PartyGaugeFillEndChain = Enhancement("Rechain",110, 121, Medium, Description="Fills the Party Gauge\nat the end of each Chain Attack by [ML:Enhance kind=Param1 ].")
EtherCannonRange =Enhancement("Sniper",111, 122, Mini)
WhenDiesHealAllies = Enhancement("Wish",112, 123, Medium)
FirstArtDamage = Enhancement("STRIKE",114,125, Mega)
RingABell = Enhancement("Special",115, 126, Medium)
AutoBalancer = Enhancement("Balancer",116, 127)
EnemyGoldDrop = Enhancement("Alchemy",117, 128, Large)
AllWeaponAttackUp = Enhancement("Master",120, 130, Small)
PreventAffinityLossOnDeath = Enhancement("Affinity",121, 131)
AffinityUpButtonChallenge = Enhancement("Affinity",122, 132, Medium)
MissAffinityUp = Enhancement("Affinity",123, 133, Small)
DamageTakenAffinityUp = Enhancement("Affinity",124,134, Small)
BladeArtsTriggerUp = Enhancement("Artsy",125, 135, Large)
BladeArtDuration = Enhancement("Artsy",126, 136, Medium)
AffinityMaxBarrier = Enhancement("Barrier",127, 137, Small)
AffinityMaxAttack = Enhancement("Battlecry",128, 138, Medium)
AffinityMaxEvade = Enhancement("Dodgy",129, 139, Small)
HunterChem = Enhancement("Hunter",130, 140, Mega)
ShoulderToShoulder = Enhancement("Prey",131, 141, Mega)
BladeCooldownReduc = Enhancement("Swapper",132, 142, Medium)
PartyHealBladeSwitch = Enhancement("Parting Gift",133, 143, Small)
AffinityRange = Enhancement("Bluetooth",134, 144, Mega)
LV1Damage = Enhancement("LV1 Damage",135, 145,[1], Large)
LV2Damage = Enhancement("LV2 Damage",135, 145,[2], Large)
LV3Damage = Enhancement("LV3 Damage",135, 145,[3], Large)
LV4Damage = Enhancement("LV4 Damage",135, 145,[4], Large)
SmallHpPotCreate = Enhancement("Bottle",136, 146, Small)
PotionEffectUp = Enhancement("Potioneer",137, 147, Medium)
PurifyingFlames = Enhancement("Purifying",138, 148, Small, Mini)
ForeSight = Enhancement("Foresight",139, 149, Small)
DreamOfTheFuture = Enhancement("Dream",140, 150)
ReduceEnemyBladeComboDamage = Enhancement("Blade Res",142, 151, Medium)
DamagePerEvadeUp = Enhancement("Counterattack",143, 152, Mini)
ArtsRechargeMaxAffinity = Enhancement("Arts Charging",144, 154, Small)
ReduceAggroFromAttacks = Enhancement("Aggro Down",145, 155, Small)
PhyAndEthDefenseUp = Enhancement("Full Guard",146, 156, Small)
ChanceToPerfectHitAndEvade = Enhancement("Parry",147, 157, Small)
Reflection = Enhancement("Reflection",148, 158, Small)
MaxAffinityEvadeXAttacks = Enhancement("Harmony",149, 159, Mini)
ToppleANDLaunchDamageUp = Enhancement("Top Launch",150, 160, Large)
InstaKill = Enhancement("Instakill",151,161, Baby)
PartyDamageReducMaxAffinity = Enhancement("Ally Guard",152, 162, Mini)
KaiserZone = Enhancement("Kaiser",153, 163, Medium)
TastySnack = Enhancement("Snack",154, 164, Medium)
HealingUpMaxAffinity =  Enhancement("Healing",155, 165, Small)
AggroPerSecondANDAggroUp  = Enhancement("Aggy",156, 166, Small, Small)
MoreDamTakeLessAllyLowOrDown = Enhancement("Super",157, 167, Large, Small)
StopThinking = Enhancement("Enthrall",158, 168, Medium, Baby)
LowHPSpecialUp = Enhancement("Specialist",159, 169, Baby) #Uses decimals weird one not sure how it scales
TranquilGuard = Enhancement("Stance",160, 171, Small)
HPRestoreFusionCombo = Enhancement("Fusion",161, 172, Baby)
AttackUpGoldUp = Enhancement("Mercenary",162, 173, Baby, Mega, Description="Increases attack power by [ML:Enhance kind=Param1 ]'%' as gold is\ncollected during battle (max: [ML:Enhance kind=Param2 ]%).")
EnemyDropGoldOnHit = Enhancement("Pickpocket",163, 174, Medium)
ReduceEnemyChargeMaxAffinity = Enhancement("Syrup",164, 175, Small)
VersusBossUniqueEnemyDamageUp = Enhancement("Challenger",165, 176, Medium)
DidIDoThat = Enhancement("Repeat",166, 177, Small)
AnnulEnemyDefAndSpecialDamageUp = Enhancement("Pierce Special",167, 178, Small)
GlassCannon = Enhancement("Reckless",168, 179, Large, Small)
AnnulDef = Enhancement("Pierce",169, 180, Medium)
Transmigration = Enhancement("Transmigration",170, 181, Medium)
ElementalWeaknessDamageUP = Enhancement("Elementalist",171, 182, Large, Description= "Increases damage dealt when elemental\nweakness exploited by [ML:Enhance kind=Param1 ]% (affects all).") 
GravityPinwheel = Enhancement("Rebound",172, 183, Small, Baby)
AutoAttackSpeed= Enhancement("Tempo",173, 184, Large)
DoubleHitExtraAutoDamage = Enhancement("Restrike",174, 185, Large)
ToppleDamageANDDurationUp = Enhancement("Piledriver",175, 186, Medium, Mini)
EvadeDrainHp = Enhancement("Evade",176, 187, Mini) # Rocs Evasion art
AggroReducOnLandingHit = Enhancement("Concussion",177, 188, Medium)
RecoverRechargeCrit = Enhancement("Flurry",178, 189, Medium)
SpecialAffinityUp = Enhancement("Specialist",179,191, Medium)
BreakResDown = Enhancement("Breaker",180, 192, Small)
RepeatSpecialDamage = Enhancement("Magician",182, 193, Small)
Twang = Enhancement("Twang",183, 194, Small, Baby)
MaxAffinityAccuracy = Enhancement("Hone",184, 195, Large)
PotionStayLonger = Enhancement("Preservative",185, 196, Small)
FemaleDamageUp = Enhancement("Girly",186, 197, Mini)
DealMoreTakeLessMaxAffinity = Enhancement("Overwhelm",187, 198, Mini, Small)
CritUpChainAttackSelected =Enhancement("Critical",188,199,Medium)
BladeSwapDamage = Enhancement("Entrance",189, 200, Mini)
CancelWindowUp = Enhancement("Canceller",191, 201, Medium)
RestoreHitDamageToParty = Enhancement("Omnipotent Vamp",192, 202, Baby)
AddBufferTimeSwitchingToComboBlade = Enhancement("Buffer",193, 203, Medium)
PartyDamageMaxAffinity = Enhancement("Partygoer",194, 204, Mini)
AegisDriver = Enhancement("Dream",195, 205, Medium, Small)
AegisParty = Enhancement("Dream",196, 206)
ReduceFireDamage = Enhancement("Fire Res",58, 207, [1], Medium)
ReduceWaterDamage = Enhancement("Water Res",58, 208, [2], Medium)
ReduceWindDamage = Enhancement("Wind Res",58, 209, [3], Medium)
ReduceEarthDamage = Enhancement("Earth Res",58, 210, [4], Medium)
ReduceElectricDamage = Enhancement("Electric Res",58, 211, [5], Medium)
ReduceIceDamage = Enhancement("Ice Res",58, 212, [6], Medium)
ReduceLightDamage = Enhancement("Light Res",58, 213, [7], Medium)
ReduceDarkDamage = Enhancement("Dark Res",58, 214, [8], Medium)
ChainAttackPower = Enhancement("Superchain",106, 215, Baby, Description="Increases attack power ratio\nat the start of a Chain Attack by [ML:Enhance kind=Param1 ]%")
LowHPHeal = Enhancement("Regenerate",181, 230, Baby)
ArtUseHeal = Enhancement("Art Heal",86, 231, Baby)
AutoDriverArtCancelHeal = Enhancement("Cancel Heal",91, 233, Baby)
TakeDamageHeal = Enhancement("Mending",90, 235, Mini)
HealMoving = Enhancement("Rehab",87, 236, Mini)
MaxAffinityHeal = Enhancement("Recovery",141,237,Mini)
AbsorbFireBlock = Enhancement("Absorb Fire",60, 238, [1])
AbsorbWaterBlock = Enhancement("Absorb Water",60, 239, [2])
AbsorbWindBlock = Enhancement("Absorb Wind",60, 240, [3])
AbsorbEarthBlock = Enhancement("Absorb Earth",60, 241, [4])
AbsorbElectricBlock = Enhancement("Absorb Electric",60, 242, [5])
AbsorbIceBlock = Enhancement("Absorb Ice",60, 243, [6])
AbsorbLightBlock = Enhancement("Absorb Light",60, 244, [7])
AbsorbDarkBlock = Enhancement("Absorb Dark",60, 245, [8])
ReflectFireBlock = Enhancement("Reflect Fire",61, 246, [1])
ReflectWaterBlock = Enhancement("Reflect Water",61, 247, [2])
ReflectWindBlock = Enhancement("Reflect Wind",61, 248, [3])
ReflectEarthBlock = Enhancement("Reflect Earth",61, 249, [4])
ReflectElectricBlock = Enhancement("Reflect Electric",61, 250, [5])
ReflectIceBlock = Enhancement("Reflect Ice",61, 251, [6])
ReflectLightBlock = Enhancement("Reflect Light",61, 252, [7])
ReflectDarkBlock = Enhancement("Reflect Dark",61, 253, [8])
AegisPowerUp = Enhancement("Aegis",119, 254, [1], Small)
CatScimPowerUp = Enhancement("Scimitar",119, 255, [2], Small)
TwinRingPowerUp = Enhancement("Ring",119, 256, [3], Small)
DrillShieldPowerUp = Enhancement("Drill",119, 257, [4], Small)
MechArmsPowerUp = Enhancement("Arms",119, 258, [5], Small)
VarSaberPowerUp = Enhancement("Saber",119, 259, [6], Small)
WhipswordPowerUp = Enhancement("Whipsword",119, 260, [7], Small)
BigBangPowerUp = Enhancement("Big Bang",119, 261, [8], Small)
DualScythesPowerUp = Enhancement("Scythe",119, 262, [9], Small)
GreataxePowerUp = Enhancement("Greataxe",119, 263, [10], Small)
MegalancePowerUp = Enhancement("Megalance",119, 264, [11], Small)
EtherCannonPowerUp = Enhancement("Cannon",119, 265, [12], Small)
ShieldHammerPowerUp = Enhancement("Shield",119, 266, [13], Small)
ChromaKatanaPowerUp = Enhancement("Katana",119, 267, [14], Small)
BitballPowerUp = Enhancement("Bitball",119, 268, [15], Small)
KnuckleClawsPowerUp = Enhancement("Claws",119, 269, [16], Small)
HPGuardArtRechargeAttacked = Enhancement("Kinetic Reversal",197,270, Mini)
Jamming = Enhancement("Jamming",198, 271, Medium)
XStartBattle = Enhancement("X Start",113, 272, [0])
YStartBattle = Enhancement("Y Start",113, 274, [1])
BStartBattle = Enhancement("B Start",113, 276, [2])
ArtCancel = Enhancement("Arts Cancel",190, 278)
BladeSwitchCooldownWithArts = Enhancement("Ready",200, 279, Small)
TauntRes = Enhancement("Calm",217, 280, Medium)
DriverShackRes = Enhancement("Free",218, 281, Medium)
BladeShackRes = Enhancement("Free",219, 282, Medium)
BurstDestroyAnotherOrb = Enhancement("Splash",226, 283)
HpPotChanceFor2 = Enhancement("Potted",227, 284, Medium)
DestroyOrbOpposingElement = Enhancement("ElementX",228, 285)
TargetNearbyOrbsChainAttack = Enhancement("Splash",229, 286, Medium)
TargetDamagedNonOpposingElement = Enhancement("Splash",230, 287)
StenchRes = Enhancement("Anosmic",231, 288, Medium)
HPPotOnHitAgain = Enhancement("Potter",227, 289)
BladeComboOrbAdder = Enhancement("Orbs",234,290, Medium)
EvadeDriverArt = Enhancement("Evader",32, 292)
RetainAggro = Enhancement("Grudge",235, 293, Medium)
DamageUpOnDeath = Enhancement("Martyr",238, 295, Large)
AutoSpeedArtsSpeed= Enhancement("Lightning",240, 296, Small, Small)
LV4EachUseDmageUp = Enhancement("Glow",241, 297, Large)
Vision = Enhancement("Monado",242, 298, Medium, ReverseOdds=True)
AwakenPurge = Enhancement("Sleepy",243, 299, Medium)
PartyCritMaxAffinity = Enhancement("Critical",244, 300, Small)
DamageUpPerCrit = Enhancement("Exploit",245, 301, Mini)
RechargeOnEvade = Enhancement("Flicker",248, 304, Baby)
DamageAndEvadeAffinityMax = Enhancement("Counterattack",269, 305, Medium, Mini)
PartyLaunchDamageUp = Enhancement("Sky High",249, 306, Mega)
PotionPickupDamageUp = Enhancement("Drunkard",250, 307, Small)
ItemCollectionRange = Enhancement("Collector",251, 308, Mega)
CombatSpeed = Enhancement("Blitz",211, 309, Mega)
NullHealRes = Enhancement("Healers",252, 310, Medium)
DoomRes = Enhancement("Optimist",253, 311, Medium)
PartyDrainRes = Enhancement("Party",254, 312, Medium)
DealTakeMore = Enhancement("Reckless",255, 313, Medium, Medium)
AllDebuffRes = Enhancement("Dream",258, 316, Small)
DamageUpOnCancel = Enhancement("Rhythm",259, 317, Mini)
PurgeRage = Enhancement("Soothe",261, 318, Medium)
DamageAndCritUpMaxAffinity = Enhancement("Lucky",263, 320, Medium, Medium)
ReducesTerrainDamage = Enhancement("Weathered",264, 334, Medium)
SpecialRecievesAfterImage = Enhancement("Afterimage",213, 335, Baby)
EyeOfJustice = Enhancement("Eye of Shining Justice",236,294)
#There are some torna effects not including them recoverable hp.
