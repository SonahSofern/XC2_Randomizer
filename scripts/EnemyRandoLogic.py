import json
import random
import time
import Helper
from IDs import ValidEnemies, ValidEnemyPopFileNames, FlyingEnArrangeIDs, OriginalFlyingHeights, OriginalWalkSpeeds, OriginalRunSpeeds, OriginalBtlSpeeds, SwimmingEnArrangeIDs
import copy, Options

AllBossDefaultIDs = [179, 180, 181, 182, 184, 185, 186, 187, 189, 190, 191, 193, 195, 196, 197, 198, 199, 201, 202, 203, 204, 206, 208, 210, 212, 214, 216, 217, 219, 220, 221, 222, 223, 225, 227, 229, 231, 232, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 248, 249, 250, 251, 252, 253, 254, 256, 258, 260, 262, 266, 267, 268, 269, 270, 271, 274, 1342, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1448, 1454, 1632, 1733, 1746, 1747, 1748, 1749, 1754, 1755]
AllBossDefaultLevels = [1, 2, 4, 5, 6, 8, 6, 10, 11, 12, 13, 15, 22, 25, 24, 26, 20, 18, 19, 21, 22, 24, 23, 23, 24, 26, 29, 31, 27, 29, 31, 32, 33, 34, 32, 35, 40, 38, 38, 39, 42, 42, 43, 42, 44, 46, 44, 52, 54, 56, 52, 50, 60, 60, 57, 66, 68, 60, 60, 60, 60, 13, 24, 26, 32, 33, 34, 60, 36, 2, 2, 8, 10, 10, 14, 10, 11, 20, 16, 17, 18, 29, 29, 40, 38, 48, 53, 3, 32, 63, 60, 58, 64, 62, 64, 64]
#print(Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllBossDefaultIDs, "Lv"))

AllQuestDefaultEnemyIDs = [303, 304, 305, 307, 308, 309, 310, 318, 319, 320, 323, 324, 325, 326, 329, 332, 341, 342, 345, 346, 347, 348, 349, 350, 351, 352, 356, 359, 365, 367, 369, 372, 373, 374, 375, 376, 383, 384, 385, 386, 389, 390, 391, 392, 393, 394, 395, 396, 399, 401, 403, 404, 405, 406, 407, 409, 411, 414, 415, 418, 436, 437, 445, 446, 447, 448, 450, 451, 454, 455, 456, 457, 458, 459, 461, 462, 463, 464, 466, 468, 470, 475, 477, 479, 481, 483, 485, 487, 488, 489, 490, 491, 492, 493, 495, 496, 497, 498, 500, 501, 503, 504, 506, 508, 510, 512, 513, 515, 517, 519, 525, 532, 533, 534, 535, 536, 538, 540, 542, 544, 546, 547, 548, 549, 550, 551, 552, 553, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 569, 570, 571, 572, 573, 576, 577, 578, 579, 581, 583, 588, 591, 593, 598, 600, 601, 602, 603, 604, 607, 608, 609, 610, 613, 635, 636, 639, 640, 641, 642, 644, 649, 650, 661, 663, 667, 669, 671, 673, 677, 690, 697, 739, 740, 741, 742, 743, 744, 746, 747, 748, 750, 751, 752, 753, 755, 759, 760, 761, 765, 767, 768, 775, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 797, 821, 822, 823, 824, 826, 827, 828, 829, 830, 831, 832, 833, 834, 837, 838, 839, 840, 841, 842, 848, 930, 932, 934, 935, 936, 938, 939, 943, 944, 946, 947, 948, 949, 964, 965, 967, 968, 970, 975, 984, 985, 996, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1046, 1047, 1048, 1049, 1052, 1053, 1054, 1055, 1058, 1059, 1065, 1066, 1071, 1074, 1075, 1076, 1077, 1078, 1093, 1094, 1095, 1096, 1097, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1128, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1172, 1173, 1174, 1175, 1196, 1197, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1210, 1211, 1212, 1215, 1216, 1218, 1219, 1223, 1224, 1225, 1226, 1227, 1229, 1230, 1231, 1234, 1236, 1237, 1238, 1239, 1240, 1242, 1244, 1245, 1246, 1248, 1249, 1250, 1343, 1344, 1345, 1348, 1386, 1387, 1388, 1389, 1391, 1393, 1395, 1397, 1398, 1400, 1402, 1404, 1405, 1406, 1407, 1408, 1410, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1422, 1423, 1424, 1425, 1457, 1458, 1465, 1467, 1468, 1469, 1470, 1471, 1472, 1482, 1484, 1485, 1486, 1489, 1490, 1491, 1497, 1499, 1502, 1512, 1516, 1518, 1519, 1526, 1527, 1528, 1534, 1537, 1540, 1546, 1548, 1549, 1551, 1575, 1576, 1579, 1581, 1585, 1589, 1592, 1594, 1596, 1598, 1602, 1604, 1605, 1607, 1610, 1614, 1616, 1618, 1619, 1621, 1628, 1634, 1644, 1648, 1651, 1653, 1655, 1674, 1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683, 1684, 1686, 1687, 1688, 1689, 1690, 1888]
AllQuestEnemyDefaultLevels = [5, 14, 22, 18, 19, 21, 12, 33, 35, 40, 41, 56, 56, 58, 25, 47, 25, 26, 10, 12, 9, 91, 36, 41, 57, 57, 38, 54, 25, 26, 28, 30, 32, 25, 26, 49, 44, 41, 27, 29, 22, 28, 29, 31, 33, 30, 31, 32, 60, 61, 58, 60, 62, 63, 62, 63, 64, 36, 34, 61, 42, 41, 69, 66, 67, 70, 50, 40, 40, 42, 42, 42, 44, 46, 51, 50, 53, 26, 26, 26, 30, 55, 52, 33, 34, 33, 38, 38, 38, 38, 40, 33, 33, 35, 35, 45, 46, 43, 53, 51, 48, 51, 45, 45, 46, 46, 47, 47, 48, 48, 50, 48, 51, 53, 52, 33, 33, 34, 35, 36, 39, 42, 42, 42, 44, 45, 44, 43, 56, 57, 50, 64, 43, 42, 45, 58, 55, 55, 57, 60, 61, 56, 58, 60, 43, 19, 19, 36, 36, 37, 42, 44, 44, 58, 58, 56, 61, 59, 9, 20, 40, 60, 80, 39, 6, 15, 6, 2, 7, 3, 2, 11, 14, 33, 25, 5, 16, 13, 23, 39, 19, 35, 17, 18, 20, 9, 18, 19, 18, 19, 19, 22, 23, 20, 21, 23, 20, 18, 35, 22, 20, 37, 20, 20, 21, 20, 19, 19, 18, 22, 75, 74, 76, 74, 75, 77, 78, 23, 35, 25, 27, 27, 25, 26, 27, 29, 81, 27, 26, 83, 83, 28, 80, 28, 33, 28, 29, 28, 80, 44, 43, 45, 46, 45, 44, 43, 44, 44, 44, 46, 43, 45, 34, 34, 39, 35, 39, 42, 34, 35, 42, 38, 39, 39, 36, 38, 35, 39, 41, 38, 40, 41, 39, 39, 40, 80, 41, 40, 39, 40, 40, 38, 38, 42, 42, 42, 42, 42, 84, 84, 84, 84, 85, 46, 48, 51, 49, 47, 49, 47, 47, 60, 49, 47, 50, 52, 52, 52, 52, 52, 53, 53, 54, 55, 53, 58, 57, 60, 55, 55, 55, 55, 58, 58, 58, 60, 55, 58, 60, 60, 58, 31, 32, 31, 31, 32, 33, 32, 42, 44, 32, 31, 32, 47, 44, 43, 38, 31, 32, 34, 32, 32, 44, 31, 31, 31, 43, 31, 33, 33, 33, 33, 33, 32, 43, 42, 44, 43, 42, 42, 58, 43, 42, 41, 9, 7, 65, 68, 66, 62, 38, 43, 45, 58, 60, 70, 70, 70, 70, 60, 58, 63, 61, 60, 84, 78, 81, 92, 88, 125, 96, 96, 62, 32, 35, 42, 46, 35, 40, 37, 39, 41, 20, 19, 24, 50, 10, 16, 43, 40, 14, 12, 15, 41, 32, 15, 26, 34, 14, 12, 32, 37, 38, 33, 9, 40, 20, 18, 40, 40, 23, 43, 38, 36, 6, 38, 23, 5, 28, 21, 32, 23, 30, 42, 3, 38, 19, 38, 40, 39, 25, 28, 38, 62, 63, 61, 65, 64, 62, 61, 33, 62, 68, 66, 59, 60, 61, 60, 59, 62]
#print(Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllQuestDefaultEnemyIDs, "Lv"))

