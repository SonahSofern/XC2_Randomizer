import random, JSONParser, Helper

from IDs import BladeArts

def BladeArtsRandomization():
    # Regular Blades
    JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], Helper.StartsWith("NArts", 1, 3), BladeArts, BladeArts)

    # Poppi Default Blade Arts
    PoppiBladeArts = Helper.InclRange(59001, 59045)
    random.shuffle(PoppiBladeArts)
    def ReplacePoppiChipset(poppi):
        for i in Helper.InclRange(1, 3):
            if poppi['NArtsParts' + str(i)]:
                poppi['NArtsParts' + str(i)] = PoppiBladeArts[0]
                del PoppiBladeArts[0]
    JSONParser.ChangeJSONLineWithCallback(["common/BTL_HanaChipset.json"], [], ReplacePoppiChipset, replaceAll=True)