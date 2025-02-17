import JSONParser, Helper, Options, copy, random

Name2Elem = dict()
OriginalID2Name = dict()

# First key is ComboStage. Second key is name. Content is dictionary of original bdat
OriginalCombos = {
    1: dict(),
    2: dict(),
    3: dict()
}

# Key is ID. This is used to look up the entire route when randomizing combos 2 and 3
ReplacedCombos = dict()
ReplacedComboRoutes = list()

CustomLevel2s = list()
BaseLevel3s = list()
CustomLevel3Templates = dict() # Key is element


class CustomLevel2Combo:
    def __init__(self, name, elemRoute, baseName, tier3adjectives):
        random.shuffle(tier3adjectives)
        self.elemRoute = list()
        for elem in elemRoute:
            self.elemRoute.append(Name2Elem[elem])
        self.name = name
        self.base = copy.deepcopy(OriginalCombos[2][baseName])
        self.tier3adjectives = tier3adjectives

        CustomLevel2s.append(self)


class Level3Combo:
    def __init__(self, name, elemRoute):
        self.name = name
        self.elemRoute = elemRoute
        self.base = copy.deepcopy(OriginalCombos[3][name])

        BaseLevel3s.append(self)


class CustomLevel3ComboTemplate:
    def __init__(self, elem, nameNouns, baseNames):
        # Shuffle the names and bases while making sure the indices still correspond with each other
        combined = list(zip(nameNouns, baseNames))
        random.shuffle(combined)
        nameNouns_shuffled, baseNames_shuffled = zip(*combined)
        nameNouns = list(nameNouns_shuffled)
        baseNames = list(baseNames_shuffled)
        self.elem = Name2Elem[elem]
        self.nameNouns = nameNouns
        self.bases = list()
        for baseName in baseNames:
            self.bases.append(copy.deepcopy(OriginalCombos[3][baseName]))

        CustomLevel3Templates[self.elem] = self


def BladeComboRandomization():
    PopulateMaps()

    if Options.BladeCombosOption_ElementRoutes.GetState():
        CreateCustomCombos()
        RandomizeElementRoutes()
    if Options.BladeCombosOption_AOE.GetState():
        RandomizeAOE()
    if Options.BladeCombosOption_DOT.GetState():
        RandomizeDOT()
    if Options.BladeCombosOption_Damage.GetState():
        RandomizeDamage()
    if Options.BladeCombosOption_Reactions.GetState():
        RandomizeReactions()


