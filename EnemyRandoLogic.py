import json
import random
import time
from IDs import *

#Notes: This: (Sets enemy levels to the enemy they replace) (Allows some fights to be losable) (Allows swapping between types of enemies only) (Sets always attack to shuffled bosses)

AllEnemyDefaultLevels = [1, 2, 4, 5, 6, 8, 6, 10, 11, 12, 13, 15, 22, 25, 24, 26, 20, 18, 19, 21, 22, 24, 23, 23, 24, 26, 29, 31, 27, 29, 31, 32, 33, 34, 32, 35, 40, 38, 38, 38, 39, 42, 43, 42, 46, 44, 52, 54, 56, 99, 52, 50, 60, 60, 57, 66, 68, 60, 60, 60, 60, 70, 13, 24, 26, 32, 33, 34, 60, 70, 5, 14, 22, 18, 19, 21, 12, 31, 29, 33, 35, 40, 41, 56, 56, 58, 25, 47, 2, 25, 26, 10, 12, 9, 91, 36, 41, 57, 57, 38, 54, 25, 26, 28, 30, 32, 25, 26, 49, 44, 41, 27, 29, 22, 28, 29, 31, 33, 30, 31, 32, 60, 61, 58, 60, 62, 63, 62, 63, 64, 36, 36, 34, 61, 42, 41, 69, 66, 67, 70, 50, 40, 40, 42, 42, 42, 44, 46, 51, 50, 25, 62, 63, 61, 65, 64, 62, 61, 33, 62, 68, 66, 59, 60, 61, 60, 59, 66, 25, 26, 27, 26, 28, 29, 27, 30, 25, 30, 32, 28, 30, 36, 27, 29, 26, 33, 32, 35, 30, 33, 26, 28, 35, 58, 60, 62, 66, 68, 70, 100, 62, 64, 60, 62, 80, 70, 60, 56, 60, 63, 58, 60, 63, 66, 50, 50, 53, 55, 56, 58, 60, 62, 60, 58, 64, 62, 64, 64, 110, 96, 104, 100, 90, 98, 94, 100, 96, 102, 104, 100, 101, 105, 104, 106, 103, 108, 99, 106, 108, 110, 113, 115, 90, 90, 90, 120, 110, 100, 140, 106, 102, 110, 99, 99, 102, 110, 115, 150, 95, 96, 95, 96, 200, 98, 110, 106, 120, 100, 102, 98, 100, 100, 99, 112, 130, 108, 104, 58, 56, 55, 62, 60, 61, 56, 62, 66, 68, 60, 46, 48, 44, 53, 55, 52, 51, 51, 58, 57, 54, 56, 55, 59, 58, 57, 56, 55, 60, 62, 60, 60, 60, 64, 60, 61, 62, 63, 61, 63, 62, 61, 64, 54, 53, 51, 55, 50, 56, 64, 62, 61, 58, 60, 60, 63, 59, 57, 61, 65, 64, 66, 63, 70, 99, 60, 60, 60, 65, 65, 66, 62]
# Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], ValidEnemies, "Lv")

BossDefaultEnem1Levels = [1, 2, 4, 5, 4, 6, 8, 10, 12, 13, 13, 15, 22, 26, 60, 20, 21, 22, 24, 23, 23, 24, 24, 29, 31, 32, 29, 31, 32, 32, 34, 33, 39, 42, 42, 43, 46, 35, 44, 52, 56, 54, 60, 60, 52, 50, 60, 60, 60, 57, 66, 68, 60, 60, 60, 60, 70, 70, 8, 10, 29, 29, 40, 38, 50, 50, 50, 50, 1, 1, 1, 2, 2, 3, 32, 32, 32, 32, 14, 20, 53]
BossDefaultEnem2Levels = [6, 8, 11, 13, 13, 22, 25, 18, 26, 26, 27, 29, 33, 34, 39, 42, 44, 44, 54, 56, 50, 57, 10, 38, 48, 1, 10, 16]
BossDefaultEnem3Levels = [24, 19, 42, 60, 11, 17]
BossDefaultEnem4Levels = [18]

BossDefaultStageSpecificEnem1IDs = [1001, 4001, 4002, 4003, 4004, 5001, 5500, 5501, 5502, 5503, 5504, 5505, 5506, 5507, 5549, 7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 11001, 11002, 13001, 13002, 13003, 15001, 16149, 17001, 17002, 17003, 17005, 17006, 18001, 18002, 18003, 18004, 18100, 20001, 20002, 20003, 21001, 21002, 21003, 21004, 21005, 21006, 40001, 40002, 40003, 40004, 40008, 40009, 40010, 40011, 40012, 40013, 40014, 40015, 40016, 40547, 40548, 40549, 40561, 40562, 40563, 40564, 41001, 41002, 42001, 10001, 10002, 10003, 10374, 10366]
BossDefaultEnem1IDs = [179, 180, 181, 182, 1319, 184, 185, 187, 190, 191, 192, 193, 195, 198, 256, 199, 203, 204, 206, 208, 210, 212, 267, 216, 217, 227, 220, 221, 222, 269, 225, 270, 235, 236, 237, 238, 241, 229, 242, 243, 245, 272, 260, 262, 248, 249, 250, 274, 258, 252, 253, 254, 256, 258, 260, 262, 265, 275, 1431, 1433, 1441, 1442, 1443, 1444, 1446, 1447, 1449, 1450, 1451, 1452, 1453, 1430, 1429, 1454, 1632, 1632, 1632, 1632, 1434, 1437, 1448, 231, 232, 233, 1342, 234]

BossDefaultStageSpecificEnem2IDs = [5500, 5501, 5502, 5503, 5504, 5506, 5507, 7001, 7007, 7008, 8002, 8004, 8008, 8009, 11001, 13001, 13002, 16149, 17002, 17003, 18002, 20001, 40002, 40009, 40010, 40548, 41001, 41002]
BossDefaultEnem2IDs = [186, 185, 189, 192, 266, 195, 196, 201, 214, 268, 219, 220, 223, 271, 235, 237, 240, 242, 244, 273, 249, 252, 1432, 1444, 1445, 1428, 1435, 1438]

BossDefaultStageSpecificEnem3IDs =  [5507, 7001, 13002, 20001, 41001, 41002]
BossDefaultEnem3IDs = [197, 202, 239, 251, 1436, 1439]

BossDefaultStageSpecificEnem4IDs = [41002]
BossDefaultEnem4IDs = [1440]

