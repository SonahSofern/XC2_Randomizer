import JSONParser, Options

    
def RemoveFieldSkills():
    isAllChecks  = Options.RemoveFieldSkillsOption_AllFieldSkills.GetState()
    UMHUNT = Options.UMHuntOption.GetState()
    if isAllChecks or UMHUNT:
        mapGimmickIds = range(1,186)
        npcPopIds = range(1,50000)     
        jumpGimiickIds = range(1,45)
        tBoxIds = range(1,4000)
        diveIds = range(1,12)
    else:
        mapGimmickIds = [
            4, 5,           # Trees in early Gormott
            16,11,          # Vent/Valve in Gormott Titan Battleship
            36,             # Tardy Gate flood blockade
            7,              # Ether Miasma
            55, 57,         # Old Factory ventilation fans
            111,            # Spider Web
            113,            # Stele of Judgement
            37,             # World Tree Skyport
            129             # The Door
        ]
        npcPopIds = [
            8006,           # Green Barrel
            5267,           # Pyra's Cooking
            5268            # Pyra's Cooking
        ]    
        jumpGimiickIds = [
            34, 33,38,      # Cliffs of Morytha
            39,42           # Temperantia wind jump
        ]        
        
        tBoxIds = [] # No required treasure chests
        
        diveIds = [] # No required dive spots
    
    JSONParser.ChangeJSONLine(["common_gmk/FLD_MapGimmick.json"], mapGimmickIds, ["FSID"], 0)
    JSONParser.ChangeJSONLine(["common_gmk/FLD_JumpGimmick.json"], jumpGimiickIds, ["FSID"], 0)
    JSONParser.ChangeJSONLine(["common_gmk/FLD_WarpGimmick.json"], diveIds, ["FSID"], 0)
    for i in range(51):
        JSONParser.ChangeJSONLine([f"common_gmk/ma{i:02}a_FLD_NpcPop.json"], npcPopIds, ["FSID1", "FSID2", "FSID3"], 0)
        JSONParser.ChangeJSONLine([f"common_gmk/ma{i:02}a_FLD_TboxPop.json"], tBoxIds, ["FSID", "FSID2"], 0)