def CreateCustomCombos():
    # Every combination of first 2 stages are defined with a custom name.
    # Some of these already exist in the base game and are duplicated here for convenience
    # Each custom combo has a "base" of an existing blade combo. It copies all damage, animations, etc. of that base
    # Each custom combo also contains 2 adjectives which become the beginning of the following stage 3's names
    CustomLevel2Combo('Burnout', ['Fire', 'Fire'], 'Burnout', ['Scorching', 'Searing'])
    CustomLevel2Combo('Steam Bomb', ['Fire', 'Water'], 'Steam Bomb', ['Steamy', 'Hydrothermal'])
    CustomLevel2Combo('Ember Quake', ['Fire', 'Earth'], 'Volcano', ['Smoldering', 'Techtonic'])
    CustomLevel2Combo('Plasma Flare', ['Fire', 'Electric'], 'Flame Bolt', ['Electrified', 'Plasmatic'])
    CustomLevel2Combo('Frostfire', ['Fire', 'Ice'], 'Burnout', ['Pyrofrigid', 'Frostburning'])
    CustomLevel2Combo('Blazing Zephyr', ['Fire', 'Wind'], 'Cyclone', ['Fervent', 'Blistering'])
    CustomLevel2Combo('Hellfire', ['Fire', 'Dark'], 'Volcano', ['Infernal', 'Malevolent'])
    CustomLevel2Combo('Solar Flare', ['Fire', 'Light'], 'Gamma Ray', ['Incandescent', 'Glimmering'])
    CustomLevel2Combo('Boiling Point', ['Water', 'Fire'], 'Steam Bomb', ['Scalding', 'Simmering'])
    CustomLevel2Combo('Venom Water', ['Water', 'Water'], 'Venom Water', ['Venomous', 'Toxic'])
    CustomLevel2Combo('Pandemic', ['Water', 'Earth'], 'Pandemic', ['Infectious', 'Virulent'])
    CustomLevel2Combo('Conductivity', ['Water', 'Electric'], '1,000,000 Volt', ['Voltaic', 'Cascading'])
    CustomLevel2Combo('Glacier Surge', ['Water', 'Ice'], 'Freeze', ['Arctic', 'Bleak'])
    CustomLevel2Combo('Maelstrom Gale', ['Water', 'Wind'], 'Ice Wind', ['Tropical', 'Nautical'])
    CustomLevel2Combo('Abyssal Tide', ['Water', 'Dark'], 'Black Abyss', ['Abyssal', 'Dismal'])
    CustomLevel2Combo('Holy Rain', ['Water', 'Light'], 'Steam Bomb', ['Sacred', 'Celestial'])
    CustomLevel2Combo('Volcano', ['Earth', 'Fire'], 'Volcano', ['Volcanic', 'Eruptive'])
    CustomLevel2Combo('Mudslide', ['Earth', 'Water'], 'Venom Water', ['Raging', 'Corrosive'])
    CustomLevel2Combo('Gaia Crash', ['Earth', 'Earth'], 'Gaia Crash', ['Primordial', 'Continental'])
    CustomLevel2Combo('Aftershock', ['Earth', 'Electric'], 'Flame Bolt', ['Seismic', 'Jolting'])
    CustomLevel2Combo('Glacial Rift', ['Earth', 'Ice'], 'Freeze', ['Glacial', 'Fractured'])
    CustomLevel2Combo('Dust Devil', ['Earth', 'Wind'], 'Cyclone', ['Earth-Shattering', 'Atmospheric'])
    CustomLevel2Combo('Tombstone', ['Earth', 'Dark'], 'Gaia Crash', ['Undead', 'Necromantic'])
    CustomLevel2Combo('Earthlight', ['Earth', 'Light'], 'Gamma Ray', ['Resplendent', 'Luminous'])
    CustomLevel2Combo('Flame Bolt', ['Electric', 'Fire'], 'Flame Bolt', ['Pyrocharged', 'Sparking'])
    CustomLevel2Combo('Shockwave', ['Electric', 'Water'], 'Pandemic', ['Sparkling', 'Surging'])
    CustomLevel2Combo('Voltquake', ['Electric', 'Earth'], 'Gaia Crash', ['Voltanic', 'Quaking'])
    CustomLevel2Combo('1,000,000 Volt', ['Electric', 'Electric'], '1,000,000 Volt', ['Dynamic', 'Overcharged'])
    CustomLevel2Combo('Cryocharge', ['Electric', 'Ice'], 'Lightning Bolt', ['Cryogenic', 'Electrochilled'])
    CustomLevel2Combo('Cumulonimbus ', ['Electric', 'Wind'], 'Lightning Bolt', ['Galvanic', 'Turbulent'])
    CustomLevel2Combo('Shadow Spark', ['Electric', 'Dark'], 'Pandemic', ['Umbral', 'Flickering'])
    CustomLevel2Combo('Radiant Charge', ['Electric', 'Light'], 'Gamma Ray', ['Luminescent', 'Vibrant'])
    CustomLevel2Combo('Scorched Frost', ['Ice', 'Fire'], 'Burnout', ['Frostburned', 'Chillscorched'])
    CustomLevel2Combo('Cold Snap', ['Ice', 'Water'], 'Cold Snap', ['Brisk', 'Frigid'])
    CustomLevel2Combo('Permafrost', ['Ice', 'Earth'], 'Freeze', ['Cryolithic', 'Icelocked'])
    CustomLevel2Combo('Frozen Current', ['Ice', 'Electric'], 'Lightning Bolt', ['Nordic', 'Frantic'])
    CustomLevel2Combo('Freeze', ['Ice', 'Ice'], 'Freeze', ['Freezing', 'Frosty'])
    CustomLevel2Combo('Hailstorm', ['Ice', 'Wind'], 'Cold Snap', ['Wintry', 'Blustery'])
    CustomLevel2Combo('Frostbite', ['Ice', 'Dark'], 'Ice Wind', ['Numbing', 'Absolute'])
    CustomLevel2Combo('Diamond Flash', ['Ice', 'Light'], '1,000,000 Volt', ['Brilliant', 'Prismatic'])
    CustomLevel2Combo('Firestorm', ['Wind', 'Fire'], 'Volcano', ['Roaring', 'Incendiary'])
    CustomLevel2Combo('Rainstorm', ['Wind', 'Water'], 'Steam Bomb', ['Torrential', 'Pluvial'])
    CustomLevel2Combo('Sand Strike', ['Wind', 'Earth'], 'Gaia Crash', ['Swirling', 'Howling'])
    CustomLevel2Combo('Thunderstorm', ['Wind', 'Electric'], '1,000,000 Volt', ['Thunderous', 'Destructive'])
    CustomLevel2Combo('Ice Wind', ['Wind', 'Ice'], 'Ice Wind', ['Squalling', 'Gusty'])
    CustomLevel2Combo('Cyclone', ['Wind', 'Wind'], 'Cyclone', ['Jet Stream', 'Whirling'])
    CustomLevel2Combo('Twilight Tempest', ['Wind', 'Dark'], 'Ray of Light', ['Ruinous', 'Freudian'])
    CustomLevel2Combo('Aurora Gale', ['Wind', 'Light'], 'Cold Snap', ['Ethereal', 'Heavenly'])
    CustomLevel2Combo('Campfire ', ['Dark', 'Fire'], 'Burnout', ['Dire', 'Harsh'])
    CustomLevel2Combo('Deep Ocean', ['Dark', 'Water'], 'Venom Water', ['Drenched', 'Drowning'])
    CustomLevel2Combo('Obsidian Rift', ['Dark', 'Earth'], 'Black Abyss', ['Obsidian', 'Gravitational'])
    CustomLevel2Combo('Nocturnal Surge', ['Dark', 'Electric'], 'Ray of Light', ['Quantum', 'Apocalyptic'])
    CustomLevel2Combo('Black Ice', ['Dark', 'Ice'], 'Venom Water', ['Chilling', 'Sinister'])
    CustomLevel2Combo('Midnight Gale', ['Dark', 'Wind'], 'Black Abyss', ['Haunting', 'Nocturnal'])
    CustomLevel2Combo('Black Abyss', ['Dark', 'Dark'], 'Black Abyss', ['Dark', 'Pitchblack'])
    CustomLevel2Combo('Ray of Light', ['Dark', 'Light'], 'Ray of Light', ['Blinding', 'Unholy'])
    CustomLevel2Combo('Solar Wrath', ['Light', 'Fire'], 'Flame Bolt', ['Radiant', 'Furious'])
    CustomLevel2Combo('Atlantis', ['Light', 'Water'], 'Cold Snap', ['Iridescent', 'Neptunian'])
    CustomLevel2Combo('Shooting Star', ['Light', 'Earth'], 'Ray of Light', ['Terrestrial', 'Gaian'])
    CustomLevel2Combo('Lightning Bolt', ['Light', 'Electric'], 'Lightning Bolt', ['Electrifying', 'Swift'])
    CustomLevel2Combo('Glacial Gleam', ['Light', 'Ice'], 'Ice Wind', ['Lustrous', 'Crystalline'])
    CustomLevel2Combo('Solar Wind', ['Light', 'Wind'], 'Cyclone', ['Heaven\'s', 'Windswept'])
    CustomLevel2Combo('Luminous Dusk', ['Light', 'Dark'], 'Pandemic', ['Midnight', 'Interstellar'])
    CustomLevel2Combo('Gamma Ray', ['Light', 'Light'], 'Gamma Ray', ['Illuminating', 'Spectral'])

    # Since there are 512 possible combinations, I'm not creating names for all stage 3s
    # Instead, the first 2 stages determine an adjective. The element types determine possible nouns. Combine the 2 to form a new combo name
    CustomLevel3ComboTemplate('Fire', ['Inferno', 'Blaze', 'Explosion', 'Combustion', 'Conflagration'], ['Volcanic Storm', 'Mega Explosion', 'Mega Explosion', 'Nuclear Blast', 'Mega Eruption'])
    CustomLevel3ComboTemplate('Water', ['Tsunami', 'Torrent', 'Maelstrom', 'Riptide', 'Undertow'], ['Steam Explosion', 'Electrolysis', 'Electrolysis', 'Steam Explosion', 'Splash Hazard'])
    CustomLevel3ComboTemplate('Earth', ['Landslide', 'Fissure', 'Fracture', 'Ragnarök', 'Earthquake '], ['Splash Hazard', 'Mega Eruption', 'Nuclear Blast', 'Meteorite', 'Lightning Quake'])
    CustomLevel3ComboTemplate('Electric', ['Electrocution', 'Voltage', 'Surge', 'Lightning', 'Fulmination'], ['Lightning Quake', 'Heaven\'s Bolt', 'Ruinous Weather', 'Heaven\'s Bolt', 'Ultimate Aurora'])
    CustomLevel3ComboTemplate('Ice', ['Avalanche', 'Blizzard', 'Fimbulvetr', 'Glacier', 'Cryofreeze'], ['Frost Typhoon', 'Diamond Mist', 'Dead of Winter', 'Permafrost Crash', 'Gravity Blizzard'])
    CustomLevel3ComboTemplate('Wind', ['Whirlwind', 'Hurricane', 'Twister', 'Zephyr', 'Tornado'], ['Final Disaster', 'Thunder Gale', 'Electrofire Storm', 'Dead of Winter', 'Sandstorm'])
    CustomLevel3ComboTemplate('Dark', ['Eclipse', 'Nightfall', 'Void', 'Poltergeist', 'Nosferatu'], ['Hyper Graviton', 'Dark Tide', 'Dark Tide', 'Hyper Graviton', 'Gravity Blizzard'])
    CustomLevel3ComboTemplate('Light', ['Corona', 'Beacon', 'Nova', 'Flash', 'Quazar'], ['Second Sun', 'Supernova', 'Second Sun', 'Ultimate Aurora', 'Supernova'])


