from ROOT import TChain
from os import listdir
from sys import argv
from numpy import mean,std
from math import sqrt,sin,cos,pi,isnan,log,isinf
import matplotlib.pyplot as plt

# LL Distributions from MC Study #
dqdsHist_good = [[ 0.15443279,  0.1029552 ,  0.37750238,  0.56625357,  0.97807436,
                   1.18398475,  1.01239276,  1.44137274,  1.71591992,  2.05910391,
                   2.2306959 ,  2.53956149,  2.57387989,  2.43660629,  2.11058151,
                   1.75023832,  1.68160153,  1.75023832,  1.51000953,  0.94375596,
                   1.06387035,  0.85795996,  0.85795996,  0.68636797,  0.54909438,
                   0.60057197,  0.41182078,  0.37750238,  0.42897998,  0.24022879,
                   0.22306959,  0.20591039,  0.12011439,  0.0514776 ,  0.1029552 ,
                   0.1029552 ],
                  [ 0.        ,  0.02777778,  0.05555556,  0.08333333,  0.11111111,
                    0.13888889,  0.16666667,  0.19444444,  0.22222222,  0.25      ,
                    0.27777778,  0.30555556,  0.33333333,  0.36111111,  0.38888889,
                    0.41666667,  0.44444444,  0.47222222,  0.5       ,  0.52777778,
                    0.55555556,  0.58333333,  0.61111111,  0.63888889,  0.66666667,
                    0.69444444,  0.72222222,  0.75      ,  0.77777778,  0.80555556,
                    0.83333333,  0.86111111,  0.88888889,  0.91666667,  0.94444444,
                    0.97222222,  1.        ]]

dqdsHist_bad = [[  2.95095532e+00,   5.77055021e+00,   5.33819853e+00,
                   4.35764976e+00,   3.49811809e+00,   2.83097256e+00,
                   2.39965522e+00,   1.88455682e+00,   1.56391323e+00,
                   1.20189628e+00,   9.47450079e-01,   7.32308576e-01,
                   5.98879471e-01,   4.14767993e-01,   3.46501939e-01,
                   2.32725183e-01,   1.92386151e-01,   1.39635110e-01,
                   1.16879759e-01,   9.30900733e-02,   6.10257147e-02,
                   4.86137049e-02,   3.93046976e-02,   3.30986927e-02,
                   2.17210171e-02,   2.89613561e-02,   2.17210171e-02,
                   1.75836805e-02,   1.44806781e-02,   1.65493464e-02,
                   1.24120098e-02,   4.13733659e-03,   3.10300244e-03,
                   3.10300244e-03,   6.20600488e-03,   5.68883781e-02],
                [ 0.        ,  0.02777778,  0.05555556,  0.08333333,  0.11111111,
                  0.13888889,  0.16666667,  0.19444444,  0.22222222,  0.25      ,
                  0.27777778,  0.30555556,  0.33333333,  0.36111111,  0.38888889,
                  0.41666667,  0.44444444,  0.47222222,  0.5       ,  0.52777778,
                  0.55555556,  0.58333333,  0.61111111,  0.63888889,  0.66666667,
                  0.69444444,  0.72222222,  0.75      ,  0.77777778,  0.80555556,
                  0.83333333,  0.86111111,  0.88888889,  0.91666667,  0.94444444,
                  0.97222222,  1.        ]]


pzHist_good = [[  2.81396561e-05,   0.00000000e+00,   0.00000000e+00,
                  9.37988536e-06,   0.00000000e+00,   1.87597707e-05,
                  9.37988536e-06,   2.81396561e-05,   8.44189682e-05,
                  9.37988536e-06,   1.87597707e-05,   1.12558624e-04,
                  1.03178739e-04,   2.06357478e-04,   2.43877019e-04,
                  3.56435644e-04,   3.75195414e-04,   4.31474726e-04,
                  4.50234497e-04,   6.00312663e-04,   7.78530485e-04,
                  1.00364773e-03,   1.00364773e-03,   1.10682647e-03,
                  1.15372590e-03,   1.36008338e-03,   1.36008338e-03,
                  1.30380406e-03,   1.31318395e-03,   8.72329338e-04,
                  9.09848880e-04,   8.81709224e-04,   6.47212090e-04,
                  4.40854612e-04,   5.15893695e-04,   2.62636790e-04],
               [-1000.        ,  -944.44444444,  -888.88888889,  -833.33333333,
                -777.77777778,  -722.22222222,  -666.66666667,  -611.11111111,
                -555.55555556,  -500.        ,  -444.44444444,  -388.88888889,
                -333.33333333,  -277.77777778,  -222.22222222,  -166.66666667,
                -111.11111111,   -55.55555556,     0.        ,    55.55555556,
                111.11111111,   166.66666667,   222.22222222,   277.77777778,
                333.33333333,   388.88888889,   444.44444444,   500.        ,
                555.55555556,   611.11111111,   666.66666667,   722.22222222,
                777.77777778,   833.33333333,   888.88888889,   944.44444444,
                1000.        ]]