AllBossDefaultIDs = list(set(BossDefaultEnem1IDs + BossDefaultEnem2IDs + BossDefaultEnem3IDs + BossDefaultEnem4IDs))
AllBossDefaultIDs = list(set(AllBossDefaultIDs) & set(ValidEnemies))
AllBossDefaultIDs.sort()

AllBossDefaultLevels = [1, 2, 4, 5, 6, 8, 6, 10, 11, 12, 13, 15, 22, 25, 24, 26, 20, 18, 19, 21, 22, 24, 23, 23, 24, 26, 29, 31, 27, 29, 31, 32, 33, 34, 32, 35, 40, 38, 38, 38, 39, 42, 43, 42, 46, 44, 52, 54, 56, 52, 50, 60, 60, 57, 66, 68, 60, 60, 60, 60, 70, 13, 24, 26, 32, 33, 34, 60, 70, 4, 36, 2, 2, 8, 10, 10, 14, 10, 11, 20, 16, 17, 18, 29, 29, 40, 38, 48, 50, 50, 53, 50, 50, 3, 32]
# Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllBossDefaultIDs, "Lv")

QuestDefaultEnemyIDs = [1, 1, 179, 180, 181, 182, 184, 0, 0, 0, 0, 0, 190, 191, 266, 193, 0, 201, 202, 203, 204, 206, 208, 210, 0, 214, 0, 214, 216, 0, 227, 220, 221, 222, 269, 0, 225, 0, 225, 195, 196, 197, 0, 229, 1342, 231, 237, 237, 0, 239, 240, 241, 235, 236, 242, 243, 0, 245, 0, 245, 248, 249, 250, 274, 0, 253, 254, 256, 258, 0, 262, 264, 265, 264, 275, 604, 80, 80, 296, 298, 0, 303, 304, 305, 307, 0, 310, 311, 0, 318, 276, 276, 276, 320, 323, 324, 325, 326, 329, 330, 595, 0, 332, 276, 334, 0, 395, 0, 338, 0, 481, 481, 496, 496, 503, 497, 497, 503, 498, 498, 503, 508, 0, 0, 340, 341, 342, 347, 348, 348, 349, 350, 352, 354, 276, 797, 356, 948, 930, 359, 360, 364, 365, 367, 369, 371, 0, 0, 376, 377, 276, 276, 276, 383, 384, 385, 0, 389, 0, 393, 398, 0, 0, 0, 0, 276, 414, 415, 416, 418, 968, 419, 422, 423, 436, 437, 438, 443, 0, 448, 439, 440, 441, 442, 450, 451, 454, 455, 458, 459, 461, 462, 462, 461, 0, 461, 463, 0, 466, 0, 470, 472, 473, 475, 477, 0, 481, 481, 0, 479, 479, 479, 0, 0, 0, 0, 0, 496, 497, 498, 0, 0, 512, 0, 0, 0, 0, 0, 546, 547, 548, 0, 552, 553, 0, 559, 560, 560, 0, 0, 564, 564, 564, 565, 566, 567, 0, 0, 570, 571, 572, 573, 0, 576, 577, 0, 588, 0, 598, 0, 0, 0, 0, 0, 0, 0, 0, 613, 0, 0, 0, 1118, 1131, 932, 1146, 0, 957, 751, 1200, 1119, 752, 1116, 830, 1132, 767, 0, 0, 0, 1175, 827, 0, 1199, 1025, 779, 1224, 949, 1160, 0, 775, 0, 0, 0, 0, 1229, 0, 0, 0, 965, 0, 0, 0, 1121, 809, 0, 936, 0, 1155, 0, 1227, 0, 1146, 1174, 948, 1113, 930, 0, 755, 1020, 1219, 775, 938, 1156, 1229, 1146, 0, 1230, 1119, 0, 0, 0, 1175, 1224, 0, 1260, 1203, 1157, 1218, 1159, 1227, 946, 0, 1201, 932, 0, 1165, 1182, 1210, 1264, 1160, 1119, 1185, 1226, 1230, 0, 1261, 747, 1202, 0, 1159, 970, 1116, 967, 1117, 1234, 1134, 996, 0, 1181, 779, 842, 949, 1265, 1234, 1174, 748, 985, 0, 748, 1126, 810, 1256, 1131, 1134, 812, 1258, 1132, 893, 890, 815, 1155, 1157, 709, 1255, 1156, 1186, 713, 895, 957, 1187, 808, 896, 958, 1023, 711, 894, 1020, 1025, 705, 891, 1261, 706, 892, 1113, 0, 1023, 1201, 1186, 636, 0, 822, 0, 0, 822, 760, 1159, 840, 0, 1165, 0, 0, 975, 1264, 0, 944, 958, 0, 957, 1262, 975, 930, 778, 938, 1174, 0, 944, 0, 1158, 841, 1205, 1041, 1125, 1134, 1200, 0, 1218, 1260, 0, 1231, 1187, 0, 827, 1131, 1042, 755, 0, 0, 0, 1183, 0, 0, 1146, 0, 1174, 967, 1118, 1210, 1262, 0, 1160, 1261, 1119, 0, 0, 1173, 932, 0, 930, 1225, 1131, 778, 946, 1126, 748, 0, 0, 743, 1132, 1234, 0, 743, 1117, 1118, 1216, 1158, 748, 0, 1120, 1025, 1242, 0, 1165, 1159, 0, 1184, 1125, 1165, 1104, 649, 650, 669, 0, 739, 740, 741, 744, 746, 0, 765, 759, 753, 775, 767, 821, 824, 834, 0, 826, 827, 831, 830, 0, 713, 0, 0, 0, 1196, 0, 1116, 1199, 939, 1122, 1203, 946, 1126, 1229, 930, 1125, 1225, 936, 0, 1216, 948, 1119, 1219, 943, 1121, 1204, 938, 1145, 1158, 1146, 1159, 1147, 1160, 1148, 1165, 0, 0, 0, 0, 0, 0, 1152, 1173, 1153, 1174, 1154, 0, 0, 0, 1169, 0, 219, 234, 251, 0, 0, 456, 457, 319, 564, 564, 1343, 1343, 564, 0, 1388, 1393, 1391, 1389, 1395, 0, 1404, 0, 1412, 1417, 1422, 1418, 0, 1415, 1416, 1417, 0, 1431, 0, 0, 0, 1441, 1442, 1632, 1443, 1444, 0, 1447, 1448, 1405, 1406, 1457, 1458, 0, 0, 0, 0, 1468, 1468, 1482, 1469, 1465, 1674, 0, 0, 1681, 1197, 1109, 1188, 708, 899, 736, 814, 671, 775, 1046, 1122, 0, 663, 1223, 947, 1167, 828, 984, 1119, 1147, 1491, 0, 635, 1470, 1471, 1472, 1467, 1486, 1484, 1581, 1527, 1489, 1489, 1490, 1485, 1632, 1632, 1502, 1616, 1579, 1499, 1592, 1593, 1497, 1596, 1607, 1634, 1576, 1548, 1653, 1537, 1512, 1628, 1516, 1549, 1546, 1614, 1618, 1604, 1605, 1644, 1518, 1551, 1594, 1621, 1585, 1602, 1648, 1528, 1610, 1540, 1534, 1655, 1619, 1651, 1598, 1575, 1533, 1526, 1589, 1519, 0, 0, 1682, 1683, 792, 1196, 1042, 829, 752, 1207, 1047, 833, 744, 1216, 1049, 739, 1218, 832, 753, 1071, 848, 1225, 1043, 837, 1425, 1682, 1468, 661, 761, 964, 938, 1159, 1468]
QuestDefaultEnemyGroupIDs = [0, 0, 0, 0, 0, 0, 0, 75, 0, 76, 0, 77, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 79, 0, 89, 0, 0, 81, 0, 0, 0, 0, 0, 82, 0, 90, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 83, 0, 0, 0, 0, 0, 0, 0, 84, 0, 91, 0, 0, 0, 0, 0, 85, 0, 0, 0, 0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 103, 0, 0, 0, 0, 93, 0, 0, 88, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 94, 0, 0, 0, 13, 0, 14, 0, 71, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 61, 62, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 11, 0, 0, 15, 16, 17, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 101, 0, 0, 68, 0, 69, 0, 0, 0, 0, 0, 72, 0, 0, 73, 0, 0, 0, 1, 2, 98, 98, 3, 0, 0, 0, 4, 70, 0, 5, 6, 7, 66, 67, 0, 0, 0, 8, 0, 0, 74, 0, 0, 0, 99, 9, 0, 0, 0, 0, 0, 0, 106, 106, 0, 0, 0, 0, 0, 0, 0, 96, 0, 97, 0, 64, 65, 22, 22, 22, 22, 22, 22, 0, 0, 23, 110, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 42, 0, 0, 115, 0, 0, 0, 0, 0, 0, 122, 0, 44, 36, 39, 123, 0, 44, 36, 39, 0, 49, 43, 111, 0, 0, 38, 0, 44, 0, 39, 0, 110, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 26, 0, 0, 25, 45, 48, 0, 0, 34, 0, 0, 0, 0, 0, 0, 0, 108, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34, 0, 0, 0, 0, 119, 0, 119, 50, 0, 0, 0, 0, 115, 0, 119, 115, 0, 0, 27, 0, 0, 121, 0, 0, 0, 0, 0, 0, 0, 108, 0, 28, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 29, 0, 0, 24, 0, 0, 0, 0, 116, 120, 30, 0, 30, 33, 0, 109, 0, 0, 0, 0, 0, 104, 0, 0, 0, 37, 105, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 46, 50, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 46, 0, 0, 0, 120, 0, 0, 115, 0, 0, 0, 0, 0, 0, 0, 102, 0, 0, 0, 0, 0, 108, 0, 0, 0, 0, 0, 0, 0, 0, 107, 0, 0, 0, 0, 105, 0, 51, 53, 54, 0, 112, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 114, 118, 124, 119, 113, 120, 0, 0, 0, 0, 0, 115, 116, 117, 0, 63, 0, 0, 0, 0, 95, 0, 0, 0, 0, 0, 0, 0, 0, 125, 0, 0, 0, 0, 0, 127, 0, 128, 0, 0, 0, 0, 136, 0, 0, 0, 139, 0, 135, 130, 131, 0, 0, 0, 0, 0, 132, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 137, 138, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 119, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 140, 142, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

EnemyGroupDefaultID1s = [487, 487, 493, 500, 513, 517, 532, 549, 561, 385, 390, 393, 394, 396, 399, 403, 403, 407, 445, 487, 487, 606, 640, 639, 780, 739, 838, 641, 741, 1145, 828, 934, 677, 1118, 930, 1120, 1037, 1035, 1052, 1065, 1039, 1074, 1196, 1210, 1236, 1206, 1151, 1244, 1163, 1166, 1255, 953, 1131, 1155, 390, 393, 399, 403, 403, 407, 374, 372, 487, 600, 602, 536, 540, 464, 464, 506, 479, 479, 479, 557, 185, 187, 190, 199, 212, 198, 217, 223, 238, 244, 252, 260, 455, 823, 267, 270, 272, 296, 309, 345, 577, 579, 591, 491, 1344, 1151, 461, 673, 297, 1052, 1123, 569, 838, 750, 768, 1048, 1055, 934, 1151, 1149, 1161, 1162, 1163, 1166, 1168, 1172, 667, 1052, 1052, 1150, 1386, 1389, 1397, 1408, 1412, 1434, 1437, 1446, 0, 1406, 1432, 1419, 1675, 1678, 1430, 1686, 639, 1684]
EnemyGroupDefaultID2s = [488, 488, 495, 501, 515, 519, 533, 550, 562, 386, 391, 397, 390, 390, 400, 404, 406, 408, 446, 488, 488, 607, 642, 640, 781, 740, 839, 642, 742, 1146, 829, 935, 690, 1121, 948, 1123, 1038, 1036, 1053, 1066, 1040, 1075, 1197, 1211, 1237, 1207, 1152, 1245, 1164, 1167, 1256, 954, 1132, 1156, 391, 397, 400, 404, 406, 409, 375, 373, 488, 601, 603, 538, 542, 466, 466, 508, 481, 481, 481, 558, 186, 185, 189, 201, 214, 196, 219, 225, 239, 245, 251, 262, 456, 846, 268, 271, 273, 297, 308, 346, 578, 581, 593, 492, 1345, 1152, 462, 1347, 296, 1365, 1370, 567, 1354, 1351, 1353, 1358, 1359, 1368, 1371, 1372, 1373, 1374, 1375, 1376, 1380, 1381, 724, 1365, 1365, 1372, 1387, 1391, 1398, 1410, 1413, 1435, 1438, 1445, 0, 1407, 1433, 1420, 1676, 1679, 1429, 1687, 641, 1687]
EnemyGroupDefaultID3s = [0, 489, 0, 504, 0, 525, 534, 551, 563, 0, 392, 0, 0, 0, 401, 405, 0, 409, 447, 489, 489, 608, 644, 0, 782, 0, 1354, 697, 0, 1147, 0, 1368, 0, 1122, 949, 1128, 0, 0, 1054, 0, 0, 1076, 0, 1212, 1238, 0, 1153, 1246, 1375, 1376, 1258, 955, 1134, 1157, 392, 0, 401, 405, 0, 411, 0, 0, 489, 0, 0, 0, 544, 468, 468, 510, 0, 483, 483, 0, 0, 0, 0, 202, 0, 197, 0, 0, 240, 0, 0, 0, 457, 0, 0, 0, 0, 0, 0, 0, 0, 583, 0, 0, 0, 1153, 463, 0, 0, 0, 0, 0, 0, 0, 0, 1362, 0, 1369, 0, 0, 0, 0, 0, 1377, 0, 0, 725, 0, 0, 0, 0, 1393, 0, 0, 1414, 1436, 1439, 0, 0, 0, 0, 0, 1677, 1680, 1428, 1690, 0, 1688]
EnemyGroupDefaultID4s = [0, 490, 0, 0, 0, 0, 535, 0, 0, 0, 0, 0, 0, 0, 402, 0, 0, 410, 0, 0, 0, 609, 0, 0, 783, 0, 0, 0, 0, 1148, 0, 1369, 0, 1123, 0, 1370, 0, 0, 1055, 0, 0, 1077, 0, 1215, 1239, 0, 1154, 0, 0, 1377, 1260, 957, 1135, 0, 0, 0, 402, 0, 0, 408, 0, 0, 490, 0, 0, 0, 0, 0, 470, 0, 0, 0, 485, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1378, 0, 0, 1348, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1440, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1689]
EnemyGroupDefaultID5s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 411, 0, 0, 0, 610, 0, 0, 784, 0, 0, 0, 0, 0, 0, 0, 0, 1124, 0, 0, 0, 0, 1058, 0, 0, 1078, 0, 1219, 1240, 0, 1371, 0, 0, 1378, 1261, 958, 1137, 0, 0, 0, 0, 0, 0, 410, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1379, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID6s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 412, 0, 0, 0, 611, 0, 0, 785, 0, 0, 0, 0, 0, 0, 0, 0, 1370, 0, 0, 0, 0, 1059, 0, 0, 1093, 0, 1384, 1248, 0, 0, 0, 0, 1379, 1262, 0, 0, 0, 0, 0, 0, 0, 0, 412, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID7s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 786, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1359, 0, 0, 1094, 0, 318, 1249, 0, 0, 0, 0, 0, 1264, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID8s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 787, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1365, 0, 0, 1095, 0, 0, 1250, 0, 0, 0, 0, 0, 1265, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID9s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 788, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1096, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID10s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 789, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1097, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID11s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 790, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EnemyGroupDefaultID12s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 791, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

AllQuestandBossDefaultEnemyIDs = list(set(QuestDefaultEnemyIDs + EnemyGroupDefaultID1s + EnemyGroupDefaultID2s + EnemyGroupDefaultID3s + EnemyGroupDefaultID4s + EnemyGroupDefaultID5s + EnemyGroupDefaultID6s + EnemyGroupDefaultID7s + EnemyGroupDefaultID8s + EnemyGroupDefaultID9s + EnemyGroupDefaultID10s + EnemyGroupDefaultID11s + EnemyGroupDefaultID12s))
AllQuestandBossDefaultEnemyIDs = list(set(AllQuestandBossDefaultEnemyIDs) & set(ValidEnemies))

AllQuestDefaultEnemyIDs = list(set(AllQuestandBossDefaultEnemyIDs) - set(AllBossDefaultIDs))
AllQuestDefaultEnemyIDs.sort()

AllQuestEnemyDefaultLevels = [5, 14, 22, 18, 19, 21, 12, 33, 35, 40, 41, 56, 56, 58, 25, 47, 25, 26, 10, 12, 9, 91, 36, 41, 57, 38, 54, 25, 26, 28, 30, 32, 25, 26, 49, 44, 41, 27, 29, 22, 28, 29, 31, 33, 30, 31, 32, 60, 61, 58, 60, 62, 63, 62, 63, 64, 36, 34, 61, 42, 41, 69, 66, 67, 70, 50, 40, 40, 42, 42, 42, 44, 46, 51, 50, 53, 26, 26, 26, 30, 55, 52, 33, 34, 33, 38, 38, 38, 38, 40, 33, 33, 35, 35, 45, 46, 43, 53, 51, 48, 51, 45, 45, 46, 46, 47, 47, 48, 48, 50, 48, 51, 53, 52, 33, 33, 34, 35, 36, 39, 42, 42, 42, 44, 45, 44, 43, 56, 57, 50, 64, 43, 42, 45, 58, 55, 55, 57, 60, 61, 56, 58, 60, 43, 19, 19, 36, 36, 37, 42, 44, 44, 58, 58, 56, 61, 59, 9, 20, 40, 60, 80, 99, 39, 6, 15, 6, 2, 7, 3, 2, 11, 14, 33, 25, 5, 16, 13, 23, 39, 19, 35, 12, 8, 90, 25, 18, 20, 3, 3, 27, 17, 18, 20, 9, 18, 19, 18, 19, 19, 22, 23, 20, 21, 23, 20, 18, 35, 22, 20, 37, 20, 20, 21, 20, 19, 19, 18, 22, 75, 74, 76, 74, 75, 77, 78, 23, 35, 23, 65, 24, 23, 78, 41, 25, 27, 27, 25, 26, 27, 29, 81, 27, 26, 83, 83, 28, 80, 28, 33, 28, 29, 28, 24, 80, 30, 32, 31, 62, 33, 33, 33, 40, 44, 43, 45, 46, 45, 44, 43, 44, 44, 44, 46, 43, 45, 46, 47, 48, 50, 51, 34, 34, 39, 35, 39, 42, 34, 35, 42, 55, 58, 62, 38, 39, 39, 36, 38, 35, 39, 41, 38, 40, 41, 39, 39, 40, 80, 41, 40, 39, 40, 40, 38, 38, 42, 42, 42, 42, 42, 84, 84, 84, 84, 85, 42, 43, 60, 46, 48, 51, 49, 47, 49, 47, 47, 60, 49, 47, 50, 53, 54, 58, 100, 117, 52, 52, 52, 52, 52, 53, 53, 54, 55, 53, 56, 57, 58, 58, 57, 60, 55, 55, 55, 55, 58, 58, 58, 60, 55, 58, 60, 60, 58, 62, 60, 58, 64, 66, 65, 66, 66, 31, 32, 31, 31, 32, 33, 32, 42, 44, 32, 31, 32, 47, 44, 43, 38, 31, 32, 34, 32, 32, 44, 31, 31, 31, 43, 31, 33, 33, 33, 33, 33, 32, 43, 42, 44, 43, 42, 42, 38, 38, 39, 47, 49, 48, 48, 45, 58, 43, 42, 23, 41, 70, 35, 26, 38, 39, 40, 40, 43, 45, 45, 49, 53, 54, 54, 54, 54, 55, 65, 99, 100, 65, 42, 9, 7, 65, 68, 66, 62, 38, 43, 45, 70, 70, 70, 70, 60, 58, 63, 61, 60, 84, 78, 81, 92, 88, 84, 125, 62, 32, 35, 42, 46, 35, 40, 37, 39, 41, 20, 19, 24, 50, 10, 16, 43, 40, 14, 12, 15, 41, 32, 15, 26, 34, 14, 34, 12, 32, 37, 38, 33, 9, 40, 20, 18, 40, 40, 23, 43, 38, 32, 36, 6, 38, 23, 5, 28, 21, 32, 23, 30, 42, 3, 38, 19, 38, 40, 39, 25, 28, 38, 62, 63, 61, 65, 64, 62, 61, 33, 62, 68, 66, 59, 60, 61, 60, 59]
# Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllQuestDefaultEnemyIDs, "Lv")

AllSuperbossDefaultIDs = [714, 928, 1018, 1022, 1027, 1110, 1189, 1560, 1723, 1756, 1758, 1759, 1763, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1775, 1776, 1777, 1778, 1779, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1792, 1793, 1794, 1795, 1800, 1802, 1803, 1804, 1805, 1806, 1808, 1809, 1811, 1812, 1813, 1814]
#Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["Lv"], Helper.inclRange(100,200), "$id")
#AllSuperbossDefaultIDs = list(set(AllSuperbossDefaultIDs) & set(ValidEnemies))
#AllSuperbossDefaultIDs = list(set(AllSuperbossDefaultIDs).difference(set(AllQuestDefaultEnemyIDs),set(AllBossDefaultIDs)))
#AllSuperbossDefaultIDs.sort()
#print(AllSuperbossDefaultIDs)

AllSuperbossDefaultLevels = [104, 120, 130, 130, 109, 110, 114, 100, 100, 110, 104, 100, 100, 102, 104, 100, 101, 105, 104, 106, 103, 108, 106, 108, 110, 113, 115, 120, 110, 100, 140, 106, 102, 110, 102, 110, 115, 150, 200, 110, 106, 120, 100, 102, 100, 100, 112, 130, 108, 104]
#Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllSuperbossDefaultIDs, "Lv")

AllUniqueMonsterDefaultIDs = [707, 710, 712, 715, 738, 811, 816, 817, 819, 898, 926, 929, 1019, 1026, 1101, 1102, 1106, 1108, 1111, 1112, 1114, 1115, 1321, 1322, 1324, 1326, 1559, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1670]
#Helper.FindSubOptionValuesList("./_internal/JsonOutputs/common/CHR_EnArrange.json", "Flag", "Named", 1, "$id") 
#AllUniqueMonsterDefaultIDs = list(set(AllUniqueMonsterDefaultIDs) & set(ValidEnemies))
#AllUniqueMonsterDefaultIDs = list(set(AllUniqueMonsterDefaultIDs).difference(set(AllQuestDefaultEnemyIDs), set(AllBossDefaultIDs), set(AllSuperbossDefaultIDs)))
#AllUniqueMonsterDefaultIDs.sort()
#print(AllUniqueMonsterDefaultIDs)

AllUniqueMonsterDefaultLevels = [81, 45, 75, 28, 14, 80, 48, 99, 26, 86, 99, 99, 95, 94, 41, 42, 46, 44, 51, 42, 54, 46, 8, 10, 9, 12, 75, 85, 65, 50, 45, 10, 25, 18, 34, 48, 44, 50, 40, 38, 33, 23, 48, 36, 55, 25]
#Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllUniqueMonsterDefaultIDs, "Lv")

AllNormalEnemyDefaultIDs = list(set(ValidEnemies) - set(AllBossDefaultIDs) - set(AllQuestDefaultEnemyIDs) - set(AllUniqueMonsterDefaultIDs) - set(AllSuperbossDefaultIDs))
AllNormalEnemyDefaultIDs.sort()

AllNormalEnemyDefaultLevels = [99, 31, 29, 2, 57, 36, 46, 54, 48, 49, 47, 58, 99, 3, 2, 2, 2, 3, 5, 69, 6, 8, 6, 3, 8, 9, 10, 5, 7, 8, 42, 22, 4, 90, 74, 34, 5, 71, 73, 12, 13, 24, 4, 5, 39, 72, 10, 13, 15, 40, 14, 39, 14, 38, 11, 22, 5, 38, 40, 37, 70, 21, 24, 12, 15, 16, 4, 4, 4, 6, 16, 34, 36, 40, 3, 3, 22, 7, 7, 13, 9, 9, 9, 11, 17, 74, 17, 24, 32, 61, 63, 21, 47, 17, 20, 20, 39, 21, 18, 18, 72, 34, 21, 62, 38, 75, 95, 97, 96, 23, 22, 19, 27, 28, 32, 29, 28, 85, 32, 31, 33, 31, 31, 32, 33, 34, 35, 34, 28, 29, 26, 29, 31, 61, 60, 61, 62, 63, 60, 33, 33, 33, 33, 43, 43, 59, 60, 25, 25, 26, 25, 26, 30, 31, 30, 24, 25, 26, 28, 32, 34, 36, 29, 28, 29, 28, 28, 29, 29, 27, 27, 27, 32, 33, 96, 97, 98, 44, 45, 43, 44, 45, 45, 45, 45, 46, 45, 49, 50, 51, 54, 56, 35, 38, 40, 41, 88, 44, 39, 90, 48, 93, 50, 49, 40, 43, 46, 46, 45, 35, 49, 44, 45, 47, 60, 45, 50, 50, 51, 50, 50, 50, 53, 49, 52, 51, 44, 51, 41, 44, 49, 50, 49, 56, 32, 33, 42, 43, 46, 48, 51, 39, 42, 38, 38, 80, 78, 40, 79, 40, 84, 86, 79, 82, 84, 87, 81, 88, 40, 43, 39, 41, 41, 40, 41, 41, 42, 41, 53, 53, 54, 53, 83, 39, 39, 47, 44, 45, 46, 47, 48, 50, 52, 55, 55, 97, 97, 58, 52, 55, 56, 57, 59, 61, 44, 43, 42, 43, 42, 32, 43, 43, 43, 42, 43, 44, 34, 34, 43, 43, 43, 34, 32, 32, 32, 32, 38, 40, 42, 44, 2, 4, 2, 23, 24, 67, 65, 69, 36, 36, 38, 30, 40, 5, 6, 43, 40, 60, 59, 29, 39, 43, 39, 39, 40, 48, 80, 41, 42, 43, 40, 40, 54, 58, 60, 95, 96, 96, 31, 30, 38, 39, 39, 35, 37, 36, 38, 9, 10, 52, 52, 54, 41, 18, 37, 39, 38, 12, 16, 10, 8, 11, 6, 35, 33, 11, 36, 12, 11, 15, 36, 12, 30, 13, 38, 37, 38, 38, 36, 35, 36, 39, 60, 99, 4, 3, 32, 21, 18, 26, 4, 6, 4, 32, 43, 30, 3, 9, 19, 13, 5, 3, 39, 43, 45, 44, 20, 4, 33, 48, 40, 20, 10, 36, 25, 51, 21, 20, 19, 21, 43, 20, 32, 33, 20, 11, 23, 2, 4, 21, 30, 22, 27, 39, 39, 39, 21, 28, 30, 66, 25, 26, 27, 26, 28, 29, 27, 30, 25, 30, 32, 28, 30, 36, 27, 29, 26, 33, 32, 35, 30, 33, 26, 28, 35, 58, 60, 62, 66, 68, 70, 62, 64, 60, 62, 80, 70, 60, 56, 60, 63, 58, 60, 63, 66, 50, 50, 53, 55, 56, 58, 60, 62, 60, 58, 64, 62, 64, 64, 96, 90, 98, 94, 96, 99, 90, 90, 90, 99, 99, 95, 96, 95, 96, 98, 98, 99, 58, 56, 55, 62, 60, 61, 56, 62, 66, 68, 60, 46, 48, 44, 53, 55, 52, 51, 51, 58, 57, 54, 56, 55, 59, 58, 57, 56, 55, 60, 62, 60, 60, 60, 64, 60, 61, 62, 63, 61, 63, 62, 61, 64, 54, 53, 51, 55, 50, 56, 64, 62, 61, 58, 60, 60, 63, 59, 57, 61, 65, 64, 66, 63, 70, 99, 60, 60, 60, 65, 65, 66, 62]
# Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllNormalEnemyDefaultIDs, "Lv")

def FindMatchingInfo(file1path, file2path, keyword0, keyword1, keyword2, keyword3): # file 1 path, file 2 path, file 1 header to search through, file 1 header to return data from, file 2 header to search through (same values as keyword1, maybe different header name), file 2 header to return data from
    namemat = []
    IDMat = [] 
    LevelMat = []
    mapspecID = []
    if file1path == "":
        mapname = ""
        i = 1
        j = 1
        for i in range(1,90):
            if i >= 10:
                mapnum = str(i)
            if i < 10:
                mapnum = "0" + str(i)
            for j in range(1,3):
                if j == 1:
                    mapname = "a"
                if j == 2:
                    mapname = "b"
                if j == 3:
                    mapname = "c"
                combinedmapname = "./_internal/JsonOutputs/common_gmk/ma" + mapnum + mapname + "_FLD_EnemyPop.json"
                file1path = combinedmapname
                try:
                    with open(combinedmapname, 'r+', encoding='utf-8') as file:
                        data = json.load(file)
                        for row in data['rows']:
                            if "boss" in row.get(keyword0):
                                if row.get(keyword1) != 0 and row.get(keyword1) != "":
                                    namemat.append(row[keyword1])
                                    mapspecID.append(row["$id"]) 
                except:
                    pass
    else:
        with open(file1path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data['rows']:
                if "boss" in row.get(keyword0):
                    if row.get(keyword1) != 0 and row.get(keyword1) != "":
                        namemat.append(row[keyword1])
                        mapspecID.append(row["$id"])   
    if file2path == "":
        chrenname = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
        file2path = chrenname
    with open(chrenname, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for k in range(0, len(namemat)):
            idsearch = namemat[k]
            for row in data["rows"]:
                for key, value in row.items():
                    if key in keyword2 and value == idsearch: 
                            IDMat.append(row[keyword2])
                            LevelMat.append(row[keyword3])
    print(namemat)
    print(mapspecID)                    
    print(IDMat)
    print(LevelMat)

def ReadPostRandomizationChanges(filepath, keyword1): # file to read after randomization, keyword1 column header
    retIDmatrix = []
    retkey1matrix = []
    with open(filepath, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            for key in row.items():
                if key == keyword1:
                    retIDmatrix.append(row["$id"])
                    retkey1matrix.append(row[keyword1])
    return retIDmatrix, retkey1matrix

def ReworkedEnemyRando (DefaultEnemyIDs, RandomizedEnemyIDs):
    for i in range(1,51):
        if i >= 10:
            mapnum = str(i)
        if i < 10:
            mapnum = "0" + str(i)
        for j in range(1,3):
            if j == 1:
                mapname = "a"
            if j == 2:
                mapname = "b"
            if j == 3:
                mapname = "c"
            enemypopfile = "./_internal/JsonOutputs/common_gmk/ma" + mapnum + mapname + "_FLD_EnemyPop.json"
            try:
                with open(enemypopfile, 'r+', encoding='utf-8') as file:
                    data = json.load(file)
                    for row in data['rows']: #for each row in the Enemy Pop file
                        if row["ene1ID"] == 0:
                            continue
                        ene1changed = 0
                        ene2changed = 0
                        ene3changed = 0
                        ene4changed = 0
                        for key, value in row.items():
                            if row["ene2ID"] == 0:
                                ene2changed = 1
                            if row["ene3ID"] == 0:
                                ene3changed = 1
                            if row["ene4ID"] == 0:
                                ene4changed = 1
                            if ene1changed + ene2changed + ene3changed + ene4changed == 4:
                                break
                            if key not in ("ene1ID", "ene2ID", "ene3ID", "ene4ID"):
                                continue
                            for k in range(0, len(DefaultEnemyIDs)):
                                if ene1changed == 0:
                                    if row["ene1ID"] == DefaultEnemyIDs[k]: 
                                        row["ene1ID"] = RandomizedEnemyIDs[k]
                                        ene1changed = 1
                                if ene2changed == 0:
                                    if row["ene2ID"] == DefaultEnemyIDs[k]: 
                                        row["ene2ID"] = RandomizedEnemyIDs[k]
                                        ene2changed = 1
                                if ene3changed == 0:
                                    if row["ene3ID"] == DefaultEnemyIDs[k]: 
                                        row["ene3ID"] = RandomizedEnemyIDs[k]
                                        ene3changed = 1      
                                if ene4changed == 0:
                                    if row["ene4ID"] == DefaultEnemyIDs[k]: 
                                        row["ene4ID"] = RandomizedEnemyIDs[k]
                                        ene4changed = 1
                                if ene1changed + ene2changed + ene3changed + ene4changed == 4:
                                    break
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=2)
            except:
                pass     
    with open("./_internal/JsonOutputs/common/FLD_QuestBattle.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            enechanged = 0
            if row["EnemyID"] != 0:
                for k in range(0, len(DefaultEnemyIDs)):
                    if enechanged == 1:
                        break
                    if enechanged == 0:
                        if row["EnemyID"] == DefaultEnemyIDs[k]:
                            row["EnemyID"] = RandomizedEnemyIDs[k]
                            enechanged = 1                 
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)
    with open("./_internal/JsonOutputs/common/FLD_EnemyGroup.json", 'r+', encoding='utf-8') as file:
        start_time = time.time()
        data = json.load(file)
        for row in data["rows"]:
            for l in range (1,13):
                keymatchval = str("EnemyID" + str(l))
                matching = 0
                if row[keymatchval] == 0:
                    break
                for k in range(0, len(DefaultEnemyIDs)):
                    if matching == 1:
                        break
                    if row[keymatchval] == DefaultEnemyIDs[k]:
                        row[keymatchval] = RandomizedEnemyIDs[k]
                        matching = 1                  
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)
    with open("./_internal/JsonOutputs/common/FLD_SalvageEnemySet.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data['rows']: #for each row in the Enemy Pop file
            if row["ene1ID"] == 0:
                continue
            ene1changed = 0
            ene2changed = 0
            ene3changed = 0
            ene4changed = 0
            for key, value in row.items():
                if row["ene2ID"] == 0:
                    ene2changed = 1
                if row["ene3ID"] == 0:
                    ene3changed = 1
                if row["ene4ID"] == 0:
                    ene4changed = 1
                if ene1changed + ene2changed + ene3changed + ene4changed == 4:
                    break
                if key not in ("ene1ID", "ene2ID", "ene3ID", "ene4ID"):
                    continue
                for k in range(0, len(DefaultEnemyIDs)):
                    if ene1changed == 0:
                        if row["ene1ID"] == DefaultEnemyIDs[k]: 
                            row["ene1ID"] = RandomizedEnemyIDs[k]
                            ene1changed = 1
                    if ene2changed == 0:
                        if row["ene2ID"] == DefaultEnemyIDs[k]: 
                            row["ene2ID"] = RandomizedEnemyIDs[k]
                            ene2changed = 1
                    if ene3changed == 0:
                        if row["ene3ID"] == DefaultEnemyIDs[k]: 
                            row["ene3ID"] = RandomizedEnemyIDs[k]
                            ene3changed = 1      
                    if ene4changed == 0:
                        if row["ene4ID"] == DefaultEnemyIDs[k]: 
                            row["ene4ID"] = RandomizedEnemyIDs[k]
                            ene4changed = 1
                    if ene1changed + ene2changed + ene3changed + ene4changed == 4:
                        break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

def ColumnAdjust(filename, clearedCols, desiredValue):
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for k in range(0, len(clearedCols)):
            for row in data["rows"]:
                for key, value in row.items():
                    if key != clearedCols[k]:
                        continue
                    row[clearedCols[k]] = desiredValue
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

def SubColumnAdjust(filename, colName, adjustedSubColName, desiredValue): #when your column you want to adjust is nested inside a dict
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            row[colName][adjustedSubColName] = desiredValue
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

def ReducePCHPBattle1():
    filename = "./_internal/JsonOutputs/common/FLD_QuestBattle.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 3: #battle on gramps at start of game
                row["ReducePCHP"] = 1
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

def BossQuestAggroAdjustments(DefaultIDs, RandomizedIDs):
    filename = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(DefaultIDs)): # for each row in the default ID matrix
            if DefaultIDs[i] in AllQuestandBossDefaultEnemyIDs: # if the default ID is in the list of default boss/quest IDs
                for row in data["rows"]: # for each row in CHR_EnArrange
                    if row["$id"] == RandomizedIDs[i]: # If the row's ID corresponds to the randomized ID with index i
                        row["Flag"]["AlwaysAttack"] = 1
                        row["Detects"] = 3
                        row["SearchRange"] = 300
                        row["SearchAngle"] = 360
                        row["SearchRadius"] = 200
                        break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)

def LevelReversion(FullDefaultIDs, FullRandomizedIDs, SpecificDefaultIDs, SpecificDefaultLevels): #specificdefaultids is boss or quest at the moment (not randomized)
    filename = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(FullDefaultIDs)): # for each row in the default ID matrix
            changed = 0
            if FullDefaultIDs[i] in SpecificDefaultIDs: # if the default ID is in the list of default specific IDs
                for j in range(0, len(SpecificDefaultIDs)): # for each row in the default specific IDs
                    if changed == 1:
                        break
                    if FullDefaultIDs[i] == SpecificDefaultIDs[j]: # if the jth element of the default specific ID list is equal to the ith element of the full default ID list
                        for row in data["rows"]:
                            if row["$id"] == FullRandomizedIDs[i]:
                                row["Lv"] = SpecificDefaultLevels[j]
                                changed = 1
                                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2)                        
                     
