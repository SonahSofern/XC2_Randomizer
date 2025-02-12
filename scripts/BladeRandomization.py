import copy, random, JSONParser, Helper, Options
# TODO:
#  - Replace the text "Make Nia a Driver" with "Turn {Blade}} into Nia"
#  - Replace the text "Make Nia a Blade" with "Turn Nia into {Blade}"
#  - Replace "Switch to Pyra?" and "Switch to Mythra" menu text
#     - Only do these if blade Nia was actually replaced with something that isn't Blade Nia
#  - Replace "Pandoria" on Zeke's Unleash Shining Justice skill
#  - Probably various other menu texts
#  - Randomize Poppi Forms
#  - Figure out how to randomize Torna blades properly (Apparently NoBuildWpn in CHR_Bl is not sufficient)
#  - Blade names should be replaced in all dialogs where possible
#  - Cosmetics do not work
#  - Replace driver voice lines when changing blades (Rex will currently shout "Pyra" when switching to Pyra's replacement)
#  - Replace field skill voice lines (Pyra's replacement currently says "I bring upon the power of fire!" in Pyra's voice)

OriginalBlades = dict()        # Maps Blade ID to the dictionary of the unrandomized blade date. Populated in PopulateBlades()
BladeNames = dict()            # Maps ID to Blade Name. Populated in PopulateBlades()
Original2Replacement = dict()  # Maps Unrandomized Blade ID to Randomized Blade ID. Populated in RandomizeBlades()
Replacement2Original = dict()  # Maps Randomized Blade ID to Unrandomized Blade ID. Populated in RandomizeBlades()

BladesRexCantUse = []
BladesNiaCantUse = [1001, 1002, 1009, 1010, 1011]
BladesMoragCantUse = [1001, 1002, 1010, 1011]
BladesZekeCantUse = [1001, 1002, 1009, 1011]

# Specifically, these are healers which have a healing halo equivalent move. So Twin Rings and Bitballs
# TODO: How does this work when considering randomized art effects?
GuaranteedHealer = None
RexHealerBlades = [1011]
NiaHealerBlades = [1004, 1021, 1033, 1038, 1041, 1107, 1109, 1111] # + Obrona if we can get NG+ Blades working without the weapon chip quirks
PossibleGuaranteedHealerBlades = RexHealerBlades + NiaHealerBlades

PoppiForms = [1005, 1006, 1007]

# Note: Every Blade besides Roc is randomizable. Roc being randomized would mess up Vandham, and he's exclusive to Rex anyway so may as well keep it that way.
# The NG+ Exclusive blades cannot use weapon chips, so they cannot be randomized in Race Mode (where their chips are defined by the save file). Exclude those blades in Race Mode to account for this
BladesAlwaysRandomized = [1001, 1002, 1009, 1010, 1011, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1050, 1104, 1105, 1106, 1107, 1108, 1109, 1111]
NewGamePlusBlades = [1043, 1044, 1045, 1046, 1047, 1048, 1049] # Currently cannot be randomized, but I would like to figure this out eventually. Will be an option when that works though, because they would be unbalanced if you get them early on

include_printouts = False  # Debugging

def BladeRandomization():
    InitialSetup()

    BugFixes_PreRandomization()
    RandomizeBlades()
    # RandomizePoppiForms() # TODO
    BugFixes_PostRandomization()

    # FinalTouches() #TODO


def InitialSetup():
    JSONParser.ChangeJSONLineWithCallback(["common/CHR_Bl.json"], [], PopulateBlades, replaceAll=True)
    JSONParser.ChangeJSONLineWithCallback(["common/BTL_Arts_Dr.json"], [], MakeAllArtsAccessible, replaceAll=True)


def PopulateBlades(blade):
    blade_id = blade['$id']
    OriginalBlades[blade_id] = dict()
    for key, value in blade.items():
        OriginalBlades[blade_id][key] = blade[key]

    Name = ''
    name_id = blade['Name']

    def getName(row):
        nonlocal Name
        Name = row['name']
    JSONParser.ChangeJSONLineWithCallback(["common_ms/chr_bl_ms.json"], [name_id], getName)

    BladeNames[blade_id] = Name


def MakeAllArtsAccessible(art):
    # Sets all arts to be unlocked at level 1.
    # In a normal playthrough, these arts only really matter for Broadsword and Aegis Sword, as those
    # are the only weapons can possibly use this early. However, a handful of arts have high enough
    # requirements that Rex can't use it if randomization gives him something like Brighid or Pandoria
    # early on. For simplicity and potential future-proofing, just set all arts to level 1 besides the
    # Broadsword. It is desirable that the Junk Sword still behaves as intended prior to Rex getting
    # his first blade.
    if art['WpnType'] not in [17]: # Broadsword
        for i in Helper.InclRange(1,5):
            art['ReleaseLv' + str(i)] = 1


def BugFixes_PreRandomization():
    # Replace Dagas 1022 with Dagas 1050 in gacha table. Since they are different blades, they could randomize weirdly.
    # For the purposes of this randomizer, 1022 is inaccessible
    JSONParser.ChangeJSONLine(["common/BLD_RareList.json"], [7], ['Blade'], 1050)