pzHist_bad   = [[  1.22634790e-04,   1.28766529e-04,   1.48276610e-04,
                   1.57195503e-04,   1.87296770e-04,   2.12938590e-04,
                   2.52516181e-04,   2.80387724e-04,   3.35573380e-04,
                   3.85184726e-04,   4.40927813e-04,   5.22870150e-04,
                   5.96451024e-04,   7.43612771e-04,   8.62902976e-04,
                   1.04685516e-03,   1.20516553e-03,   1.87185284e-03,
                   1.50283361e-03,   1.21018240e-03,   9.81078319e-04,
                   8.37818587e-04,   6.48292094e-04,   5.55201140e-04,
                   4.91654021e-04,   4.11383977e-04,   3.46721997e-04,
                   3.04357251e-04,   2.56418197e-04,   2.03462265e-04,
                   1.91756217e-04,   1.49948902e-04,   1.15388189e-04,
                   1.15945620e-04,   9.42058159e-05,   8.19423369e-05],
                [-1000.        ,  -944.44444444,  -888.88888889,  -833.33333333,
                 -777.77777778,  -722.22222222,  -666.66666667,  -611.11111111,
                 -555.55555556,  -500.        ,  -444.44444444,  -388.88888889,
                 -333.33333333,  -277.77777778,  -222.22222222,  -166.66666667,
                 -111.11111111,   -55.55555556,     0.        ,    55.55555556,
                 111.11111111,   166.66666667,   222.22222222,   277.77777778,
                 333.33333333,   388.88888889,   444.44444444,   500.        ,
                 555.55555556,   611.11111111,   666.66666667,   722.22222222,
                 777.77777778,   833.33333333,   888.88888889,   944.44444444,
                 1000.        ]]

angminHist_good = [[ 0.00247855,  0.00181125,  0.00200191,  0.00209724,  0.00343184,
                    0.00305052,  0.00314585,  0.0036225 ,  0.00533842,  0.0049571 ,
                    0.00552908,  0.00571973,  0.00581506,  0.00743565,  0.0079123 ,
                    0.00819828,  0.00734032,  0.00648236,  0.0056244 ,  0.00486177,
                    0.00448046,  0.0049571 ,  0.00753098,  0.00629171,  0.00762631,
                    0.00695901,  0.00581506,  0.00600572,  0.00848427,  0.00619638,
                    0.00695901,  0.00762631,  0.00619638,  0.00629171,  0.00457579,
                    0.00714967],
                   [   0.,    5.,   10.,   15.,   20.,   25.,   30.,   35.,   40.,
                       45.,   50.,   55.,   60.,   65.,   70.,   75.,   80.,   85.,
                       90.,   95.,  100.,  105.,  110.,  115.,  120.,  125.,  130.,
                       135.,  140.,  145.,  150.,  155.,  160.,  165.,  170.,  175.,  180.]]

angminHist_bad = [[ 0.01071685,  0.00390748,  0.00205143,  0.00161471,  0.00125844,
                    0.00117225,  0.00117225,  0.00105157,  0.00106881,  0.00121247,
                    0.00107456,  0.0010918 ,  0.00110329,  0.00109754,  0.00164344,
                    0.00094239,  0.0013274 ,  0.00117225,  0.0018618 ,  0.0014021 ,
                    0.00129866,  0.00131016,  0.00123545,  0.00153426,  0.00171814,
                    0.001948  ,  0.00200546,  0.00208591,  0.00230427,  0.00263181,
                    0.00324091,  0.00493607,  0.00748168,  0.01173969,  0.0242379 ,
                    0.0923488 ],
                  [   0.,    5.,   10.,   15.,   20.,   25.,   30.,   35.,   40.,
                      45.,   50.,   55.,   60.,   65.,   70.,   75.,   80.,   85.,
                      90.,   95.,  100.,  105.,  110.,  115.,  120.,  125.,  130.,
                      135.,  140.,  145.,  150.,  155.,  160.,  165.,  170.,  175.,  180.]]

ang3DHist_good = [[ 0.79790276,  0.69494757,  0.84080076,  0.81506196,  0.72068637,
                    0.68636797,  0.62631077,  0.75500477,  0.81506196,  0.77216397,
                    0.72068637,  0.66920877,  0.64346997,  0.64346997,  0.54909438,
                    0.54051478,  0.73784557,  0.67778837,  0.64346997,  0.54909438,
                    0.50619638,  0.70352717,  0.33460439,  0.31744519,  0.25738799,
                    0.25738799,  0.34318398,  0.18017159,  0.17159199,  0.15443279,
                    0.12011439,  0.16301239,  0.12869399,  0.17159199,  0.14585319,
                    0.14585319],
                  [-1.        , -0.94444444, -0.88888889, -0.83333333, -0.77777778,
                   -0.72222222, -0.66666667, -0.61111111, -0.55555556, -0.5       ,
                   -0.44444444, -0.38888889, -0.33333333, -0.27777778, -0.22222222,
                   -0.16666667, -0.11111111, -0.05555556,  0.        ,  0.05555556,
                   0.11111111,  0.16666667,  0.22222222,  0.27777778,  0.33333333,
                   0.38888889,  0.44444444,  0.5       ,  0.55555556,  0.61111111,
                   0.66666667,  0.72222222,  0.77777778,  0.83333333,  0.88888889,
                   0.94444444,  1.        ]]