def EnemyLogic(CheckboxList, CheckboxStates):
    print("Randomizing Enemies")
    EnemyRandoOn = False
    EnemiestoPass = []
    LevelstoPass = []
    for j in range(0, len(CheckboxList)):
        if CheckboxList[j] == "Story Bosses Box":
            StoryBossesBox = j
            continue
        if CheckboxList[j] == "Keep Story Boss Levels Box":
            KeepStoryBossesLevelsBox = j
            continue
        if CheckboxList[j] == "Quest Enemies Box":
            QuestEnemyBox = j
            continue
        if CheckboxList[j] == "Keep Quest Enemy Levels Box":
            KeepQuestEnemyLevelsBox = j
            continue
        if CheckboxList[j] == "Unique Monsters Box":
            UniqueMonstersBox = j
            continue
        if CheckboxList[j] == "Superbosses Box":
            SuperbossesBox = j
            continue
        if CheckboxList[j] == "Normal Enemies Box":
            NormalEnemiesBox = j
            continue
        if CheckboxList[j] == "Keep All Enemy Levels Box":
            KeepAllEnemyLevelsBox = j
            continue           
    for k in range(0, len(CheckboxList)):
        if CheckboxList[k] == "Story Bosses Box":
            if (CheckboxStates[k].get() == True) or (CheckboxStates[k+1].get() == True) or (CheckboxStates[k+2].get() == True) or (CheckboxStates[k+3].get() == True) or (CheckboxStates[k+4].get() == True):
                EnemyRandoOn = True
                break
    if EnemyRandoOn == True:
        for n in range(0, len(CheckboxList)):
            if CheckboxList[n] == "Mix Enemies Between Types Box" and CheckboxStates[n].get() == True:
                if CheckboxStates[StoryBossesBox].get() == True:
                    EnemiestoPass += AllBossDefaultIDs
                    LevelstoPass += AllBossDefaultLevels
                if CheckboxStates[QuestEnemyBox].get() == True:
                    EnemiestoPass += AllQuestDefaultEnemyIDs
                    LevelstoPass += AllQuestEnemyDefaultLevels
                if CheckboxStates[UniqueMonstersBox].get() == True:
                    EnemiestoPass += AllUniqueMonsterDefaultIDs
                    LevelstoPass += AllUniqueMonsterDefaultLevels
                if CheckboxStates[SuperbossesBox].get() == True:
                    EnemiestoPass += AllSuperbossDefaultIDs
                    LevelstoPass += AllSuperbossDefaultLevels             
                if CheckboxStates[NormalEnemiesBox].get() == True:
                    EnemiestoPass += AllNormalEnemyDefaultIDs
                    LevelstoPass += AllNormalEnemyDefaultLevels              
                DefaultEnemyIDs = EnemiestoPass.copy()
                RandomizedEnemyIDs = DefaultEnemyIDs.copy()
                random.shuffle(RandomizedEnemyIDs)
                ReworkedEnemyRando(DefaultEnemyIDs, RandomizedEnemyIDs)
                if EnemiestoPass:
                    if CheckboxStates[KeepAllEnemyLevelsBox].get() == True:
                        LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, DefaultEnemyIDs, LevelstoPass)
                        break
                    if CheckboxStates[QuestEnemyBox].get() == True:
                        if CheckboxStates[KeepQuestEnemyLevelsBox].get() == True:
                            LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, AllQuestDefaultEnemyIDs, AllQuestEnemyDefaultLevels)
                    if CheckboxStates[StoryBossesBox].get() == True:
                        if CheckboxStates[KeepStoryBossesLevelsBox].get() == True:
                            LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, AllBossDefaultIDs, AllBossDefaultLevels)
            if CheckboxList[n] == "Mix Enemies Between Types Box" and CheckboxStates[n].get() == False:
                for o in range(0, len(CheckboxList)):
                    EnemiestoPass = []
                    LevelstoPass = []
                    if CheckboxList[o] == "Story Bosses Box" and CheckboxStates[o].get() == True:
                        EnemiestoPass = AllBossDefaultIDs
                        LevelstoPass = AllBossDefaultLevels
                    if CheckboxList[o] == "Quest Enemies Box" and CheckboxStates[o].get() == True:
                        EnemiestoPass = AllQuestDefaultEnemyIDs
                        LevelstoPass = AllQuestEnemyDefaultLevels                      
                    if CheckboxList[o] == "Unique Monsters Box" and CheckboxStates[o].get() == True:
                        EnemiestoPass = AllUniqueMonsterDefaultIDs
                        LevelstoPass = AllUniqueMonsterDefaultLevels
                    if CheckboxList[o] == "Superbosses Box" and CheckboxStates[o].get() == True:
                        EnemiestoPass = AllSuperbossDefaultIDs
                        LevelstoPass = AllSuperbossDefaultLevels
                    if CheckboxList[o] == "Normal Enemies Box" and CheckboxStates[o].get() == True:
                        EnemiestoPass = AllNormalEnemyDefaultIDs
                        LevelstoPass = AllNormalEnemyDefaultLevels
                    if EnemiestoPass: #if the list of enemies to pass is not empty
                        DefaultEnemyIDs = EnemiestoPass.copy()
                        RandomizedEnemyIDs = DefaultEnemyIDs.copy()
                        random.shuffle(RandomizedEnemyIDs)
                        ReworkedEnemyRando(DefaultEnemyIDs, RandomizedEnemyIDs)
                        if CheckboxStates[KeepAllEnemyLevelsBox].get() == True:
                            LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, DefaultEnemyIDs, LevelstoPass)
                        if CheckboxList[o] == "Quest Enemies Box" and CheckboxStates[o].get() == True:
                            if CheckboxStates[KeepQuestEnemyLevelsBox].get() == True:
                                LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, AllQuestDefaultEnemyIDs, AllQuestEnemyDefaultLevels)
                        if CheckboxList[o] == "Story Bosses Box" and CheckboxStates[o].get() == True:
                            if CheckboxStates[KeepStoryBossesLevelsBox].get() == True: # need to change this to check specific index instead of using == to value of checkboxlist, probably in initial loop find index corresponding to this box then use this
                                LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, AllBossDefaultIDs, AllBossDefaultLevels)
        SubColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", "Flag", "AlwaysAttack", 0)
        ColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["SearchRange", "SearchRadius", "SearchAngle", "Detects"], 0)
        BossQuestAggroAdjustments(DefaultEnemyIDs, RandomizedEnemyIDs)
        ReducePCHPBattle1()

        ColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["LvRand"], 0)
        ColumnAdjust("./_internal/JsonOutputs/common/FLD_SalvageEnemySet.json", ["ene1Lv", "ene2Lv", "ene3Lv", "ene4Lv"], 0)
        