def RandomizeBlades():
    # Determine the guaranteed healer, if specified
    if Options.BladesOption_Healer.GetCheckBox():
        global GuaranteedHealer

        # If Dromarch isn't randomized, he's the healer by default
        if not Options.BladesOption_Dromarch.GetCheckBox():
            GuaranteedHealer = 1004
            if include_printouts:
                print("The guaranteed healer is Dromarch (by default).")
        else:
            potential_healers = PossibleGuaranteedHealerBlades.copy()
            random.shuffle(potential_healers)
            GuaranteedHealer = potential_healers[0]
            if include_printouts:
                print("The guaranteed healer is " + BladeNames[GuaranteedHealer])

    # Note: It is important that BladesLeftToRandomize starts with the default blades,
    # as otherwise the below loop could be stuck indefinitely if the last replacement is incompatible
    blades_left_to_randomize = BladesAlwaysRandomized.copy()

    # Only add Dromarch to the pool if explicitly randomizing him
    if Options.BladesOption_Dromarch.GetCheckBox():
        blades_left_to_randomize = [1004] + blades_left_to_randomize

    # TODO: Re-add this once NG+ blades' weapon chips work properly
    # if not OptionsRunDict["Blades"]["subOptionObjects"]["Include NG+ Blades"]["subOptionTypeVal"]:
    #    blades_left_to_randomize = blades_left_to_randomize + NewGamePlusBlades
    randomized_order = blades_left_to_randomize.copy()
    random.shuffle(randomized_order)

    # Determine the randomization prior to randomizing.
    # This way we can populate Original2Replacement and Replacement2Original,
    # which will be needed later on for various reasons
    while blades_left_to_randomize:
        next_blade = blades_left_to_randomize[0]
        next_replacement = randomized_order[0]
        if canBeReplaced(next_blade, next_replacement):
            Original2Replacement[next_blade] = next_replacement
            Replacement2Original[next_replacement] = next_blade
            if include_printouts:
                print('========================================')
                print(BladeNames[next_blade] + ' was replaced with ' + BladeNames[next_replacement])
                print(str(next_blade) + ' was replaced with ' + str(next_replacement))
            del blades_left_to_randomize[0]
            del randomized_order[0]
        else:
            # Next blade doesn't work, randomize again
            random.shuffle(randomized_order)

    # Apply Randomizations
    JSONParser.ChangeJSONLineWithCallback(["common/CHR_Bl.json"], [], ApplyBladeRandomization, replaceAll=True)


def canBeReplaced(original, replacement):
    # Handle the case of having the guaranteed healer
    if Options.BladesOption_Healer.GetCheckBox():
        if (original == 1001 and GuaranteedHealer in RexHealerBlades) or \
           (original == 1004 and GuaranteedHealer in NiaHealerBlades):
            return replacement == GuaranteedHealer

    # Handle cases where arts wouldn't be defined for the replacement
    # Note: Rex can be the master driver, so it's fine if his blades get randomized to whoever.
    if original == 1004: # Dromarch
        return replacement not in BladesNiaCantUse
    if original in [1009, 1014]: # Brighid and Aegeaon
        return replacement not in BladesMoragCantUse
    if original == 1010: # Pandoria
        return replacement not in BladesZekeCantUse

    return True


def ApplyBladeRandomization(blade):
    # Certain field skills are not randomized for progression reasons
    excluded_field_skills = dict()
    excluded_field_skills[1001] = ['FSkill1', 'FSkill2', 'FSkill3']  # Pyra: Fire Mastery, Focus, Cooking
    excluded_field_skills[1005] = ['FSkill3']  # Poppi Alpha: Superstrength
    excluded_field_skills[1008] = ['FSkill2']  # Roc: Miasma Dispersal

    blade_id = blade['$id']
    if blade_id in Original2Replacement:
        replace_with_id = Original2Replacement[blade_id]

        # Copy all fields (except ID, ReleaseLock, and the excluded field skills)
        # from the replacement blade to the original blade
        for key, value in blade.items():
            if key in ['$id', 'ReleaseLock']:
                continue
            if blade_id in excluded_field_skills and key in excluded_field_skills[blade_id]:
                continue
            if key == 'Flag':
                for flag_key, flag_value in OriginalBlades[replace_with_id]['Flag'].items():
                    if flag_key in ['FreeEngage', 'NoMapRev']:
                        continue

                    blade['Flag'][flag_key] = OriginalBlades[replace_with_id]['Flag'][flag_key]
            else:
                blade[key] = OriginalBlades[replace_with_id][key]



def RandomizePoppiForms():
    print('TODO: RandomizePoppiForms()')
    # TODO: Randomize Poppi forms so they appear in a random order (such as QTpi in Ch2, then Alpha in Ch4, then QT after doing QTpi's side quest)
    # TODO: How do I make it so the poppiswaps are in the right spot?


