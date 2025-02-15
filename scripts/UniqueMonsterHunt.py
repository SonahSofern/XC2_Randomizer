import json, random, Helper, IDs, EnemyRandoLogic, RaceMode, math, Options
from Enhancements import *
from collections import OrderedDict

#Keeping these 3 separate from the already existing IDs in EnemyRandoLogic in case I want to do some balancing or something
AllUniqueMonsterDefaultIDs = [611, 612, 705, 706, 707, 708, 709, 710, 711, 712, 713, 715, 736, 738, 808, 809, 810, 811, 812, 814, 815, 816, 817, 819, 890, 891, 892, 893, 894, 895, 896, 898, 899, 926, 929, 953, 954, 955, 957, 958, 1019, 1020, 1023, 1025, 1026, 1101, 1102, 1104, 1106, 1108, 1109, 1111, 1112, 1113, 1114, 1115, 1131, 1132, 1134, 1155, 1156, 1157, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1255, 1256, 1258, 1260, 1261, 1262, 1264, 1265, 1563, 1564, 1566, 1567, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1670, 1774]
AllSuperBossDefaultIDs = [247, 714, 928, 1022, 1027, 1110, 1135, 1137, 1189, 1559, 1560, 1561, 1562, 1723, 1756, 1758, 1759, 1763, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1775, 1776, 1777, 1778, 1779, 1783, 1784, 1785, 1786, 1792, 1793, 1794, 1795, 1800, 1802, 1803, 1804, 1808, 1809, 1811, 1812, 1813, 1814, 1886]
AllNormalEnemyDefaultIDs = [313, 315, 339, 413, 476, 521, 523, 555, 568, 630, 631, 632, 633, 634, 638, 645, 646, 647, 648, 651, 652, 653, 655, 656, 659, 660, 662, 664, 665, 666, 668, 675, 676, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 691, 692, 694, 695, 699, 701, 703, 716, 717, 718, 719, 720, 721, 722, 723, 729, 730, 731, 732, 734, 749, 756, 757, 758, 762, 763, 764, 766, 771, 772, 773, 774, 794, 795, 796, 798, 800, 802, 804, 806, 825, 835, 843, 844, 847, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 865, 867, 868, 869, 870, 872, 873, 874, 875, 876, 877, 879, 880, 881, 882, 884, 886, 888, 901, 902, 903, 904, 905, 906, 907, 908, 909, 911, 912, 913, 914, 915, 916, 917, 918, 919, 922, 924, 931, 933, 937, 940, 941, 942, 945, 950, 951, 952, 959, 960, 961, 962, 963, 974, 977, 978, 979, 980, 981, 983, 989, 990, 991, 992, 994, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1015, 1016, 1017, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1050, 1051, 1060, 1061, 1063, 1064, 1069, 1070, 1072, 1073, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1098, 1100, 1127, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1171, 1176, 1177, 1178, 1190, 1191, 1192, 1193, 1194, 1195, 1198, 1208, 1209, 1213, 1214, 1217, 1221, 1222, 1228, 1232, 1233, 1235, 1241, 1251, 1254, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1276, 1277, 1279, 1281, 1282, 1283, 1284, 1286, 1287, 1288, 1320, 1321, 1322, 1324, 1326, 1329, 1366, 1380, 1396, 1399, 1421, 1455, 1456, 1459, 1460, 1461, 1462, 1463, 1464, 1466, 1473, 1474, 1476, 1477, 1478, 1479, 1483, 1487, 1488, 1496, 1498, 1500, 1501, 1503, 1507, 1508, 1511, 1513, 1515, 1522, 1529, 1530, 1531, 1532, 1535, 1536, 1539, 1541, 1542, 1543, 1544, 1545, 1547, 1550, 1565, 1570, 1571, 1572, 1573, 1574, 1577, 1578, 1580, 1582, 1583, 1584, 1586, 1587, 1588, 1590, 1591, 1595, 1597, 1600, 1601, 1603, 1606, 1608, 1609, 1611, 1612, 1613, 1617, 1622, 1623, 1624, 1625, 1626, 1627, 1629, 1630, 1631, 1635, 1636, 1637, 1638, 1639, 1640, 1642, 1643, 1645, 1646, 1647, 1649, 1650, 1652, 1656, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1728, 1729, 1730, 1732, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1757, 1760, 1761, 1762, 1764, 1780, 1781, 1782, 1790, 1791, 1796, 1797, 1798, 1799, 1801, 1810, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1882, 1884]
AllQuestDefaultEnemyIDs = [303, 304, 305, 307, 308, 309, 310, 318, 319, 320, 323, 324, 325, 326, 329, 332, 341, 342, 345, 346, 347, 348, 349, 350, 351, 352, 356, 359, 365, 367, 369, 372, 373, 374, 375, 376, 383, 384, 385, 386, 389, 390, 391, 392, 393, 394, 395, 396, 399, 401, 403, 404, 405, 406, 407, 409, 411, 414, 415, 418, 436, 437, 445, 446, 447, 448, 450, 451, 454, 455, 456, 457, 458, 459, 461, 462, 463, 464, 466, 468, 470, 475, 477, 479, 481, 483, 485, 487, 488, 489, 490, 491, 492, 493, 495, 496, 497, 498, 500, 501, 503, 504, 506, 508, 510, 512, 513, 515, 517, 519, 525, 532, 533, 534, 535, 536, 538, 540, 542, 544, 546, 547, 548, 549, 550, 551, 552, 553, 557, 558, 559, 560, 561, 562, 563, 565, 566, 569, 570, 571, 572, 573, 576, 577, 578, 579, 581, 583, 588, 591, 593, 598, 600, 601, 602, 603, 604, 607, 608, 609, 610, 613, 640, 641, 642, 644, 649, 663, 667, 673, 740, 742, 744, 746, 750, 751, 752, 759, 760, 761, 778, 780, 782, 784, 785, 786, 787, 788, 789, 790, 791, 824, 827, 828, 829, 832, 833, 834, 837, 838, 839, 840, 848, 930, 934, 935, 939, 946, 947, 948, 949, 964, 965, 967, 970, 975, 984, 985, 996, 1035, 1036, 1041, 1053, 1054, 1058, 1059, 1066, 1074, 1075, 1076, 1077, 1078, 1093, 1094, 1095, 1096, 1097, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1128, 1145, 1147, 1148, 1151, 1152, 1153, 1154, 1158, 1159, 1160, 1162, 1164, 1167, 1168, 1169, 1172, 1173, 1174, 1196, 1197, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1212, 1215, 1223, 1226, 1229, 1230, 1231, 1236, 1237, 1238, 1239, 1240, 1242, 1245, 1246, 1248, 1249, 1250, 1343, 1344, 1345, 1348, 1386, 1387, 1388, 1389, 1391, 1393, 1395, 1397, 1398, 1400, 1402, 1404, 1405, 1406, 1407, 1408, 1410, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1422, 1423, 1424, 1425, 1457, 1458, 1465, 1467, 1468, 1469, 1470, 1471, 1472, 1482, 1484, 1485, 1486, 1489, 1490, 1491, 1497, 1499, 1502, 1512, 1516, 1518, 1519, 1526, 1527, 1528, 1534, 1537, 1540, 1546, 1548, 1549, 1551, 1575, 1576, 1579, 1581, 1585, 1589, 1592, 1594, 1596, 1598, 1602, 1604, 1605, 1607, 1610, 1614, 1616, 1618, 1619, 1621, 1628, 1634, 1644, 1648, 1651, 1653, 1655, 1674, 1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683, 1684, 1686, 1687, 1688, 1689, 1690, 1888]
AllBossDefaultIDs = [179, 180, 181, 182, 184, 185, 186, 187, 189, 190, 191, 193, 195, 196, 197, 198, 199, 201, 202, 203, 204, 206, 208, 210, 212, 214, 216, 217, 219, 220, 221, 222, 223, 225, 227, 229, 231, 232, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 248, 249, 250, 251, 252, 253, 254, 266, 267, 268, 269, 270, 271, 274, 1342, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1448, 1454, 1632, 1733, 1746, 1747, 1748, 1749, 1754, 1755]

# "Location": [Warp Cutscene, "chgEdID", Map Name, Map ID]
ContinentInfo = {"Gormott": [10043, 10044, "ma05a", 6], "Uraya": [10088, 10079, "ma07a", 9], "Mor Ardain": [10156, 10149, "ma08a", 10], "Leftheria": [10197, 10192, "ma15a", 14], "Temperantia": [10233, 10224, "ma10a", 11], "Tantal": [10272, 10269, "ma13a", 13], "Spirit Crucible": [10325, 10323, "ma16a", 15], "Cliffs of Morytha": [10351, 10345, "ma17a", 16], "Land of Morytha": [10369, 10363, "ma18a", 18], "World Tree": [10399, 10393, "ma20a", 20]}

TotalAreaPool = ["Gormott", "Uraya", "Mor Ardain", "Leftheria", "Temperantia", "Tantal", "Spirit Crucible", "Cliffs of Morytha", "Land of Morytha", "World Tree"]

# "Driver": ["scriptName", "scriptStartID"]
PartyMembersAddScripts = {"Tora": ["chapt02", 7], "Nia": ["chapt02", 9], "Morag": ["chapt05", 7], "Zeke": ["chapt06", 5]}

ProofofPurchaseIDs = Helper.InclRange(25306, 25321)

ValidPouchItems = [x for x in IDs.PouchItems if x not in [40314, 40428]]

InvalidMapNPCs = [8284, 5487]

#25333->25348 for Casino Vouchers
#25479->25488 for Bounty Tokens
#25405->25407 for WP Manuals
#25349->25351 for SP Manuals
#25489 for Doubloons (1)

# TO DO

# Maybe change the blade bundles to be from the same overall class distribution pool, but have them be mixed up, and change the names to "Blade Bundle 1->10", and increase the cost accordingly
# add um sets for superbosses?
# add the names of weapons

# Known Issues: 
# Poppiswap is going to be fucked up with custom enhancements

def UMHunt():
    if IDs.CurrentSliderOdds != 0:
        SetCount = IDs.CurrentSliderOdds
        ChosenAreaOrder = []
        if IDs.CurrentSliderOdds > 10: #really need to limit the spinbox instead
            SetCount = 10
        CheckForSuperbosses(SetCount)
        ChosenAreaOrder.extend(random.sample(TotalAreaPool, SetCount))
        #FindMonsters(ChosenAreaOrder)
        PartyMemberstoAdd = PartyMemberAddition(SetCount)
        AreaUMs, AllAreaMonsters = CustomEnemyRando(ChosenAreaOrder)
        EnemySets = ChosenEnemySets(SetCount, AreaUMs)
        WarpManagement(SetCount, ChosenAreaOrder, PartyMemberstoAdd, EnemySets)
        CHR_EnArrangeAdjustments(AllAreaMonsters, EnemySets, ChosenAreaOrder)
        LandmarkAdjustments(ChosenAreaOrder)
        NoUnintendedRewards(ChosenAreaOrder)
        SpiritCrucibleEntranceRemoval()
        ShopChanges(ChosenAreaOrder)
        BalanceChanges(ChosenAreaOrder)
        if ExtraSuperbosses:
            OhBoyHereWeGoAgain()
        Cleanup()
        UMHuntMenuTextChanges()
        #DebugItemsPlace() # currently doesnt matter since I hide all the argentum chests anyways
        #DebugEasyMode()
        #DebugSpawnCountPrint(EnemySets, ChosenAreaOrder)

def FindMonsters(ChosenAreaOrder): # was used to debug and find enemies that spawned in too often. If the objective pointer points towards defeating an enemy of which there are 16 or more on the map you're on, the game will freeze upon loading.
    enemycountholder = Helper.ExtendListtoLength([0], len(AllQuestDefaultEnemyIDs),"0")
    for i in range(0, len(ChosenAreaOrder)):
        enemypopfile = "./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_EnemyPop.json"
        with open(enemypopfile, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                for k in range(1, 5):
                    if row[f"ene{k}ID"] == 0:
                            break
                    else:
                        for j in range(0, len(AllQuestDefaultEnemyIDs)):
                            if row[f"ene{k}ID"] == AllQuestDefaultEnemyIDs[j]:
                                enemycountholder[j] += row[f"ene{k}num"]
                                break
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    toolargepool = {
        "IDs": [],
        "Counts": []
    }
    for i in range(0, len(enemycountholder)):
        if enemycountholder[i] >= 10: # I chose 10 as an arbitrary number under 16. 
            toolargepool["IDs"].append(AllQuestDefaultEnemyIDs[i])
            toolargepool["Counts"].append(enemycountholder[i])
    print(toolargepool)

def CheckForSuperbosses(SetCount):
    global ExtraSuperbosses
    global SuperbossCount
    if (Options.UMHuntOption_SuperbossWave.GetState()) & (SetCount == 10):
        ExtraSuperbosses = True
        SuperbossCount = 5
    else:
        ExtraSuperbosses = False
        SuperbossCount = 0

def Cleanup():
    with open("./_internal/JsonOutputs/common/FLD_QuestList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] >= 25:
                row["PRTQuestID"] = 6
                row["FlagPRT"] = 0
            if row["$id"] == 15: # Talking to Spraine, this doesnt work with the Quest Flags turned off
                row["NextQuestA"] = 234
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/EVT_listBf.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10013:
                row["nextID"] = 10464
                row["scenarioFlag"] = 10009
                row["nextIDtheater"] = 10464
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_Dr.json", ["DefAcce", "DefWP", "DefSP"], 0)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_Dr.json", ["DefLv"], 10)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_Dr.json", ["DefWPType", "DefLvType"], 1)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_Dr.json", ["DefSPType"], 2)
    GimmickAdjustments()

def ShopChanges(ChosenAreaOrder): # Moved these out since they were cluttering the main function up. Order probably matters
    UMRewardDropChanges()
    CoreCrystalIdentification()
    WeaponPowerLevel()
    BladeTrustRequirementChanges()
    PoppiswapCostChanges()
    AddDLCRewards(ChosenAreaOrder)
    CustomShopSetup()
    MoveSpeedDeedSetup()
    InnShopCosts()
    ReplaceBana()
    SecretShopMaker(ChosenAreaOrder)
    ReAddInns()

def BalanceChanges(ChosenAreaOrder): # Moved to reduce clutter, doesn't matter order for these
    PneumaNerfs()
    SpiritCrucibleNerfs(ChosenAreaOrder)
    RaceMode.SecondSkillTreeCostReduc()