AllSuperbossDefaultIDs = [247, 714, 928, 1022, 1027, 1110, 1135, 1137, 1189, 1559, 1560, 1561, 1562, 1723, 1756, 1758, 1759, 1763, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1775, 1776, 1777, 1778, 1779, 1783, 1784, 1785, 1786, 1792, 1793, 1794, 1795, 1800, 1802, 1803, 1804, 1808, 1809, 1811, 1812, 1813, 1814, 1886]
AllSuperbossDefaultLevels = [99, 104, 120, 130, 109, 110, 100, 117, 114, 75, 100, 85, 65, 100, 110, 104, 100, 100, 102, 104, 100, 101, 105, 104, 106, 103, 108, 106, 108, 110, 113, 115, 120, 110, 100, 140, 102, 110, 115, 150, 200, 110, 106, 120, 100, 100, 112, 130, 108, 104, 66]
#print(Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllSuperbossDefaultIDs, "Lv"))

AllUniqueMonsterDefaultIDs = [611, 612, 705, 706, 707, 708, 709, 710, 711, 712, 713, 715, 736, 738, 808, 809, 810, 811, 812, 814, 815, 816, 817, 819, 890, 891, 892, 893, 894, 895, 896, 898, 899, 926, 929, 953, 954, 955, 957, 958, 1019, 1020, 1023, 1025, 1026, 1101, 1102, 1104, 1106, 1108, 1109, 1111, 1112, 1113, 1114, 1115, 1131, 1132, 1134, 1155, 1156, 1157, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1255, 1256, 1258, 1260, 1261, 1262, 1264, 1265, 1563, 1564, 1566, 1567, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1670, 1774]
AllUniqueMonsterDefaultLevels = [99, 99, 12, 8, 81, 90, 25, 45, 18, 75, 20, 28, 27, 14, 23, 65, 24, 80, 23, 78, 41, 48, 99, 26, 30, 32, 31, 62, 33, 33, 33, 86, 40, 99, 99, 46, 47, 48, 50, 51, 95, 55, 58, 62, 94, 41, 42, 42, 46, 44, 43, 51, 42, 60, 54, 46, 53, 54, 58, 56, 57, 58, 62, 60, 58, 64, 66, 65, 66, 66, 38, 38, 39, 47, 49, 48, 48, 45, 50, 45, 25, 18, 34, 48, 44, 50, 40, 38, 33, 23, 48, 36, 55, 25, 99]
#print(Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllUniqueMonsterDefaultIDs, "Lv"))