def getCustomStage2Combo(elemRoute):
    for combo in CustomLevel2s:
        if combo.elemRoute == elemRoute:
            return combo
    return None


def getBaseStage3Combo(elemRoute):
    for combo in BaseLevel3s:
        if combo.elemRoute == elemRoute:
            return combo
    return None


def PopulateMaps():
    def getNames(combo):
        OriginalID2Name[combo['$id']] = combo['name']
    JSONParser.ChangeJSONLineWithCallback(["common_ms/BTL_ElementalCombo_ms.json"], [], getNames, replaceAll=True)

    def getCombos(combo):
        name = OriginalID2Name[combo['$id']]
        OriginalCombos[combo['ComboStage']][name] = combo
        if combo['ComboStage'] == 3 and combo['PreCombo'] != 0: # Note: PreCombo is 0 for the Torna combos (Heat III, Stone III, etc)
            stage3elem = combo['Atr']
            stage2combo = OriginalCombos[2][OriginalID2Name[combo['PreCombo']]]
            stage2elem = stage2combo['Atr']
            stage1combo = OriginalCombos[1][OriginalID2Name[stage2combo['PreCombo']]]
            stage1elem = stage1combo['Atr']
            Level3Combo(name, [stage1elem, stage2elem, stage3elem])
    JSONParser.ChangeJSONLineWithCallback(["common/BTL_ElementalCombo.json"], [], getCombos, replaceAll=True)

    def getElems(elem):
        # Note: -1 because the blade combo elements are offset by 1 for some reason (presumably as there is no "None" in blade combos)
        Name2Elem[elem['name']] = elem['$id']-1
    JSONParser.ChangeJSONLineWithCallback(["common_ms/menu_attr_ms.json"], Helper.InclRange(2,9), getElems)


