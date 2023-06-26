import streamlit as st
import pandas as pd
import requests
from env_canada import ECHistorical
import asyncio
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def compose_date(years, months=1, days=1, weeks=None, hours=None, minutes=None,
                 seconds=None, milliseconds=None, microseconds=None, nanoseconds=None):
    years = np.asarray(years) - 1970
    months = np.asarray(months) - 1
    days = np.asarray(days) - 1
    types = ('<M8[Y]', '<m8[M]', '<m8[D]', '<m8[W]', '<m8[h]',
             '<m8[m]', '<m8[s]', '<m8[ms]', '<m8[us]', '<m8[ns]')
    vals = (years, months, days, weeks, hours, minutes, seconds,
            milliseconds, microseconds, nanoseconds)
    return sum(np.asarray(v, dtype=t) for t, v in zip(types, vals)
               if v is not None)


@st.cache_data
def get_historical_level_data():
    historical_water_data_array = [
        [0, 8.221, 8.315714285714288, 8.461],
        [1, 8.217, 8.310999999999998, 8.457],
        [2, 8.211, 8.308142857142858, 8.452],
        [3, 8.206, 8.305, 8.456],
        [4, 8.2, 8.299857142857144, 8.452],
        [5, 8.2, 8.294714285714287, 8.446],
        [6, 8.199, 8.290142857142856, 8.443],
        [7, 8.2, 8.289, 8.437],
        [8, 8.194, 8.286428571428571, 8.435],
        [9, 8.19, 8.285142857142857, 8.429],
        [10, 8.19, 8.289714285714286, 8.424],
        [11, 8.187, 8.298285714285715, 8.42],
        [12, 8.185, 8.295571428571428, 8.411],
        [13, 8.182, 8.291714285714287, 8.402],
        [14, 8.177, 8.287857142857144, 8.395],
        [15, 8.175, 8.287142857142856, 8.39],
        [16, 8.177, 8.284428571428572, 8.382],
        [17, 8.173, 8.281000000000002, 8.377],
        [18, 8.169, 8.278428571428572, 8.372],
        [19, 8.164, 8.273428571428571, 8.364],
        [20, 8.164, 8.268714285714285, 8.359],
        [21, 8.16, 8.264857142857142, 8.357],
        [22, 8.156, 8.264285714285714, 8.355],
        [23, 8.151, 8.262, 8.356],
        [24, 8.147, 8.259285714285713, 8.352],
        [25, 8.144, 8.25514285714286, 8.349],
        [26, 8.142, 8.251714285714286, 8.346],
        [27, 8.137, 8.239833333333333, 8.345],
        [28, 8.132, 8.246, 8.344],
        [29, 8.128, 8.241142857142856, 8.339],
        [30, 8.124, 8.237142857142857, 8.335],
        [31, 8.12, 8.235285714285714, 8.332],
        [32, 8.115, 8.23157142857143, 8.329],
        [33, 8.11, 8.230714285714285, 8.324],
        [34, 8.106, 8.229857142857144, 8.325],
        [35, 8.108, 8.229714285714286, 8.322],
        [36, 8.114, 8.228571428571428, 8.322],
        [37, 8.114, 8.226428571428572, 8.323],
        [38, 8.114, 8.226428571428572, 8.326],
        [39, 8.109, 8.223142857142857, 8.322],
        [40, 8.106, 8.218285714285715, 8.32],
        [41, 8.103, 8.215857142857143, 8.323],
        [42, 8.099, 8.214142857142857, 8.322],
        [43, 8.095, 8.212714285714286, 8.322],
        [44, 8.094, 8.209285714285715, 8.32],
        [45, 8.095, 8.207142857142857, 8.319],
        [46, 8.099, 8.204714285714287, 8.314],
        [47, 8.093, 8.197714285714286, 8.291],
        [48, 8.09, 8.191857142857144, 8.272],
        [49, 8.088, 8.189142857142858, 8.274],
        [50, 8.086, 8.191571428571427, 8.289],
        [51, 8.084, 8.195285714285715, 8.325],
        [52, 8.085, 8.194142857142857, 8.335],
        [53, 8.085, 8.194857142857142, 8.342],
        [54, 8.09, 8.199571428571428, 8.348],
        [55, 8.094, 8.214, 8.38],
        [56, 8.09, 8.216571428571429, 8.408],
        [57, 8.094, 8.220428571428572, 8.435],
        [58, 8.095, 8.222285714285714, 8.448],
        [59, 8.095, 8.221285714285715, 8.448],
        [60, 8.093, 8.224142857142857, 8.469],
        [61, 8.091, 8.22557142857143, 8.483],
        [62, 8.089, 8.222428571428571, 8.487],
        [63, 8.09, 8.219, 8.487],
        [64, 8.088, 8.215428571428571, 8.485],
        [65, 8.086, 8.211285714285713, 8.482],
        [66, 8.085, 8.209428571428571, 8.487],
        [67, 8.079, 8.206714285714286, 8.493],
        [68, 8.079, 8.206999999999999, 8.492],
        [69, 8.079, 8.211285714285715, 8.49],
        [70, 8.085, 8.212142857142856, 8.485],
        [71, 8.093, 8.212571428571428, 8.479],
        [72, 8.094, 8.212428571428571, 8.473],
        [73, 8.096, 8.212714285714284, 8.465],
        [74, 8.096, 8.217285714285714, 8.455],
        [75, 8.096, 8.218285714285713, 8.447],
        [76, 8.095, 8.222285714285714, 8.439],
        [77, 8.095, 8.225, 8.432],
        [78, 8.092, 8.224, 8.425],
        [79, 8.091, 8.225857142857143, 8.419],
        [80, 8.091, 8.226428571428572, 8.414],
        [81, 8.092, 8.226571428571429, 8.409],
        [82, 8.089, 8.226, 8.403],
        [83, 8.088, 8.228714285714286, 8.406],
        [84, 8.087, 8.236571428571429, 8.422],
        [85, 8.092, 8.242285714285716, 8.423],
        [86, 8.097, 8.247571428571428, 8.424],
        [87, 8.095, 8.254714285714286, 8.441],
        [88, 8.091, 8.263285714285715, 8.452],
        [89, 8.095, 8.27142857142857, 8.457],
        [90, 8.096, 8.284428571428572, 8.498],
        [91, 8.093, 8.298428571428571, 8.568],
        [92, 8.095, 8.305142857142858, 8.597],
        [93, 8.102, 8.313142857142857, 8.604],
        [94, 8.102, 8.324285714285713, 8.602],
        [95, 8.099, 8.328285714285714, 8.595],
        [96, 8.1, 8.336428571428572, 8.594],
        [97, 8.101, 8.348142857142857, 8.61],
        [98, 8.101, 8.354142857142858, 8.607],
        [99, 8.102, 8.363, 8.598],
        [100, 8.124, 8.373285714285714, 8.589],
        [101, 8.14, 8.384142857142857, 8.612],
        [102, 8.154, 8.392857142857144, 8.633],
        [103, 8.179, 8.401714285714286, 8.644],
        [104, 8.225, 8.411857142857142, 8.646],
        [105, 8.24, 8.425142857142857, 8.652],
        [106, 8.255, 8.439571428571428, 8.685],
        [107, 8.254, 8.451285714285714, 8.713],
        [108, 8.25, 8.464285714285714, 8.719],
        [109, 8.245, 8.482428571428573, 8.718],
        [110, 8.241, 8.498571428571427, 8.719],
        [111, 8.239, 8.52, 8.723],
        [112, 8.241, 8.533714285714286, 8.723],
        [113, 8.248, 8.543000000000001, 8.724],
        [114, 8.259, 8.551285714285715, 8.76],
        [115, 8.289, 8.558285714285715, 8.777],
        [116, 8.328, 8.566714285714285, 8.799],
        [117, 8.369, 8.576285714285715, 8.833],
        [118, 8.41, 8.586, 8.842],
        [119, 8.43, 8.589428571428572, 8.839],
        [120, 8.444, 8.594285714285714, 8.829],
        [121, 8.46, 8.605142857142857, 8.834],
        [122, 8.483, 8.614285714285714, 8.847],
        [123, 8.509, 8.620714285714286, 8.85],
        [124, 8.492, 8.620714285714286, 8.848],
        [125, 8.527, 8.630571428571429, 8.84],
        [126, 8.525, 8.633571428571429, 8.829],
        [127, 8.521, 8.636571428571429, 8.818],
        [128, 8.518, 8.636285714285714, 8.805],
        [129, 8.525, 8.63642857142857, 8.802],
        [130, 8.535, 8.639857142857144, 8.801],
        [131, 8.535, 8.641857142857143, 8.794],
        [132, 8.54, 8.642285714285714, 8.782],
        [133, 8.549, 8.641571428571428, 8.774],
        [134, 8.575, 8.641285714285713, 8.765],
        [135, 8.574, 8.641857142857143, 8.752],
        [136, 8.571, 8.638999999999998, 8.738],
        [137, 8.568, 8.636571428571429, 8.729],
        [138, 8.567, 8.633571428571429, 8.715],
        [139, 8.564, 8.631714285714285, 8.71],
        [140, 8.562, 8.632, 8.715],
        [141, 8.56, 8.628285714285715, 8.709],
        [142, 8.561, 8.620428571428572, 8.697],
        [143, 8.56, 8.61, 8.693],
        [144, 8.554, 8.609142857142858, 8.692],
        [145, 8.554, 8.616428571428573, 8.684],
        [146, 8.556, 8.621714285714285, 8.681],
        [147, 8.557, 8.61957142857143, 8.672],
        [148, 8.551, 8.614428571428572, 8.663],
        [149, 8.542, 8.610285714285714, 8.654],
        [150, 8.535, 8.60342857142857, 8.641],
        [151, 8.531, 8.597142857142858, 8.63],
        [152, 8.529, 8.592857142857143, 8.628],
        [153, 8.529, 8.589142857142857, 8.626],
        [154, 8.528, 8.582857142857142, 8.629],
        [155, 8.527, 8.579857142857144, 8.63],
        [156, 8.527, 8.581285714285714, 8.627],
        [157, 8.529, 8.579142857142857, 8.625],
        [158, 8.529, 8.575142857142856, 8.621],
        [159, 8.53, 8.574142857142858, 8.615],
        [160, 8.522, 8.572714285714286, 8.612],
        [161, 8.525, 8.570142857142857, 8.61],
        [162, 8.526, 8.571857142857143, 8.614],
        [163, 8.522, 8.571714285714286, 8.603],
        [164, 8.519, 8.573142857142857, 8.593],
        [165, 8.522, 8.572428571428572, 8.599],
        [166, 8.526, 8.57342857142857, 8.606],
        [167, 8.515, 8.574571428571428, 8.61],
        [168, 8.506, 8.57042857142857, 8.602],
        [169, 8.506, 8.571142857142858, 8.595],
        [170, 8.51, 8.573285714285714, 8.604],
        [171, 8.508, 8.571428571428571, 8.608],
        [172, 8.505, 8.56914285714286, 8.611],
        [173, 8.505, 8.565142857142858, 8.608],
        [174, 8.498, 8.563428571428572, 8.612],
        [175, 8.495, 8.557142857142855, 8.581],
        [176, 8.501, 8.55742857142857, 8.584],
        [177, 8.516, 8.559142857142858, 8.595],
        [178, 8.54, 8.564571428571428, 8.611],
        [179, 8.537, 8.566571428571429, 8.618],
        [180, 8.535, 8.567857142857143, 8.639],
        [181, 8.543, 8.570142857142857, 8.649],
        [182, 8.547, 8.575571428571427, 8.66],
        [183, 8.55, 8.574857142857143, 8.665],
        [184, 8.547, 8.572142857142858, 8.667],
        [185, 8.544, 8.567428571428573, 8.659],
        [186, 8.54, 8.563, 8.646],
        [187, 8.539, 8.562999999999999, 8.634],
        [188, 8.526, 8.559285714285714, 8.626],
        [189, 8.517, 8.558571428571428, 8.613],
        [190, 8.512, 8.561714285714286, 8.611],
        [191, 8.511, 8.557714285714285, 8.617],
        [192, 8.504, 8.545285714285715, 8.603],
        [193, 8.499, 8.532428571428571, 8.599],
        [194, 8.49, 8.521714285714285, 8.584],
        [195, 8.501, 8.522714285714285, 8.577],
        [196, 8.494, 8.52142857142857, 8.578],
        [197, 8.491, 8.518428571428572, 8.581],
        [198, 8.493, 8.518142857142857, 8.572],
        [199, 8.487, 8.519285714285715, 8.563],
        [200, 8.485, 8.520714285714286, 8.564],
        [201, 8.483, 8.521142857142857, 8.578],
        [202, 8.481, 8.519142857142857, 8.579],
        [203, 8.476, 8.517, 8.574],
        [204, 8.469, 8.514142857142858, 8.572],
        [205, 8.461, 8.519857142857143, 8.592],
        [206, 8.456, 8.528142857142857, 8.631],
        [207, 8.45, 8.526, 8.636],
        [208, 8.45, 8.523714285714286, 8.62],
        [209, 8.466, 8.520285714285714, 8.594],
        [210, 8.463, 8.514999999999999, 8.588],
        [211, 8.459, 8.509571428571428, 8.578],
        [212, 8.453, 8.504714285714286, 8.566],
        [213, 8.448, 8.504285714285714, 8.561],
        [214, 8.445, 8.503142857142858, 8.548],
        [215, 8.447, 8.507000000000001, 8.572],
        [216, 8.442, 8.507714285714286, 8.573],
        [217, 8.435, 8.507857142857144, 8.575],
        [218, 8.435, 8.507142857142858, 8.575],
        [219, 8.435, 8.506857142857143, 8.574],
        [220, 8.438, 8.50557142857143, 8.573],
        [221, 8.434, 8.506571428571428, 8.575],
        [222, 8.43, 8.509285714285715, 8.599],
        [223, 8.429, 8.510285714285713, 8.593],
        [224, 8.425, 8.511714285714286, 8.606],
        [225, 8.417, 8.508714285714285, 8.601],
        [226, 8.424, 8.507428571428571, 8.589],
        [227, 8.418, 8.504142857142858, 8.578],
        [228, 8.414, 8.501000000000001, 8.567],
        [229, 8.413, 8.505714285714285, 8.56],
        [230, 8.413, 8.509285714285715, 8.562],
        [231, 8.407, 8.506142857142859, 8.571],
        [232, 8.404, 8.503142857142857, 8.574],
        [233, 8.401, 8.506428571428572, 8.565],
        [234, 8.398, 8.521428571428572, 8.643],
        [235, 8.392, 8.523285714285713, 8.696],
        [236, 8.385, 8.52, 8.699],
        [237, 8.382, 8.512857142857143, 8.689],
        [238, 8.377, 8.504571428571428, 8.679],
        [239, 8.375, 8.501571428571427, 8.668],
        [240, 8.377, 8.49757142857143, 8.656],
        [241, 8.373, 8.497571428571428, 8.644],
        [242, 8.374, 8.495571428571429, 8.632],
        [243, 8.371, 8.49457142857143, 8.624],
        [244, 8.367, 8.492285714285716, 8.608],
        [245, 8.364, 8.493428571428572, 8.594],
        [246, 8.364, 8.494142857142858, 8.591],
        [247, 8.388, 8.493714285714285, 8.602],
        [248, 8.387, 8.491285714285715, 8.625],
        [249, 8.388, 8.489714285714285, 8.625],
        [250, 8.39, 8.492571428571429, 8.624],
        [251, 8.391, 8.501285714285713, 8.619],
        [252, 8.387, 8.499571428571429, 8.609],
        [253, 8.385, 8.495857142857144, 8.599],
        [254, 8.389, 8.491714285714286, 8.588],
        [255, 8.384, 8.485714285714286, 8.578],
        [256, 8.374, 8.483142857142857, 8.569],
        [257, 8.367, 8.484571428571428, 8.56],
        [258, 8.365, 8.482428571428573, 8.551],
        [259, 8.363, 8.477428571428572, 8.541],
        [260, 8.36, 8.476285714285716, 8.553],
        [261, 8.361, 8.478142857142858, 8.587],
        [262, 8.366, 8.474428571428572, 8.59],
        [263, 8.365, 8.471428571428572, 8.58],
        [264, 8.362, 8.468285714285715, 8.569],
        [265, 8.358, 8.476714285714285, 8.569],
        [266, 8.356, 8.489142857142856, 8.601],
        [267, 8.355, 8.486714285714287, 8.617],
        [268, 8.35, 8.486, 8.636],
        [269, 8.344, 8.490142857142859, 8.665],
        [270, 8.339, 8.488285714285714, 8.673],
        [271, 8.336, 8.486428571428572, 8.67],
        [272, 8.352, 8.488857142857142, 8.663],
        [273, 8.354, 8.484571428571428, 8.654],
        [274, 8.345, 8.474857142857143, 8.638],
        [275, 8.339, 8.468285714285713, 8.639],
        [276, 8.327, 8.464857142857143, 8.675],
        [277, 8.318, 8.463142857142858, 8.675],
        [278, 8.319, 8.458142857142859, 8.668],
        [279, 8.317, 8.45, 8.659],
        [280, 8.317, 8.446, 8.648],
        [281, 8.315, 8.443571428571428, 8.637],
        [282, 8.327, 8.44142857142857, 8.629],
        [283, 8.323, 8.438714285714287, 8.63],
        [284, 8.321, 8.434857142857142, 8.632],
        [285, 8.321, 8.42657142857143, 8.629],
        [286, 8.322, 8.424142857142858, 8.644],
        [287, 8.323, 8.420142857142856, 8.644],
        [288, 8.327, 8.420285714285715, 8.641],
        [289, 8.331, 8.427285714285714, 8.654],
        [290, 8.332, 8.426857142857143, 8.654],
        [291, 8.33, 8.423285714285715, 8.65],
        [292, 8.323, 8.418999999999999, 8.641],
        [293, 8.326, 8.416142857142857, 8.633],
        [294, 8.325, 8.414428571428571, 8.639],
        [295, 8.328, 8.414142857142858, 8.648],
        [296, 8.328, 8.41157142857143, 8.643],
        [297, 8.326, 8.411857142857142, 8.638],
        [298, 8.323, 8.409857142857144, 8.637],
        [299, 8.32, 8.405285714285714, 8.626],
        [300, 8.315, 8.403142857142857, 8.616],
        [301, 8.31, 8.401857142857141, 8.605],
        [302, 8.311, 8.401428571428571, 8.594],
        [303, 8.308, 8.396142857142857, 8.583],
        [304, 8.302, 8.396428571428572, 8.57],
        [305, 8.303, 8.398142857142856, 8.558],
        [306, 8.31, 8.399428571428572, 8.548],
        [307, 8.309, 8.398285714285715, 8.537],
        [308, 8.304, 8.395571428571428, 8.525],
        [309, 8.299, 8.394714285714285, 8.514],
        [310, 8.299, 8.395571428571428, 8.503],
        [311, 8.295, 8.397, 8.493],
        [312, 8.302, 8.395714285714286, 8.485],
        [313, 8.31, 8.39357142857143, 8.477],
        [314, 8.305, 8.391428571428571, 8.467],
        [315, 8.307, 8.390428571428572, 8.459],
        [316, 8.3, 8.386142857142858, 8.452],
        [317, 8.3, 8.382428571428573, 8.451],
        [318, 8.3, 8.376428571428571, 8.448],
        [319, 8.3, 8.37257142857143, 8.441],
        [320, 8.302, 8.376142857142856, 8.434],
        [321, 8.302, 8.372571428571428, 8.427],
        [322, 8.302, 8.368571428571428, 8.425],
        [323, 8.304, 8.368142857142857, 8.43],
        [324, 8.306, 8.363857142857144, 8.426],
        [325, 8.303, 8.358999999999998, 8.421],
        [326, 8.294, 8.35842857142857, 8.418],
        [327, 8.285, 8.35357142857143, 8.413],
        [328, 8.279, 8.350285714285715, 8.411],
        [329, 8.279, 8.348857142857144, 8.415],
        [330, 8.283, 8.349, 8.415],
        [331, 8.293, 8.358571428571429, 8.413],
        [332, 8.29, 8.359714285714286, 8.418],
        [333, 8.286, 8.358714285714287, 8.418],
        [334, 8.281, 8.355857142857143, 8.412],
        [335, 8.276, 8.357571428571429, 8.41],
        [336, 8.284, 8.357571428571427, 8.406],
        [337, 8.294, 8.35657142857143, 8.402],
        [338, 8.288, 8.354000000000001, 8.399],
        [339, 8.286, 8.353, 8.404],
        [340, 8.288, 8.352, 8.41],
        [341, 8.283, 8.348571428571427, 8.413],
        [342, 8.278, 8.345142857142857, 8.417],
        [343, 8.272, 8.343857142857143, 8.422],
        [344, 8.267, 8.342857142857142, 8.423],
        [345, 8.263, 8.341714285714286, 8.419],
        [346, 8.259, 8.344, 8.419],
        [347, 8.253, 8.342857142857142, 8.414],
        [348, 8.247, 8.341142857142856, 8.407],
        [349, 8.243, 8.340857142857143, 8.403],
        [350, 8.237, 8.336857142857143, 8.402],
        [351, 8.23, 8.334428571428571, 8.406],
        [352, 8.224, 8.331428571428571, 8.408],
        [353, 8.218, 8.327714285714286, 8.407],
        [354, 8.213, 8.323857142857142, 8.406],
        [355, 8.229, 8.323857142857143, 8.406],
        [356, 8.232, 8.322428571428572, 8.408],
        [357, 8.231, 8.318714285714288, 8.407],
        [358, 8.232, 8.316142857142859, 8.406],
        [359, 8.229, 8.315428571428571, 8.406],
        [360, 8.225, 8.312714285714287, 8.409],
        [361, 8.221, 8.310857142857143, 8.416],
        [362, 8.232, 8.307142857142859, 8.405],
        [363, 8.227, 8.306428571428572, 8.394],
        [364, 8.224, 8.302714285714286, 8.391],
        [365, 8.224, 8.300714285714287, 8.39],
    ]

    df = pd.DataFrame(historical_water_data_array,
                      columns=['Day', 'Low', 'Average', 'High'])

    todays_date = datetime.today()
    year = int(todays_date.year)
    df['Year'] = year
    df['Day'] = df['Day'].astype(int)
    df['Date'] = compose_date(df['Year'], days=df['Day'])
    df['Date'][0] = df['Date'][1]
    df['Month'] = df['Date'].dt.strftime('%b')

    return df