AllNormalEnemyDefaultIDs = [313, 315, 339, 413, 474, 476, 521, 523, 555, 568, 630, 631, 632, 633, 634, 637, 638, 643, 645, 646, 647, 648, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 662, 664, 665, 666, 668, 670, 672, 674, 675, 676, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 691, 692, 693, 694, 695, 696, 699, 701, 703, 716, 717, 718, 719, 720, 721, 722, 723, 729, 730, 731, 732, 733, 734, 735, 745, 749, 754, 756, 757, 758, 762, 763, 764, 766, 769, 770, 771, 772, 773, 774, 776, 777, 793, 794, 795, 796, 798, 800, 802, 804, 806, 825, 835, 836, 843, 844, 845, 847, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 884, 886, 888, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 922, 924, 931, 933, 937, 940, 941, 942, 945, 950, 951, 952, 959, 960, 961, 962, 963, 966, 969, 971, 972, 973, 974, 976, 977, 978, 979, 980, 981, 982, 983, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1015, 1016, 1017, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1044, 1045, 1050, 1051, 1056, 1057, 1060, 1061, 1062, 1063, 1064, 1067, 1068, 1069, 1070, 1072, 1073, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1098, 1099, 1100, 1127, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1170, 1171, 1176, 1177, 1178, 1190, 1191, 1192, 1193, 1194, 1195, 1198, 1208, 1209, 1213, 1214, 1217, 1220, 1221, 1222, 1228, 1232, 1233, 1235, 1241, 1243, 1247, 1251, 1254, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1276, 1277, 1279, 1281, 1282, 1283, 1284, 1286, 1287, 1288, 1320, 1321, 1322, 1324, 1326, 1329, 1366, 1380, 1396, 1399, 1421, 1455, 1456, 1459, 1460, 1461, 1462, 1463, 1464, 1466, 1473, 1474, 1476, 1477, 1478, 1479, 1483, 1487, 1488, 1496, 1498, 1500, 1501, 1503, 1507, 1508, 1511, 1513, 1515, 1522, 1529, 1530, 1531, 1532, 1535, 1536, 1539, 1541, 1542, 1543, 1544, 1545, 1547, 1550, 1565, 1570, 1571, 1572, 1573, 1574, 1577, 1578, 1580, 1582, 1583, 1584, 1586, 1587, 1588, 1590, 1591, 1595, 1597, 1600, 1601, 1603, 1606, 1608, 1609, 1611, 1612, 1613, 1617, 1622, 1623, 1624, 1625, 1626, 1627, 1629, 1630, 1631, 1635, 1636, 1637, 1638, 1639, 1640, 1642, 1643, 1645, 1646, 1647, 1649, 1650, 1652, 1656, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1728, 1729, 1730, 1732, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1757, 1760, 1761, 1762, 1764, 1780, 1781, 1782, 1790, 1791, 1796, 1797, 1798, 1799, 1801, 1810, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1882, 1884]
AllNormalEnemyDefaultLevels = [31, 29, 2, 36, 46, 54, 48, 49, 47, 58, 3, 2, 2, 2, 3, 5, 69, 6, 8, 6, 3, 8, 9, 10, 5, 7, 8, 42, 22, 4, 90, 74, 34, 5, 71, 73, 12, 13, 24, 4, 5, 39, 72, 10, 13, 15, 40, 14, 39, 14, 38, 11, 22, 5, 38, 40, 37, 70, 21, 24, 12, 15, 16, 4, 4, 4, 6, 16, 34, 36, 40, 7, 7, 13, 9, 9, 9, 11, 17, 74, 17, 24, 32, 61, 63, 21, 47, 17, 20, 20, 39, 21, 18, 18, 72, 34, 21, 62, 38, 75, 95, 97, 96, 23, 22, 19, 27, 28, 32, 29, 28, 85, 32, 31, 33, 31, 31, 32, 33, 34, 35, 34, 28, 29, 26, 29, 31, 61, 60, 61, 62, 63, 60, 33, 33, 33, 33, 43, 43, 59, 60, 25, 25, 26, 25, 26, 30, 31, 30, 24, 25, 26, 28, 32, 34, 36, 29, 28, 29, 28, 28, 29, 29, 27, 27, 27, 32, 33, 96, 97, 98, 44, 45, 43, 44, 45, 45, 45, 45, 46, 45, 49, 50, 51, 54, 56, 35, 38, 40, 41, 88, 44, 39, 90, 48, 93, 50, 49, 40, 43, 46, 46, 45, 35, 49, 44, 45, 47, 60, 45, 50, 50, 51, 50, 50, 50, 53, 49, 52, 51, 44, 51, 41, 44, 49, 50, 49, 56, 32, 33, 42, 43, 46, 48, 51, 39, 42, 38, 38, 80, 78, 40, 79, 40, 84, 86, 79, 82, 84, 87, 81, 88, 40, 43, 39, 41, 41, 40, 41, 41, 42, 41, 53, 53, 54, 53, 83, 39, 39, 47, 44, 45, 46, 47, 48, 50, 52, 55, 55, 97, 97, 58, 52, 55, 56, 57, 59, 61, 44, 43, 42, 43, 42, 32, 43, 43, 43, 42, 43, 44, 34, 34, 43, 43, 43, 34, 32, 32, 32, 32, 38, 40, 42, 44, 2, 4, 2, 23, 24, 67, 65, 36, 36, 38, 5, 8, 10, 9, 12, 6, 80, 100, 40, 54, 95, 31, 30, 38, 39, 39, 35, 37, 36, 38, 9, 10, 52, 52, 54, 41, 18, 37, 39, 38, 12, 16, 10, 8, 11, 6, 35, 33, 11, 12, 11, 15, 36, 12, 30, 13, 38, 37, 38, 38, 36, 35, 36, 39, 10, 4, 3, 32, 21, 18, 26, 4, 6, 4, 32, 43, 30, 3, 9, 19, 13, 5, 3, 43, 45, 44, 20, 4, 33, 48, 40, 20, 10, 36, 25, 51, 21, 20, 19, 21, 43, 20, 33, 20, 11, 23, 2, 4, 30, 22, 27, 39, 39, 39, 21, 28, 30, 66, 25, 26, 27, 26, 28, 29, 27, 30, 30, 32, 28, 30, 36, 27, 29, 26, 33, 32, 35, 30, 33, 26, 28, 35, 58, 60, 62, 66, 68, 70, 80, 70, 60, 60, 58, 60, 63, 66, 50, 50, 53, 55, 56, 58, 60, 62, 96, 90, 98, 94, 96, 90, 90, 90, 99, 99, 95, 96, 95, 96, 98, 99, 58, 56, 55, 62, 60, 61, 56, 62, 66, 68, 60, 46, 48, 44, 53, 55, 52, 51, 51, 58, 57, 54, 56, 55, 59, 58, 57, 56, 55, 60, 62, 60, 60, 60, 64, 60, 61, 62, 63, 61, 63, 62, 61, 64, 54, 53, 51, 55, 50, 56, 64, 62, 61, 58, 60, 60, 63, 59, 57, 61, 65, 64, 66, 63, 70, 99, 60, 65]
#print(Helper.FindValues("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["$id"], AllNormalEnemyDefaultIDs, "Lv"))