def RandomizeElementRoutes():
    # Note: Debug names are set for 2 reasons:
    # 1. So I can understand the randomization as it's happening
    # 2. So we can iterate over ReplacedCombos once done to apply all the names at once

    RemainingTier1s = list(OriginalCombos[1].values())
    random.shuffle(RemainingTier1s)
    RemainingTier2Elements = list() # Initially empty, populated below in randomize()
    RemainingTier3Elements = list() # Initially empty, populated below in randomize()

    def randomize(combo):
        # Each potential randomization is lists of [1, 1, 2, 2, 3, 3, ...]
        # This ensures each element appears twice in the pool
        # This is not sufficient to account for all combos, so once the list runs out, populate the list again in the same way
        # This ensures that each element appears at least twice for each stage and prevents cases where the element does not appear at all
        nonlocal RemainingTier2Elements
        nonlocal RemainingTier3Elements
        if len(RemainingTier2Elements) == 0:
            RemainingTier2Elements = [i for i in Helper.InclRange(1, 8) for _ in range(2)]
            random.shuffle(RemainingTier2Elements)
        if len(RemainingTier3Elements) == 0:
            RemainingTier3Elements = [i for i in Helper.InclRange(1, 8) for _ in range(2)]
            random.shuffle(RemainingTier3Elements)

        # Skip Torna combos such as Heat II, Stone II, etc. (they should still work after randomization)
        if combo['ComboStage'] != 1 and combo['PreCombo'] == 0:
            return

        # For tier 1s, we just shuffle the list of tier 1s and reassign them
        if combo['ComboStage'] == 1:
            combo['DebugName'] = OriginalID2Name[RemainingTier1s[0]['$id']]
            for key, value in combo.items():
                if key not in ['$id', 'DebugName', 'Name']:  # Note: Name is excluded because we handle that ourselves down below
                    combo[key] = RemainingTier1s[0][key]
            del RemainingTier1s[0]

        # For tier 2s, we start by randomizing an element. Once we have the element,
        # we determine the custom combo based on the first and second stages.
        elif combo['ComboStage'] == 2:
            # Determine the next combo based on randomized tier 2 elements
            stage1Element = ReplacedCombos[combo['PreCombo']]['Atr']
            stage2Element = RemainingTier2Elements[0]
            comboRoute = [stage1Element, stage2Element]
            newCombo = getCustomStage2Combo(comboRoute)

            # If this combo has happened previously, shuffle the elements again
            while any(previousCombo == comboRoute for previousCombo in ReplacedComboRoutes):
                random.shuffle(RemainingTier2Elements)
                stage2Element = RemainingTier2Elements[0]
                comboRoute = [stage1Element, stage2Element]
                newCombo = getCustomStage2Combo(comboRoute)

            # Replace the combo
            combo['DebugName'] = newCombo.name
            combo['Atr'] = stage2Element
            for key, value in combo.items():
                if key not in ['$id', 'DebugName', 'Atr', 'PreCombo', 'Name']: # Note: Name is excluded because we handle that ourselves down below
                    combo[key] = newCombo.base[key]

            del RemainingTier2Elements[0]
            ReplacedComboRoutes.append(comboRoute)

        # For tier 3s, we start by randomizing an element. Once we have the element,
        # we determine the final combo based on the 5 combos possible for that element.
        # This final combo corresponds to the noun in the combo name. The prior 2 stages
        # of the combo determine the adjective which comes before this noun.
        elif combo['ComboStage'] == 3:
            # Determine the next combo based on randomized tier 2 elements
            stage2Combo = ReplacedCombos[combo['PreCombo']]
            stage1Combo = ReplacedCombos[stage2Combo['PreCombo']]
            stage1Element = stage1Combo['Atr']
            stage2Element = stage2Combo['Atr']
            stage2Combo = getCustomStage2Combo([stage1Element, stage2Element])
            stage3Element = RemainingTier3Elements[0]
            comboRoute = [stage1Element, stage2Element, stage3Element]

            # If this combo has happened previously, shuffle the elements again
            while any(previousCombo == comboRoute for previousCombo in ReplacedComboRoutes):
                random.shuffle(RemainingTier3Elements)
                stage3Element = RemainingTier3Elements[0]
                comboRoute = [stage1Element, stage2Element, stage3Element]

            # Create the new combo
            baseStage3Combo = getBaseStage3Combo(comboRoute)
            if baseStage3Combo is None: # Custom combo, create it
                stage3ComboTemplate = CustomLevel3Templates[stage3Element]
                newComboName = stage2Combo.tier3adjectives[0] + " " + stage3ComboTemplate.nameNouns[0]
                newComboBase = stage3ComboTemplate.bases[0]
                del stage3ComboTemplate.nameNouns[0]
                del stage3ComboTemplate.bases[0]
            else: # Combo that exists in the base game, just use that as is
                newComboName = baseStage3Combo.name
                newComboBase = baseStage3Combo.base

            # Replace the combo
            combo['DebugName'] = newComboName
            combo['Atr'] = stage3Element
            for key, value in combo.items():
                if key not in ['$id', 'DebugName', 'Atr', 'PreCombo', 'Name']:  # Note: Name is excluded because we handle that ourselves down below
                    combo[key] = newComboBase[key]

            del RemainingTier3Elements[0]
            del stage2Combo.tier3adjectives[0]
            ReplacedComboRoutes.append(comboRoute)

        ReplacedCombos[combo['$id']] = combo

    def updateNames(combo):
        if combo['$id'] in ReplacedCombos:
            combo['name'] = ReplacedCombos[combo['$id']]['DebugName']

    JSONParser.ChangeJSONLineWithCallback(["common/BTL_ElementalCombo.json"], [], randomize, replaceAll=True)
    JSONParser.ChangeJSONLineWithCallback(["common_ms/BTL_ElementalCombo_ms.json"], [], updateNames, replaceAll=True)