def GimmickAdjustments():
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_DoorGimmick.json", ["Condition"], 0)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_JumpGimmick.json", ["Condition"], 0)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_MapGimmick.json", ["Condition"], 0)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_ElevatorGimmick.json", ["OP_Condition"], 0)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_EffectPop.json", ["Condition", "QuestFlagMin", "QuestFlagMax"], 0)
    with open("./_internal/JsonOutputs/common/FLD_LODList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in [211, 226]: # door in urayan titan's head that blocks off Vampire Bride Marion, Ether Gust Wall thingy in Uraya
                row["flag"]["Visible"] = 0
                row["ScenarioFlagMin1"] = 1001
                row["ScenarioFlagMax1"] = 10048
                row["QuestFlag1"] = 0
                row["QuestFlagMin1"] = 0
                row["QuestFlagMax1"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def InnShopCosts(): # Removes cost to stay at inn
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/MNU_ShopInn.json", ["Price"], 0)

def PneumaNerfs(): # Mods, break her kneecaps
    with open("./_internal/JsonOutputs/common/ITM_PcWpn.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 5970:
                row["Damage"] = 1 # Nerfing her base damage to 1 seems good enough, you can still use her for elemental combos, but it wont do much damage. The utility is still nice, but won't let you cheese a fight
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def SpiritCrucibleNerfs(ChosenAreaOrder): # Spirit Crucible is way too oppressive when the unique monsters can be so strong
    if "Spirit Crucible" in ChosenAreaOrder[:3]: # if spirit crucible is one of the first 3 chosen areas, no affinity or art restrictions
        Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_MapRev.json", ["KizunaCap"], 1000)
        Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_MapRev.json", ["ArtSp"], 3)  
    elif "Spirit Crucible" in ChosenAreaOrder[:6]: # if spirit crucible is in areas 4->6, nerfs to art restrictions
        Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_MapRev.json", ["KizunaCap"], 1000)

def ReplaceBana(): # I want to use Bana as the exchange shop, so I move rumtumtum into Bana's spots on the map
    with open("./_internal/JsonOutputs/common_gmk/ma02a_FLD_NpcPop.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for row in data["rows"]:
            if (row["$id"] != 2079) & (row["NpcID"] == 2002):
                row["NpcID"] = 2233
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def MoveSpeedDeedSetup():
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # Changes caption and name
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 25249:
                row["Caption"] = 603 # Increases running speed by 500%
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_OwnerBonus.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1:
                row["Value"] = 500
                row["Type"] = 1
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_OwnerBonusParam.json", 'r+', encoding='utf-8') as file: # Changes max movespeed bonus to 250%
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1:
                row["Max"] = 750
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 491:
                row["name"] = "Movespeed Deed"
            if row["$id"] == 608:
                row["name"] = "Increases running speed by 500%."
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def OhBoyHereWeGoAgain():
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: # Adjusts the levels of the superbosses
        data = json.load(file)
        for i in range(0, len(ChosenSuperbosses)):
            for row in data["rows"]:
                if row["$id"] == ChosenSuperbosses[i]:
                    row["Lv"] = 115 + i*10
                    if row["Scale"] < 35:
                        row["Scale"] = 35
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def WarpManagement(SetCount, ChosenAreaOrder, PartyMemberstoAdd, EnemySets): # Main function was getting a bit too cluttered
    if ExtraSuperbosses:
        EnemyGroupSetup()
    EventSetup(SetCount, ChosenAreaOrder, PartyMemberstoAdd)
    EventChangeSetup(SetCount, ChosenAreaOrder)
    QuestListSetup(SetCount, ChosenAreaOrder)
    QuestTaskSetup(SetCount,EnemySets)
    FieldQuestBattleSetup(SetCount,EnemySets)
    FieldQuestTaskLogSetup(EnemySets)
    AddQuestConditions(SetCount, ChosenAreaOrder)

def EnemyGroupSetup(): # Makes extra group for superbosses:
    StartingGroupRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_EnemyGroup.json", "$id") + 1
    with open("./_internal/JsonOutputs/common/FLD_EnemyGroup.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["rows"].append({"$id": StartingGroupRow, "EnemyID1": ChosenSuperbosses[0], "EnemyID2": ChosenSuperbosses[1], "EnemyID3": ChosenSuperbosses[2], "EnemyID4": ChosenSuperbosses[3], "EnemyID5": 0, "EnemyID6": 0, "EnemyID7": 0, "EnemyID8": 0, "EnemyID9": 0, "EnemyID10": 0, "EnemyID11": 0, "EnemyID12": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def QuestListSetup(SetCount, ChosenAreaOrder): # Adjusting the quest list
    with open("./_internal/JsonOutputs/common/FLD_QuestList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        CurrArea = 0
        for row in data["rows"]:
            rowID = row["$id"]
            match rowID:
                case rowID if rowID in range(235, 235 + SetCount - 1): # For all except the last set, do this
                    row["Talker"] = 1001
                    row["FlagCLD"] = 832 + CurrArea
                    row["PurposeID"] = 249 + CurrArea
                    row["CountCancel"] = 1
                    row["NextQuestA"] = row["$id"] + 1
                    row["CallEventA"] = ContinentInfo[ChosenAreaOrder[CurrArea+1]][0]
                    CurrArea += 1
                case rowID if rowID == 235 + SetCount - 1: # for the last quest
                    if not ExtraSuperbosses: # if we don't have extrasuperbosses, warp us to the credits
                        row["Talker"] = 1001
                        row["FlagCLD"] = 832 + CurrArea
                        row["PurposeID"] = 249 + CurrArea
                        row["CountCancel"] = 0
                        row["NextQuestA"] = 236 + CurrArea
                        row["NextQuestA"] = 30000
                        row["CallEventA"] = 10494
                        break
                    else: # otherwise, the set doesn't warp you anywhere, and instead starts the next quest
                        row["Talker"] = 1001
                        row["FlagCLD"] = 832 + CurrArea
                        row["PurposeID"] = 249 + CurrArea
                        row["CountCancel"] = 0
                        row["NextQuestA"] = 236 + CurrArea
                        row["CallEventA"] = 0
                        CurrArea += 1
                case rowID if rowID in range(235 + SetCount, 235 + SetCount + SuperbossCount - 1): # for all except the last quest (superbosses on)
                    row["Talker"] = 1001
                    row["FlagCLD"] = 832 + CurrArea
                    row["PurposeID"] = 249 + CurrArea
                    row["CountCancel"] = 0
                    row["NextQuestA"] = 236 + CurrArea
                    row["CallEventA"] = 0
                    CurrArea += 1
                case rowID if rowID == 235 + SetCount + SuperbossCount - 1: # for the instance where we have superbosses on, the very last quest
                    row["Talker"] = 1001
                    row["FlagCLD"] = 832 + CurrArea
                    row["PurposeID"] = 249 + CurrArea
                    row["CountCancel"] = 1
                    row["NextQuestA"] = 30000
                    row["CallEventA"] = 10494
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def EventSetup(SetCount, ChosenAreaOrder, PartyMemberstoAdd): # Adjusting the initial area warp events
    with open("./_internal/JsonOutputs/common/EVT_listBf.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10465:
                row["nextID"] = ContinentInfo[ChosenAreaOrder[0]][0]
                row["nextIDtheater"] = row["nextID"]
                break
        for i in range(0, SetCount):
            for row in data["rows"]:
                if row["$id"] == ContinentInfo[ChosenAreaOrder[i]][0]:
                    row["scenarioFlag"] = 10010 + i
                    row["chapID"] = 10
                    row["linkID"] = 0
                    row["nextID"] = 0
                    row["nextIDtheater"] = 0

                    if PartyMemberstoAdd[i] != 0:
                        row["scriptName"] = PartyMembersAddScripts[PartyMemberstoAdd[i]][0]
                        row["scriptStartId"] = PartyMembersAddScripts[PartyMemberstoAdd[i]][1]
                    else:
                        row["scriptName"] = ""
                        row["scriptStartId"] = 0
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def EventChangeSetup(SetCount, ChosenAreaOrder): # Adjusting the warp event endings that change scenario flags
    with open("./_internal/JsonOutputs/common/EVT_chgBf01.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, SetCount):
            for row in data["rows"]:
                if row["$id"] == ContinentInfo[ChosenAreaOrder[i]][1]:
                    row["id"] = 10011 + i
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def PartyMemberAddition(SetCount): # Adds new party members
    ChosenPartyMemberOrder = []
    FirstPartyMember = []
    ChosenPartyMemberOrder.extend(random.sample(["Tora", "Zeke", "Nia", "Morag"], min(SetCount, 4)))
    FirstPartyMember.append(ChosenPartyMemberOrder[0]) # We want to guarantee getting 1 teammate minimum to start with
    ChosenPartyMemberOrder.pop(0)
    while len(ChosenPartyMemberOrder) < SetCount - 1:
        ChosenPartyMemberOrder.append(0)
    random.shuffle(ChosenPartyMemberOrder)
    FirstPartyMember.extend(ChosenPartyMemberOrder)
    RNGAdjustedChosenPartyMemberOrder = FirstPartyMember
    return RNGAdjustedChosenPartyMemberOrder

def QuestTaskSetup(SetCount, EnemySets): # Adds the new quest tasks
    StartingQuestTaskRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_QuestBattle.json", "$id") + 1
    StartingQuestLogRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_quest.json", "$id") + 1
    with open("./_internal/JsonOutputs/common/FLD_QuestTask.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, SetCount):
            if len(EnemySets[i]) == 4:
                data["rows"].append({"$id": 249 + i, "PreCondition": 0, "TaskType1": 1, "TaskID1": StartingQuestTaskRow, "Branch1": 0, "TaskLog1": StartingQuestLogRow, "TaskUI1": 0, "TaskCondition1": 0, "TaskType2": 1, "TaskID2": StartingQuestTaskRow + 1, "Branch2": 0, "TaskLog2": StartingQuestLogRow + 1, "TaskUI2": 0, "TaskCondition2": 0, "TaskType3": 1, "TaskID3": StartingQuestTaskRow + 2, "Branch3": 0, "TaskLog3": StartingQuestLogRow + 2, "TaskUI3": 0, "TaskCondition3": 0, "TaskType4": 1, "TaskID4": StartingQuestTaskRow + 3, "Branch4": 0, "TaskLog4": StartingQuestLogRow + 3, "TaskUI4": 0, "TaskCondition4": 0}) 
                StartingQuestTaskRow += 4
                StartingQuestLogRow += 4
            else: # if it's not 4, its 3, currently unused
                data["rows"].append({"$id": 249 + i, "PreCondition": 0, "TaskType1": 1, "TaskID1": StartingQuestTaskRow, "Branch1": 0, "TaskLog1": StartingQuestLogRow, "TaskUI1": 0, "TaskCondition1": 0, "TaskType2": 1, "TaskID2": StartingQuestTaskRow + 1, "Branch2": 0, "TaskLog2": StartingQuestLogRow + 1, "TaskUI2": 0, "TaskCondition2": 0, "TaskType3": 1, "TaskID3": StartingQuestTaskRow + 2, "Branch3": 0, "TaskLog3": StartingQuestLogRow + 2, "TaskUI3": 0, "TaskCondition3": 0, "TaskType4": 0, "TaskID4": 0, "Branch4": 0, "TaskLog4": 0, "TaskUI4": 0, "TaskCondition4": 0}) 
                StartingQuestTaskRow += 3
                StartingQuestLogRow += 3
        if ExtraSuperbosses:
            for i in range(0, SuperbossCount):
                data["rows"].append({"$id": 259 + i, "PreCondition": 0, "TaskType1": 1, "TaskID1": StartingQuestTaskRow, "Branch1": 0, "TaskLog1": StartingQuestLogRow, "TaskUI1": 0, "TaskCondition1": 0, "TaskType2": 0, "TaskID2": 0, "Branch2": 0, "TaskLog2": 0, "TaskUI2": 0, "TaskCondition2": 0, "TaskType3": 1, "TaskID3": 0, "Branch3": 0, "TaskLog3": 0, "TaskUI3": 0, "TaskCondition3": 0, "TaskType4": 0, "TaskID4": 0, "Branch4": 0, "TaskLog4": 0, "TaskUI4": 0, "TaskCondition4": 0})
                StartingQuestTaskRow += 1
                StartingQuestLogRow += 1        
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def FieldQuestBattleSetup(SetCount, EnemySets): # Adds new rows in FLD_QuestBattle accordingly
    StartingQuestBattleFlag = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_QuestBattle.json", "CountFlag") + 1
    with open("./_internal/JsonOutputs/common/FLD_QuestBattle.json", 'r+', encoding='utf-8') as file:
        LastRow = 777
        LastFlag = 795
        data = json.load(file)
        for i in range(0, SetCount):
            for j in range(0, len(EnemySets[i])):
                data["rows"].append({"$id": LastRow, "Refer": 1, "EnemyID": EnemySets[i][j], "EnemyGroupID": 0, "EnemySpeciesID": 0, "EnemyRaceID": 0, "Count": 1, "CountFlag": LastFlag, "DeadAll": 0, "TimeCount": 0, "TimeCountFlag": 0, "ReduceEnemyHP": 0, "ReducePCHP": 0, "TargetOff": 0}) 
                LastRow += 1
                LastFlag += 1
        if ExtraSuperbosses:
            for i in range(0, SuperbossCount):
                data["rows"].append({"$id": LastRow, "Refer": 1, "EnemyID": ChosenSuperbosses[i], "EnemyGroupID": 0, "EnemySpeciesID": 0, "EnemyRaceID": 0, "Count": 1, "CountFlag": LastFlag, "DeadAll": 0, "TimeCount": 0, "TimeCountFlag": 0, "ReduceEnemyHP": 0, "ReducePCHP": 0, "TargetOff": 0}) 
                LastRow += 1
                LastFlag += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def FieldQuestTaskLogSetup(EnemySets): # Adds the task logs for the field quests
    AllEnemySetNames = []
    AllEnemySetNameIDs = []
    SuperbossNameIDs = []
    SuperbossNames = []
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: # add level scaling here
        data = json.load(file)
        for i in range(0, len(EnemySets)):
            CurrEnemySetNameIDs = []
            for j in range(0, len(EnemySets[i])):
                for row in data["rows"]:
                    if row["$id"] == EnemySets[i][j]:
                        CurrEnemySetNameIDs.append(row["Name"])
                        row["Lv"] = 5 + 12*i # Sets level of enemy equal to 5 min, then for each set after, the level goes up by 11 more
                        LuckyDrop = random.randint(0, 99)
                        if LuckyDrop <= 74:
                            break
                        elif LuckyDrop >= 99: # 1% chance for Bounty Token, of any level!
                            row["PreciousID"] = random.choice(Helper.InclRange(25479, 25488))
                            break
                        elif LuckyDrop >= 95: # 4% chance for Casino Voucher
                            row["PreciousID"] = random.choice(Helper.InclRange(25479, 25488))
                            break
                        elif LuckyDrop >= 90: # 5% chance for SP Manual
                            row["PreciousID"] = random.choice([25349, 25350, 25351])
                            break
                        elif LuckyDrop >= 85: # 5% chance for WP Manual
                            row["PreciousID"] = random.choice([25405, 25406, 25407])
                            break
                        elif LuckyDrop >= 75: # 10% chance for a doubloon
                            row["PreciousID"] = 25489
                        break
            AllEnemySetNameIDs.append(CurrEnemySetNameIDs)        
        if ExtraSuperbosses:
            for i in range(0, len(ChosenSuperbosses)):
                for row in data["rows"]:
                    if row["$id"] == ChosenSuperbosses[i]:
                        row["PreciousID"] = 25488 # You get another level 10 bounty token per um defeated
                        SuperbossNameIDs.append(row["Name"])
                        break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_enemyname.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(EnemySets)):
            CurrEnemySetNames = []
            for j in range(0, len(EnemySets[i])):
                for row in data["rows"]:
                    if row["$id"] == AllEnemySetNameIDs[i][j]:
                        CurrEnemySetNames.append(row["name"])
                        break
            AllEnemySetNames.append(CurrEnemySetNames)
        for i in range(0, len(SuperbossNameIDs)):
            for row in data["rows"]:
                if row["$id"] == SuperbossNameIDs[i]:
                    SuperbossNames.append(row["name"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_quest.json", 'r+', encoding='utf-8') as file:
        StartRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_quest.json", "$id") + 1
        data = json.load(file)
        for i in range(0, len(EnemySets)):
            for j in range(0, len(EnemySets[i])):
                data["rows"].append({"$id": StartRow, "style": 62, "name": f"Defeat [System:Color name=tutorial]{AllEnemySetNames[i][j]}[/System:Color]"})
                StartRow += 1
        if ExtraSuperbosses:
            for i in range(0, SuperbossCount):
                data["rows"].append({"$id": StartRow, "style": 62, "name": f"Defeat [System:Color name=tutorial]{SuperbossNames[0]}[/System:Color] in\n{SuperbossMaps[0].strip()}."})
                StartRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ChosenEnemySets(SetCount, AreaUMs): # Figuring out what enemies to turn into a set
    EnemySets = []
    for i in range(0, SetCount):
        if len(AreaUMs[i]) >= 4:
            EnemySets.append(random.sample(AreaUMs[i], 4))
        else: # currently unused
            EnemySets.append(random.sample(AreaUMs[i], len(AreaUMs[i])))
    return EnemySets

def CustomEnemyRando(ChosenAreaOrder): # Custom shuffling of enemies
    AllAreaUMs = []
    AllAreaMonsters = []
    AllAreaSuperbosses = []
    SuperbossMapsFull = []
    ShuffledUniqueEnemyIDs = AllUniqueMonsterDefaultIDs.copy()
    ShuffledSuperBossIDs = AllSuperBossDefaultIDs.copy()
    random.shuffle(ShuffledSuperBossIDs)
    random.shuffle(ShuffledUniqueEnemyIDs)
    for k in range(0, len(ChosenAreaOrder)):
        Chosen4UMs = ShuffledUniqueEnemyIDs[(4*k):(4+4*k)]
        ChosenSuperBoss = ShuffledSuperBossIDs[k]
        for i in range(0, len(IDs.ValidEnemyPopFileNames)):
            UniqueAreaEnemies = []
            if ContinentInfo[ChosenAreaOrder[k]][2] in IDs.ValidEnemyPopFileNames[i]:
                OriginalAreaEnemies = []
                CurrentAreaUMs = []
                CurrentAreaMonsters = []
                enemypopfile = "./_internal/JsonOutputs/common_gmk/" + IDs.ValidEnemyPopFileNames[i]
                Helper.ColumnAdjust(enemypopfile, ["battlelockname"], 0)
                with open(enemypopfile, 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data["rows"]:
                        for j in range(1, 5):
                            if row[f"ene{j}ID"] in IDs.ValidEnemies: # if it's not a boss row and has a valid enemy id
                                OriginalAreaEnemies.append(row[f"ene{j}ID"]) # add to list of enemies to choose from
                    UniqueAreaEnemies = list(OrderedDict.fromkeys(OriginalAreaEnemies)) # then we remove dupes, and sort it
                    OriginalAreaEnemies = UniqueAreaEnemies
                    #print(OriginalAreaEnemies)
                    NewAreaEnemies = OriginalAreaEnemies.copy() # make a copy of the list
                    NewAreaEnemies = [x for x in NewAreaEnemies if x not in AllUniqueMonsterDefaultIDs + AllSuperBossDefaultIDs] # now remove all ums and superbosses
                    del NewAreaEnemies[-2:] # remove two slots, this accounts for the land of morytha, where there's only 3 unique monsters, and no superbosses. Everywhere else has 4, and we need at least 5 slots to add 4 ums + 1 superboss to each area
                    NewAreaEnemies.extend(Chosen4UMs) # add the 4 UMs back to the pool
                    if ExtraSuperbosses:
                        NewAreaEnemies.append(ChosenSuperBoss) # add the superboss to the pool
                    while len(NewAreaEnemies) < len(OriginalAreaEnemies): # while the new enemy pool is less than the original, we need to add more to make them equal
                        ChosenNormalEnemy = random.choice(AllNormalEnemyDefaultIDs)
                        if ChosenNormalEnemy not in NewAreaEnemies:
                            NewAreaEnemies.append(ChosenNormalEnemy)
                            AllNormalEnemyDefaultIDs.remove(ChosenNormalEnemy)
                    random.shuffle(NewAreaEnemies) # now mix up the enemies
                    #print(NewAreaEnemies)
                    #print("-------------")
                    for row in data["rows"]: # row
                        for j in range(1, 5): # column
                            if row[f"ene{j}ID"] == 0:
                                break
                            else:
                                for m in range(0, len(NewAreaEnemies)): # enemy
                                    if row[f"ene{j}ID"] == OriginalAreaEnemies[m]: # if it matches the original enemy number
                                        row[f"ene{j}ID"] = NewAreaEnemies[m] # give it the new 
                                        break
                    for row in data["rows"]:
                        for j in range(1, 5):
                            if row[f"ene{j}ID"] == 0:
                                break
                            else:
                                CurrentAreaMonsters.append(row[f"ene{j}ID"])
                                if row[f"ene{j}ID"] in AllUniqueMonsterDefaultIDs: # if it's a um we want it to always show up
                                    row["Condition"] = row["ScenarioFlagMax"] = row["ScenarioFlagMin"] = row["QuestFlag"] = row["QuestFlagMin"] = row["QuestFlagMax"] = row["muteki_QuestFlag"] = row["muteki_QuestFlagMin"] = row["muteki_QuestFlagMax"] = row["muteki_Condition"] = row[f"ene{j}Lv"] = 0
                                    row["POP_TIME"] = 256
                                    row["popWeather"] = 255
                                    CurrentAreaUMs.append(row[f"ene{j}ID"]) # now add it to the list of ums for this area, used in many places, so we need to keep track of this
                                elif row[f"ene{j}ID"] in AllSuperBossDefaultIDs: # if it's a superboss, do the same as for ums, except add it to its' own list
                                    row["Condition"] = row["ScenarioFlagMax"] = row["ScenarioFlagMin"] = row["QuestFlag"] = row["QuestFlagMin"] = row["QuestFlagMax"] = row["muteki_QuestFlag"] = row["muteki_QuestFlagMin"] = row["muteki_QuestFlagMax"] = row["muteki_Condition"] = row[f"ene{j}Lv"] = 0
                                    row["POP_TIME"] = 256
                                    row["popWeather"] = 255
                                    AllAreaSuperbosses.append(row[f"ene{j}ID"])
                                    SuperbossMapsFull.append(ChosenAreaOrder[k])
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
                CurrentAreaUMs = list(set(CurrentAreaUMs))
                AllAreaUMs.append(CurrentAreaUMs)
                AllAreaMonsters.append(CurrentAreaMonsters)
        EnemyRandoLogic.FlyingEnemyFix(OriginalAreaEnemies, NewAreaEnemies)
        EnemyRandoLogic.SwimmingEnemyFix(OriginalAreaEnemies, NewAreaEnemies)
    EnemyRandoLogic.FishFix()
    EnemyRandoLogic.BigEnemyCollisionFix()
    if ExtraSuperbosses:
        UniqueSuperbosses = list(OrderedDict.fromkeys(AllAreaSuperbosses))
        ChosenSuperbossNumbers = random.choices(Helper.InclRange(0, 9), k = SuperbossCount)
        global ChosenSuperbosses
        ChosenSuperbosses = []
        for i in range(0, SuperbossCount):
            ChosenSuperbosses.append(UniqueSuperbosses[ChosenSuperbossNumbers[i]])
        global SuperbossMaps
        SuperbossMaps = []
        for i in range(0, SuperbossCount):
            for j in range(0, len(AllAreaSuperbosses)):
                if AllAreaSuperbosses[j] == ChosenSuperbosses[i]: # if we have a chosen superboss that matches the entire list of superbosses and their maps (both of equal length!)
                    SuperbossMaps.append(SuperbossMapsFull[j]) # add the superboss's map to the list of maps we care about
                    break
    UMEnemyAggro()
    return AllAreaUMs, AllAreaMonsters
    
def UMEnemyAggro(): # custom enemy aggro
    EnemyAggroSliderOdds = Options.EnemyAggroOption.GetOdds()
    if EnemyAggroSliderOdds == 0: #if the slider is 0, turn every enemy passive, except the unique monsters
        with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for row in data["rows"]:
                if (row["$id"] in IDs.ValidEnemies) & (row["$id"] not in AllUniqueMonsterDefaultIDs + AllSuperBossDefaultIDs):
                    row["Flag"]["AlwaysAttack"] = 0
                    row["Flag"]["mBoss"] = 0
                    row["SearchRange"] = 0
                    row["SearchRadius"] = 0
                    row["SearchAngle"] = 0
                    row["Detects"] = 0
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
                elif (row["$id"] in AllUniqueMonsterDefaultIDs + AllSuperBossDefaultIDs) & (row["$id"] in IDs.ValidEnemies):
                    row["Flag"]["AlwaysAttack"] = 1
                    row["Flag"]["mBoss"] = 0
                    row["Flag"]["Named"] = 1
                    row["Detects"] = 3
                    row["SearchRange"] = 10
                    row["SearchAngle"] = 360
                    row["SearchRadius"] = 5
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    else: # everything can be aggro or not. ums untouched, since they all aggro by default i believe? nope
        with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for row in data["rows"]:
                if (EnemyAggroSliderOdds != 100) & (row["$id"] not in AllUniqueMonsterDefaultIDs + AllSuperBossDefaultIDs) & (random.randint(0,100) >= EnemyAggroSliderOdds) & (row["$id"] in IDs.ValidEnemies):
                    row["Flag"]["AlwaysAttack"] = 0
                    row["Flag"]["mBoss"] = 0
                    row["SearchRange"] = 0
                    row["SearchRadius"] = 0
                    row["SearchAngle"] = 0
                    row["Detects"] = 0
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
                elif (row["$id"] in AllUniqueMonsterDefaultIDs + AllSuperBossDefaultIDs) & (row["$id"] in IDs.ValidEnemies):
                    row["Flag"]["AlwaysAttack"] = 1
                    row["Flag"]["mBoss"] = 0
                    row["Flag"]["Named"] = 1
                    row["Detects"] = 3
                    row["SearchRange"] = 10
                    row["SearchAngle"] = 360
                    row["SearchRadius"] = 5
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def CHR_EnArrangeAdjustments(AllAreaMonsters, EnemySets, ChosenAreaOrder): # adjusts aggro + drops of all enemies + levels + stats
    EnemyParamstoNerf = Helper.ExtendListtoLength([], len(EnemySets), "[]") # we want to nerf the early enemies in all their stats, you just don't have much damage or tankiness
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["ExpRev", "GoldRev", "WPRev", "SPRev", "DropTableID", "DropTableID2", "DropTableID3"], 0)         
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(AllAreaMonsters)):
            for row in data["rows"]:
                if row["$id"] in AllAreaMonsters[i]:
                    row["Lv"] = 5 + 12*i # Level Formula: Sets level of enemy equal to 5 min, then for each set after, the level goes up by 12 more, so eventually the enemies outscale you
                    row["ZoneID"] = ContinentInfo[ChosenAreaOrder[i]][3] # this fixes pointers not working?
        for i in range(0, len(EnemySets)):
            for j in range(0, len(EnemySets[i])):
                for row in data["rows"]:
                    if row["$id"] == EnemySets[i][j]:
                        EnemyParamstoNerf[i].append(row["ParamID"])
                        if row["Scale"] < 35:
                            row["Scale"] = 35
                        break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/CHR_EnParam.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, min(len(EnemySets),4)):
            NerfRatio = 0.6 + (i+1)*0.1 # 60%->70%->80%->90%->100% after area 4 ends
            for row in data["rows"]:
                if row["$id"] in EnemyParamstoNerf[i]:
                    for stat in ["HpMaxRev", "StrengthRev", "PowEtherRev", "DexRev", "AgilityRev", "LuckRev"]:
                        row[stat] = round(row[stat]*NerfRatio)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    EnemyRandoLogic.SummonsLevelAdjustment()

def LandmarkAdjustments(ChosenAreaOrder): # removes xp and sp gains from landmarks, except for the first one
    for i in range(0, len(ChosenAreaOrder)):
        landmarkpopfile = "./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_LandmarkPop.json"
        with open(landmarkpopfile, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                row["getEXP"] = 0
                row["getSP"] = 0
                row["developZone"] = 0
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_gmk/ma02a_FLD_LandmarkPop.json", 'r+', encoding='utf-8') as file: # removes xp gains from argentum landmarks
            data = json.load(file)
            for row in data["rows"]:
                row["getEXP"] = 0
                row["getSP"] = 0
                row["developZone"] = 0
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_gmk/ma21a_FLD_LandmarkPop.json", 'r+', encoding='utf-8') as file: # removes xp gains from elysium landmarks
            data = json.load(file)
            for row in data["rows"]:
                row["getEXP"] = 0
                row["getSP"] = 0
                row["developZone"] = 0
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def AddQuestConditions(SetCount, ChosenAreaOrder): # Adding conditions for each area's warp to be unlocked + 1 to allow me to disable all other stuff (salvage points are the big one atm)
    # First, need to replace any conditions
    with open("./_internal/JsonOutputs/common/FLD_ConditionScenario.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["ScenarioMax"] > 10009:
                row["ScenarioMax"] = 10009
            if row["NotScenarioMin"] < 10009:
                row["NotScenarioMin"] = 10009
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    for i in range(0, len(ChosenAreaOrder)):
        eventpopfile = "./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_EventPop.json"
        with open(eventpopfile, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                if row["ScenarioFlagMax"] > 10009:
                    row["ScenarioFlagMax"] = 10009
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    # Condition 3903 Disables Stuff when applied to it.
    with open("./_internal/JsonOutputs/common/FLD_ConditionScenario.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["rows"].append({"$id": 322, "ScenarioMin": 1001, "ScenarioMax": 1002, "NotScenarioMin": 0, "NotScenarioMax": 0})
        for i in range(0, SetCount):
            data["rows"].append({"$id": 323 + i, "ScenarioMin": 10011 + i, "ScenarioMax": 10048, "NotScenarioMin": 0, "NotScenarioMax": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["rows"].append({"$id": 3903, "Premise": 0, "ConditionType1": 1, "Condition1": 322, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        for i in range(0, SetCount):
            data["rows"].append({"$id": 3904 + i, "Premise": 0, "ConditionType1": 1, "Condition1": 323 + i, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    OrderedMapIDs = []
    with open("./_internal/JsonOutputs/common/FLD_maplist.json", 'r+', encoding='utf-8') as file: # pretty sure this is messing up stuff with the maps
        data = json.load(file)
        for i in range(0, len(ChosenAreaOrder)):
            for row in data["rows"]:
                if row["select"] == ContinentInfo[ChosenAreaOrder[i]][2]:
                    OrderedMapIDs.append(row["$id"])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_WorldMapCond.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] <= len(ChosenAreaOrder):
                row["mapId"] = ContinentInfo[ChosenAreaOrder[row["$id"] - 1]][3] # puts the mapIDs in order, so we can assign conditions in order
                row["cond1"] = 3903 + row["$id"]
                row["enter"] = 0
            elif row["$id"] == len(ChosenAreaOrder) + 1:
                row["mapId"] = 3
                row["cond1"] = 3904
            else:
                row["mapId"] = 0
                row["cond1"] = 3903
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def NoUnintendedRewards(ChosenAreaOrder): # Removes any cheese you can do by doing sidequests, selling Collection Point items
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/FLD_QuestReward.json", ["Gold", "EXP", "Sp", "Coin", "DevelopZone", "DevelopPoint", "TrustPoint", "MercenariesPoint", "IdeaCategory", "IdeaValue", "ItemID1", "ItemNumber1", "ItemID2", "ItemNumber2", "ItemID3", "ItemNumber3", "ItemID4", "ItemNumber4"], 0) # doing quests don't reward you
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/ITM_CollectionList.json", ["Price"], 0) # collectables sell for 0
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_SalvagePointList.json", ["Condition"], 3903) # salvaging is disabled
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_Grow.json"], ["LevelExp", "LevelExp2", "EnemyExp"], ['252']) # It costs 252 xp to level up, regardless of level
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/FLD_GravePopList.json", ["en_popID"], 0) # Keeps you from respawning a UM.
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/ma02a_FLD_TboxPop.json", ["Condition"], 3903) # removes drops from chests in argentum
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/ma02a_FLD_NpcPop.json", ["QuestID"], 0) # removes talking to NPCs in argentum
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/ma21a_FLD_TboxPop.json", ["Condition"], 3903) # removes treasure chests from Elysium
    for area in ChosenAreaOrder:
        Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/" + ContinentInfo[area][2] + "_FLD_TboxPop.json", ["Condition"], 3903) # removes drops from chests
        Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/" + ContinentInfo[area][2] + "_FLD_NpcPop.json", ["QuestID"], 0) # removes talking to NPCs in area

def SpiritCrucibleEntranceRemoval(): # Exiting or Entering Spirit Crucible has problems with resetting the quest condition. So we remove that by warping the player back to the original landmark in that area.
    with open("./_internal/JsonOutputs/common_gmk/FLD_MapJump.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 3: # Leftherian Entrance to Spirit Crucible
                row["MapJumpId"] = 166 # get pranked lmao
            if row["$id"] == 4: # Spirit Crucible Entrance to Leftheria
                row["MapJumpId"] = 167 # get pranked lmao
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def BladeTrustRequirementChanges(): # changes the blade trust/skill unlock requirements to defeating a specific number of UMs
    NumberofUMstoDefeat = [8, 16, 24, 32]
    KeyAchievementIDs = [15, 25, 0, 35, 45, 55, 65, 75, 85, 95, 105, 0, 0, 115, 125, 135, 145, 375, 385, 155, 185, 165, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295, 305, 315, 325, 335, 345, 195, 355, 365, 395, 0, 415, 425, 465, 455, 445, 435, 405, 175, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 95, 405, 455, 455, 445, 435, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 365, 85, 1668, 1678, 1648, 1658, 1739, 1749, 0, 1759, 1739, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 325, 325, 325, 1679, 1689, 1699, 1709, 1719, 1729]
    KeyAchievementIDs = list(set([x for x in KeyAchievementIDs if x != 0]))
    TaskIDs = Helper.ExtendListtoLength([Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_QuestCondition.json", "$id") + 1], 4, "inputlist[i-1]+1")
    TaskLogIDs = [659, 660, 661, 662]
    ValidBladeIDs = [1001, 1002, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1076, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1111, 1112]
    StarterBladeTrustSetAppearance = [16, 11, 12, 13, 14] #rank 1
    Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopchange.json", "$id") + 1
    ArtandSkillCols = ["ArtsAchievement1", "ArtsAchievement2", "ArtsAchievement3", "SkillAchievement1", "SkillAchievement2", "SkillAchievement3", "FskillAchivement1", "FskillAchivement2", "FskillAchivement3"]
    TrustCol = "KeyAchievement"

    ArtandSkillIDs = []
    TrustIDs = []

    for i in range(0, len(ArtandSkillCols)):
        ArtandSkillIDs += Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/CHR_Bl.json", ["$id"], ValidBladeIDs, ArtandSkillCols[i])
        ArtandSkillIDs = [x for x in ArtandSkillIDs if x != 0]

    TrustIDs.extend(Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/CHR_Bl.json", ["$id"], ValidBladeIDs, TrustCol))
    TrustIDs = [x for x in TrustIDs if x != 0]

    with open("./_internal/JsonOutputs/common/FLD_AchievementSet.json", 'r+', encoding='utf-8') as file: # now we need to modify corresponding set ids
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in ArtandSkillIDs:
                for j in range(1, 6):
                    if (row[f"AchievementID{j}"] != 0):
                        row[f"AchievementID{j}"] = 16
            if row["$id"] in TrustIDs:
                for j in range(1,6):
                    row[f"AchievementID{j}"] = StarterBladeTrustSetAppearance[j-1]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_Achievement.json", 'r+', encoding='utf-8') as file: #we need to change FLD_Achievement ID 1 to walk 1 step total
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1:
                    row["StatsID"] = 60
                    row["Count"] = 1
                    row["DebugName"] = "WALK_TOTAL"
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_QuestTaskAchievement.json", 'r+', encoding='utf-8') as file: #now we need to modify the FLD_QuestTaskAchievement
        data = json.load(file)
        for i in range(0, 4):
            for row in data["rows"]:
                if row["$id"] <= 7004:
                    row["TaskType1"] = 10
                    row["TaskID1"] = TaskIDs[row["$id"]-7001]
                    row["TaskCondition1"] = 0
                if row["$id"] == 7005:
                    row["TaskType1"] = 12
                    row["TaskID1"] = 1
                    row["TaskCondition1"] = 0
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_QuestCondition.json", 'r+', encoding='utf-8') as file: # Adding new Quest Conditions
        data = json.load(file)
        ConditionListRows = Helper.ExtendListtoLength([Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_ConditionList.json", "$id") + 1], 4, "inputlist[i-1]+1")
        for i in range(0, 4):
            data["rows"].append({"$id": TaskIDs[i], "ConditionID": ConditionListRows[i], "MapID": 0, "NpcID": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file: # Adding new ConditionIDs for Quest Condition
        data = json.load(file)
        FlagListRows = Helper.ExtendListtoLength([Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_ConditionFlag.json", "$id") + 1], 4, "inputlist[i-1]+1")
        for i in range(0, 4):
           data["rows"].append({"$id": ConditionListRows[i], "Premise": 0, "ConditionType1": 4, "Condition1": FlagListRows[i], "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0 , "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    
    with open("./_internal/JsonOutputs/common/FLD_ConditionFlag.json", 'r+', encoding='utf-8') as file: # Adding new checks for the # of UMs defeated flag
        data = json.load(file)
        for i in range(0, 4):
           data["rows"].append({"$id": FlagListRows[i], "FlagType": 8, "FlagID": 2164, "FlagMin": NumberofUMstoDefeat[i], "FlagMax": 256})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    with open("./_internal/JsonOutputs/common_ms/fld_quest_achievement.json", 'r+', encoding='utf-8') as file: #modifying the text files that describe what you need to do to unlock the node
        data = json.load(file)
        for i in range(0, 4):
            for row in data["rows"]:
                if row["$id"] == TaskLogIDs[i]:
                    row["name"] = f"Defeat {NumberofUMstoDefeat[i]} total Unique Monsters."
                    break
            for row in data["rows"]:
                if row["$id"] == 663:
                    row["name"] = "Unlocked once you unlock the \n corresponding Trust Level."
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def UMHuntMenuTextChanges():
    seedhashcomplete = random.choice(IDs.SeedHashAdj) + " " + random.choice(IDs.SeedHashNoun) 
    with open("./_internal/JsonOutputs/common_ms/menu_ms.json", 'r+', encoding='utf-8') as file: #puts the seed hash text on the main menu and on the save game screen
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 128:
                row["name"] = f"Seed Hash: [System:Color name=green]{seedhashcomplete}[/System:Color]"
                row["style"] = 166
            if row["$id"] == 129:
                row["name"] = "[System:Color name=tutorial]Unique Monster Hunt[/System:Color]"
            if row["$id"] in [983, 1227]:
                row["name"] = "Bounties"
            if row["$id"] == 1644:
                row["name"] = f"{seedhashcomplete}"
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/menu_main_contents_ms.json", 'r+', encoding='utf-8') as file: # Changes the name of "Expansion Pass"
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 10:
                row["name"] = "Voucher Rewards"
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ReceiptTextChanges(): # Changes the test for the Core Crystal Shop Receipts
    ProofofPurchaseNameIDs = Helper.InclRange(617, 632)
    ProofofPurchaseNameTexts = ["ATK 1 Receipt", "ATK 2 Receipt", "ATK 3 Receipt", "ATK 4 Receipt", "TNK 1 Receipt", "TNK 2 Receipt", "TNK 3 Receipt", "HLR 1 Receipt", "HLR 2 Receipt", "HLR 3 Receipt", "DLC 1 Receipt", "DLC 2 Receipt", "DLC 3 Receipt", "NG+ 1 Receipt", "NG+ 2 Receipt", "NG+ 3 Receipt"]
    ProofofPurchaseDescriptionIDs = Helper.InclRange(718, 733)
    ProofofPurchaseDescriptionText = "Proof you purchased this Blade Bundle."
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in ProofofPurchaseIDs: # Proof of Purchases for Core Crystal Bundles
                row["ValueMax"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for i in range(0, len(ProofofPurchaseIDs)):
            for row in data["rows"]:
                if row["$id"] == ProofofPurchaseNameIDs[i]:
                    row["name"] = ProofofPurchaseNameTexts[i]
                if row["$id"] == ProofofPurchaseDescriptionIDs[i]:
                    row["name"] = ProofofPurchaseDescriptionText
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def UMRewardDropChanges(): #Changes text for the UM drops we want
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in Helper.InclRange(25479, 25489): # Custom Shop/UM Drop Token IDs
                row["ValueMax"] = 255
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes name text file
        data = json.load(file)
        for i in range(1, 11):
            for row in data["rows"]:
                if row["$id"] == 962 + i:
                    row["name"] = f"[System:Color name=green]Bounty Token Lv {i}[/System:Color]"
                if row["$id"] == 978 + i:
                    row["name"] = "Can be traded at the \nBounty Token Exchange for upgrades."
                    break
        for row in data["rows"]:
            if row["$id"] == 973:
                row["name"] = "[System:Color name=tutorial]Doubloon[/System:Color]"
            if row["$id"] == 989:
                row["name"] = "Can be traded at shops for upgrades."
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def IdentifyDLCBladeCrystals(CrystalList):
    DLCBladeCrystalList = []
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: # Adds the exchange tasks
        data = json.load(file)
        for i in range(0, len(CrystalList)):
            for row in data["rows"]:
                if (row["$id"] == CrystalList[i]) and (row["BladeID"] in [1105, 1106, 1107, 1108, 1109, 1111]):
                    DLCBladeCrystalList.append(row["$id"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    return DLCBladeCrystalList

def IdentifyClassBladeCrystals(CrystalList): # go from ITM_CrystalList $id->bladeID-> CHR_Bl $id->WeaponType-> ITM_PcWpnType $id->Role
    CrystalBladeIDList = []
    CrystalWeaponTypeIDList = []
    CrystalWeaponRoleList = []
    AttackerList = []
    HealerList = []
    TankList = []
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: # Getting BladeIDs for a Crystal $id
        data = json.load(file)
        for i in range(0, len(CrystalList)):
            for row in data["rows"]:
                if row["$id"] == CrystalList[i]:
                    CrystalBladeIDList.append(row["BladeID"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/CHR_Bl.json", 'r+', encoding='utf-8') as file: # Getting WeaponType for a Blade $id
        data = json.load(file)
        for i in range(0, len(CrystalBladeIDList)):
            for row in data["rows"]:
                if row["$id"] == CrystalBladeIDList[i]:
                    CrystalWeaponTypeIDList.append(row["WeaponType"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_PcWpnType.json", 'r+', encoding='utf-8') as file: # Getting Role for a WeaponType $id
        data = json.load(file)
        for i in range(0, len(CrystalWeaponTypeIDList)):
            for row in data["rows"]:
                if row["$id"] == CrystalWeaponTypeIDList[i]:
                    CrystalWeaponRoleList.append(row["Role"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    for i in range(0, len(CrystalList)):
        if CrystalWeaponRoleList[i] == 1: # Tank
            TankList.append(CrystalList[i])
        elif CrystalWeaponRoleList[i] == 2: # Attacker
            AttackerList.append(CrystalList[i])
        else: # Healer
            HealerList.append(CrystalList[i])
    return TankList, AttackerList, HealerList

def CoreCrystalIdentification(): # Figuring out the groups that each Core Crystal Belongs to, then picking items from each group for the shop
    ShuffleCoreCrystals()
    AllBladeCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    NGPlusBladeCrystalIDs = RaceMode.DetermineNGPlusBladeCrystalIDs()
    RemainingBladeCrystalIDs = [x for x in AllBladeCrystalIDs if x not in NGPlusBladeCrystalIDs]
    DLCBladeCrystalIDs = IdentifyDLCBladeCrystals(RemainingBladeCrystalIDs)
    RemainingBladeCrystalIDs = [x for x in RemainingBladeCrystalIDs if x not in DLCBladeCrystalIDs]
    TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs = IdentifyClassBladeCrystals(RemainingBladeCrystalIDs)
    CoreCrystalGroupCreation(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs)

def ShuffleCoreCrystals(): # first we need to shuffle the blade ids into the core crystal pool
    AllBladeCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    BladeIDs = [1008, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1050, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1104, 1108, 1109, 1105, 1106, 1107, 1111]
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        RandomBlades = BladeIDs.copy()
        random.shuffle(RandomBlades)
        for i in range(0, len(AllBladeCrystalIDs)):
            for row in data["rows"]:
                if row["$id"] == AllBladeCrystalIDs[i]:
                    row["BladeID"] = RandomBlades[i]
                    row["ValueMax"] = 1
                    row["NoMultiple"] = i + 11
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def CoreCrystalGroupCreation(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs):
    Item1IDs, Item2IDs, Item3IDs, Item4IDs = [], [], ProofofPurchaseIDs, Helper.ExtendListtoLength([], 16, "0")
    ChosenAtkBlades, ChosenTnkBlades, ChosenHlrBlades = random.sample(AttackerBladeCrystalIDs, min(8, len(AttackerBladeCrystalIDs))), random.sample(TankBladeCrystalIDs, min(6, len(TankBladeCrystalIDs))), random.sample(HealerBladeCrystalIDs, min(6, len(HealerBladeCrystalIDs)))
    ChosenAtkBlades = Helper.ExtendListtoLength(ChosenAtkBlades, 8 , "0")
    ChosenTnkBlades = Helper.ExtendListtoLength(ChosenTnkBlades, 6 , "0")
    ChosenHlrBlades = Helper.ExtendListtoLength(ChosenHlrBlades, 6 , "0")
    ChosenNGPlusBladeCrystalIDs = random.sample(NGPlusBladeCrystalIDs, min(3, len(NGPlusBladeCrystalIDs)))
    ChosenDLCBladeCrystalIDs = random.sample(DLCBladeCrystalIDs, min(3, len(DLCBladeCrystalIDs)))
    ChosenNGPlusBladeCrystalIDs = Helper.ExtendListtoLength(ChosenNGPlusBladeCrystalIDs, 3, "0")
    ChosenDLCBladeCrystalIDs = Helper.ExtendListtoLength(ChosenDLCBladeCrystalIDs, 3, "0")
    Item1IDs.extend(ChosenAtkBlades[:4])
    Item1IDs.extend(ChosenTnkBlades[:3])
    Item1IDs.extend(ChosenHlrBlades[:3])
    Item1IDs.extend(ChosenDLCBladeCrystalIDs[:3])
    Item1IDs.extend(ChosenNGPlusBladeCrystalIDs[:3])
    Item2IDs.extend(ChosenAtkBlades[-4:])
    Item2IDs.extend(ChosenTnkBlades[-3:])
    Item2IDs.extend(ChosenHlrBlades[-3:])
    Item2IDs = Helper.ExtendListtoLength(Item2IDs, 16, "0")
    global OutputCrystalGroupItemIDs
    OutputCrystalGroupItemIDs = [Item1IDs, Item2IDs, Item3IDs, Item4IDs]
    RenameCrystals(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs)
    # Output should be [16, 16, 16, 16] format, with last 2 entries being 0

def RenameCrystals(NGPlusBladeCrystalIDs, DLCBladeCrystalIDs, TankBladeCrystalIDs, AttackerBladeCrystalIDs, HealerBladeCrystalIDs):    
    AllBladeCrystalIDs = Helper.InclRange(45002,45004) + Helper.InclRange(45006, 45009) + [45016] + Helper.InclRange(45017,45049) + [45056, 45057]
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/ITM_CrystalList.json", ["Condition", "CommonID", "CommonWPN", "CommonAtr", "Price", "RareTableProb", "RareBladeRev", "AssureP"], 0)
    with open("./_internal/JsonOutputs/common_ms/itm_crystal.json", "r+", encoding='utf-8') as file: # Now we want to rename crystals according to their category
        IDNumbers = Helper.InclRange(16, 20)
        CrystalCategoryNames = ["NG+ Core Crystal", "DLC Core Crystal", "TNK Core Crystal", "ATK Core Crystal", "HLR Core Crystal"]
        data = json.load(file)
        for i in range(0, len(IDNumbers)):
            data["rows"].append({"$id": IDNumbers[i], "style": 36, "name": CrystalCategoryNames[i]})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_CrystalList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in NGPlusBladeCrystalIDs:
                row["Name"] = 16
            elif row["$id"] in DLCBladeCrystalIDs:
                row["Name"] = 17
            elif row["$id"] in TankBladeCrystalIDs:
                row["Name"] = 18
            elif row["$id"] in AttackerBladeCrystalIDs:
                row["Name"] = 19
            elif row["$id"] in HealerBladeCrystalIDs:
                row["Name"] = 20
            else:
                row["Name"] = 12
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def WPAdjustments(): # Changes how much a weapon manual gives, and how much is needed to max an art
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP2"], 250) # 250 to upgrade each level
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP3"], 250)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP4"], 250)
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", ["NeedWP5"], 250)
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 25405:
                row["Type"] = 250 # Changed the amount of WP it gives to 250
                continue
            if row["$id"] == 25406:
                row["Type"] = 500
                continue
            if row["$id"] == 25407:
                row["Type"] = 1000
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes names of WP Boosting Items
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 715:
                row["name"] = "250 WP Booster"
                continue
            if row["$id"] == 716:
                row["name"] = "500 WP Booster"
                continue
            if row["$id"] == 717:
                row["name"] = "1000 WP Booster"
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ChipShopRewards():
    ChipStrengthLists = Helper.ExtendListtoLength([], 20, "[]")
    global ChipBundleNames
    Chips1, Chips2, Chips3, Chips4, ChipBundleNames = [], [], [], Helper.ExtendListtoLength([], 16, "0"), []
    with open("./_internal/JsonOutputs/common/ITM_PcWpnChip.json", 'r+', encoding='utf-8') as file: # Assigns weapons to groups based on category
        data = json.load(file)
        for row in data["rows"]:
            ChipStrengthLists[row["Rank"] - 1].append(row["$id"])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    for i in range(0, 16):
        if i <= 13:
            chosenrewards = random.choices(ChipStrengthLists[i+1] + ChipStrengthLists[i+2], weights= Helper.ExtendListtoLength([], len(ChipStrengthLists[i+1]), "2") + Helper.ExtendListtoLength([], len(ChipStrengthLists[i+2]), "1"), k = 3)
        elif i == 14:
            chosenrewards = random.choices(ChipStrengthLists[16] + ChipStrengthLists[17], weights= Helper.ExtendListtoLength([], len(ChipStrengthLists[16]), "2") + Helper.ExtendListtoLength([], len(ChipStrengthLists[17]), "1"), k = 3)    
        elif i == 15:
            chosenrewards = random.choices(ChipStrengthLists[18] + ChipStrengthLists[19], weights= Helper.ExtendListtoLength([], len(ChipStrengthLists[18]), "2") + Helper.ExtendListtoLength([], len(ChipStrengthLists[19]), "1"), k = 3)    
        else:
            chosenrewards = random.choices(ChipStrengthLists[19] + ChipStrengthLists[20], weights= Helper.ExtendListtoLength([], len(ChipStrengthLists[19]), "2") + Helper.ExtendListtoLength([], len(ChipStrengthLists[20]), "1"), k = 3) 
        Chips1.append(chosenrewards[0])
        Chips2.append(chosenrewards[1])
        Chips3.append(chosenrewards[2])
    global ChipShopRewardDistribution
    ChipShopRewardDistribution = [Chips1, Chips2, Chips3, Chips4]
    for i in range(0, 16):
        ChipBundleNames.append(f"Chip Bundle {i+1}")

def WeaponPowerLevel(): # Assigns appropriately powered enhancement and damage value based on rank of weapon
    WeaponStrengthList = Helper.ExtendListtoLength([], 20, "[]")
    WeaponDamageRanges = [[14, 31], [26, 61], [49, 117], [86, 184], [123, 248], [160, 324], [197, 409], [243, 480], [275, 544], [307, 588], [332, 639], [360, 695], [387, 746], [421, 811], [470, 872], [501, 919], [527, 967], [549, 990], [553, 1037], [592, 1108]]
    InvalidSkillEnhancements = [ArtCancel,EyeOfJustice, XStartBattle, YStartBattle, BStartBattle, BladeSwapDamage, CatScimPowerUp, EvadeDrainHp, EvadeDriverArt, EtherCannonRange,ArtDamageHeal, DreamOfTheFuture, WPEnemiesBoost, ExpEnemiesBoost]
    ValidSkills = [x for x in EnhanceClassList if x not in InvalidSkillEnhancements]
    Common, Rare, Legendary = 0, 1, 2
    with open("./_internal/JsonOutputs/common/ITM_PcWpnChip.json", 'r+', encoding='utf-8') as file: # Assigns weapons to groups based on category
        data = json.load(file)
        for row in data["rows"]:
            for i in range(1, 37):
                WeaponStrengthList[row["Rank"] - 1].append(row[f"CreateWpn{i}"])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/ITM_PcWpn.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for row in data["rows"]:
            for i in range(0, len(WeaponStrengthList)):
                if row["$id"] in WeaponStrengthList[i]:
                    row["Damage"] = random.randrange(WeaponDamageRanges[i][0], WeaponDamageRanges[i][1])
                    if row["Rank"] <= 7:
                        curEnh:Enhancement = random.choice(ValidSkills)
                        while curEnh.Caption > 256: # This is needed because the chips descriptions will not load properly they overflow if a caption is above 256. Super annoying the effects work the caption doesnt.
                            curEnh = random.choice(ValidSkills)
                        curEnh.RollEnhancement(Common)
                        row["Enhance1"] = curEnh.id
                    elif row["Rank"] <= 14:
                        curEnh:Enhancement = random.choice(ValidSkills)
                        while curEnh.Caption > 256: # This is needed because the chips descriptions will not load properly they overflow if a caption is above 256. Super annoying the effects work the caption doesnt.
                            curEnh = random.choice(ValidSkills)
                        curEnh.RollEnhancement(Rare)
                        row["Enhance1"] = curEnh.id
                    else:
                        curEnh:Enhancement = random.choice(ValidSkills)
                        while curEnh.Caption > 256: # This is needed because the chips descriptions will not load properly they overflow if a caption is above 256. Super annoying the effects work the caption doesnt.
                            curEnh = random.choice(ValidSkills)
                        curEnh.RollEnhancement(Legendary)
                        row["Enhance1"] = curEnh.id
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def AuxCoreRewards(): # Makes the Aux Core Bundles
    AuxCoreSkillGroups = {
        "Common": {
            "Damage": [TitanDamageUp, MachineDamageUp, HumanoidDamageUp, AquaticDamageUp, AerialDamageUp, InsectDamageUp, BeastDamageUp, BladeComboDamUp, FusionComboDamUp, CritDamageUp, PercentDoubleAuto, FrontDamageUp, SideDamageUp, BackDamageUp, SmashDamageUp, HigherLVEnemyDamageUp, AllyDownDamageUp, BattleDurationDamageUp, LV1Damage, LV2Damage, LV3Damage, LV4Damage],
            "Defensive": [HPLowEvasion, HPLowBlockRate, ReduceSpikeDamage, SpecialAndArtsAggroDown, AggroPerSecondANDAggroUp, AffinityMaxBarrier, AffinityMaxEvade, LowHPRegen, AllDebuffRes, BladeArtsTriggerUp, BladeArtDuration],
            "Playstyle Defining": [SpecialRechargeCancelling, EnemyDropGoldOnHit, DealTakeMore, AwakenPurge, BurstDestroyAnotherOrb, AttackUpGoldUp, DidIDoThat]
        },
        "Rare": {
            "Damage": [IndoorsDamageUp, OutdoorsDamageUp, DamageUpOnEnemyKill, DoubleHitExtraAutoDamage, ToppleANDLaunchDamageUp, PartyDamageMaxAffinity, PartyCritMaxAffinity, AutoAttackCancelDamageUp, AggroedEnemyDamageUp, Transmigration, OppositeGenderBladeDamageUp],
            "Defensive": [HunterChem, ShoulderToShoulder, WhenDiesHealAllies, SmallHpPotCreate, Twang, Jamming, PotionEffectUp, EtherCounter, PhysCounter, RechargeOnEvade],
            "Playstyle Defining": [CritHeal, PartyGaugeCritFill, GlassCannon, CombatMoveSpeed, DestroyOrbOpposingElement, TargetNearbyOrbsChainAttack, PartyGaugeDriverArtFill]
        },
        "Legendary": {
            "Damage": [KaiserZone, AffinityMaxAttack, VersusBossUniqueEnemyDamageUp, AutoSpeedArtsSpeed, DamageUpOnCancel, DamageAndCritUpMaxAffinity, FlatCritBoost],
            "Defensive": [PartyDamageReducMaxAffinity, PhyAndEthDefenseUp, ReduceEnemyChargeMaxAffinity, GravityPinwheel, RestoreHitDamageToParty, ForeSight, FlatBlockBoost],
            "Playstyle Defining": [RecoverRechargeCrit, DealMoreTakeLessMaxAffinity, HpPotChanceFor2, BladeComboOrbAdder, PotionPickupDamageUp, Vision, DamageUpPerCrit, HealingUpMaxAffinity, TakeDamageHeal, StopThinking, ChainAttackPower, DamagePerEvadeUp]
        },
        "Secret":{
            "All": [UMFlatCritBoost, UMSurpriseAttackUp, UMSpecialRecievesAfterImage, UMAutoSpeedArtsSpeed, UMPhyAndEthDefenseUp, UMOnBlockNullDamage, UMFlatBlockBoost]
        }
    }

    Common, Rare, Legendary = 0, 1, 2

    ChosenAuxCores = {
        Common: {
            "Damage": random.sample(AuxCoreSkillGroups["Common"]["Damage"], 16),
            "Defensive": random.sample(AuxCoreSkillGroups["Common"]["Defensive"], 8),
            "Playstyle Defining": random.sample(AuxCoreSkillGroups["Common"]["Playstyle Defining"], 4)
        },
        Rare: {
            "Damage": random.sample(AuxCoreSkillGroups["Rare"]["Damage"], 8),
            "Defensive": random.sample(AuxCoreSkillGroups["Rare"]["Defensive"], 8),
            "Playstyle Defining": random.sample(AuxCoreSkillGroups["Rare"]["Playstyle Defining"], 4)
        },
        Legendary: {
            "Damage": random.sample(AuxCoreSkillGroups["Legendary"]["Damage"], 4),
            "Defensive": random.sample(AuxCoreSkillGroups["Legendary"]["Defensive"], 4),
            "Playstyle Defining": random.sample(AuxCoreSkillGroups["Legendary"]["Playstyle Defining"], 8)
        }
    }

    SecretAuxCores = AuxCoreSkillGroups["Secret"]["All"]

    with open("./_internal/JsonOutputs/common/ITM_OrbEquip.json", 'r+', encoding='utf-8') as file: 
        with open("./_internal/JsonOutputs/common_ms/itm_orb.json", 'r+', encoding='utf-8') as namefile:
            
            namedata = json.load(namefile) 
            data = json.load(file)

            CurRow = 1
            for rarity in ChosenAuxCores:
                for category in ChosenAuxCores[rarity]:
                    for auxCore in ChosenAuxCores[rarity][category]:
                        for row in data["rows"]:
                            if row["$id"] == CurRow + 17000:
                                curAuxCore:Enhancement = auxCore
                                curAuxCore.RollEnhancement(rarity)
                                row["Enhance"] = curAuxCore.id
                                row["Rarity"] = curAuxCore.Rarity
                                row["EnhanceCategory"] = CurRow
                                CurName = row["Name"]
                                CurRow += 1
                                break
                        for namerow in namedata["rows"]:  
                            if namerow["$id"] == CurName:    
                                namerow["name"] = f"{curAuxCore.name} Core"
                                break
            for auxCore in SecretAuxCores:
                for row in data["rows"]:
                    if row["$id"] == CurRow + 17000:
                        curAuxCore:UMHuntSecretShopEnhancements = auxCore
                        curAuxCore.RollEnhancement(2)
                        row["Enhance"] = curAuxCore.id
                        row["Rarity"] = curAuxCore.Rarity
                        row["EnhanceCategory"] = CurRow
                        CurName = row["Name"]
                        CurRow += 1
                        break
                for namerow in namedata["rows"]:  
                    if namerow["$id"] == CurName:    
                        namerow["name"] = f"{curAuxCore.name} Core"
                        break
            namefile.seek(0)
            namefile.truncate()
            json.dump(namedata, namefile, indent=2, ensure_ascii=False)

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    global AuxCoreShopRewardDistribution
    AuxCoreShopRewardDistribution = [Helper.ExtendListtoLength([17001], 16, "inputlist[i-1]+4"), Helper.ExtendListtoLength([17002], 16, "inputlist[i-1]+4"), Helper.ExtendListtoLength([17003], 16, "inputlist[i-1]+4"), Helper.ExtendListtoLength([17004], 16, "inputlist[i-1]+4")]

def PouchItemRewards():
    global PouchItemShopRewardDistribution
    PouchItemShopRewardDistribution = [[],[],[],[]]
    with open("./_internal/JsonOutputs/common/ITM_FavoriteList.json", 'r+', encoding='utf-8') as file: 
        data = json.load(file)
        for i in range(0, 4):
            for j in range(0, 4):
                PouchItemShopRewardDistribution[i].append(random.choice(ValidPouchItems))
        for i in range(12, 24):
            CurrentItemTypeList = []
            for row in data["rows"]:
                if (row["Category"] == i) & (row["$id"] in ValidPouchItems):
                    CurrentItemTypeList.append(row["$id"])
            ChosenItems = random.sample(CurrentItemTypeList, 2)
            PouchItemShopRewardDistribution[0].append(ChosenItems[0])
            PouchItemShopRewardDistribution[1].append(ChosenItems[1])
        PouchItemShopRewardDistribution[2] = Helper.ExtendListtoLength(PouchItemShopRewardDistribution[2], 16, "0")
        PouchItemShopRewardDistribution[3] = Helper.ExtendListtoLength(PouchItemShopRewardDistribution[2], 16, "0")    
        for row in data["rows"]: # Change the duration of all to 60 minutes, and they all give no trust points
            row["Time"] = 60
            row["ValueMax"] = 10
            row["TrustPoint"] = 0
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def AccessoryShopRewards(): # Creates the accessory shop
    AccessorySkillGroups = {
        "Common": {
            "Damage": [TitanDamageUp, MachineDamageUp, HumanoidDamageUp, AquaticDamageUp, AerialDamageUp, InsectDamageUp, BeastDamageUp, CritDamageUp, PercentDoubleAuto, FrontDamageUp, SideDamageUp, BackDamageUp, SmashDamageUp, HigherLVEnemyDamageUp, AllyDownDamageUp, BattleDurationDamageUp],
            "Defensive": [HPLowEvasion, HPLowBlockRate, ReduceSpikeDamage, SpecialAndArtsAggroDown, AggroPerSecondANDAggroUp, LowHPRegen, AllDebuffRes, TastySnack, DoomRes, TauntRes, BladeShackRes, DriverShackRes],
            "Playstyle Defining": [SpecialRechargeCancelling, EnemyDropGoldOnHit, DealTakeMore, AwakenPurge, BurstDestroyAnotherOrb, AttackUpGoldUp, DidIDoThat]
        },
        "Rare": {
            "Damage": [IndoorsDamageUp, OutdoorsDamageUp, DamageUpOnEnemyKill, DoubleHitExtraAutoDamage, ToppleANDLaunchDamageUp, AutoAttackCancelDamageUp, AggroedEnemyDamageUp, Transmigration, OppositeGenderBladeDamageUp, BladeSwitchDamageUp, BreakResDown],
            "Defensive": [WhenDiesHealAllies, SmallHpPotCreate, Twang, Jamming, PotionEffectUp, EtherCounter, PhysCounter, RechargeOnEvade, FlatHPBoost, ArtUseHeal, AgiBoost],
            "Playstyle Defining": [CritHeal, PartyGaugeCritFill, GlassCannon, CombatMoveSpeed, DestroyOrbOpposingElement, TargetNearbyOrbsChainAttack, PartyGaugeDriverArtFill]
        },
        "Legendary": {
            "Damage": [KaiserZone, VersusBossUniqueEnemyDamageUp, AutoSpeedArtsSpeed, DamageUpOnCancel, FlatStrengthBoost, FlatEtherBoost],
            "Defensive": [GravityPinwheel, RestoreHitDamageToParty, ForeSight, FlatAgiBoost, HPBoost, CritHeal],
            "Playstyle Defining": [RecoverRechargeCrit, HpPotChanceFor2, BladeComboOrbAdder, PotionPickupDamageUp, Vision, DamageUpPerCrit, TakeDamageHeal, DamagePerEvadeUp, PartyHealBladeSwitch, LowHPSpecialUp]
        },
        "Secret": {
            "All": [UMAllWeaponAttackUp, UMSpecialRechargeCancelling, UMHigherLVEnemyDamageUp, UMVision, UMBreakResDown, UMStrengthBoost, UMEtherBoost]
        }
    }

    Common, Rare, Legendary = 0, 1, 2

    ChosenAccessories = {
        Common: {
            "Damage": random.sample(AccessorySkillGroups["Common"]["Damage"], 16),
            "Defensive": random.sample(AccessorySkillGroups["Common"]["Defensive"], 8),
            "Playstyle Defining": random.sample(AccessorySkillGroups["Common"]["Playstyle Defining"], 4)
        },
        Rare: {
            "Damage": random.sample(AccessorySkillGroups["Rare"]["Damage"], 8),
            "Defensive": random.sample(AccessorySkillGroups["Rare"]["Defensive"], 8),
            "Playstyle Defining": random.sample(AccessorySkillGroups["Rare"]["Playstyle Defining"], 4)
        },
        Legendary: {
            "Damage": random.sample(AccessorySkillGroups["Legendary"]["Damage"], 4),
            "Defensive": random.sample(AccessorySkillGroups["Legendary"]["Defensive"], 4),
            "Playstyle Defining": random.sample(AccessorySkillGroups["Legendary"]["Playstyle Defining"], 8)
        }
    }

    SecretAccessories = AccessorySkillGroups["Secret"]["All"]

    AccessoryTypesandNames = { # What icon should go with what noun:
        0:["Sandals", "Crocs", "Jordans", "Boots", "Sneakers"], 
        1:["Baseball Cap", "Sweatband", "Beanie", "Earmuffs"], 
        2:["Vest", "Tuxedo", "T-Shirt", "Tank Top", "Jacket"], 
        3:["Choker", "Necklace", "Locket", "Tie"], 
        4:["Belt", "Sash", "Scarf"], 
        5:["Banner", "Loincloth", "Swimsuit", "Thread", "Lamp", "Incense"], 
        6:["Gloves", "Silly Bandz", "Gauntlets", "Bangles", "Watches"],
        7:["Cube", "AirPods", "Headphones", "Hard Drive", "Attachment"],
        8:["Garnet", "Sapphire", "Diamond", "Ruby", "Emerald", "Prismarine"],
        9:["Feather", "Medal", "Bling"]
    }

    with open("./_internal/JsonOutputs/common/ITM_PcEquip.json", 'r+', encoding='utf-8') as file: 
        with open("./_internal/JsonOutputs/common_ms/itm_pcequip.json", 'r+', encoding='utf-8') as namefile:
            
            namedata = json.load(namefile) 
            data = json.load(file)
            
            CurRow = 1
            for rarity in ChosenAccessories:
                for category in ChosenAccessories[rarity]:
                    for accessory in ChosenAccessories[rarity][category]:
                        for row in data["rows"]:
                            if row["$id"] == CurRow:
                                curAccessory:Enhancement = accessory
                                curAccessory.RollEnhancement(rarity)
                                row["Enhance1"] = curAccessory.id
                                row["Rarity"] = curAccessory.Rarity
                                ItemType = random.randint(0,9)
                                row["Icon"] = ItemType
                                CurName = row["Name"]
                                CurRow += 1
                                break
                        for namerow in namedata["rows"]:  
                            if namerow["$id"] == CurName:
                                lastWord = random.choice(AccessoryTypesandNames[ItemType])
                                namerow["name"] = f"{curAccessory.name} {lastWord}"
                                break
            for accessory in SecretAccessories:
                for row in data["rows"]:
                    if row["$id"] == CurRow:
                        curAccessory:UMHuntSecretShopEnhancements = accessory
                        curAccessory.RollEnhancement(2)
                        row["Enhance1"] = curAccessory.id
                        row["Rarity"] = curAccessory.Rarity
                        ItemType = random.randint(0,9)
                        row["Icon"] = ItemType
                        CurName = row["Name"]
                        CurRow += 1
                        break
                for namerow in namedata["rows"]:  
                    if namerow["$id"] == CurName:
                        lastWord = random.choice(AccessoryTypesandNames[ItemType])
                        namerow["name"] = f"{curAccessory.name} {lastWord}"
                        break
            namefile.seek(0)
            namefile.truncate()
            json.dump(namedata, namefile, indent=2, ensure_ascii=False)

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    global AccessoryShopRewardDistribution
    AccessoryShopRewardDistribution = [Helper.ExtendListtoLength([1], 16, "inputlist[i-1]+4"), Helper.ExtendListtoLength([2], 16, "inputlist[i-1]+4"), Helper.ExtendListtoLength([3], 16, "inputlist[i-1]+4"), Helper.ExtendListtoLength([4], 16, "inputlist[i-1]+4")]

def PoppiswapShopRewards(): # Creates rewards for Poppiswap Shop
    CrystalRows = Helper.InclRange(27, 37)
    StartingCondListRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_ConditionList.json", "$id") + 1
    StartingItemCondRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_ConditionItem.json", "$id") + 1
    StartingDLCItemTextRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/menu_dlc_gift.json", "$id") + 1
    CrystalVoucherNameIDs = Helper.InclRange(633, 643)
    CrystalVoucherCaptionIDs = Helper.InclRange(734, 744)
    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, 11): # ConditionType of 5 is "Item", meaning you need that item listed in FLD_ConditionItem
            data["rows"].append({"$id": StartingCondListRow + i, "Premise": 0, "ConditionType1": 5, "Condition1": StartingItemCondRow + i, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_ConditionItem.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, 11):
            data["rows"].append({"$id": StartingItemCondRow + i, "ItemCategory": 0, "ItemID": 25322 + i, "Number": 1})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes names of Contracts
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] >= 633:
                for i in range(0, len(CrystalVoucherNameIDs)):
                    if row["$id"] == CrystalVoucherNameIDs[i]:
                        row["name"] = f"Ether Crystal Pack {i+1}"
                    if row["$id"] == CrystalVoucherCaptionIDs[i]:
                        row["name"] = f"Unlocks a DLC {1000*(i+1)} Ether Crystal Reward"
            if row["$id"] >= 745:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_DlcGift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in CrystalRows:
                row["releasecount"] = 2
                row["item_id"] = 0
                row["category"] = 3
                row["value"] = 1000*(row["$id"] - 26)
                row["disp_item_info"] = 0
                row["condition"] = StartingCondListRow + (row["$id"] - 27)
                row["title"] = StartingDLCItemTextRow + (row["$id"] - 27)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/menu_dlc_gift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for i in range(0, 11):
            data["rows"].append({"$id": StartingDLCItemTextRow + i, "style": 162, "name": f"Poppiswap Crafting Materials Rank {i+1}"})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def PoppiswapCostChanges(): # Reduces cost of poppiswap stuff
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/ITM_HanaArtsEnh.json","./_internal/JsonOutputs/common/ITM_HanaAssist.json", "./_internal/JsonOutputs/common/ITM_HanaAtr.json", "./_internal/JsonOutputs/common/ITM_HanaNArtsSet.json", "./_internal/JsonOutputs/common/ITM_HanaRole.json"], ["NeedEther", "DustEther"], ['max(row[key] // 4, 1)'])
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_HanaPower.json"], ["EtherNum1", "EtherNum2", "EtherNum3"], ['max(row[key] // 4, 1)'])
    Helper.MathmaticalColumnAdjust(["./_internal/JsonOutputs/common/BTL_HanaBase.json"], ["Circuit4Num", "Circuit5Num", "Circuit6Num"], ['max(row[key] // 10, 1)'])

def GambaShopRewards(): # Makes the rewards for the gamba shop
    GambaCouponRows = Helper.InclRange(11, 26)
    StartingCondListRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_ConditionList.json", "$id") + 1
    StartingItemCondRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_ConditionItem.json", "$id") + 1
    StartingDLCItemTextRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/menu_dlc_gift.json", "$id") + 1
    GambaVoucherNameIDs = Helper.InclRange(644, 659)
    GambaVoucherCaptionIDs = Helper.InclRange(745, 760)
    global ShopTokenRewardResults
    ShopTokenRewardResults = random.choices([5, 10, 15, 25, 35, 50, 100], weights=[30, 20, 15, 15, 10, 5, 5], k = 16) # 50% chance to lose tokens, 50% chance to make winnings back + some in theory, but can be better or worse depending on rolled values
    with open("./_internal/JsonOutputs/common/FLD_ConditionList.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, 16): # ConditionType of 5 is "Item", meaning you need that item listed in FLD_ConditionItem
            data["rows"].append({"$id": StartingCondListRow + i, "Premise": 0, "ConditionType1": 5, "Condition1": StartingItemCondRow + i, "ConditionType2": 0, "Condition2": 0, "ConditionType3": 0, "Condition3": 0, "ConditionType4": 0, "Condition4": 0, "ConditionType5": 0, "Condition5": 0, "ConditionType6": 0, "Condition6": 0, "ConditionType7": 0, "Condition7": 0, "ConditionType8": 0, "Condition8": 0})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_ConditionItem.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, 16):
            data["rows"].append({"$id": StartingItemCondRow + i, "ItemCategory": 0, "ItemID": 25333 + i, "Number": 1})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes names of Contracts
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] >= 644:
                for i in range(0, len(GambaVoucherNameIDs)):
                    if row["$id"] == GambaVoucherNameIDs[i]:
                        row["name"] = f"Mystery Voucher {i+1}"
                    if row["$id"] == GambaVoucherCaptionIDs[i]:
                        row["name"] = f"Unlocks the corresponding\n [System:Color name=tutorial]Doubloon[/System:Color] Booster Pack."
            if row["$id"] >= 761:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_DlcGift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for i in range(0, len(GambaCouponRows)):
            for row in data["rows"]:
                if row["$id"] == GambaCouponRows[i]:
                    row["releasecount"] = 3
                    row["item_id"] = 25489
                    row["category"] = 1
                    row["value"] = ShopTokenRewardResults[i]
                    row["disp_item_info"] = 0
                    row["condition"] = StartingCondListRow + i
                    row["title"] = StartingDLCItemTextRow + i
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/menu_dlc_gift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for i in range(0, 16):
            data["rows"].append({"$id": StartingDLCItemTextRow + i, "style": 162, "name": f"[System:Color name=tutorial]Doubloon[/System:Color] Booster Pack {i+1}"})
        for row in data["rows"]:
            if row["$id"] == 8:
                row["name"] = "[System:Color name=green]Bounty Token[/System:Color] Rewards"
            if row["$id"] == 9:
                row["name"] = "Poppiswap Crafting Materials"
            if row["$id"] == 38:
                row["name"] = "[System:Color name=tutorial]Doubloon[/System:Color] Booster Packs"
            if row["$id"] == 10:
                row["name"] = "Junk"
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    global GambaShopRewardList
    GambaShopRewardList = Helper.ExtendListtoLength([25333], 16, "inputlist[i-1] + 1")
    random.shuffle(GambaShopRewardList)

def AddDLCRewards(ChosenAreaOrder):
    BountyCollectionRewards = Helper.InclRange(1, 10)
    StartingDLCItemTextRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/menu_dlc_gift.json", "$id") + 1
    with open("./_internal/JsonOutputs/common/MNU_DlcGift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for i in range(0, len(BountyCollectionRewards)):
            for row in data["rows"]:
                if row["$id"] == BountyCollectionRewards[i]:
                    row["releasecount"] = 1
                    row["item_id"] = 25479 + i
                    row["category"] = 1
                    row["value"] = 4
                    row["disp_item_info"] = 0
                    row["condition"] = 3904 + i
                    row["title"] = StartingDLCItemTextRow + i
                    break
        if len(ChosenAreaOrder) != len(BountyCollectionRewards):
            for i in range(len(ChosenAreaOrder), len(BountyCollectionRewards)):
                for row in data["rows"]:
                    if row["$id"] == BountyCollectionRewards[i]:
                        row["condition"] = 3903
        del data["rows"][37:]
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/menu_dlc_gift.json", 'r+', encoding='utf-8') as file: #edits DLC items
        data = json.load(file)
        for i in range(0, 10):
            data["rows"].append({"$id": StartingDLCItemTextRow + i, "style": 162, "name": f"[System:Color name=green]Bounty Token[/System:Color] Rewards, Set {i+1}"})
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def AddSPManual(): # Creates 3 SP Manuals, using ID 25015, 25018, 25033
    SPManualIDs = [25349, 25350, 25351]
    SPManualNameIDs = [660, 661, 662]
    SPManualCaptionIDs = [761, 762, 763]
    SPManualValues = [1500, 3000, 6000]
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # Changes max quantity
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in SPManualIDs:
                row["ValueMax"] == 99
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes names of Contracts
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] >= 660:
                for i in range(0, len(SPManualIDs)):
                    if row["$id"] == SPManualNameIDs[i]:
                        row["name"] = f"{SPManualValues[i]} SP Receipt"
                    if row["$id"] == SPManualCaptionIDs[i]:
                        row["name"] = f"Proof that you purchased {SPManualValues[i]} SP\n for the driver skill trees."
            if row["$id"] >= 764:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def ReAddInns(): # Need to readd inns to Mor Ardain and Gormott to allow you to change the tide level
    with open("./_internal/JsonOutputs/common_gmk/ma05a_FLD_NpcPop.json", 'r+', encoding='utf-8') as file: # Gormott Inn
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 5487:
                row["EventID"] = 40318
                row["ShopID"] = 31
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_gmk/ma08a_FLD_NpcPop.json", 'r+', encoding='utf-8') as file: # Mor Ardain Inn
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 8284:
                row["EventID"] = 40660
                row["ShopID"] = 87
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def CustomShopSetup(): # Sets up the custom shops with loot
    
    # Shop Item Setup
    ReceiptTextChanges()
    WPAdjustments()
    ChipShopRewards()
    AuxCoreRewards()
    PouchItemRewards()
    AccessoryShopRewards()
    PoppiswapShopRewards()
    GambaShopRewards()
    AddSPManual()
    
    # Cost Distributions
    TokenExchangeRewards = []
    for i in range(0, 10):
        TokenExchangeRewards.append([random.randint(2 + 4*i, 4 + 5*i)])
    CoreCrystalCostDistribution = [4, 8, 12, 16, 4, 8, 12, 4, 8, 12, 20, 30, 40, 130, 145, 160]
    ManualCostDistribution = [3, 6, 9, 20, 35, 9, 17, 33]
    ChipShopCostDistribution = Helper.ExtendListtoLength([1],16,"inputlist[i-1]+9")
    
    CommonAuxCoreCosts = [3, 6, 9, 12, 3, 6, 9]
    RareAuxCoreCosts = [6, 12, 6, 12, 10]
    LegendaryAuxCoreCosts = [20, 20, 30, 30]
    AuxCoreShopCostDistribution = CommonAuxCoreCosts + RareAuxCoreCosts + LegendaryAuxCoreCosts

    PouchItemShopCostDistribution = [5,5,5,5,10,5,5,5,15,15,15,10,10,15,10,5]
    
    CommonAccessoryCosts = [4, 8, 12, 16, 4, 8, 12]
    RareAccessoryCosts = [15, 20, 15, 20, 25]
    LegendaryAccessoryCosts = [30, 30, 50, 50]
    AccessoryShopCostDistribution = CommonAccessoryCosts + RareAccessoryCosts + LegendaryAccessoryCosts

    PoppiswapShopCosts = [10, 20, 30, 40, 50, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44]
    GambaShopCosts = Helper.ExtendListtoLength([], 16, "15")

    # Filler Lists
    TokenFillerList = Helper.ExtendListtoLength([], 10, "0") # This gets used so much, I'd rather not screw up typing it out, also by initializing it here, it doesn't calculate the value every time in the dictionary
    EmptyFillerList = Helper.ExtendListtoLength([], 16, "0") # Empty list of full size
    FullFillerList = Helper.ExtendListtoLength([], 16, "1") # Full list of full size
    ManualFillerList = Helper.ExtendListtoLength([], 8, "0") # Empty list for manual shop
    
    # List of Shops
    # Sanity Checks: The number of items in InputTaskIDs should always be less than 16
    # The number of SetItem1IDs, RewardIDs, RewardNames, RewardSP, and RewardXP should all be the same, and also equal to the number of non-zero InputTaskIDs
    # Reward IDs, RewardQtys should have same number of values in each list as SetItem1IDs, however, each list should be made up of 4 lists, 1 for each item slot that a reward can be

    TokenExchangeShop = {
        "NPCModel": 2002, # from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Bana
        "NPCID": 2079, # ma02a_FLD_NpcPop $id
        "ShopIcon": 420, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 18, # MNU_ShopList $id
        "ShopNametoReplace": 9, # fld_shopname $id
        "ShopEventID": 40045, # ma02a_FLD_NpcPop EventID
        "Name": "[System:Color name=green]Bounty Token[/System:Color] Bartering", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(917, 926), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8.
        "AddTaskConditions": [1, 1], # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s,
        "SetItemIDs": [Helper.InclRange(25479, 25488), TokenFillerList, TokenFillerList, TokenFillerList, TokenFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [Helper.ExtendListtoLength([], 10, "1"), TokenFillerList, TokenFillerList, TokenFillerList, TokenFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1282, 1291), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": [Helper.ExtendListtoLength([], 10, "25489"), TokenFillerList, TokenFillerList, TokenFillerList], # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [TokenExchangeRewards, TokenFillerList, TokenFillerList, TokenFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["Doubloons + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP", "Doubloons + EXP + SP"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": [250, 375, 500, 625, 750, 875, 1000, 1250, 1500, 1750], #FLD_QuestReward Sp
        "RewardXP": [0, 630, 630, 630, 630, 630, 630, 630, 630, 630], # FLD_QuestReward EXP
        "HideReward": TokenFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    CoreCrystalShop = {
        "NPCModel": 2008,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Amalthus
        "NPCID": 2080, # ma02a_FLD_NpcPop $id
        "ShopIcon": 427, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 17, # MNU_ShopList $id
        "ShopNametoReplace": 8, # fld_shopname $id
        "ShopEventID": 40054, # ma02a_FLD_NpcPop EventID
        "Name": "Core Crystal Cache", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(927, 942), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [CoreCrystalCostDistribution, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1292, 1307), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": OutputCrystalGroupItemIDs, # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [FullFillerList, FullFillerList, FullFillerList, EmptyFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["ATK Blade Bundle 1", "ATK Blade Bundle 2", "ATK Blade Bundle 3", "ATK Blade Bundle 4", "TNK Blade Bundle 1", "TNK Blade Bundle 2", "TNK Blade Bundle 3", "HLR Blade Bundle 1", "HLR Blade Bundle 2", "HLR Blade Bundle 3", "DLC Core Crystal 1", "DLC Core Crystal 2", "DLC Core Crystal 3", "NG+ Core Crystal 1", "NG+ Core Crystal 2", "NG+ Core Crystal 3"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": EmptyFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    WPManualShop = {
        "NPCModel": 2001,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Gramps
        "NPCID": 2086, # ma02a_FLD_NpcPop $id
        "ShopIcon": 442, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 24, # MNU_ShopList $id
        "ShopNametoReplace": 16, # fld_shopname $id
        "ShopEventID": 40051, # ma02a_FLD_NpcPop EventID
        "Name": "Manual Marketplace", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(943, 950), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": [], # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 8, "25489"), ManualFillerList, ManualFillerList, ManualFillerList, ManualFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [ManualCostDistribution, ManualFillerList, ManualFillerList, ManualFillerList, ManualFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1308, 1315), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": [[25405, 25406, 25407, 25305, 25450, 25349, 25350, 25351], ManualFillerList, ManualFillerList, ManualFillerList], # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [Helper.ExtendListtoLength([], 8, "1"), ManualFillerList, ManualFillerList, ManualFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["250 Art WP", "500 Art WP", "1000 Art WP", "Pouch Expander", "Accessory Expander", "1500 Driver SP", "3000 Driver SP", "6000 Driver SP"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": ManualFillerList, #FLD_QuestReward Sp
        "RewardXP": ManualFillerList, # FLD_QuestReward EXP
        "HideReward": ManualFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    WeaponChipShop = {
        "NPCModel": 3457,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Padraig
        "NPCID": 2087, # ma02a_FLD_NpcPop $id
        "ShopIcon": 430, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 21, # MNU_ShopList $id
        "ShopNametoReplace": 13, # fld_shopname $id
        "ShopEventID": 40048, # ma02a_FLD_NpcPop EventID
        "Name": "Weapon Warehouse", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(951, 966), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [ChipShopCostDistribution, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1316, 1331), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": ChipShopRewardDistribution, # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [Helper.ExtendListtoLength([], 16, "4"), Helper.ExtendListtoLength([], 16, "4"), Helper.ExtendListtoLength([], 16, "4"), EmptyFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ChipBundleNames, # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": EmptyFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    AuxCoreShop = {
        "NPCModel": 3106,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Yumyum the Burglar
        "NPCID": 2088, # ma02a_FLD_NpcPop $id
        "ShopIcon": 432, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 26, # MNU_ShopList $id
        "ShopNametoReplace": 17, # fld_shopname $id
        "ShopEventID": 40052, # ma02a_FLD_NpcPop EventID
        "Name": "Aux Core Auction", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(967, 982), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [AuxCoreShopCostDistribution, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1332, 1347), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": AuxCoreShopRewardDistribution, # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [FullFillerList, FullFillerList, FullFillerList, FullFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["[System:Color name=blue]Common[/System:Color] Damage 1", "[System:Color name=blue]Common[/System:Color] Damage 2", "[System:Color name=blue]Common[/System:Color] Damage 3", "[System:Color name=blue]Common[/System:Color] Damage 4", "[System:Color name=blue]Common[/System:Color] Defense 1", "[System:Color name=blue]Common[/System:Color] Defense 2", "[System:Color name=blue]Common[/System:Color] Unique", "[System:Color name=red]Rare[/System:Color] Damage 1", "[System:Color name=red]Rare[/System:Color] Damage 2", "[System:Color name=red]Rare[/System:Color] Defense 1", "[System:Color name=red]Rare[/System:Color] Defense 2", "[System:Color name=red]Rare[/System:Color] Unique", "[System:Color name=tutorial]Legendary[/System:Color] Damage", "[System:Color name=tutorial]Legendary[/System:Color] Defense", "[System:Color name=tutorial]Legendary[/System:Color] Unique 1", "[System:Color name=tutorial]Legendary[/System:Color] Unique 2"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": FullFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    PouchItemShop = {
        "NPCModel": 2534,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Head Fire Dragon
        "NPCID": 2092, # ma02a_FLD_NpcPop $id
        "ShopIcon": 426, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 114, # MNU_ShopList $id
        "ShopNametoReplace": 113, # fld_shopname $id
        "ShopEventID": 40731, # ma02a_FLD_NpcPop EventID
        "Name": "Pouch Item Patisserie", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(983, 998), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [PouchItemShopCostDistribution, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1348, 1363), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": PouchItemShopRewardDistribution, # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [Helper.ExtendListtoLength([1,1,1,1], 16, "2"), Helper.ExtendListtoLength([1,1,1,1], 16, "2"), Helper.ExtendListtoLength([1,1,1,1], 16, "0"), Helper.ExtendListtoLength([1,1,1,1], 16, "0")], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["Mystery Set 1", "Mystery Set 2", "Mystery Set 3", "Mystery Set 4", "Staple Foods", "Vegetables", "Meat", "Seafood", "Desserts", "Drinks", "Instruments", "Art", "Literature", "Board Games", "Cosmetics", "Textiles"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": Helper.ExtendListtoLength([1,1,1,1], 16, "0") # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    DriverAccessoryShop = {
        "NPCModel": 2031,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Yew
        "NPCID": 2097, # ma02a_FLD_NpcPop $id
        "ShopIcon": 446, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 23, # MNU_ShopList $id
        "ShopNametoReplace": 15, # fld_shopname $id
        "ShopEventID": 40050, # ma02a_FLD_NpcPop EventID
        "Name": "Excess Accessories", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(999, 1014), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [AccessoryShopCostDistribution, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1364, 1379), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": AccessoryShopRewardDistribution, # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [FullFillerList, FullFillerList, FullFillerList, FullFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["[System:Color name=blue]Common[/System:Color] Damage 1", "[System:Color name=blue]Common[/System:Color] Damage 2", "[System:Color name=blue]Common[/System:Color] Damage 3", "[System:Color name=blue]Common[/System:Color] Damage 4", "[System:Color name=blue]Common[/System:Color] Defense 1", "[System:Color name=blue]Common[/System:Color] Defense 2", "[System:Color name=blue]Common[/System:Color] Unique", "[System:Color name=red]Rare[/System:Color] Damage 1", "[System:Color name=red]Rare[/System:Color] Damage 2", "[System:Color name=red]Rare[/System:Color] Defense 1", "[System:Color name=red]Rare[/System:Color] Defense 2", "[System:Color name=red]Rare[/System:Color] Unique", "[System:Color name=tutorial]Legendary[/System:Color] Damage", "[System:Color name=tutorial]Legendary[/System:Color] Defense", "[System:Color name=tutorial]Legendary[/System:Color] Unique 1", "[System:Color name=tutorial]Legendary[/System:Color] Unique 2"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": FullFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    PoppiswapShop = {
        "NPCModel": 3576,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Soosoo
        "NPCID": 2182, # ma02a_FLD_NpcPop $id
        "ShopIcon": 433, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 16, # MNU_ShopList $id
        "ShopNametoReplace": 7, # fld_shopname $id
        "ShopEventID": 40058, # ma02a_FLD_NpcPop EventID
        "Name": "The Poppishop", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(1015, 1030), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [PoppiswapShopCosts, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1380, 1395), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": [Helper.ExtendListtoLength(Helper.ExtendListtoLength([25218], 5, "inputlist[i-1]+1") + [25322], 16, "inputlist[i-1]+1"), EmptyFillerList, EmptyFillerList, EmptyFillerList], # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [FullFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": ["Poppiswap Manual 1", "Poppiswap Manual 2", "Poppiswap Manual 3", "Poppiswap Manual 4", "Poppiswap Manual 5", "Ether Crystal Pack 1", "Ether Crystal Pack 2", "Ether Crystal Pack 3", "Ether Crystal Pack 4", "Ether Crystal Pack 5", "Ether Crystal Pack 6", "Ether Crystal Pack 7", "Ether Crystal Pack 8", "Ether Crystal Pack 9", "Ether Crystal Pack 10", "Ether Crystal Pack 11"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": EmptyFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    GambaShop = {
        "NPCModel": 3324,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Generic Mercenary
        "NPCID": 2188, # ma02a_FLD_NpcPop $id
        "ShopIcon": 443, # MNU_ShopList ShopIcon
        "ShopIDtoReplace": 27, # MNU_ShopList $id
        "ShopNametoReplace": 18, # fld_shopname $id
        "ShopEventID": 40053, # ma02a_FLD_NpcPop EventID
        "Name": "The [System:Color name=tutorial]Casino[/System:Color]", # fld_shopname name
        "InputTaskIDs": Helper.InclRange(1031, 1046), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
        "AddTaskConditions": Helper.ExtendListtoLength([], 8, "1"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
        "SetItemIDs": [Helper.ExtendListtoLength([], 16, "25489"), EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
        "SetItemQtys": [GambaShopCosts, EmptyFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
        "RewardIDs": Helper.InclRange(1396, 1411), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
        "RewardItemIDs": [GambaShopRewardList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
        "RewardQtys": [FullFillerList, EmptyFillerList, EmptyFillerList, EmptyFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
        "RewardNames": Helper.ExtendListtoLength(["Reward Voucher"], 16, "inputlist[0] + ' ' + str(i + 1)"), # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
        "RewardSP": EmptyFillerList, #FLD_QuestReward Sp
        "RewardXP": EmptyFillerList, # FLD_QuestReward EXP
        "HideReward": FullFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
    }

    ShopList = [TokenExchangeShop, CoreCrystalShop, WPManualShop, WeaponChipShop, AuxCoreShop, PouchItemShop, DriverAccessoryShop, PoppiswapShop, GambaShop]
    ShopCreator(ShopList, True)

def ShopCreator(ShopList: list, DeleteArgentumShops: bool): # Makes the shops
    with open("./_internal/JsonOutputs/common/MNU_ShopChange.json", 'r+', encoding='utf-8') as file: # Adds the exchange tasks
        data = json.load(file)
        ShopChangeStartRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChange.json", "$id") + 1 # used in MNU_ShopList for "TableID"
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChange.json", "$id") + 1
        for shop in ShopList:
            ShopChangeRowToAdd = {"$id": CurrRow, "DefTaskSet1": 0, "DefTaskSet2": 0, "DefTaskSet3": 0, "DefTaskSet4": 0, "DefTaskSet5": 0, "DefTaskSet6": 0, "DefTaskSet7": 0, "DefTaskSet8": 0, "AddTaskSet1": 0, "AddCondition1": 0, "AddTaskSet2": 0, "AddCondition2": 0, "AddTaskSet3": 0, "AddCondition3": 0, "AddTaskSet4": 0, "AddCondition4": 0, "AddTaskSet5": 0, "AddCondition5": 0, "AddTaskSet6": 0, "AddCondition6": 0, "AddTaskSet7": 0, "AddCondition7": 0, "AddTaskSet8": 0, "AddCondition8": 0, "LinkQuestTask": 0, "LinkQuestTaskID": 0, "UnitText": 0}
            for i in range(0, len(shop["InputTaskIDs"])):
                if i <= 7:
                    ShopChangeRowToAdd[f"DefTaskSet{i+1}"] = shop["InputTaskIDs"][i]
                else: # once we get past all the regular tasks, we add new ones to addtaskset instead
                    ShopChangeRowToAdd[f"AddTaskSet{i-7}"] = shop["InputTaskIDs"][i]
                    ShopChangeRowToAdd[f"AddCondition{i-7}"] = shop["AddTaskConditions"][i-8]
            data["rows"].append(ShopChangeRowToAdd)
            CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_shopchange.json", 'r+', encoding='utf-8') as file: # Changes the reward name for the token shop
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopchange.json", "$id") + 1
        StartingShopChangeNameRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopchange.json", "$id") + 1 # Used in MNU_ShopChangeTask for "Name"
        for shop in ShopList:
            for reward in shop["RewardNames"]:
                data["rows"].append({"$id": CurrRow, "style": 36, "name": reward})
                CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_ShopChangeTask.json", 'r+', encoding='utf-8') as file: # Now we define what each task does
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChangeTask.json", "$id") + 1
        for shop in ShopList:
            for i in range(0, len(shop["SetItemIDs"][0])):
                data["rows"].append({"$id": CurrRow, "Name": StartingShopChangeNameRow, "SetItem1": shop["SetItemIDs"][0][i], "SetNumber1": shop["SetItemQtys"][0][i], "SetItem2": shop["SetItemIDs"][1][i], "SetNumber2": shop["SetItemQtys"][1][i], "SetItem3": shop["SetItemIDs"][2][i], "SetNumber3": shop["SetItemQtys"][2][i], "SetItem4": shop["SetItemIDs"][3][i], "SetNumber4": shop["SetItemQtys"][3][i], "SetItem5": shop["SetItemIDs"][4][i], "SetNumber5": shop["SetItemQtys"][4][i], "HideReward": shop["HideReward"][i], "Reward": shop["RewardIDs"][i], "HideRewardFlag": 0, "AddFlagValue": 0, "forcequit": 0, "IraCraftIndex": 0})
                CurrRow += 1
                StartingShopChangeNameRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_QuestReward.json", 'r+', encoding='utf-8') as file: # Sets the reward for each task
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_QuestReward.json", "$id") + 1
        for shop in ShopList:
            for i in range(0, len(shop["RewardIDs"])):
                data["rows"].append({"$id": CurrRow, "Gold": 0, "EXP": shop["RewardXP"][i], "Sp": shop["RewardSP"][i], "Coin": 0, "DevelopZone": 0, "DevelopPoint": 0, "TrustPoint": 0, "MercenariesPoint": 0, "IdeaCategory": 0, "IdeaValue": 0, "ItemID1": shop["RewardItemIDs"][0][i], "ItemNumber1": shop["RewardQtys"][0][i], "ItemID2": shop["RewardItemIDs"][1][i], "ItemNumber2": shop["RewardQtys"][1][i], "ItemID3": shop["RewardItemIDs"][2][i], "ItemNumber3": shop["RewardQtys"][2][i], "ItemID4": shop["RewardItemIDs"][3][i], "ItemNumber4": shop["RewardQtys"][3][i]})
                CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/fld_shopname.json", 'r+', encoding='utf-8') as file: # Adds new shop name to list 
        data = json.load(file)
        CurrRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopname.json", "$id") + 1
        ShopNameStartingRow = Helper.GetMaxValue("./_internal/JsonOutputs/common_ms/fld_shopname.json", "$id") + 1 # used in MNU_ShopList for "Name"
        for i in range(0, len(ShopList)):
            data["rows"].append({"$id": CurrRow, "style": 70, "name": ShopList[i]["Name"]})
            CurrRow += 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/MNU_ShopList.json", 'r+', encoding='utf-8') as file: # Changes existing shop to match what we want
        data = json.load(file)
        for i in range(0, len(ShopList)):
            for row in data["rows"]:
                if row["$id"] == ShopList[i]["ShopIDtoReplace"]:
                    row["Name"] = ShopNameStartingRow
                    row["ShopIcon"] = ShopList[i]["ShopIcon"]
                    row["TableID"] = ShopChangeStartRow
                    row["Discount1"] = row["Discount2"] = row["Discount3"] = row["Discount4"] = row["Discount5"] = 0
                    row["ShopType"] = 1
                    ShopChangeStartRow += 1
                    ShopNameStartingRow += 1
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    if DeleteArgentumShops:
        with open("./_internal/JsonOutputs/common_gmk/ma02a_FLD_NpcPop.json", 'r+', encoding='utf-8') as file: # Lets you rest in the Argentum Trade Guild Inn, but removes all other shops (we're adding them back after)
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] != 2096: # keeps only the inn as a shop in Argentum
                    row["ShopID"] = 0
                    row["flag"]["Talkable"] = 0
                    row["EventID"] = 0
                    row["QuestFlag"] = 0
            for i in range(0, len(ShopList)): # gives a specific npc the shop we want
                for row in data["rows"]:
                    if row["$id"] == ShopList[i]["NPCID"]:
                        row["ScenarioFlagMin"] = row["QuestFlag"] = row["QuestFlagMin"] = row["QuestFlagMax"] = row["TimeRange"] = row["Condition"] = row["Mot"] = row["QuestID"] = 0
                        row["ScenarioFlagMax"] = 10048
                        row["flag"]["Talkable"] = 1
                        row["EventID"] = ShopList[i]["ShopEventID"]
                        row["ShopID"] = ShopList[i]["ShopIDtoReplace"]
                        row["NpcID"] = ShopList[i]["NPCModel"]
                        break
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def SecretShopMaker(ChosenAreaOrder): # Adds some secret shops in the areas of interest
    CreateSecretShopReceipts()
    SecretShopRewardGeneration(ChosenAreaOrder)
    UsableShopEventIDs = [40338, 40441, 40339, 40442, 40340, 40443, 40444, 40445, 40446, 40450] # NpcPop EventID
    UsableShopIDs = Helper.InclRange(65, 73) + [81] # MNU_ShopList $id, NpcPop ShopID
    UsableShopNames = [66, 51, 72, 52, 68, 53, 54, 55, 56, 61] # MNU_ShopList Name
    SecretEmptyFillerList = Helper.ExtendListtoLength([], 5, "0")
    SecretFullFillerList = Helper.ExtendListtoLength([], 5, "1")
    InputTaskStartingID = Helper.GetMaxValue("./_internal/JsonOutputs/common/MNU_ShopChangeTask.json", "$id") + 1
    RewardTaskStartingID = Helper.GetMaxValue("./_internal/JsonOutputs/common/FLD_QuestReward.json", "$id") + 1
    Helper.ColumnAdjust("./_internal/JsonOutputs/common_gmk/ma07a_FLD_NpcPop.json", ["FSID1", "FSID2", "FSID3"], 0)
    ShopList = []
    for i in range(0, len(ChosenAreaOrder)):
        MapValidNPCIDs = [x for x in Helper.FindSubOptionValuesList("./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_NpcPop.json", "flag", "Talkable", 1, "$id") if x not in InvalidMapNPCs]
        ChosenSecretNPCID = random.choice(MapValidNPCIDs)
        with open("./_internal/JsonOutputs/common_gmk/" + ContinentInfo[ChosenAreaOrder[i]][2] + "_FLD_NpcPop.json", 'r+', encoding='utf-8') as file: # Lets you rest in the Argentum Trade Guild Inn, but removes all other shops (we're adding them back after)
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] == ChosenSecretNPCID:
                    OrigNPCID = row["NpcID"]
                    row["ScenarioFlagMin"] = row["QuestFlag"] = row["QuestFlagMin"] = row["QuestFlagMax"] = row["TimeRange"] = row["Condition"] = row["Mot"] = row["QuestID"] = row["FSID1"] = row["FSID2"] = row["FSID3"] = 0
                    row["ScenarioFlagMax"] = 10048
                    row["EventID"] = UsableShopEventIDs[i]
                    row["ShopID"] = UsableShopIDs[i]
                    row["NpcID"] = 2012 # Klaus
                    row["LookAt"] = 0
                    row["NpcTurn"] = 0
                else:
                    row["EventID"] = 0
                    row["ShopID"] = 0
                    row["QuestID"] = 0
            for row in data["rows"]: # Need to account for more lines where the original NPC speaks, they overlap bodies and it looks weird
                if row["NpcID"] == OrigNPCID:
                    row["NpcID"] = 3445
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
        RewardSPList = random.choices([0, 1000, 2000, 3000, 4000], weights = [49, 25, 15, 10, 1], k = 5)
        
        # defining the shop itself

        SecretShop = {
            "NPCModel": 3445,# from RSC_NpcList, goes to ma02a_FLD_NpcPop NpcID. Soosoo
            "NPCID": ChosenSecretNPCID, # ma02a_FLD_NpcPop $id
            "ShopIcon": 419, # MNU_ShopList ShopIcon
            "ShopIDtoReplace": UsableShopIDs[i], # MNU_ShopList $id
            "ShopNametoReplace": UsableShopNames[i], # fld_shopname $id
            "ShopEventID": UsableShopEventIDs[i], # ma02a_FLD_NpcPop EventID
            "Name": f"[System:Color name=tutorial]Super-Secret Shop {i+1}[/System:Color]", # fld_shopname name
            "InputTaskIDs": Helper.ExtendListtoLength([InputTaskStartingID], 5, "inputlist[i-1]+1"), # MNU_ShopChangeTask $id, feeds into MNU_ShopChange DefTaskSet1->8 and AddTaskSet1->8. Should always have length of 16
            "AddTaskConditions": Helper.ExtendListtoLength([], 8, "0"), # MNU_ShopChange AddCondition1->8 (0 if no task, 1 otherwise) # how many InputTaskIDs you have past 8 determines number of 1s, always 8 items long
            "SetItemIDs": [SecretEmptyFillerList, SecretEmptyFillerList, SecretEmptyFillerList, SecretEmptyFillerList, SecretEmptyFillerList], # MNU_ShopChangeTask SetItem1->5, 1 list for each SetItem1->SetItem5, and a number of items in each list equal to the number of InputTaskIDs
            "SetItemQtys": [SecretEmptyFillerList, SecretEmptyFillerList, SecretEmptyFillerList, SecretEmptyFillerList, SecretEmptyFillerList], # MNU_ShopChangeTask SetNumber1->5, 1 list for each 
            "RewardIDs": Helper.ExtendListtoLength([RewardTaskStartingID], 5, "inputlist[i-1]+1"), # FLD_QuestReward $id, feeds into MNU_ShopChangeTask Reward
            "RewardItemIDs": [Helper.ExtendListtoLength([SecretReceiptIDs[i]], 5, "inputlist[i-1]"), SecretShopRewardListItem1[i], SecretShopRewardListItem2[i], SecretEmptyFillerList], # FLD_QuestReward ItemID1->4, item ids from ITM files, same number as RewardQtys
            "RewardQtys": [SecretShopCostList[i], SecretShopRewardQuantities1[i], SecretShopRewardQuantities2[i], SecretEmptyFillerList], # FLD_QuestReward ItemNumber1->4, 1 list for each ItemNumber, and number of items in each list equal to the number of InputTaskIDs
            "RewardNames": ["Secret Trade 1", "Secret Trade 2", "Secret Trade 3", "Secret Trade 4", "Secret Trade 5"], # names for items with IDs in FLD_QuestReward, as many items as non-zero InputTaskIDs
            "RewardSP": RewardSPList, #FLD_QuestReward Sp
            "RewardXP": SecretEmptyFillerList, # FLD_QuestReward EXP
            "HideReward": SecretEmptyFillerList # Whether or not to hide the reward, MNU_ShopChangeTask "HideReward"
        }

        #print(SecretShop["NPCID"])

        ShopList.append(SecretShop)

        InputTaskStartingID += 5
        RewardTaskStartingID += 5

    ShopCreator(ShopList, False) # run the function on the whole list at once

def CreateSecretShopReceipts(): # Makes receipts for secret shops, limiting the amount of things a player can buy from a shop.
    global SecretReceiptIDs
    SecretReceiptIDs = Helper.ExtendListtoLength([25352], 10, "inputlist[i-1]+1")
    SecretReceiptNameIDs = Helper.ExtendListtoLength([663], 10, "inputlist[i-1]+1")
    SecretReceiptCaptionIDs = Helper.ExtendListtoLength([764], 10, "inputlist[i-1]+1")
    with open("./_internal/JsonOutputs/common/ITM_PreciousList.json", 'r+', encoding='utf-8') as file: # changes max quantity
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in SecretReceiptIDs:
                row["ValueMax"] = 5
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common_ms/itm_precious.json", 'r+', encoding='utf-8') as file: # Changes names of Contracts
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] >= 663:
                for i in range(0, len(SecretReceiptIDs)):
                    if row["$id"] == SecretReceiptNameIDs[i]:
                        row["name"] = f"Secret Shop Receipt {i+1}"
                    if row["$id"] == SecretReceiptCaptionIDs[i]:
                        row["name"] = f"Proof that you purchased \nan item set from the Secret Shop {i+1}."
            if row["$id"] >= 773:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

class UMHuntSecretShopEnhancements(Enhancement):
    def __init__(self, name, Enhancement, Caption, Param1 = [0,0,0,0], Param2 = [0,0,0,0], ReversePar1 = False, DisTag = ""):
        self.addToList = False 
        self.name = name
        self.EnhanceEffect = Enhancement
        self.Caption = Caption
        self.Param1 = Param1
        self.Param2 = Param2
        self.ReversePar1 = ReversePar1
        self.DisTag = DisTag

# Accessories
UMAllWeaponAttackUp = UMHuntSecretShopEnhancements("Master",120, 130, Medium)
UMSpecialRechargeCancelling = UMHuntSecretShopEnhancements("Special",92, 100, Large)
UMHigherLVEnemyDamageUp = UMHuntSecretShopEnhancements("Underdog",40,41, Mega)
UMVision = UMHuntSecretShopEnhancements("Monado",242, 298, Small, ReversePar1=True)
UMBreakResDown = UMHuntSecretShopEnhancements("Breaker",180, 192, Medium)
UMStrengthBoost = UMHuntSecretShopEnhancements("Strength", 2,2, Medium)
UMEtherBoost = UMHuntSecretShopEnhancements("Ether", 3,3, Medium)

# Aux Cores
UMFlatCritBoost = UMHuntSecretShopEnhancements("Critical",17,17, Medium)
UMSurpriseAttackUp = UMHuntSecretShopEnhancements("Surprise",36,37, [0, 0, 10000, 20000], DisTag="Surprise!")
UMSpecialRecievesAfterImage = UMHuntSecretShopEnhancements("Afterimage",213, 335, Mini, DisTag="Afterimage")
UMAutoSpeedArtsSpeed= UMHuntSecretShopEnhancements("Lightning",240, 296, High, High)
UMPhyAndEthDefenseUp = UMHuntSecretShopEnhancements("Full Guard",146, 156, [0, 0, 60, 100])
UMOnBlockNullDamage = UMHuntSecretShopEnhancements("Guardian",59, 59, Medium, DisTag="Null Damage")
UMFlatBlockBoost = UMHuntSecretShopEnhancements("Block",20,20, Medium)

def SecretShopRewardGeneration(ChosenAreaOrder): # Makes the reward sets for the secret shops
    global SecretShopRewardListItem1
    SecretShopRewardListItem1 = []
    global SecretShopRewardListItem2
    SecretShopRewardListItem2 = []
    global SecretShopRewardQuantities1
    SecretShopRewardQuantities1 = [] 
    global SecretShopRewardQuantities2
    SecretShopRewardQuantities2 = []
    global SecretShopCostList
    SecretShopCostList = []

    WeaponRankList = Helper.ExtendListtoLength([], 20, "[]")
    with open("./_internal/JsonOutputs/common/ITM_PcWpnChip.json", 'r+', encoding='utf-8') as file: # Assigns weapons to groups based on category
        data = json.load(file)
        for row in data["rows"]:
            WeaponRankList[row["Rank"] - 1].append(row["$id"])
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

    RewardTypes = {
        1: "WP Manual", 
        2: "Pouch Item Set",
        3: "Driver Accessory Set",
        4: "Bounty Tokens",
        5: "Weapon Chips",
        6: "Pouch/Accessory Expander",
        7: "Aux Cores"
    }

    # Now assign rewards
    for j in range(0, len(ChosenAreaOrder)):
        SetRewards1 = [0,0,0,0,0]
        SetRewards2 = [0,0,0,0,0]
        SetQuantities1 = [1,1,1,1,1]
        SetQuantities2 = [1,1,1,1,1]
        RewardTypeChoices = random.choices([1, 2, 3, 4, 5, 6, 7], weights = [20, 20, 15, 10, 15, 5, 15], k = 5) # Choose Type of Reward
        ShopCostReceiptList = [0,0,0,0,0]
        for i in range(0, 5): # For each reward,
            match RewardTypeChoices[i]:
                case 1: # WP Manual
                    RandomManuals = random.choices([25405, 25406, 25407], weights = [1, 2, 3], k = 2)
                    SetRewards1[i] = RandomManuals[0]
                    SetRewards2[i] = RandomManuals[1]
                    ShopCostReceiptList[i] = 1
                case 2: # Pouch Item Set
                    RandomPouchItems = random.choices(ValidPouchItems, k = 2)
                    SetRewards1[i] = RandomPouchItems[0]
                    SetRewards2[i] = RandomPouchItems[1]
                    ShopCostReceiptList[i] = 1
                case 3: # Driver Accessory Set
                    RandomAccessories = random.choices(Helper.InclRange(65, 71), k = 2)
                    SetRewards1[i] = RandomAccessories[0]
                    SetRewards2[i] = RandomAccessories[1]
                    ShopCostReceiptList[i] = 5
                case 4: # Bounty Tokens
                    RandomBountyToken = random.choice(Helper.InclRange(25479, 25481))
                    SetRewards1[i] = RandomBountyToken
                    SetRewards2[i] = 0
                    SetQuantities2[i] = 0
                    ShopCostReceiptList[i] = 3
                case 5: # Weapon Chips
                    RandomWeaponChips = random.choices(WeaponRankList[min((i+1)*2,19)], k = 2)
                    SetRewards1[i] = RandomWeaponChips[0]
                    SetRewards2[i] = RandomWeaponChips[1]
                    ShopCostReceiptList[i] = 2
                case 6: # Pouch/Accessory Expander
                    RandomPouchorAccessoryExpander = random.choices([25305, 25450], weights = [66, 34], k = 2)
                    SetRewards1[i] = RandomPouchorAccessoryExpander[0]
                    SetRewards2[i] = RandomPouchorAccessoryExpander[1]
                    ShopCostReceiptList[i] = 2
                case _: # Aux Cores
                    RandomAuxCores = random.choices(Helper.InclRange(17065, 17071), k = 2)
                    SetRewards1[i] = RandomAuxCores[0]
                    SetRewards2[i] = RandomAuxCores[1]
                    ShopCostReceiptList[i] = 4
        SecretShopCostList.append(ShopCostReceiptList)
        SecretShopRewardListItem1.append(SetRewards1)
        SecretShopRewardListItem2.append(SetRewards2)
        SecretShopRewardQuantities1.append(SetQuantities1)
        SecretShopRewardQuantities2.append(SetQuantities2)

def DebugItemsPlace(): #need to place some tokens to play around with them in the shops
    with open("./_internal/JsonOutputs/common_gmk/ma02a_FLD_TboxPop.json", 'r+', encoding='utf-8') as file: # Lets you rest in the Argentum Trade Guild Inn, but removes all other shops (we're adding them back after)
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 209:
                row["itm1ID"] = 25488
                row["itm1Num"] = 1
                row["itm2ID"] = 25487
                row["itm2Num"] = 1
                row["itm3ID"] = 25489
                row["itm3Num"] = 1
                row["itm4ID"] = 25485
                row["itm4Num"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def DebugEasyMode(): # if this is on, enemies will be lv 1, makes it easier to playtest
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: # Adjusted their levels
        data = json.load(file)
        for row in data["rows"]:
            row["Lv"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def DebugSpawnCountPrint(EnemySets, ChosenAreaOrder): # Prints how many times an enemy spawns, think it's causing a crash
    debugfilename = "D:/XC2 Rando Debug Logs/EnemyCounting.txt"
    debugfile = open(debugfilename, "w", encoding= "utf-8")
    for k in range(0, len(ChosenAreaOrder)):
        for i in range(0, len(IDs.ValidEnemyPopFileNames)):
            if ContinentInfo[ChosenAreaOrder[k]][2] in IDs.ValidEnemyPopFileNames[i]:
                enemypopfile = "./_internal/JsonOutputs/common_gmk/" + IDs.ValidEnemyPopFileNames[i]
                AreaUMCount = [0,0,0,0]
                with open(enemypopfile, 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data["rows"]:
                        for j in range(0, len(EnemySets[k])):
                            for l in range(1, 5):
                                if row[f"ene{l}ID"] == EnemySets[k][j]:
                                    AreaUMCount[j] += row[f"ene{l}num"]
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2, ensure_ascii=False)
                debugfile.write(f"{ChosenAreaOrder[k]}\n\n")
                for j in range(0, 4):
                    debugfile.write(f"ID:{EnemySets[k][j]} Count:{AreaUMCount[j]}\n")  
    debugfile.close()