def ReworkedEnemyRando (DefaultEnemyIDs, RandomizedEnemyIDs):
    for i in range(0,len(ValidEnemyPopFileNames)):
        enemypopfile = "./_internal/JsonOutputs/common_gmk/" + ValidEnemyPopFileNames[i]
        try:
            with open(enemypopfile, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                for row in data['rows']: 
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
                json.dump(data, file, indent=2, ensure_ascii=False)
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
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_EnemyGroup.json", 'r+', encoding='utf-8') as file:
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
        json.dump(data, file, indent=2, ensure_ascii=False)
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
        json.dump(data, file, indent=2, ensure_ascii=False)

def ReducePCHPBattle1():
    filename = "./_internal/JsonOutputs/common/FLD_QuestBattle.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 3 or row["$id"] == 6: #battle on gramps at start of game
                row["ReducePCHP"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if (row["$id"] == 633) or (row["$id"] == 1346): #battle on gramps at start of game
                row["ExpRev"] = 1000
            if row["$id"] == 1346:
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii= False)

def SummonsLevelAdjustment(): # We want the summoned enemies to be the same level as the enemy that summoned them
    OriginalSummonedFirstIDs = [724, 1369, 1304, 1385, 1372, 1308, 242, 1376, 1378, 1379, 1807, 1373, 1377, 1380, 1806, 1285, 725, 1358, 1362, 1700, 1521, 728, 846, 1347, 1370, 1354, 1352, 1367, 1371, 1368, 1356, 1357, 1365, 1384, 1593, 1599, 1353, 1349, 1355, 1361, 1382, 1364, 1350, 1724, 1724, 1724, 1724, 1731, 1787, 1788, 1789, 1805, 1881, 1883, 1885, 1641, 1533, 1568, 1569, 1569]
    OriginalSummonedSecondIDs = [0, 0, 0, 0, 0, 0, 0, 1376, 1378, 1379, 1807, 1374, 0, 0, 0, 0, 726, 1359, 1362, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1382, 0, 1350, 1725, 1725, 1725, 1726, 0, 0, 0, 0, 1805, 0, 1883, 1885, 0, 0, 0, 0, 0]
    OriginalSummonedThirdIDs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1375, 0, 0, 0, 0, 727, 1360, 1363, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1383, 0, 1351, 0, 1726, 1727, 1727, 0, 0, 0, 0, 1805, 0, 1883, 1885, 0, 0, 0, 0, 0]
    EnemyIDThatSummonedThem = [[184], [957], [222, 269], [236], [250, 274, 351], [239], [242], [1168, 1177, 326], [1188], [1380], [1803], [1165, 1184, 558], [1184], [1189], [1802], [265, 275], [655], [1046], [1109], [1699], [1516], [711], [862], [688], [1128], [860], [794], [951], [1154], [950], [1009], [1010], [1081], [1212], [1635], [1630], [795], [710], [892], [772, 1065, 1066, 1115, 1225, 1613, 1717], [1260], [1114], [714], [1723], [1723], [1723], [1723], [1733], [1786], [1786], [1786], [1804], [1864], [1882, 1883, 1885], [1884], [1629], [1547], [1562], [1560], [1560]]
    MinLevels = []
    MinLevel = 255
    filename = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(EnemyIDThatSummonedThem)):
            MinLevel = 255
            for j in range(0, len(EnemyIDThatSummonedThem[i])):
                if EnemyIDThatSummonedThem[i][0] == 0:
                    MinLevel = 1
                    break
                for row in data["rows"]:
                    if row["$id"] == EnemyIDThatSummonedThem[i][j]:
                        if row["Lv"] < MinLevel:
                            MinLevel = row["Lv"]
                            break
            MinLevels.append(MinLevel)
        for i in range(0, len(OriginalSummonedFirstIDs)):
            for row in data["rows"]:
                if (row["$id"] == OriginalSummonedFirstIDs[i]) and (MinLevels[i] != 255):
                    if row["Lv"] > MinLevels[i]:
                        row["Lv"] = MinLevels[i]
                if (row["$id"] == OriginalSummonedSecondIDs[i]) and (MinLevels[i] != 255):
                    if row["Lv"] > MinLevels[i]:
                        row["Lv"] = MinLevels[i]
                if (row["$id"] == OriginalSummonedThirdIDs[i]) and (MinLevels[i] != 255):
                    if row["Lv"] > MinLevels[i]:
                        row["Lv"] = MinLevels[i]
        for row in data["rows"]: # artifice aion core summons these
            if row["$id"] == 1285:
                row["Lv"] = 69
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def KeyItemsReAdd(): 
    Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["PreciousID"], 0)
    #The following are all the replacement enemy IDs that replaced the original ID in the FLD_EnemyPop file. The variable name is the name of the original enemy that was replaced
    SargeantID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma05a_FLD_EnemyPop.json", ["$id"], [5502] , "ene1ID")
    DughallID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma05a_FLD_EnemyPop.json", ["$id"], [5504] , "ene2ID")
    HermitTirkinID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma05a_FLD_EnemyPop.json", ["$id"], [5554] , "ene1ID")
    SlyKrabbleID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common/FLD_SalvageEnemySet.json", ["$id"], [148] , "ene1ID")
    EngineerTirkinID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma08a_FLD_EnemyPop.json", ["$id"], [8387] , "ene1ID")
    SecurityTirkinID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma08a_FLD_EnemyPop.json", ["$id"], [8374] , "ene1ID")
    GigaRosaID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma11a_FLD_EnemyPop.json", ["$id"], [11002] , "ene1ID")
    GeglQuadwingID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma15a_FLD_EnemyPop.json", ["$id"], [15358] , "ene1ID")
    ArtificeOphionID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma17a_FLD_EnemyPop.json", ["$id"], [17059] , "ene1ID")
    RelicHolderTyrannorID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma18a_FLD_EnemyPop.json", ["$id"], [18098] , "ene1ID")
    StopperSovereign1ID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma18a_FLD_EnemyPop.json", ["$id"], [18101] , "ene1ID")
    StopperSovereign2ID = Helper.AdjustedFindBadValuesList("./_internal/JsonOutputs/common_gmk/ma18a_FLD_EnemyPop.json", ["$id"], [18102] , "ene1ID")
    OriginalEnemyIDsList = [SargeantID, DughallID, HermitTirkinID, SlyKrabbleID, EngineerTirkinID, SecurityTirkinID, GigaRosaID, GeglQuadwingID, ArtificeOphionID, RelicHolderTyrannorID, StopperSovereign1ID, StopperSovereign2ID]
    PreciousIDsList = [25224, 25305, 25442, 25149, 25227, 25228, 25305, 25017, 25404, 25084, 25451, 25452]
    filename = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(0, len(OriginalEnemyIDsList)):
            for row in data["rows"]:
                if row["$id"] == OriginalEnemyIDsList[i][0]:
                    row["PreciousID"] = PreciousIDsList[i]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def LevelReversion(FullDefaultIDs, FullRandomizedIDs, SpecificDefaultIDs, SpecificDefaultLevels): #specificdefaultids is boss or quest at the moment (not randomized)
    filename = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        try: # sometimes this breaks, and I don't know why :D
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
        except:
            pass
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)                        

def FightBalancing(filenames, TargetIDs, LevelChange): #Changes the level scaling of any desired fights
    for i in range(0, len(LevelChange)):
        with open(filenames[i], 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data["rows"]:
                if row["$id"] == TargetIDs[i]:
                    for j in range(1, 5):
                        if row[f"ene{j}ID"] != 0:
                            row[f"ene{j}Lv"] = LevelChange[i]
                        else:
                            break
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)                            

def BigEnemyCollisionFix(): # Fixes ophion/other large enemies going outside the spawn circle and flying out of range in a boss fight
    with open("./_internal/JsonOutputs/common/RSC_En.json", 'r+', encoding='utf-8') as file: 
        BigEnemies = [64,65,70,154,245,249,252]
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in BigEnemies:
                row["CharColli"] = 0 #removes enemy collision
                row["EnRadius"] = 255 #sets radius you can hit them
                row["EnRadius2"] = 255 # sets radius they can hit you
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
        
