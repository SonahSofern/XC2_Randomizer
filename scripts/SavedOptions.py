saveFolderName = "SaveData"
import os, json, traceback, Options


def saveData(DataList, Filename):
    with open(f"{saveFolderName}/{Filename}", 'w') as file:
        sav= {}
        for saveData in DataList:
            sav.update({saveData.name: saveData.checkBoxVal.get()})
            if saveData.spinBoxVal != None:
                sav.update({f"{saveData.name} Spinbox: ": saveData.spinBoxVal.get()})
            for sub in saveData.subOptions:
                sav.update({f"{saveData.name}->{sub.name}": sub.checkBoxVal.get()})
        json.dump(sav, file, indent=4, ensure_ascii=True)


            
def loadData(DataList, Filename):
    try:
        os.makedirs(saveFolderName, exist_ok=True)
        with open(f"{saveFolderName}/{Filename}", 'r') as file:
            data = json.load(file)
            for option in DataList:
                try:
                    option.checkBoxVal.set(data[option.name])
                except:
                    pass
                try:
                    option.spinBoxVal.set(data[f"{option.name} Spinbox: "])
                except:
                    pass
                for sub in option.subOptions:
                    try:
                        sub.checkBoxVal.set(data[f"{option.name}->{sub.name}"])
                        option.StateUpdate()
                    except:
                        pass
    except:
        pass # The file is created upon closing the window so it will error initial launch
    # except Exception as error:
    #             print(f"{traceback.format_exc()}") # shows the full error

class SavedEntry:
    def __init__(self, _name, _val):
        self.name =_name
        self.checkBoxVal = _val # Polymorphism with the Option Class
        self.subOptions = []
        self.spinBoxVal = None
    def StateUpdate(self): # Used so loadData doesnt care
        pass
    