@st.cache_data
def get_precipitation_data():
    ec = ECHistorical(station_id=54604, year=2023, language="english", format="csv")

    asyncio.run(ec.update())

    df = pd.read_csv(ec.station_data)
    df['Day chart'] = df['Day'] - 1
    df = df.fillna(0)

    return df


@st.cache_data
def get_recent_level_data():
    todays_date = datetime.today()

    year = todays_date.year
    start_string = str(year) + '-01-01 00:00:00'

    time_now_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    download_url = 'https://wateroffice.ec.gc.ca/services/real_time_data/csv/inline?stations[]=02EA020&parameters[]=46&start_date=' + start_string + '&end_date=' + time_now_string

    r = requests.get(download_url)

    ZWNBSP_delimiter = '﻿ '
    csv_after_split = r.text.split(ZWNBSP_delimiter)[1]

    list_of_csv = csv_after_split.split('\r\n')
    headers = list_of_csv[0].split(',')
    list_of_csv.pop(0)
    list_to_pass_to_df = []
    for list_item in list_of_csv:
        list_to_pass_to_df.append(list_item.split(','))
    df = pd.DataFrame(list_to_pass_to_df, columns=headers)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = df['Date'].dt.dayofyear - 1

    df['Level'] = df['Value/Valeur'].astype(float).fillna(0.0)

    return df