def BugFixes_PostRandomization():
    JSONParser.ChangeJSONLineWithCallback(["common/CHR_EnArrange.json"], [], FixRandomizedEnemyBladeCrashes, replaceAll=True)
    JSONParser.ChangeJSONLineWithCallback(["common/EVT_cutscene_wp.json"], [], FixCutsceneCrashForNotHavingTwoWeapons, replaceAll=True)
    FixPandoriaSpriteAfterElpys()


# Unsure why, but it is possible for the game to crash when an enemy blade gets randomized (for example, Pandoria).
# Replace the enemy version of the blade with the blade who that enemy replaced.
# TODO: Investigate the crash and see if it becomes possible to resolve while preserving the randomization. It would be
#       cool to fight against Zeke with Pandoria replaced with something else. But for now, this is not the case.
def FixRandomizedEnemyBladeCrashes(enemy):
    if enemy['BladeID'] in Replacement2Original:
        if include_printouts:
            print("Enemy: " + BladeNames[enemy['BladeID']] + " (" + str(enemy['BladeID']) + ") was replaced with " + BladeNames[Replacement2Original[enemy['BladeID']]] + " (" + str(Replacement2Original[enemy['BladeID']]) + ")")
        enemy['BladeID'] = Replacement2Original[enemy['BladeID']]


# When randomizing blades, there is a bug where cutscenes will crash when attempting to load. This is caused because in 2 ways
# 1. A blade which uses dual-wield weapons is replaced with a blade which does not. The cutscene tries to load the offhand
#    weapon, which does not exist, and so the game crashes
# 2. A blade's weapon has a special animation or model which the replaced weapon does not support. For example, Brighid's
#    whipsword has special properties due to how it extends. Replacing this with a different weapon can cause crashes.
# To fix these bugs, this cutscene replaces all weapon resources with the weapons of the original blade who was supposed
# to appear in that cutscene. For safety, all single-hand weapons are written to both the left and right hand resource
# slots to ensure things are always defined.
def FixCutsceneCrashForNotHavingTwoWeapons(cutscene):
    original = cutscene['blade']

    # Bail if this blade was not randomized
    if original not in Original2Replacement:
        return

    # Replace resources with weapon type of the blade who replaced the original
    replacement = Original2Replacement[original]
    cutscene['resourceL'] = WeaponType2Resource(OriginalBlades[replacement]['WeaponType'], 'L')
    cutscene['resourceR'] = WeaponType2Resource(OriginalBlades[replacement]['WeaponType'], 'R')


# side is either 'L' or 'R' (case doesn't matter).
def WeaponType2Resource(weapon_type, side):

    base_string = 'wp' + str(weapon_type).zfill(2) + '0101'

    two_handed_weapons = [3, 5, 7, 9, 16, 22, 23, 25, 26, 30, 32, 34, 35]
    if weapon_type in two_handed_weapons:
        return base_string + '_' + side[0].lower()
    else:
        return base_string

# Pandoria's menu icon and portrait changes at some point in chapter 7. Her glasses go from opaque to transparent.
# When this happens, the icon and portrait would replace whichever blade replaced her.
# This function replaces the transparent glasses images with images for whoever replaced Pandoria
def FixPandoriaSpriteAfterElpys():
    # Get the still of the blade which replaced Pandoria
    pandoria_replacement_still = OriginalBlades[Original2Replacement[1010]]['Still']

    # Use the still to find the icon index of the blade which replaced Pandoria
    icon_index = JSONParser.QueryJSONLine("common/MNU_IconList.json", "$id", pandoria_replacement_still)["icon_index"]

    # Fix the small icon for Pandoria's replacement. Row 261 corresponds to Pandoria's icon with transparent glasses
    JSONParser.ChangeJSONLine(["common/MNU_IconList.json"], [261], ['icon_index'], icon_index)

    # Get the blade image for Pandoria's replacement
    # This includes both the File ID and scaling/cropping information of the image
    PandoriaReplacementImageRow = JSONParser.QueryJSONLine("common/MNU_BlImageID.json", "icon_id", pandoria_replacement_still)

    # Grab the file name from the File ID
    fileName = JSONParser.QueryJSONLine("common/MNU_Stream_full_bl.json", "$id", PandoriaReplacementImageRow['$id'])['filename']

    # Replace the image for Pandoria with her replacement's image. Row 50 corresponds to Pandoria's portrait with transparent glasses
    JSONParser.ChangeJSONLine(["common/MNU_Stream_full_bl.json"], [50], ['filename'], fileName)

    # Fix the cropping of the image of Pandoria's replacement. Row 50 corresponds to Pandoria's portrait with transparent glasses
    for field in ['offs_x', 'offs_y', 'scale', 'offs_x2', 'offs_y2', 'scale2', 'offs_x3', 'offs_y3', 'scale3', 'offs_x4', 'offs_y4', 'scale4', 'offs_x5', 'offs_y5', 'scale5']:
        JSONParser.ChangeJSONLine(["common/MNU_BlImageID.json"], [50], [field], PandoriaReplacementImageRow[field])

def FinalTouches():
    # This function is a placeholder for all the small things. Menu text, etc. Not yet implemented
    print('TODO: FinalTouches()')