ang3DHist_bad = [[ 7.19048303,  1.25892934,  0.75463349,  0.52808827,  0.40136778,
                   0.39516106,  0.33878337,  0.36774805,  0.69308353,  0.94704175,
                   0.27775064,  0.21620068,  0.19913221,  0.16396081,  0.17999483,
                   0.1541335 ,  0.14016839,  0.13706503,  0.12516882,  0.13240999,
                   0.12309991,  0.11534151,  0.12465159,  0.1287894 ,  0.1365478 ,
                   0.1443062 ,  0.53532944,  0.32016321,  0.13913393,  0.11689319,
                   0.10396253,  0.10913479,  0.10861757,  0.12361714,  0.14120284,
                   0.92790437],
                 [-1.        , -0.94444444, -0.88888889, -0.83333333, -0.77777778,
                  -0.72222222, -0.66666667, -0.61111111, -0.55555556, -0.5       ,
                  -0.44444444, -0.38888889, -0.33333333, -0.27777778, -0.22222222,
                  -0.16666667, -0.11111111, -0.05555556,  0.        ,  0.05555556,
                  0.11111111,  0.16666667,  0.22222222,  0.27777778,  0.33333333,
                  0.38888889,  0.44444444,  0.5       ,  0.55555556,  0.61111111,
                  0.66666667,  0.72222222,  0.77777778,  0.83333333,  0.88888889,
                  0.94444444,  1.        ]]

npxHist_good = [[ 0.00157091,  0.00553558,  0.00785455,  0.00766753,  0.00617143,
                  0.00519896,  0.00400208,  0.00314182,  0.00235636,  0.00265558,
                  0.00213195,  0.00231896,  0.00179532,  0.00209455,  0.0014961 ,
                  0.00112208,  0.00157091,  0.0014213 ,  0.00089766,  0.00127169,
                  0.00044883,  0.00134649,  0.00078545,  0.00082286,  0.00067325,
                  0.00086026,  0.00067325,  0.00059844,  0.00059844,  0.00067325,
                  0.00014961,  0.00059844,  0.00052364,  0.00041143,  0.00022442,
                  0.00033662],
                [   0.        ,   13.88888889,   27.77777778,   41.66666667,
                    55.55555556,   69.44444444,   83.33333333,   97.22222222,
                    111.11111111,  125.        ,  138.88888889,  152.77777778,
                    166.66666667,  180.55555556,  194.44444444,  208.33333333,
                    222.22222222,  236.11111111,  250.        ,  263.88888889,
                    277.77777778,  291.66666667,  305.55555556,  319.44444444,
                    333.33333333,  347.22222222,  361.11111111,  375.        ,
                    388.88888889,  402.77777778,  416.66666667,  430.55555556,
                    444.44444444,  458.33333333,  472.22222222,  486.11111111,  500.        ]]

npxHist_bad = [[ 0.00344452,  0.00839691,  0.00861851,  0.00620976,  0.00460312,
                 0.00397203,  0.00307838,  0.00292904,  0.00222087,  0.00226664,
                 0.00186197,  0.00185956,  0.00174394,  0.00162591,  0.00144766,
                 0.00128627,  0.0013489 ,  0.00117547,  0.00116102,  0.00111766,
                 0.0010743 ,  0.00095868,  0.00093941,  0.00084306,  0.00093219,
                 0.00085511,  0.00071058,  0.00073949,  0.00064073,  0.0006335 ,
                 0.00060941,  0.00064073,  0.00049861,  0.00047212,  0.0005516 ,
                 0.00053233],
               [   0.        ,   13.88888889,   27.77777778,   41.66666667,
                   55.55555556,   69.44444444,   83.33333333,   97.22222222,
                   111.11111111,  125.        ,  138.88888889,  152.77777778,
                   166.66666667,  180.55555556,  194.44444444,  208.33333333,
                   222.22222222,  236.11111111,  250.        ,  263.88888889,
                   277.77777778,  291.66666667,  305.55555556,  319.44444444,
                   333.33333333,  347.22222222,  361.11111111,  375.        ,
                   388.88888889,  402.77777778,  416.66666667,  430.55555556,
                   444.44444444,  458.33333333,  472.22222222,  486.11111111,  500.        ]]