# get the required data
df_historical = get_historical_level_data()
df_precip = get_precipitation_data()
df_recent = get_recent_level_data()

# condition the data to prepare for display
df_recent['Date'] = pd.to_datetime(df_recent['Date'])
df_recent['Day'] = df_recent['Date'].dt.dayofyear - 1
df_recent['Level'] = df_recent['Value/Valeur'].astype(float).fillna(0.0)
groups = df_recent.groupby(['Day'])['Level'].mean()
group_list = groups.to_list()
day_list = df_historical['Date'].to_list()[:len(group_list)]

x_list = df_historical['Month'].to_list()[:len(group_list)]
y_list = df_precip['Total Precip (mm)'].to_list()

# create plotly plots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.8, 0.2])

fig.append_trace(go.Line(x=df_historical['Date'], y=df_historical['Low'], name='Low', line_color='Blue'), row=1, col=1)
fig.append_trace(go.Line(x=df_historical['Date'], y=df_historical['Average'], name='Average', line_color='Blue'), row=1, col=1)
fig.append_trace(go.Line(x=df_historical['Date'], y=df_historical['High'], name='High', line_color='Blue'), row=1, col=1)

fig.append_trace(go.Scatter(x=day_list, y=group_list, name='Current', marker=dict(
    color='Red',
    size=4,
)), row=1, col=1)

fig.append_trace(
        go.Line(x=df_historical['Date'], y=df_precip['Total Precip (mm)'].to_list(), name='Precipitation'),
        row=2,
        col=1
    )

# plot via streamlit
st.plotly_chart(fig)
