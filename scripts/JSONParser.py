import copy
import json, random, os, IDs

def ChangeJSONFile(Filename: list, keyWords: list, rangeofValuesToReplace:list = [], rangeValidReplacements:list = [], InvalidTargetIDs:list = [], SliderOdds = 100, IgnoreID_AND_Key = [["",""]]): # make this a function to reuse, check the settings ot see if we even do this

    # print(f"Valid Replacements: {Replacements}")
    SliderOdds = IDs.CurrentSliderOdds
    rangeValidReplacements.extend(IDs.ValidReplacements)
    rangeValidReplacements = [x for x in rangeValidReplacements if x not in IDs.InvalidReplacements]
    for name in Filename:
        filePath = "./_internal/JsonOutputs/" + name
        if not os.path.exists(filePath):
          #print(filePath + " filepath does not exist.")
          continue
        with open(filePath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for item in data['rows']:
                if item["$id"] in InvalidTargetIDs:
                    continue
                for key in item:  
                    if ([item["$id"], key] in IgnoreID_AND_Key):
                        continue       
                    if key in keyWords:
                        if (((rangeofValuesToReplace == []) or (item[key] in rangeofValuesToReplace)) and (SliderOdds >= random.randint(1,100))):
                            item[key] = random.choice(rangeValidReplacements)
                    elif key == "Flag":
                        for flag, flagVal in item[key].items():
                            if flag in keyWords:
                                if ((flagVal in rangeofValuesToReplace) and (SliderOdds >= random.randint(1,100))):
                                    item[key][flag] = random.choice(rangeValidReplacements)                                
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    IDs.ValidReplacements.clear()
    IDs.InvalidReplacements.clear()
    IDs.CurrentSliderOdds = 100


def ChangeJSONLine(filenames, ids, keys, replacement, replaceAll = False):
    for name in filenames:
        filePath = "./_internal/JsonOutputs/" + name
        if not os.path.exists(filePath):
          #print(filePath + " filepath does not exist.")
          continue
        with open(filePath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for item in data['rows']:
                if replaceAll or item["$id"] in ids:
                   for key in keys:
                    item[key] = replacement
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def ChangeJSONLineWithCallback(filenames, ids, callback, replaceAll = False):
    for name in filenames:
        filePath = "./_internal/JsonOutputs/" + name
        if not os.path.exists(filePath):
          continue
        with open(filePath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for item in data['rows']:
                if replaceAll or item["$id"] in ids:
                    callback(item)
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def QueryJSONLine(filename, searchField, searchVal):
        filePath = "./_internal/JsonOutputs/" + filename
        if not os.path.exists(filePath):
            return
        with open(filePath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for item in data['rows']:
                if item[searchField] == searchVal:
                    return item
        return None

def CopyJSONFile(filename):
    filePath = "./_internal/JsonOutputs/" + filename
    if not os.path.exists(filePath):
      return dict()
    with open(filePath, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        out = dict()
        for item in data['rows']:
            out[item['$id']] = dict()
            for key, value in item.items():
                if key == '$id':
                    continue
                out[item['$id']][key] = copy.deepcopy(value)
        return out

def PrintTable(filename):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(filename)
    filePath = "./_internal/JsonOutputs/" + filename
    if not os.path.exists(filePath):
        return
    with open(filePath, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for item in data['rows']:
            print(item)
    print()

def ExtendJSONFile(filePath, additionsList = []):
    with open("./_internal/JsonOutputs/" + filePath, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for item in additionsList:
            data["rows"].extend(item)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
        
        
def ReplaceJSONFile(filePath, replacement = []):
    with open("./_internal/JsonOutputs/" + filePath, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["rows"] = replacement
        file.seek(0)
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.truncate()