def FishFix(): # changes all fish to flying type enemies so that when they spawn in, they don't instantly die and bug out. Doesn't fix enemies dying instantly in water
    with open("./_internal/JsonOutputs/common/RSC_En.json", 'r+', encoding='utf-8') as file: 
        FishIDs = [133, 135, 136, 137, 475, 476, 477, 478]
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in FishIDs:
                row["ActType"] = 3
                row["FlyHeight"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def NewNonBossandQuestIDs(): # don't trust my old method of getting quest and boss ids post randomization, here's a better approach
    BossIDsPostRandomization = []
    QuestIDsPostRandomization = []
    NonBossandQuestIDsPostRandomization = []
    for i in range(0, len(ValidEnemyPopFileNames)):
        enemypopfile = "./_internal/JsonOutputs/common_gmk/" + ValidEnemyPopFileNames[i]
        with open(enemypopfile, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for row in data['rows']:
                RedRingClear(row)
                if row["name"][:3] == "bos":
                    for j in range(1, 5):
                        if row[f"ene{j}ID"] != 0:
                            BossIDsPostRandomization.append(row[f"ene{j}ID"])
                        else:
                            break
                elif row["name"][:3] == "qst":
                    for j in range(1, 5):
                        if row[f"ene{j}ID"] != 0:
                            QuestIDsPostRandomization.append(row[f"ene{j}ID"])
                        else:
                            break
                else:
                    for j in range(1, 5):
                        if row[f"ene{j}ID"] != 0:
                            NonBossandQuestIDsPostRandomization.append(row[f"ene{j}ID"])
                        else:
                            break
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    return list(set(BossIDsPostRandomization)), list(set(QuestIDsPostRandomization)), list(set(NonBossandQuestIDsPostRandomization))       

def BossQuestAggroAdjustments(NewBossIDs, NewQuestIDs): # Required to allow bosses/quest enemies to aggro (including ones we don't randomize!)
    filename = "./_internal/JsonOutputs/common/CHR_EnArrange.json"
    with open(filename, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] in NewBossIDs:
                row["Flag"]["AlwaysAttack"] = 1
                row["Detects"] = 3
                row["SearchRange"] = 10
                row["SearchAngle"] = 360
                row["SearchRadius"] = 5
                row["BatInterval"] = 200
                row["BatArea"] = 200
                row["Flag"]["mBoss"] = 1
                row["Flag"]["Named"] = 0
                continue
            elif row["$id"] in NewQuestIDs:
                row["Flag"]["AlwaysAttack"] = 0
                row["Detects"] = 1
                row["SearchRange"] = 10
                row["SearchAngle"] = 100
                row["SearchRadius"] = 1
                row["BatInterval"] = 50
                row["BatArea"] = 50
                row["Flag"]["Named"] = 0
                continue
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def EnemyAggroProportion():
    if Options.UMHuntOption.GetState():
        return
    EnemyRandoOnBox = Options.EnemiesOption.GetState()
    StoryBossesBox = Options.EnemiesOption_Bosses.GetState()
    QuestEnemyBox = Options.EnemiesOption_QuestEnemies.GetState()
    UniqueMonstersBox = Options.EnemiesOption_UniqueMonsters.GetState()
    SuperbossesBox = Options.EnemiesOption_Superbosses.GetState()
    NormalEnemiesBox = Options.EnemiesOption_NormalEnemies.GetState()
    if EnemyRandoOnBox:
        if StoryBossesBox or UniqueMonstersBox or SuperbossesBox or NormalEnemiesBox or QuestEnemyBox: # do nothing, got handled after enemy randomization
            pass
    EnemyAggroSliderOdds = Options.EnemyAggroOption.GetState()
    NewBossIDs, NewQuestIDs, OtherEnemyIDs = NewNonBossandQuestIDs()
    if EnemyAggroSliderOdds == 0: #if the slider is 0, turn every enemy passive
        with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for row in data["rows"]:
                if (row["$id"] in ValidEnemies) & (row["$id"] in OtherEnemyIDs):
                    row["Flag"]["AlwaysAttack"] = 0
                    row["Flag"]["mBoss"] = 0
                    row["SearchRange"] = 0
                    row["SearchRadius"] = 0
                    row["SearchAngle"] = 0
                    row["Detects"] = 0
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
    else: # run aggro adjustments on non-randomized enemies, not touching boss or quest enemy ids
        with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for row in data["rows"]:
                if (EnemyAggroSliderOdds != 100) & (row["$id"] in OtherEnemyIDs) & (random.randint(0,100) >= EnemyAggroSliderOdds) & (row["$id"] in ValidEnemies):
                    row["Flag"]["AlwaysAttack"] = 0
                    row["Flag"]["mBoss"] = 0
                    row["SearchRange"] = 0
                    row["SearchRadius"] = 0
                    row["SearchAngle"] = 0
                    row["Detects"] = 0
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
                elif (row["$id"] in OtherEnemyIDs) & (row["$id"] in ValidEnemies):
                    row["Flag"]["mBoss"] = 0
                    row["Flag"]["AlwaysAttack"] = 1
                    row["Detects"] = 1
                    if row["SearchRange"] == 0:
                        row["SearchRange"] = random.randint(5, 25)
                    if row["SearchAngle"] == 0:
                        row["SearchAngle"] = random.randint(45, 135)
                    if row["SearchRadius"] == 0:
                        row["SearchRadius"] = random.randint(1, 10)
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)

def PostRandomizationNonBossandQuestAggroAdjustments(OtherEnemyIDs): #when enemy rando is on
    EnemyAggroOnBox = Options.EnemyAggroOption.GetState()
    EnemyAggroSliderOdds = Options.EnemyAggroOption.GetOdds()
    if EnemyAggroOnBox: # if enemy aggro is randomized
        with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: 
            data = json.load(file)
            for row in data["rows"]:
                if (EnemyAggroSliderOdds != 100) & (row["$id"] in OtherEnemyIDs) & (random.randint(0,100) >= EnemyAggroSliderOdds) & (row["$id"] in ValidEnemies):
                    row["Flag"]["AlwaysAttack"] = 0
                    row["Flag"]["mBoss"] = 0
                    row["SearchRange"] = 0
                    row["SearchRadius"] = 0
                    row["SearchAngle"] = 0
                    row["Detects"] = 0
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
                elif (row["$id"] in OtherEnemyIDs) & (row["$id"] in ValidEnemies):
                    row["Flag"]["mBoss"] = 0
                    row["Flag"]["AlwaysAttack"] = 1
                    row["Detects"] = 1
                    if row["SearchRange"] == 0:
                        row["SearchRange"] = random.randint(10, 25) # some enemies might naturally be passive, we need to turn them aggressive
                    if row["SearchAngle"] == 0:
                        row["SearchAngle"] = random.randint(90, 180)
                    if row["SearchRadius"] == 0:
                        row["SearchRadius"] = random.randint(5, 10)
                    row["BatInterval"] = 50
                    row["BatArea"] = 50
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=2, ensure_ascii=False)
          
def AeshmaCoreHPNerf(): #this fight sucks
    with open("./_internal/JsonOutputs/common/CHR_EnParam.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 318:
                row["HpMaxRev"] = 1500 # nerfed hp by 5/6ths
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)        