triHist_good = [[  8.58817922e-03,   5.01048618e-03,   3.73212583e-03,
                   6.17731173e-04,   4.28979981e-05,   8.57959962e-06,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
                   0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
                [    0.        ,    55.55555556,   111.11111111,   166.66666667,
                     222.22222222,   277.77777778,   333.33333333,   388.88888889,
                     444.44444444,   500.        ,   555.55555556,   611.11111111,
                     666.66666667,   722.22222222,   777.77777778,   833.33333333,
                     888.88888889,   944.44444444,  1000.        ,  1055.55555556,
                     1111.11111111,  1166.66666667,  1222.22222222,  1277.77777778,
                     1333.33333333,  1388.88888889,  1444.44444444,  1500.        ,
                     1555.55555556,  1611.11111111,  1666.66666667,  1722.22222222,
                     1777.77777778,  1833.33333333,  1888.88888889,  1944.44444444,
                     2000.        ]]

triHist_bad = [[ 0.00171746,  0.00139666,  0.00108474,  0.00092688,  0.00081403,
                 0.00069041,  0.0006809 ,  0.00063018,  0.00062003,  0.00055156,
                 0.00054776,  0.00051669,  0.00050021,  0.00049387,  0.00044505,
                 0.00045076,  0.00043364,  0.00042921,  0.0003937 ,  0.0003956 ,
                 0.000362  ,  0.00034615,  0.00033157,  0.00031255,  0.0002967 ,
                 0.00029861,  0.00026691,  0.00028149,  0.00026057,  0.00022823,
                 0.00024915,  0.00022443,  0.00022253,  0.00020034,  0.00020921,
                 0.00019019],
               [    0.        ,    55.55555556,   111.11111111,   166.66666667,
                    222.22222222,   277.77777778,   333.33333333,   388.88888889,
                    444.44444444,   500.        ,   555.55555556,   611.11111111,
                    666.66666667,   722.22222222,   777.77777778,   833.33333333,
                    888.88888889,   944.44444444,  1000.        ,  1055.55555556,
                    1111.11111111,  1166.66666667,  1222.22222222,  1277.77777778,
                    1333.33333333,  1388.88888889,  1444.44444444,  1500.        ,
                    1555.55555556,  1611.11111111,  1666.66666667,  1722.22222222,
                    1777.77777778,  1833.33333333,  1888.88888889,  1944.44444444,
                    2000.        ]]

phi1Hist_good = [[ 0.34426649,  0.36612468,  0.27869192,  0.30601465,  0.38251832,
                   0.45902198,  0.40984106,  0.30601465,  0.30055011,  0.33333739,
                   0.34973103,  0.28962101,  0.16393642,  0.26776282,  0.25683373,
                   0.22951099,  0.30055011,  0.27869192,  0.26776282,  0.33333739,
                   0.23497554,  0.22404644,  0.3114792 ,  0.22404644,  0.3114792 ,
                   0.33333739,  0.33880194,  0.35519558,  0.30601465,  0.30601465,
                   0.38798287,  0.33333739,  0.40984106,  0.37158922,  0.3224083 ,
                   0.46448653],
                 [ 0.        ,  0.08726646,  0.17453293,  0.26179939,  0.34906585,
                   0.43633231,  0.52359878,  0.61086524,  0.6981317 ,  0.78539816,
                   0.87266463,  0.95993109,  1.04719755,  1.13446401,  1.22173048,
                   1.30899694,  1.3962634 ,  1.48352986,  1.57079633,  1.65806279,
                   1.74532925,  1.83259571,  1.91986218,  2.00712864,  2.0943951 ,
                   2.18166156,  2.26892803,  2.35619449,  2.44346095,  2.53072742,
                   2.61799388,  2.70526034,  2.7925268 ,  2.87979327,  2.96705973,
                   3.05432619,  3.14159265]]

phi1Hist_bad = [[ 0.15278436,  0.16496759,  0.15739423,  0.14685738,  0.1620041 ,
                  0.16463831,  0.17122385,  0.20546862,  0.20217585,  0.25090879,
                  0.24959168,  0.28251935,  0.31577629,  0.31775195,  0.36220429,
                  0.40369314,  0.47251196,  1.41029179,  1.52356295,  0.49490277,
                  0.40270532,  0.36319212,  0.36088718,  0.30820292,  0.31017858,
                  0.25057951,  0.25749432,  0.22621304,  0.21501764,  0.20810283,
                  0.17155312,  0.16233338,  0.15969916,  0.15673567,  0.15410146,
                  0.1409304 ],
                [ 0.        ,  0.08726646,  0.17453293,  0.26179939,  0.34906585,
                  0.43633231,  0.52359878,  0.61086524,  0.6981317 ,  0.78539816,
                  0.87266463,  0.95993109,  1.04719755,  1.13446401,  1.22173048,
                  1.30899694,  1.3962634 ,  1.48352986,  1.57079633,  1.65806279,
                  1.74532925,  1.83259571,  1.91986218,  2.00712864,  2.0943951 ,
                  2.18166156,  2.26892803,  2.35619449,  2.44346095,  2.53072742,
                  2.61799388,  2.70526034,  2.7925268 ,  2.87979327,  2.96705973,
                  3.05432619,  3.14159265]]

pcadiffHist_good = [[  9.09437560e-01,   8.38894185e-02,   6.19637750e-03,4.76644423e-04],[ 0.,  1.,  2.,  3.,  4.]]

pcadiffHist_bad  = [[ 0.30794426,  0.40407987,  0.26122684,  0.02674903],[ 0.,  1.,  2.,  3.,  4.]]

etaEndHist_good  = [[ 0.24045802,  1.32251908,  2.28435115,  2.90267176,  3.28053435,
                      2.97137405,  3.14312977,  2.83396947,  2.4389313 ,  1.95801527,
                      1.92366412,  1.73473282,  1.47709924,  1.51145038,  1.1851145 ,
                      1.04770992,  0.80725191,  0.61832061,  0.56679389,  0.42938931,
                      0.13740458,  0.1889313 ,  0.1889313 ,  0.13740458,  0.24045802,
                      0.15458015,  0.06870229,  0.05152672,  0.01717557,  0.03435115,
                      0.01717557,  0.01717557,  0.05152672,  0.01717557,  0.        ,  0.        ],
                    [ 0.        ,  0.02777778,  0.05555556,  0.08333333,  0.11111111,
                      0.13888889,  0.16666667,  0.19444444,  0.22222222,  0.25      ,
                      0.27777778,  0.30555556,  0.33333333,  0.36111111,  0.38888889,
                      0.41666667,  0.44444444,  0.47222222,  0.5       ,  0.52777778,
                      0.55555556,  0.58333333,  0.61111111,  0.63888889,  0.66666667,
                      0.69444444,  0.72222222,  0.75      ,  0.77777778,  0.80555556,
                      0.83333333,  0.86111111,  0.88888889,  0.91666667,  0.94444444,
                      0.97222222,  1.        ]]

etaEndHist_bad   = [[ 0.45707376,  1.79720159,  2.76731733,  3.03990326,  2.9486958 ,
                      2.90205562,  2.66056314,  2.48333045,  2.16617723,  2.00863707,
                      1.84902401,  1.69873899,  1.48523061,  1.25099326,  1.11107272,
                      0.92243911,  0.74416998,  0.67576438,  0.52133356,  0.4664018 ,
                      0.39488685,  0.31715322,  0.24563828,  0.22076352,  0.17619623,
                      0.15132147,  0.10779064,  0.09431681,  0.07047849,  0.0642598 ,
                      0.05700466,  0.04664018,  0.03109345,  0.0321299 ,  0.01554673,
                      0.01865607],
                    [ 0.        ,  0.02777778,  0.05555556,  0.08333333,  0.11111111,
                      0.13888889,  0.16666667,  0.19444444,  0.22222222,  0.25      ,
                      0.27777778,  0.30555556,  0.33333333,  0.36111111,  0.38888889,
                      0.41666667,  0.44444444,  0.47222222,  0.5       ,  0.52777778,
                      0.55555556,  0.58333333,  0.61111111,  0.63888889,  0.66666667,
                      0.69444444,  0.72222222,  0.75      ,  0.77777778,  0.80555556,
                      0.83333333,  0.86111111,  0.88888889,  0.91666667,  0.94444444,
                      0.97222222,  1.        ]]
    
lindiffHist_good = [[ 0.05199807,  0.12566201,  0.70630717,  3.47520462,  2.20125181,
                      0.81463649,  0.38565238,  0.31632162,  0.19499278,  0.10399615,
                      0.13432836,  0.08233028,  0.05633125,  0.04333173,  0.05633125,
                      0.04333173,  0.03033221,  0.00433317,  0.02599904,  0.01299952,
                      0.01299952,  0.01299952,  0.02599904,  0.00866635,  0.01299952,
                      0.00866635,  0.00866635,  0.00433317,  0.00433317,  0.00433317,
                      0.00433317,  0.00433317,  0.00433317,  0.00433317,  0.00433317,
                      0.00866635],
                    [ 0.        ,  0.11111111,  0.22222222,  0.33333333,  0.44444444,
                      0.55555556,  0.66666667,  0.77777778,  0.88888889,  1.        ,
                      1.11111111,  1.22222222,  1.33333333,  1.44444444,  1.55555556,
                      1.66666667,  1.77777778,  1.88888889,  2.        ,  2.11111111,
                      2.22222222,  2.33333333,  2.44444444,  2.55555556,  2.66666667,
                      2.77777778,  2.88888889,  3.        ,  3.11111111,  3.22222222,
                      3.33333333,  3.44444444,  3.55555556,  3.66666667,  3.77777778,
                      3.88888889,  4.        ]]

lindiffHist_bad = [[ 0.09049409,  0.1527927 ,  0.5405478 ,  3.16541353,  1.933942  ,
                     0.81659506,  0.53625134,  0.35150376,  0.26799141,  0.18286788,
                     0.15601504,  0.1066058 ,  0.08700322,  0.08029001,  0.07089151,
                     0.05531686,  0.04591837,  0.03947368,  0.03893663,  0.03410311,
                     0.0255102 ,  0.02685285,  0.01852846,  0.01933405,  0.01315789,
                     0.01557465,  0.02228786,  0.01611171,  0.01235231,  0.01047261,
                     0.01315789,  0.01584318,  0.00832438,  0.00912997,  0.01074114,
                     0.00966702],
                   [ 0.        ,  0.11111111,  0.22222222,  0.33333333,  0.44444444,
                     0.55555556,  0.66666667,  0.77777778,  0.88888889,  1.        ,
                     1.11111111,  1.22222222,  1.33333333,  1.44444444,  1.55555556,
                     1.66666667,  1.77777778,  1.88888889,  2.        ,  2.11111111,
                     2.22222222,  2.33333333,  2.44444444,  2.55555556,  2.66666667,
                     2.77777778,  2.88888889,  3.        ,  3.11111111,  3.22222222,
                     3.33333333,  3.44444444,  3.55555556,  3.66666667,  3.77777778,
                     3.88888889,  4.        ]]

# -------------------------------------- End Distributions from MC ----------------------------------------- #

def getPi(q0,q1,dqds0,dqds1,theta0,theta1,phi0,phi1,twomu=False):

    a = 1/50.
    if not twomu:
        pmass  = 938.3
        mumass = 105.7 
    else:
        pmass  = 105.7
        mumass = 105.7

    dqds = []
    for plane in range(3):
        if dqds0[plane]>0 and dqds1[plane] > 0:
            dqds.append(dqds0[plane]-dqds1[plane])
            
    if   len(dqds) > 0 and mean(dqds) < 0:
        p0 = sqrt(a**2*q0**2+2*a*q0*mumass)
        p1 = sqrt(a**2*q1**2+2*a*q1*pmass)
    elif len(dqds) > 0 and mean(dqds) >0:
        p0 = sqrt(a**2*q0**2+2*a*q0*pmass)
        p1 = sqrt(a**2*q1**2+2*a*q1*mumass)
    else:
        p0 = sqrt(a**2*q0**2+2*a*q0*mumass)
        p1 = sqrt(a**2*q1**2+2*a*q1*mumass)
        
    pz = p0*cos(theta0)+p1*cos(theta1)
    py = p0*sin(theta0)*sin(phi0)+p1*sin(theta1)*sin(phi1)
    px = p0*sin(theta0)*cos(phi0)+p1*sin(theta1)*cos(phi1)

    if isnan(px):
        px = -100.
    if isnan(py):
        py = -100.
    if isnan(pz):
        pz = -100.
    
    return px,py,pz

def getDqDsRatio(dqds_v0,dqds_v1):

    dqds_ratios = []
    for plane in range(3):
        if dqds_v0[plane]>0 and dqds_v1[plane] > 0:
            numer = abs(dqds_v0[plane]-dqds_v1[plane])
            den   =     dqds_v0[plane]+dqds_v1[plane]
            dqds_ratios.append(numer/den)

    return dqds_ratios

def get3DAngle(theta0,theta1,phi0,phi1):

    opening3D = cos(theta0)*cos(theta1)+sin(theta0)*sin(theta1)*cos(phi1-phi0)

    if isnan(opening3D):
        return -1.
    else:
        return opening3D

def getNPixShort(npx0,npx1,len3_0,len3_1):

    if len3_0 < len3_1:
        return npx0
    else:
        return npx1
    
def nearLookup(a,b,val):

    histoStep = b[1]-b[0]

    index = len(a)-1
    for x,y in enumerate(b[:-1]):
        if val >= y and (val - y) <= histoStep:
            index = x
            break
        
    return max([a[index]*histoStep,0.00001])

def GetOptimalCut(LLList,guess=0):

    varyRange = 256
    rejThresh = .999
    tryList = [(guess+x)*0.0625 for x in range(-1*varyRange,varyRange)]

    for x in tryList:

        rejection = (sum(1. for y in LLList if y < x)+7976)/(len(LLList)+7976)
        
        if rejection > rejThresh:
            return guess+x

    return guess+varyRange

def GetTriangleArea(track_x,track_y,track_z,x,y,z):

    leg1 = sqrt((track_x[0] - x)**2 + (track_y[0] - y)**2 + (track_z[0] - z)**2)
    leg2 = sqrt((track_x[1] - x)**2 + (track_y[1] - y)**2 + (track_z[1] - z)**2)
    leg3 = sqrt((track_x[0] - track_x[1])**2 + (track_y[0] - track_y[1])**2 + (track_z[0] - track_z[1])**2)

    s = 0.5*(leg1 + leg2 + leg3)

    return sqrt(s*(s-leg1)*(s-leg2)*(s-leg3))
    
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------------------- #

#Can handle more than one input ana file if needed, just add to list
inputFiles = [argv[1]+"/"+x for x in listdir(argv[1])]

vtxChain   = TChain("VertexTree")
LEEChain   = TChain("LEE1e1pTree")
angleChain = TChain("AngleAnalysis")
shapeChain = TChain("ShapeAnalysis")
gapChain   = TChain("GapAnalysis")
dqdsChain  = TChain("dQdSAnalysis")
matchChain = TChain("MatchAnalysis")
eventChain = TChain("EventVertexTree")

for infile in inputFiles:
    
    vtxChain.Add(infile)
    LEEChain.Add(infile)
    angleChain.Add(infile)
    shapeChain.Add(infile)
    gapChain.Add(infile)
    dqdsChain.Add(infile)
    matchChain.Add(infile)
    eventChain.Add(infile)
   
vtxChain.AddFriend(LEEChain)
vtxChain.AddFriend(angleChain)
vtxChain.AddFriend(shapeChain)
vtxChain.AddFriend(gapChain)
vtxChain.AddFriend(dqdsChain)
vtxChain.AddFriend(matchChain)

# ------------------------------------------------------------------------------------------------------------------------------------------------- #
FidVolumeCut    = True
TwoParticleCut  = True
GapCut          = True
TwoTrackCut     = True
SkipManyVertCut = True

tooManyVerts = 100
binning      = 36
optCut       = 6

pz_good = []
px_good = []
py_good = []
p_good  = []
anglemin_good   = []
angle3D_good    = []
npx_good        = []
eta_good        = []
phi1_good       = []
triarea_good    = []
pcadiff_good    = []
etaEnd_good     = []
lindiff_good    = []

vtxidList_good  = []
idList_good     = []

skipList    = []
for evt in eventChain:
    if evt.num_vertex > tooManyVerts:
        skipList.append(tuple((evt.run,evt.subrun,evt.event,evt.entry)))
                       
countGood  = 0
countGood1 = 0
countGood2 = 0
countGood3 = 0
countGood4 = 0
countGood5 = 0
for evt in vtxChain:
    # ----- Looping over the good evts ----- #
    # -------- Make Some Actual Cuts ------- #
    countGood+=1
    
    if FidVolumeCut    and evt.infiducial == 0:
        continue
    countGood1+=1
    if TwoParticleCut  and evt.npar != 2:
        continue
    countGood2+=1
    if GapCut          and (evt.pathexists1+evt.pathexists2)<2:
        continue
    countGood3+=1
    if SkipManyVertCut and tuple((evt.run,evt.subrun,evt.event,evt.entry)) in skipList:
        continue
    countGood4+=1
    if TwoTrackCut     and ((evt.par1_type +evt.par2_type) != 2 or (evt.par_trunk_pca_valid_v[0]+evt.par_trunk_pca_valid_v[1]) !=2):
        continue
    countGood5+=1
    # -------------------------------------- #

    dqds_ratios      = getDqDsRatio(evt.dqdx_0_v_3dc,evt.dqdx_1_v_3dc)
    dqds_end_ratios0 = getDqDsRatio(evt.dqdx_0_end_v_3dc,evt.dqdx_0_v_3dc)
    dqds_end_ratios1 = getDqDsRatio(evt.dqdx_1_end_v_3dc,evt.dqdx_1_v_3dc)
    dosMu = False
    if len(dqds_ratios) != 0:
        eta_good.append(mean(dqds_ratios))
        if max(dqds_ratios) < 0.1: dosMu = True
    else:
        eta_good.append(0.0)
        
    if len(dqds_end_ratios0) != 0 and len(dqds_end_ratios1) !=0:
        etaEnd_good.append(mean(dqds_end_ratios0)+mean(dqds_end_ratios1))
    elif len(dqds_end_ratios0) !=0 and len(dqds_end_ratios1) == 0:
        etaEnd_good.append(mean(dqds_end_ratios0))
    elif len(dqds_end_ratios0) == 0 and len(dqds_end_ratios1) != 0:
        etaEnd_good.append(mean(dqds_end_ratios1))
    else:
        etaEnd_good.append(0)
        
    Px,Py,Pz = getPi(evt.q0,evt.q1,evt.dqdx_0_v_3dc,evt.dqdx_1_v_3dc,min([pi,evt.theta_0]),min([pi,evt.theta_1]),min([pi,evt.phi_0]),min([pi,evt.phi_1]),dosMu)
    px_good.append(Px)
    py_good.append(Py)
    pz_good.append(Pz)
    p_good.append(sqrt(Px**2+Py**2+Pz**2))
    
    anglemin_good.append(evt.anglediff)

    angle3D_good.append(get3DAngle(min([evt.theta_0,pi]),min([evt.theta_1,pi]),min([evt.phi_0,pi]),min([evt.phi_1,pi])))

    npx_good.append(getNPixShort(evt.npx0,evt.npx1,evt.par_trunk_pca_end_len_v[0],evt.par_trunk_pca_end_len_v[1]))
    
    phi1_good.append(abs(evt.phi_0))
#    phi1_good.append(abs(evt.phi_1))

    triarea_good.append(GetTriangleArea(evt.par_trunk_pca_end_x_v,evt.par_trunk_pca_end_y_v,evt.par_trunk_pca_end_z_v,evt.scex,evt.scey,evt.scez))

    pcadiff_good.append(evt.straightness)

    if evt.len0 > evt.len1:
        lindiff_good.append(evt.sigma_pixel_dist_min_v[0])
    else:
        lindiff_good.append(evt.sigma_pixel_dist_min_v[1])
    
    vtxidList_good.append(tuple((evt.run,evt.subrun,evt.event,evt.entry,evt.vtxid)))
    idList_good.append(tuple((evt.run,evt.subrun,evt.event,evt.entry)))

    
goodLL = []
for i in range(len(eta_good)):

    dqdsTerm    = log( nearLookup(dqdsHist_good[0],dqdsHist_good[1],eta_good[i])            /  nearLookup(dqdsHist_bad[0],dqdsHist_bad[1],eta_good[i])            )
    pzTerm      = log( nearLookup(pzHist_good[0],pzHist_good[1],pz_good[i])                 /  nearLookup(pzHist_bad[0],pzHist_bad[1],pz_good[i])                 )
    angleTerm   = log( nearLookup(angminHist_good[0],angminHist_good[1],anglemin_good[i])   /  nearLookup(angminHist_bad[0],angminHist_bad[1],anglemin_good[i])   )
    angle3Term  = log( nearLookup(ang3DHist_good[0],ang3DHist_good[1],angle3D_good[i])      /  nearLookup(ang3DHist_bad[0],ang3DHist_bad[1],angle3D_good[i])      )
    npxTerm     = log( nearLookup(npxHist_good[0],npxHist_good[1],npx_good[i])              /  nearLookup(npxHist_bad[0],npxHist_bad[1],npx_good[i])              )
    triTerm     = log( nearLookup(triHist_good[0],triHist_good[1],triarea_good[i])          /  nearLookup(triHist_bad[0],triHist_bad[1],triarea_good[i])          )
    phi1Term    = log( nearLookup(phi1Hist_good[0],phi1Hist_good[1],phi1_good[i])           /  nearLookup(phi1Hist_bad[0],phi1Hist_bad[1],phi1_good[i])           )
    pcaTerm     = log( nearLookup(pcadiffHist_good[0],pcadiffHist_good[1],pcadiff_good[i])  /  nearLookup(pcadiffHist_bad[0],pcadiffHist_bad[1],pcadiff_good[i])  )
    etaEndTerm  = log( nearLookup(etaEndHist_good[0],etaEndHist_good[1],etaEnd_good[i])     /  nearLookup(etaEndHist_bad[0],etaEndHist_bad[1],etaEnd_good[i])     )
    lindiffTerm = log( nearLookup(lindiffHist_good[0],lindiffHist_good[1],lindiff_good[i])  /  nearLookup(lindiffHist_bad[0],lindiffHist_bad[1],lindiff_good[i])  )

    goodLL.append(dqdsTerm+triTerm+phi1Term+angleTerm+angle3Term+npxTerm+pzTerm+pcaTerm+etaEndTerm+lindiffTerm)


    
gNumV = sum(1 for x in goodLL if x > optCut)
good_vtxed = len(set(idList_good))

passingEvents = []
for i in range(len(goodLL)):

    if goodLL[i] > optCut:
        passingEvents.append(idList_good[i])
        
gNum  = len(set(passingEvents))

eventDict = {}
for i in range(len(idList_good)):

        ID = idList_good[i]

        if ID not in eventDict:
            eventDict[ID] = goodLL[i]

        if ID in eventDict and goodLL[i] > eventDict[ID]:
            eventDict[ID] = goodLL[i]

countSelGood = 0
selectedDict = {}
for x in eventDict:

    if eventDict[x] > optCut:
        selectedDict[x] = eventDict[x]
        countSelGood+=1

print "Vertices Produced   " , countGood
print "Vertices Fid Vol    " , countGood1
print "Vertices 2 Part     " , countGood2
print "Vertices Gap        " , countGood3
print "Vertices Messy      " , countGood4
print "Vertices 2 Track    " , countGood5, "(%i)"%good_vtxed
print "Vertices: LL        " , gNumV, "(%i)"%gNum
print "Post Best Selection " , countSelGood
print ""
print "To summarize..."
print "Grand total of ", eventChain.GetEntries()," entries with 1+ ROI (not necessarily good ROI) were fed in"
print "a total of     ", countSelGood," were selected"
