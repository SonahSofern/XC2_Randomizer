import random, JSONParser, Helper

from IDs import WeaponTypeRoles

def BladeWeaponClassRandomization():
    # Regular Blades
    JSONParser.ChangeJSONFile(["common/ITM_PcWpnType.json"], ["Role"], Helper.InclRange(1, 3), WeaponTypeRoles)

    # Poppi Default Roles
    JSONParser.ChangeJSONFile(["common/BTL_HanaChipset.json"], ["RoleParts"], Helper.InclRange(56001, 56036), Helper.InclRange(56001, 56036))