def GortOgreUppercutRemoval(): # Gort 2's Ogre Uppercut seems to be buggy, reported to crash game in certain situations, so it's being removed for the time being.
    with open("./_internal/JsonOutputs/common/CHR_EnParam.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1434:
                row["ArtsNum4"] = 963 # replaced Ogre Uppercut with a second instance of Ogre Flame
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def RedRingClear(row):
    KeepRingIDs = [7007,7008,7001,7005]
    try:
        if row["$id"] not in KeepRingIDs:
            row["battlelockname"] = 0
    except:
        pass
    
def EarthBreathNerf(): # Cressidus's Earth Breath is pretty strong if the enemy happens to show up early. Nerfed by 3/4ths.
    with open("./_internal/JsonOutputs/common/BTL_Arts_Bl.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 218:
                row["DmgMgn1"] = 500
                row["DmgMgn2"] = 500
                row["DmgMgn3"] = 500
                row["DmgMgn4"] = 500
                row["DmgMgn5"] = 500
                row["DmgMgn6"] = 500
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def PadraigFightFix(): # padraig fight fails to spawn unique monster if it replaces him, after you kill him in phase 1.
    EnemyIDtoChange = []
    with open("./_internal/JsonOutputs/common_gmk/ma05a_FLD_EnemyPop.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 5500:
                if row["ene1ID"] in AllUniqueMonsterDefaultIDs:
                    EnemyIDtoChange = row["ene1ID"]
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == EnemyIDtoChange:
                row["Flag"]["Named"] = 0
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def EnemyDupeBossCondition(NewBossIDs): # If a phantasm or elma (which summon copies of themselves) end up as a boss enemy, the boss fight should require all copies to be dead for you to win.
    DupingEnemyIDs = [242, 281, 1882, 1884]
    EnemyGroupsWithDupingEnemies = []
    with open("./_internal/JsonOutputs/common/FLD_EnemyGroup.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data['rows']:
            for i in range(1, 13):
                if (row[f"EnemyID{i}"] in DupingEnemyIDs) & (row[f"EnemyID{i}"] in NewBossIDs):
                    EnemyGroupsWithDupingEnemies.append(row["$id"])
                    break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)
    with open("./_internal/JsonOutputs/common/FLD_QuestBattle.json", 'r+', encoding='utf-8') as file:
        data = json.load(file)
        for row in data['rows']:
            if ((row["EnemyID"] in DupingEnemyIDs) & (row["EnemyID"] in NewBossIDs)) or (row["EnemyGroupID"] in EnemyGroupsWithDupingEnemies):
                row["DeadAll"] = 1
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def FlyingEnemyFix(TotalDefaultEnemyIDs, TotalRandomizedEnemyIDs):
    NewFlyingEnemyIDs, NewFlyingEnemyParamIDs, NewFlyingEnemyResourceIDs = [], [], [] # Regular Enemy ID Holders
    FlyingBladeIDs, FlyingBladeParamIDs, FlyingBladeRSCIDs = [], [], [] # Blade ID Holders
    for i in range(0, len(TotalDefaultEnemyIDs)):
        if TotalDefaultEnemyIDs[i] in FlyingEnArrangeIDs:
            NewFlyingEnemyIDs.append(TotalRandomizedEnemyIDs[i]) # gets the new Flying Enemy IDs
    EnParamLastRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/CHR_EnParam.json", "$id")
    RSCEnLastRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/RSC_En.json", "$id")
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as arrangefile: #this way of nesting files gets complicated with naming, but it definitely does look cleaner
        arrangedata = json.load(arrangefile)
        with open("./_internal/JsonOutputs/common/CHR_EnParam.json", 'r+', encoding='utf-8') as paramfile:
            paramdata = json.load(paramfile) 
            with open("./_internal/JsonOutputs/common/RSC_En.json", 'r+', encoding='utf-8') as rscfile:
                rscdata = json.load(rscfile)
                FlyingBladeParamIDs = []
                FlyingBladeRSCIDs = []
                ParamCurrRow = EnParamLastRow + 1 # These two hold the current ParamID and RSCID we're on. We have to use this approach because we are only adding new Params for blades if their drivers can fly, so we skip some values of i in the loop
                RSCCurrRow = RSCEnLastRow + 1 
                for i in range(0, len(NewFlyingEnemyIDs)): # making drivers fly
                    for arrangerow in arrangedata["rows"]:
                        if arrangerow["$id"] == NewFlyingEnemyIDs[i]:
                            NewFlyingEnemyParamIDs.append(arrangerow["ParamID"])
                            if arrangerow["EnemyBladeID"] > 0:
                                FlyingBladeIDs.append(arrangerow["EnemyBladeID"])
                            else:
                                FlyingBladeIDs.append(0)
                            arrangerow["ParamID"] = ParamCurrRow
                            break
                    for paramrow in paramdata["rows"]:
                        if paramrow["$id"] == NewFlyingEnemyParamIDs[i]:
                            NewFlyingEnemyResourceIDs.append(paramrow["ResourceID"])
                            paramrownew = copy.deepcopy(paramrow)
                            paramrownew["$id"] = ParamCurrRow
                            paramrownew["ResourceID"] = RSCCurrRow
                            paramrownew["WalkSpeed"] = OriginalWalkSpeeds[i]
                            paramrownew["RunSpeed"] = OriginalRunSpeeds[i]
                            paramrownew["BtlSpeed"] = OriginalBtlSpeeds[i]
                            paramdata["rows"].append(paramrownew)
                            break
                    for rscrow in rscdata["rows"]:
                        if rscrow["$id"] == NewFlyingEnemyResourceIDs[i]:
                            rscrownew = copy.deepcopy(rscrow)
                            rscrownew["$id"] = RSCCurrRow
                            rscrownew["FlyHeight"] = OriginalFlyingHeights[i]
                            rscrownew["ActType"] = 3
                            rscrownew["Flag"]["Bait"] = 1
                            rscdata["rows"].append(rscrownew)
                            break
                    ParamCurrRow += 1
                    RSCCurrRow += 1 
                for i in range(0, len(FlyingBladeIDs)): # now we do the blades
                    if FlyingBladeIDs[i] > 0:
                        for arrangerow in arrangedata["rows"]:
                            if arrangerow["$id"] == FlyingBladeIDs[i]:
                                FlyingBladeParamIDs.append(arrangerow["ParamID"])
                                arrangerow["ParamID"] = ParamCurrRow # because these are two separate loops, we need to add the length of the first set of rows added
                                break
                        for paramrow in paramdata["rows"]:
                            if paramrow["$id"] == FlyingBladeParamIDs[i]:
                                FlyingBladeRSCIDs.append(paramrow["ResourceID"])
                                paramrownew = copy.deepcopy(paramrow)
                                paramrownew["$id"] = ParamCurrRow
                                paramrownew["ResourceID"] = RSCCurrRow
                                paramrownew["WalkSpeed"] = OriginalWalkSpeeds[i]
                                paramrownew["RunSpeed"] = OriginalRunSpeeds[i]
                                paramrownew["BtlSpeed"] = OriginalBtlSpeeds[i]
                                paramdata["rows"].append(paramrownew)
                                break
                        for rscrow in rscdata["rows"]:
                            if rscrow["$id"] == FlyingBladeRSCIDs[i]:
                                rscrownew = copy.deepcopy(rscrow)
                                rscrownew["$id"] = RSCCurrRow
                                rscrownew["FlyHeight"] = OriginalFlyingHeights[i]
                                rscrownew["ActType"] = 3
                                rscdata["rows"].append(rscrownew)
                                break
                        ParamCurrRow += 1
                        RSCCurrRow += 1 
                    else:
                        FlyingBladeParamIDs.append(0)
                        FlyingBladeRSCIDs.append(0)
                rscfile.seek(0)
                rscfile.truncate()
                json.dump(rscdata, rscfile, indent=2, ensure_ascii=False)
            paramfile.seek(0)
            paramfile.truncate()
            json.dump(paramdata, paramfile, indent=2, ensure_ascii=False)
        arrangefile.seek(0)
        arrangefile.truncate()
        json.dump(arrangedata, arrangefile, indent=2, ensure_ascii=False)

def SwimmingEnemyFix(TotalDefaultEnemyIDs, TotalRandomizedEnemyIDs):
    NewSwimmingEnemyIDs, NewSwimmingEnemyParamIDs, NewSwimmingEnemyResourceIDs = [], [], [] # Regular Enemy ID Holders
    SwimmingBladeIDs, SwimmingBladeParamIDs, SwimmingBladeRSCIDs = [], [], [] # Blade ID Holders
    for i in range(0, len(TotalDefaultEnemyIDs)):
        if TotalDefaultEnemyIDs[i] in SwimmingEnArrangeIDs:
            NewSwimmingEnemyIDs.append(TotalRandomizedEnemyIDs[i]) # gets the new Swimming Enemy IDs
    EnParamLastRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/CHR_EnParam.json", "$id")
    RSCEnLastRow = Helper.GetMaxValue("./_internal/JsonOutputs/common/RSC_En.json", "$id")
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as arrangefile: #this way of nesting files gets complicated with naming, but it definitely does look cleaner
        arrangedata = json.load(arrangefile)
        with open("./_internal/JsonOutputs/common/CHR_EnParam.json", 'r+', encoding='utf-8') as paramfile:
            paramdata = json.load(paramfile) 
            with open("./_internal/JsonOutputs/common/RSC_En.json", 'r+', encoding='utf-8') as rscfile:
                rscdata = json.load(rscfile)
                SwimmingBladeParamIDs = []
                SwimmingBladeRSCIDs = []
                ParamCurrRow = EnParamLastRow + 1 # These two hold the current ParamID and RSCID we're on. We have to use this approach because we are only adding new Params for blades if their drivers can fly, so we skip some values of i in the loop
                RSCCurrRow = RSCEnLastRow + 1 
                for i in range(0, len(NewSwimmingEnemyIDs)): # making drivers fly
                    for arrangerow in arrangedata["rows"]:
                        if arrangerow["$id"] == NewSwimmingEnemyIDs[i]:
                            NewSwimmingEnemyParamIDs.append(arrangerow["ParamID"])
                            if arrangerow["EnemyBladeID"] > 0:
                                SwimmingBladeIDs.append(arrangerow["EnemyBladeID"])
                            else:
                                SwimmingBladeIDs.append(0)
                            arrangerow["ParamID"] = ParamCurrRow
                            break
                    for paramrow in paramdata["rows"]:
                        if paramrow["$id"] == NewSwimmingEnemyParamIDs[i]:
                            NewSwimmingEnemyResourceIDs.append(paramrow["ResourceID"])
                            paramrownew = copy.deepcopy(paramrow)
                            paramrownew["$id"] = ParamCurrRow
                            paramrownew["ResourceID"] = RSCCurrRow
                            paramdata["rows"].append(paramrownew)
                            break
                    for rscrow in rscdata["rows"]:
                        if rscrow["$id"] == NewSwimmingEnemyResourceIDs[i]:
                            rscrownew = copy.deepcopy(rscrow)
                            rscrownew["$id"] = RSCCurrRow
                            rscrownew["ActType"] = 1
                            rscrownew["Flag"]["Bait"] = 1
                            rscdata["rows"].append(rscrownew)
                            break
                    ParamCurrRow += 1
                    RSCCurrRow += 1 
                for i in range(0, len(SwimmingBladeIDs)): # now we do the blades
                    if SwimmingBladeIDs[i] > 0:
                        for arrangerow in arrangedata["rows"]:
                            if arrangerow["$id"] == SwimmingBladeIDs[i]:
                                SwimmingBladeParamIDs.append(arrangerow["ParamID"])
                                arrangerow["ParamID"] = ParamCurrRow # because these are two separate loops, we need to add the length of the first set of rows added
                                break
                        for paramrow in paramdata["rows"]:
                            if paramrow["$id"] == SwimmingBladeParamIDs[i]:
                                SwimmingBladeRSCIDs.append(paramrow["ResourceID"])
                                paramrownew = copy.deepcopy(paramrow)
                                paramrownew["$id"] = ParamCurrRow
                                paramrownew["ResourceID"] = RSCCurrRow
                                paramdata["rows"].append(paramrownew)
                                break
                        for rscrow in rscdata["rows"]:
                            if rscrow["$id"] == SwimmingBladeRSCIDs[i]:
                                rscrownew = copy.deepcopy(rscrow)
                                rscrownew["$id"] = RSCCurrRow
                                rscrownew["ActType"] = 1
                                rscdata["rows"].append(rscrownew)
                                break
                        ParamCurrRow += 1
                        RSCCurrRow += 1 
                    else:
                        SwimmingBladeParamIDs.append(0)
                        SwimmingBladeRSCIDs.append(0)
                rscfile.seek(0)
                rscfile.truncate()
                json.dump(rscdata, rscfile, indent=2, ensure_ascii=False)
            paramfile.seek(0)
            paramfile.truncate()
            json.dump(paramdata, paramfile, indent=2, ensure_ascii=False)
        arrangefile.seek(0)
        arrangefile.truncate()
        json.dump(arrangedata, arrangefile, indent=2, ensure_ascii=False)

def GerolfSovereignFix(): # Gerolf Sovereign gets summoned by Mk VI. Sovereign, which in turn can summon enemies. This breaks the code that changes summons levels to match the enemy that summoned them.
    with open("./_internal/JsonOutputs/common/CHR_EnArrange.json", 'r+', encoding='utf-8') as file: #id 1379 needs to match 1380 in levels
        data = json.load(file)
        for row in data["rows"]:
            if row["$id"] == 1380:
                GerolfLevel = row["Lv"]
                break
        for row in data["rows"]:
            if row["$id"] == 1379:
                row["Lv"] = GerolfLevel
                break
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=2, ensure_ascii=False)

def BalanceFixes(): # All the bandaids I slapped on to fix problematic enemies/fights
    ReducePCHPBattle1()
    SummonsLevelAdjustment()
    FightBalancing(["./_internal/JsonOutputs/common_gmk/ma13a_FLD_EnemyPop.json", "./_internal/JsonOutputs/common_gmk/ma16a_FLD_EnemyPop.json"], [13001, 16149], [-5, -5])
    FishFix()
    BigEnemyCollisionFix()
    AeshmaCoreHPNerf()
    GortOgreUppercutRemoval()
    EarthBreathNerf()
    PadraigFightFix()
    GerolfSovereignFix()

def EnemyLogic():
    EnemyRandoOn = False
    EnemiestoPass = []
    LevelstoPass = []
    CheckboxList = [] #I'm lazy, so i'm just going to pass the names and true/false states to two arrays
    CheckboxStates = []
    StoryBossesBox = Options.EnemiesOption_Bosses.GetState()
    # KeepStoryBossesLevelsBox = OptionsRunDict["Enemies"]["subOptionObjects"]["Use Original Boss Encounter Levels"]["subOptionTypeVal"].get()
    QuestEnemyBox = Options.EnemiesOption_QuestEnemies.GetState()
    # KeepQuestEnemyLevelsBox = OptionsRunDict["Enemies"]["subOptionObjects"]["Use Original Quest Encounter Levels"]["subOptionTypeVal"].get()
    UniqueMonstersBox = Options.EnemiesOption_UniqueMonsters.GetState()
    SuperbossesBox = Options.EnemiesOption_Superbosses.GetState()
    NormalEnemiesBox = Options.EnemiesOption_NormalEnemies.GetState()
    KeepAllEnemyLevelsBox = Options.EnemiesOption_BalancedLevels.GetState()
    MixEnemiesBetweenTypesBox = Options.EnemiesOption_MixedTypes.GetState()
    AllBossDefaultIDstoUse = AllBossDefaultIDs
    AllBossDefaultLevelstoUse = AllBossDefaultLevels
    if Options.RaceModeOption.GetState(): # removing malos in auresco fight for race mode specifically, he has an absurd amount of hp and is just a slog of a fight
        AllBossDefaultIDstoUse = [x for x in AllBossDefaultIDs if x != 1443]
        del AllBossDefaultLevelstoUse[83]
    if StoryBossesBox or UniqueMonstersBox or SuperbossesBox or NormalEnemiesBox or QuestEnemyBox:
        EnemyRandoOn = True
        CheckboxList = ["Story Bosses", "Quest Enemies", "Unique Monsters", "Superbosses", "Normal Enemies", "Mix Enemies Between Types", "Use All Original Encounter Levels"]
        CheckboxStates = [StoryBossesBox, QuestEnemyBox, UniqueMonstersBox, SuperbossesBox, NormalEnemiesBox, MixEnemiesBetweenTypesBox, KeepAllEnemyLevelsBox]
    if EnemyRandoOn == True:
        print("Randomizing Enemies")
        TotalDefaultEnemyIDs = []
        TotalRandomizedEnemyIDs = []
        if MixEnemiesBetweenTypesBox:
            if StoryBossesBox:
                EnemiestoPass += AllBossDefaultIDstoUse
                LevelstoPass += AllBossDefaultLevelstoUse
                print("Bosses Added to Shuffle List")
            if QuestEnemyBox:
                EnemiestoPass += AllQuestDefaultEnemyIDs
                LevelstoPass += AllQuestEnemyDefaultLevels
                print("Quest Enemies Added to Shuffle List")
            if UniqueMonstersBox:
                EnemiestoPass += AllUniqueMonsterDefaultIDs
                LevelstoPass += AllUniqueMonsterDefaultLevels
                print("Unique Monsters Added to Shuffle List")
            if SuperbossesBox:
                EnemiestoPass += AllSuperbossDefaultIDs
                LevelstoPass += AllSuperbossDefaultLevels
                print("Superbosses Added to Shuffle List")             
            if NormalEnemiesBox:
                EnemiestoPass += AllNormalEnemyDefaultIDs
                LevelstoPass += AllNormalEnemyDefaultLevels 
                print("Normal Enemies Added to Shuffle List")             
            DefaultEnemyIDs = EnemiestoPass.copy()
            RandomizedEnemyIDs = DefaultEnemyIDs.copy()
            random.shuffle(RandomizedEnemyIDs)
            TotalDefaultEnemyIDs = DefaultEnemyIDs
            TotalRandomizedEnemyIDs = RandomizedEnemyIDs
            ReworkedEnemyRando(DefaultEnemyIDs, RandomizedEnemyIDs)
            if EnemiestoPass:
                if KeepAllEnemyLevelsBox:
                    LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, DefaultEnemyIDs, LevelstoPass)
                    print("Reverting all enemy levels")
        if not MixEnemiesBetweenTypesBox:
            print("Enemies not shuffled")
            for o in range(0, len(CheckboxList)):
                EnemiestoPass = []
                LevelstoPass = []
                if CheckboxList[o] == "Story Bosses" and CheckboxStates[o] == True:
                    EnemiestoPass = AllBossDefaultIDstoUse
                    LevelstoPass = AllBossDefaultLevelstoUse
                    print("Swapping Bosses")
                if CheckboxList[o] == "Quest Enemies" and CheckboxStates[o] == True:
                    EnemiestoPass = AllQuestDefaultEnemyIDs
                    LevelstoPass = AllQuestEnemyDefaultLevels
                    print("Swapping Quest Enemies")                      
                if CheckboxList[o] == "Unique Monsters" and CheckboxStates[o] == True:
                    EnemiestoPass = AllUniqueMonsterDefaultIDs
                    LevelstoPass = AllUniqueMonsterDefaultLevels
                    print("Swapping Unique Monsters")
                if CheckboxList[o] == "Superbosses" and CheckboxStates[o] == True:
                    EnemiestoPass = AllSuperbossDefaultIDs
                    LevelstoPass = AllSuperbossDefaultLevels
                    print("Swapping Superbosses")
                if CheckboxList[o] == "Normal Enemies" and CheckboxStates[o] == True:
                    EnemiestoPass = AllNormalEnemyDefaultIDs
                    LevelstoPass = AllNormalEnemyDefaultLevels
                    print("Swapping Normal Enemies")
                if EnemiestoPass: #if the list of enemies to pass is not empty
                    DefaultEnemyIDs = EnemiestoPass.copy()
                    RandomizedEnemyIDs = DefaultEnemyIDs.copy()
                    TotalDefaultEnemyIDs.extend(DefaultEnemyIDs)
                    random.shuffle(RandomizedEnemyIDs)
                    TotalRandomizedEnemyIDs.extend(RandomizedEnemyIDs)
                    ReworkedEnemyRando(DefaultEnemyIDs, RandomizedEnemyIDs)
                    if KeepAllEnemyLevelsBox:
                        LevelReversion(DefaultEnemyIDs, RandomizedEnemyIDs, DefaultEnemyIDs, LevelstoPass)
                        print("Reverting all enemy levels")
                        continue
        NewBossIDs, NewQuestIDs, OtherEnemyIDs = NewNonBossandQuestIDs()
        BossQuestAggroAdjustments(NewBossIDs, NewQuestIDs)
        KeyItemsReAdd()
        Helper.ColumnAdjust("./_internal/JsonOutputs/common/CHR_EnArrange.json", ["LvRand", "DriverLev"], 0)
        Helper.ColumnAdjust("./_internal/JsonOutputs/common/FLD_SalvageEnemySet.json", ["ene1Lv", "ene2Lv", "ene3Lv", "ene4Lv"], 0)
        PostRandomizationNonBossandQuestAggroAdjustments(OtherEnemyIDs)
        BalanceFixes()
        EnemyDupeBossCondition(NewBossIDs)
        FlyingEnemyFix(TotalDefaultEnemyIDs, TotalRandomizedEnemyIDs)
        SwimmingEnemyFix(TotalDefaultEnemyIDs, TotalRandomizedEnemyIDs)




        

