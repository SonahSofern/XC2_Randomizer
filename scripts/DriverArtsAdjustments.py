import Helper, JSONParser
from IDs import *

def RandomizeReactions(OptionsRunDict):
    # Randomizes all hits of all arts
    JSONParser.ChangeJSONFile(["common/BTL_Arts_Dr.json"], Helper.StartsWith("ReAct", 1,16), HitReactions, HitReactionDistribution, InvalidTargetIDs=AutoAttacks)

    # If only randomizing the final hit, remove randomized values on all but the final hit
    if OptionsRunDict["Driver Art Reactions"]['subOptionObjects']['Final Hit Only']['subOptionTypeVal'].get():
        artsWithNHits = {}
        for numHits in range (1,17):
            artsWithNHits[numHits] = []
        for artID, numHits in zip(Arts, ArtNumHits):
            artsWithNHits[numHits].append(artID)

        # For efficiency, call the JSON Parser as few times as possible. In this case, at most 16, one for each possible number of arts
        # It ends up being slightly less than 16, as for example there are no arts with 14 hits
        for numHits in range (1,17):
            artIDs = artsWithNHits[numHits]
            if len(artIDs) > 0:
                keysToReplace = []
                for hit in range(1, numHits):
                    keysToReplace.append('ReAct' + str(hit))
                if len(keysToReplace) > 0:
                    JSONParser.ChangeJSONLine(["common/BTL_Arts_Dr.json"], artIDs, keysToReplace, 0)