def RandomizeAOE():
    # Roughly half of the base combos have AoE.
    # Some have a range of 3 and others a range of 5. Unsure what happens if you do something outside of this. Not sure if 3 is a radius or an enumeration of some shape (line, circle, etc)
    def randomize(combo):
        coinFlip = random.randint(0, 1)
        if coinFlip:
            combo['Range'] = random.randint(3, 5)
        else:
            combo['Range'] = 0
    JSONParser.ChangeJSONLineWithCallback(["common/BTL_ElementalCombo.json"], [], randomize, replaceAll=True)


def RandomizeDOT():
    # Note: This function randomizes whether the combo is DoT or not.
    # This does NOT randomize the damage of the DoT. See RandomizeDamage() for that.

    def randomize(combo):
        # Stage 3 cannot have DOT
        if combo['ComboStage'] == 3:
            return

        # Determine probabilities for DoT
        if combo['ComboStage'] == 1: # 6/8 Stage 1s have a DoT. Match that distribution
            DotDistribution = [0, 0, 1, 1, 1, 1, 1, 1]
        else: # Must be ComboStage 2. 6/16 Stage 2s have a DoT. Match that distribution
            DotDistribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        hasDot = random.choice(DotDistribution)

        # Make no changes if randomization doesn't change the result
        if hasDot == combo['Dot']:
            return

        # Constants are guesstimates based on existing combos. Seems to work well
        DD_TO_DOT_SCALE = 3.8 # Used for converting DoT to no DoT and vice versa
        BASE_DOT_RATIO = 6.25 # Ratio of DoT to DD for DoT combos

        # Changing from Dot to No Dot. Increase base damage and remove DOT
        if combo['Dot']:
            combo['DD'] = round(combo['DD'] * DD_TO_DOT_SCALE)
            combo['Dot'] = 0
            combo['Interval'] = 0
        # Changing from No Dot to Dot. Decrease damage and add Dot
        else:
            combo['DD'] = round(combo['DD'] / DD_TO_DOT_SCALE)
            combo['Dot'] = round(combo['DD'] / BASE_DOT_RATIO)
            combo['Interval'] = 45 # All DoT combos use 45

    JSONParser.ChangeJSONLineWithCallback(["common/BTL_ElementalCombo.json"], [], randomize, replaceAll=True)


