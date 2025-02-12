import JSONParser, Helper

def BladeElementsRandomization():
    # Regular Blades
    JSONParser.ChangeJSONFile(["common/CHR_Bl.json"], ["Atr"], Helper.InclRange(1, 8), Helper.InclRange(1, 8))

    # Poppi Default Element Cores
    JSONParser.ChangeJSONFile(["common/BTL_HanaChipset.json"], ["AtrParts"], Helper.InclRange(57001, 57008), Helper.InclRange(57001, 57008))

    # This makes it so any Poppi can use any element type.
    AllowAllPoppisFlag = dict()
    AllowAllPoppisFlag['JS'] = 1
    AllowAllPoppisFlag['JK'] = 1
    AllowAllPoppisFlag['JD'] = 1
    JSONParser.ChangeJSONLine(["common/ITM_HanaAtr.json"], [], ['Flag'], AllowAllPoppisFlag, replaceAll=True)