def RandomizeDamage():
    # For each combo, take the base damage and add +/- 25% for both Damage and DoT
    def randomize(combo):
        minDmg = combo['DD'] * 0.75
        maxDmg = combo['DD'] * 1.25
        minDoT = combo['Dot'] * 0.75
        maxDoT = combo['Dot'] * 1.25
        minDmgEn = combo['DDEn'] * 0.75
        maxDmgEn = combo['DDEn'] * 1.25
        minDoTEn = combo['DotEn'] * 0.75
        maxDoTEn = combo['DotEn'] * 1.25
        combo['DD'] = round(random.uniform(minDmg, maxDmg))
        combo['Dot'] = round(random.uniform(minDoT, maxDoT))
        combo['DDEn'] = random.uniform(minDmgEn, maxDmgEn)
        combo['DotEn'] = random.uniform(minDoTEn, maxDoTEn)
    JSONParser.ChangeJSONLineWithCallback(["common/BTL_ElementalCombo.json"], [], randomize, replaceAll=True)


def RandomizeReactions():
    def randomize(combo):
        # To add variety while maintaining general game balance, The probabilities are:
        # Stage 1s have a 1/32 chance of a reaction. 1/32 chance of Blowdown (31/32 chance of Knockback)
        # Stage 2s have a 1/8 chance of a reaction. 1/8 chance of Blowdown (7/8 chance of Knockback)
        # Stage 3s have a 1/2 chance of a reaction. 1/2 chance of Blowdown (1/2 chance of Knockback)
        maxRandom = 2*pow(4, 3-combo['ComboStage'])
        hasReaction = random.randint(1, maxRandom) == 1

        if hasReaction:
            # Reaction level has a floor of the combo stage. 3s should be stronger than 2s, on average
            combo['ReactionLv'] = random.randint(combo['ComboStage'], 5)
            hasBlowdown = random.randint(1, maxRandom) == 1
            if hasBlowdown:
                combo['Reaction'] = 2
            else: # Knockback instead
                combo['Reaction'] = 1
        else:
            combo['Reaction'] = 0
            combo['ReactionLv'] = 0

    JSONParser.ChangeJSONLineWithCallback(["common/BTL_ElementalCombo.json"], [], randomize, replaceAll=True)
