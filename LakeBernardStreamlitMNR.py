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
        [0, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [1, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [2, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [3, 329.7, 329.3, 329.2, 329.2, 329.2, 329.09, 328.99],
        [4, 329.7, 329.3, 329.2, 329.2, 329.2, 329.09, 328.99],
        [5, 329.7, 329.3, 329.2, 329.2, 329.2, 329.09, 328.99],
        [6, 329.7, 329.3, 329.2, 329.2, 329.2, 329.09, 328.99],
        [7, 329.7, 329.3, 329.2, 329.2, 329.2, 329.09, 328.99],
        [8, 329.7, 329.3, 329.2, 329.2, 329.2, 329.08, 328.98],
        [9, 329.7, 329.3, 329.2, 329.2, 329.2, 329.08, 328.98],
        [10, 329.7, 329.3, 329.2, 329.2, 329.2, 329.08, 328.98],
        [11, 329.7, 329.3, 329.2, 329.2, 329.2, 329.08, 328.98],
        [12, 329.7, 329.3, 329.2, 329.2, 329.2, 329.08, 328.98],
        [13, 329.7, 329.3, 329.2, 329.2, 329.2, 329.07, 328.97],
        [14, 329.7, 329.3, 329.2, 329.2, 329.2, 329.07, 328.97],
        [15, 329.7, 329.3, 329.2, 329.2, 329.2, 329.07, 328.97],
        [16, 329.7, 329.3, 329.2, 329.2, 329.2, 329.07, 328.97],
        [17, 329.7, 329.3, 329.2, 329.2, 329.2, 329.07, 328.97],
        [18, 329.7, 329.3, 329.2, 329.2, 329.2, 329.06, 328.96],
        [19, 329.7, 329.3, 329.2, 329.2, 329.2, 329.06, 328.96],
        [20, 329.7, 329.3, 329.2, 329.2, 329.2, 329.06, 328.96],
        [21, 329.7, 329.3, 329.2, 329.2, 329.2, 329.06, 328.96],
        [22, 329.7, 329.3, 329.2, 329.2, 329.2, 329.06, 328.96],
        [23, 329.7, 329.3, 329.2, 329.2, 329.2, 329.05, 328.95],
        [24, 329.7, 329.3, 329.2, 329.2, 329.2, 329.05, 328.95],
        [25, 329.7, 329.3, 329.2, 329.2, 329.2, 329.05, 328.95],
        [26, 329.7, 329.3, 329.2, 329.2, 329.2, 329.05, 328.95],
        [27, 329.7, 329.3, 329.2, 329.2, 329.2, 329.05, 328.95],
        [28, 329.7, 329.3, 329.2, 329.2, 329.2, 329.04, 328.94],
        [29, 329.7, 329.3, 329.2, 329.2, 329.2, 329.04, 328.94],
        [30, 329.7, 329.3, 329.2, 329.2, 329.2, 329.04, 328.94],
        [31, 329.7, 329.3, 329.2, 329.2, 329.2, 329.04, 328.94],
        [32, 329.7, 329.3, 329.2, 329.2, 329.2, 329.04, 328.94],
        [33, 329.7, 329.3, 329.2, 329.2, 329.2, 329.03, 328.93],
        [34, 329.7, 329.3, 329.2, 329.2, 329.2, 329.03, 328.93],
        [35, 329.7, 329.3, 329.2, 329.2, 329.2, 329.03, 328.93],
        [36, 329.7, 329.3, 329.2, 329.2, 329.2, 329.03, 328.93],
        [37, 329.7, 329.3, 329.2, 329.2, 329.2, 329.02, 328.92],
        [38, 329.7, 329.3, 329.2, 329.2, 329.2, 329.02, 328.92],
        [39, 329.7, 329.3, 329.2, 329.2, 329.2, 329.02, 328.92],
        [40, 329.7, 329.3, 329.2, 329.2, 329.2, 329.02, 328.92],
        [41, 329.7, 329.3, 329.2, 329.2, 329.2, 329.02, 328.92],
        [42, 329.7, 329.3, 329.2, 329.2, 329.2, 329.01, 328.91],
        [43, 329.7, 329.3, 329.2, 329.2, 329.2, 329.01, 328.91],
        [44, 329.7, 329.3, 329.2, 329.2, 329.2, 329.01, 328.91],
        [45, 329.7, 329.3, 329.2, 329.2, 329.2, 329.01, 328.91],
        [46, 329.7, 329.29, 329.19, 329.19, 329.19, 329.01, 328.91],
        [47, 329.7, 329.29, 329.19, 329.19, 329.19, 329.0, 328.9],
        [48, 329.7, 329.28, 329.18, 329.18, 329.18, 329.0, 328.9],
        [49, 329.7, 329.28, 329.18, 329.18, 329.18, 329.0, 328.9],
        [50, 329.7, 329.27, 329.17, 329.17, 329.17, 329.0, 328.9],
        [51, 329.7, 329.27, 329.17, 329.17, 329.17, 329.0, 328.9],
        [52, 329.7, 329.26, 329.16, 329.16, 329.16, 328.99, 328.89],
        [53, 329.7, 329.26, 329.16, 329.16, 329.16, 328.99, 328.89],
        [54, 329.7, 329.25, 329.15, 329.15, 329.15, 328.99, 328.89],
        [55, 329.7, 329.25, 329.15, 329.15, 329.15, 328.99, 328.89],
        [56, 329.7, 329.24, 329.14, 329.14, 329.14, 328.99, 328.89],
        [57, 329.7, 329.24, 329.14, 329.14, 329.14, 328.98, 328.88],
        [58, 329.7, 329.23, 329.13, 329.13, 329.13, 328.98, 328.88],
        [59, 329.7, 329.23, 329.13, 329.13, 329.13, 328.98, 328.88],
        [60, 329.7, 329.22, 329.12, 329.12, 329.12, 328.98, 328.88],
        [61, 329.7, 329.21, 329.11, 329.11, 329.11, 328.98, 328.88],
        [62, 329.7, 329.21, 329.11, 329.11, 329.11, 328.97, 328.87],
        [63, 329.7, 329.2, 329.1, 329.1, 329.1, 328.97, 328.87],
        [64, 329.7, 329.2, 329.1, 329.1, 329.1, 328.97, 328.87],
        [65, 329.7, 329.19, 329.09, 329.09, 329.09, 328.97, 328.87],
        [66, 329.7, 329.19, 329.09, 329.09, 329.09, 328.97, 328.87],
        [67, 329.7, 329.18, 329.08, 329.08, 329.08, 328.96, 328.86],
        [68, 329.7, 329.18, 329.08, 329.08, 329.08, 328.96, 328.86],
        [69, 329.7, 329.17, 329.07, 329.07, 329.07, 328.96, 328.86],
        [70, 329.7, 329.17, 329.07, 329.07, 329.07, 328.96, 328.86],
        [71, 329.7, 329.16, 329.06, 329.06, 329.06, 328.96, 328.86],
        [72, 329.7, 329.16, 329.06, 329.06, 329.06, 328.95, 328.85],
        [73, 329.7, 329.15, 329.05, 329.05, 329.05, 328.95, 328.85],
        [74, 329.7, 329.18, 329.05, 329.05, 329.05, 328.95, 328.85],
        [75, 329.7, 329.2, 329.05, 329.05, 329.05, 328.95, 328.85],
        [76, 329.7, 329.23, 329.05, 329.05, 329.05, 328.95, 328.85],
        [77, 329.7, 329.25, 329.05, 329.05, 329.05, 328.95, 328.85],
        [78, 329.7, 329.28, 329.05, 329.05, 329.05, 328.95, 328.85],
        [79, 329.7, 329.3, 329.05, 329.05, 329.05, 328.95, 328.85],
        [80, 329.7, 329.33, 329.05, 329.05, 329.05, 328.95, 328.85],
        [81, 329.7, 329.35, 329.05, 329.05, 329.05, 328.95, 328.85],
        [82, 329.7, 329.38, 329.05, 329.05, 329.05, 328.95, 328.85],
        [83, 329.7, 329.4, 329.05, 329.05, 329.05, 328.95, 328.85],
        [84, 329.7, 329.43, 329.05, 329.05, 329.05, 328.95, 328.85],
        [85, 329.7, 329.45, 329.05, 329.05, 329.05, 328.95, 328.85],
        [86, 329.7, 329.48, 329.05, 329.05, 329.05, 328.95, 328.85],
        [87, 329.7, 329.5, 329.05, 329.05, 329.05, 328.95, 328.85],
        [88, 329.7, 329.53, 329.05, 329.05, 329.05, 328.95, 328.85],
        [89, 329.7, 329.55, 329.05, 329.05, 329.05, 328.95, 328.85],
        [90, 329.7, 329.55, 329.07, 329.07, 329.07, 328.95, 328.85],
        [91, 329.7, 329.55, 329.08, 329.08, 329.08, 328.95, 328.85],
        [92, 329.7, 329.55, 329.1, 329.1, 329.1, 328.95, 328.85],
        [93, 329.7, 329.55, 329.11, 329.11, 329.11, 328.95, 328.85],
        [94, 329.7, 329.55, 329.13, 329.13, 329.13, 328.95, 328.85],
        [95, 329.7, 329.55, 329.14, 329.14, 329.14, 328.95, 328.85],
        [96, 329.7, 329.55, 329.16, 329.16, 329.16, 328.95, 328.85],
        [97, 329.7, 329.55, 329.17, 329.17, 329.17, 328.95, 328.85],
        [98, 329.7, 329.55, 329.19, 329.19, 329.19, 328.95, 328.85],
        [99, 329.7, 329.55, 329.2, 329.2, 329.2, 328.95, 328.85],
        [100, 329.7, 329.55, 329.22, 329.22, 329.22, 328.95, 328.85],
        [101, 329.7, 329.55, 329.23, 329.23, 329.23, 328.95, 328.85],
        [102, 329.7, 329.55, 329.25, 329.25, 329.25, 328.95, 328.85],
        [103, 329.7, 329.55, 329.26, 329.26, 329.26, 328.95, 328.85],
        [104, 329.7, 329.55, 329.28, 329.28, 329.28, 328.95, 328.85],
        [105, 329.7, 329.55, 329.29, 329.29, 329.29, 328.96, 328.86],
        [106, 329.7, 329.55, 329.31, 329.31, 329.31, 328.97, 328.86],
        [107, 329.7, 329.55, 329.32, 329.32, 329.32, 328.98, 328.87],
        [108, 329.7, 329.55, 329.34, 329.34, 329.34, 328.99, 328.88],
        [109, 329.7, 329.55, 329.35, 329.35, 329.35, 329.0, 328.88],
        [110, 329.7, 329.55, 329.37, 329.37, 329.37, 329.01, 328.89],
        [111, 329.7, 329.55, 329.38, 329.38, 329.38, 329.02, 328.9],
        [112, 329.7, 329.55, 329.4, 329.4, 329.4, 329.03, 328.9],
        [113, 329.7, 329.55, 329.41, 329.41, 329.41, 329.04, 328.91],
        [114, 329.7, 329.55, 329.43, 329.43, 329.43, 329.05, 328.92],
        [115, 329.7, 329.55, 329.44, 329.44, 329.44, 329.06, 328.92],
        [116, 329.7, 329.55, 329.46, 329.46, 329.46, 329.07, 328.93],
        [117, 329.7, 329.55, 329.47, 329.47, 329.47, 329.08, 328.94],
        [118, 329.7, 329.55, 329.49, 329.49, 329.49, 329.09, 328.94],
        [119, 329.7, 329.55, 329.5, 329.5, 329.5, 329.1, 328.95],
        [120, 329.7, 329.55, 329.5, 329.5, 329.5, 329.11, 328.95],
        [121, 329.7, 329.55, 329.5, 329.5, 329.5, 329.12, 328.96],
        [122, 329.7, 329.55, 329.5, 329.5, 329.5, 329.13, 328.97],
        [123, 329.7, 329.55, 329.5, 329.5, 329.5, 329.14, 328.97],
        [124, 329.7, 329.55, 329.5, 329.5, 329.5, 329.15, 328.98],
        [125, 329.7, 329.55, 329.5, 329.5, 329.5, 329.16, 328.99],
        [126, 329.7, 329.55, 329.5, 329.5, 329.5, 329.17, 328.99],
        [127, 329.7, 329.55, 329.5, 329.5, 329.5, 329.18, 329.0],
        [128, 329.7, 329.55, 329.5, 329.5, 329.5, 329.19, 329.01],
        [129, 329.7, 329.55, 329.5, 329.5, 329.5, 329.2, 329.01],
        [130, 329.7, 329.55, 329.5, 329.5, 329.5, 329.21, 329.02],
        [131, 329.7, 329.55, 329.5, 329.5, 329.5, 329.22, 329.03],
        [132, 329.7, 329.55, 329.5, 329.5, 329.5, 329.23, 329.03],
        [133, 329.7, 329.55, 329.5, 329.5, 329.5, 329.24, 329.04],
        [134, 329.7, 329.55, 329.5, 329.5, 329.5, 329.25, 329.05],
        [135, 329.7, 329.55, 329.5, 329.5, 329.5, 329.25, 329.05],
        [136, 329.7, 329.55, 329.49, 329.49, 329.49, 329.26, 329.06],
        [137, 329.7, 329.55, 329.49, 329.49, 329.49, 329.26, 329.07],
        [138, 329.7, 329.55, 329.49, 329.49, 329.49, 329.26, 329.07],
        [139, 329.7, 329.55, 329.48, 329.48, 329.48, 329.27, 329.08],
        [140, 329.7, 329.55, 329.48, 329.48, 329.48, 329.27, 329.09],
        [141, 329.7, 329.55, 329.48, 329.48, 329.48, 329.27, 329.09],
        [142, 329.7, 329.55, 329.48, 329.48, 329.48, 329.28, 329.1],
        [143, 329.7, 329.55, 329.47, 329.47, 329.47, 329.28, 329.11],
        [144, 329.7, 329.55, 329.47, 329.47, 329.47, 329.28, 329.11],
        [145, 329.7, 329.55, 329.47, 329.47, 329.47, 329.29, 329.12],
        [146, 329.7, 329.55, 329.46, 329.46, 329.46, 329.29, 329.13],
        [147, 329.7, 329.55, 329.46, 329.46, 329.46, 329.29, 329.13],
        [148, 329.7, 329.55, 329.46, 329.46, 329.46, 329.3, 329.14],
        [149, 329.7, 329.55, 329.45, 329.45, 329.45, 329.3, 329.15],
        [150, 329.7, 329.55, 329.45, 329.45, 329.45, 329.3, 329.15],
        [151, 329.7, 329.55, 329.5, 329.45, 329.45, 329.3, 329.16],
        [152, 329.7, 329.55, 329.5, 329.45, 329.45, 329.31, 329.16],
        [153, 329.7, 329.55, 329.5, 329.45, 329.45, 329.31, 329.17],
        [154, 329.7, 329.55, 329.5, 329.45, 329.45, 329.31, 329.18],
        [155, 329.7, 329.55, 329.5, 329.45, 329.45, 329.32, 329.18],
        [156, 329.7, 329.55, 329.5, 329.45, 329.45, 329.32, 329.19],
        [157, 329.7, 329.55, 329.5, 329.45, 329.44, 329.32, 329.2],
        [158, 329.7, 329.55, 329.5, 329.45, 329.44, 329.33, 329.2],
        [159, 329.7, 329.55, 329.5, 329.45, 329.44, 329.33, 329.21],
        [160, 329.7, 329.55, 329.5, 329.45, 329.44, 329.33, 329.22],
        [161, 329.7, 329.55, 329.5, 329.45, 329.44, 329.34, 329.22],
        [162, 329.7, 329.55, 329.5, 329.45, 329.44, 329.34, 329.23],
        [163, 329.7, 329.55, 329.5, 329.45, 329.44, 329.34, 329.24],
        [164, 329.7, 329.55, 329.5, 329.45, 329.44, 329.35, 329.24],
        [165, 329.7, 329.55, 329.5, 329.45, 329.44, 329.35, 329.25],
        [166, 329.7, 329.55, 329.5, 329.45, 329.44, 329.35, 329.25],
        [167, 329.7, 329.55, 329.5, 329.45, 329.44, 329.35, 329.25],
        [168, 329.7, 329.55, 329.5, 329.45, 329.44, 329.35, 329.25],
        [169, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [170, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [171, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [172, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [173, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [174, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [175, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [176, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [177, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [178, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [179, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [180, 329.7, 329.55, 329.5, 329.45, 329.43, 329.35, 329.25],
        [181, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [182, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [183, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [184, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [185, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [186, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [187, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [188, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [189, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [190, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [191, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [192, 329.7, 329.55, 329.5, 329.45, 329.42, 329.35, 329.25],
        [193, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [194, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [195, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [196, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [197, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [198, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [199, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [200, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [201, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [202, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [203, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [204, 329.7, 329.55, 329.5, 329.45, 329.41, 329.35, 329.25],
        [205, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [206, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [207, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [208, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [209, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [210, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [211, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [212, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [213, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [214, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [215, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [216, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [217, 329.7, 329.55, 329.5, 329.45, 329.4, 329.35, 329.25],
        [218, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [219, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [220, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [221, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [222, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [223, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [224, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [225, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [226, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [227, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [228, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [229, 329.7, 329.55, 329.5, 329.45, 329.39, 329.35, 329.25],
        [230, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [231, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [232, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [233, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [234, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [235, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [236, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [237, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [238, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [239, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [240, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [241, 329.7, 329.55, 329.5, 329.45, 329.38, 329.35, 329.25],
        [242, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [243, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [244, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [245, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [246, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [247, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [248, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [249, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [250, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [251, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [252, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [253, 329.7, 329.55, 329.5, 329.45, 329.37, 329.35, 329.25],
        [254, 329.7, 329.55, 329.5, 329.45, 329.36, 329.35, 329.25],
        [255, 329.7, 329.55, 329.5, 329.45, 329.36, 329.35, 329.25],
        [256, 329.7, 329.55, 329.5, 329.45, 329.36, 329.35, 329.25],
        [257, 329.7, 329.55, 329.5, 329.45, 329.36, 329.35, 329.25],
        [258, 329.7, 329.55, 0.0, 329.44, 329.36, 329.34, 329.24],
        [259, 329.7, 329.55, 0.0, 329.44, 329.36, 329.34, 329.24],
        [260, 329.7, 329.55, 0.0, 329.43, 329.36, 329.33, 329.23],
        [261, 329.7, 329.55, 0.0, 329.42, 329.36, 329.32, 329.22],
        [262, 329.7, 329.55, 0.0, 329.42, 329.36, 329.32, 329.22],
        [263, 329.7, 329.55, 0.0, 329.41, 329.36, 329.31, 329.21],
        [264, 329.7, 329.54, 0.0, 329.4, 329.36, 329.3, 329.2],
        [265, 329.7, 329.54, 0.0, 329.4, 329.36, 329.3, 329.2],
        [266, 329.7, 329.53, 0.0, 329.39, 329.35, 329.29, 329.19],
        [267, 329.7, 329.53, 0.0, 329.38, 329.35, 329.28, 329.18],
        [268, 329.7, 329.52, 0.0, 329.38, 329.35, 329.28, 329.18],
        [269, 329.7, 329.52, 0.0, 329.37, 329.35, 329.27, 329.17],
        [270, 329.7, 329.51, 0.0, 329.36, 329.35, 329.26, 329.16],
        [271, 329.7, 329.51, 0.0, 329.36, 329.35, 329.26, 329.16],
        [272, 329.7, 329.5, 0.0, 329.35, 329.35, 329.25, 329.15],
        [273, 329.7, 329.5, 329.34, 329.34, 329.34, 329.24, 329.14],
        [274, 329.7, 329.49, 329.34, 329.34, 329.34, 329.24, 329.14],
        [275, 329.7, 329.49, 329.33, 329.33, 329.33, 329.23, 329.13],
        [276, 329.7, 329.48, 329.32, 329.32, 329.32, 329.22, 329.12],
        [277, 329.7, 329.48, 329.32, 329.32, 329.32, 329.22, 329.12],
        [278, 329.7, 329.47, 329.31, 329.31, 329.31, 329.21, 329.11],
        [279, 329.7, 329.47, 329.3, 329.3, 329.3, 329.2, 329.1],
        [280, 329.7, 329.46, 329.3, 329.3, 329.3, 329.2, 329.1],
        [281, 329.7, 329.46, 329.29, 329.29, 329.29, 329.19, 329.09],
        [282, 329.7, 329.45, 329.28, 329.28, 329.28, 329.18, 329.08],
        [283, 329.7, 329.45, 329.28, 329.28, 329.28, 329.18, 329.08],
        [284, 329.7, 329.44, 329.27, 329.27, 329.27, 329.17, 329.07],
        [285, 329.7, 329.44, 329.26, 329.26, 329.26, 329.16, 329.06],
        [286, 329.7, 329.43, 329.26, 329.26, 329.26, 329.16, 329.06],
        [287, 329.7, 329.43, 329.25, 329.25, 329.25, 329.15, 329.05],
        [288, 329.7, 329.42, 329.25, 329.25, 329.25, 329.15, 329.05],
        [289, 329.7, 329.42, 329.25, 329.25, 329.25, 329.15, 329.05],
        [290, 329.7, 329.41, 329.25, 329.25, 329.25, 329.15, 329.05],
        [291, 329.7, 329.41, 329.25, 329.25, 329.25, 329.15, 329.05],
        [292, 329.7, 329.4, 329.25, 329.25, 329.25, 329.15, 329.05],
        [293, 329.7, 329.4, 329.25, 329.25, 329.25, 329.15, 329.05],
        [294, 329.7, 329.39, 329.25, 329.25, 329.25, 329.15, 329.05],
        [295, 329.7, 329.39, 329.24, 329.24, 329.24, 329.14, 329.04],
        [296, 329.7, 329.38, 329.24, 329.24, 329.24, 329.14, 329.04],
        [297, 329.7, 329.38, 329.24, 329.24, 329.24, 329.14, 329.04],
        [298, 329.7, 329.37, 329.24, 329.24, 329.24, 329.14, 329.04],
        [299, 329.7, 329.37, 329.24, 329.24, 329.24, 329.14, 329.04],
        [300, 329.7, 329.36, 329.24, 329.24, 329.24, 329.14, 329.04],
        [301, 329.7, 329.36, 329.24, 329.24, 329.24, 329.14, 329.04],
        [302, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [303, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [304, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [305, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [306, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [307, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [308, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [309, 329.7, 329.35, 329.24, 329.24, 329.24, 329.14, 329.04],
        [310, 329.7, 329.34, 329.24, 329.24, 329.24, 329.14, 329.04],
        [311, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [312, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [313, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [314, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [315, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [316, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [317, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [318, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [319, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [320, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [321, 329.7, 329.34, 329.23, 329.23, 329.23, 329.13, 329.03],
        [322, 329.7, 329.33, 329.23, 329.23, 329.23, 329.13, 329.03],
        [323, 329.7, 329.33, 329.23, 329.23, 329.23, 329.13, 329.03],
        [324, 329.7, 329.33, 329.23, 329.23, 329.23, 329.13, 329.03],
        [325, 329.7, 329.33, 329.23, 329.23, 329.23, 329.13, 329.03],
        [326, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [327, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [328, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [329, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [330, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [331, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [332, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [333, 329.7, 329.33, 329.22, 329.22, 329.22, 329.12, 329.02],
        [334, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [335, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [336, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [337, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [338, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [339, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [340, 329.7, 329.32, 329.22, 329.22, 329.22, 329.12, 329.02],
        [341, 329.7, 329.32, 329.21, 329.21, 329.21, 329.11, 329.01],
        [342, 329.7, 329.32, 329.21, 329.21, 329.21, 329.11, 329.01],
        [343, 329.7, 329.32, 329.21, 329.21, 329.21, 329.11, 329.01],
        [344, 329.7, 329.32, 329.21, 329.21, 329.21, 329.11, 329.01],
        [345, 329.7, 329.32, 329.21, 329.21, 329.21, 329.11, 329.01],
        [346, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [347, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [348, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [349, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [350, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [351, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [352, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [353, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [354, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [355, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [356, 329.7, 329.31, 329.21, 329.21, 329.21, 329.11, 329.01],
        [357, 329.7, 329.31, 329.2, 329.2, 329.2, 329.1, 329.0],
        [358, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [359, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [360, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [361, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [362, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [363, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [364, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0],
        [365, 329.7, 329.3, 329.2, 329.2, 329.2, 329.1, 329.0]
    ]

    df = pd.DataFrame(historical_water_data_array,
                      columns=['Day', 'Top of High', 'Top of Normal', 'Top of BMP', 'Target', 'Best Practice', 'Bottom of Normal', 'Bottom of Low'])

    df['Day'] += 1
    todays_date = datetime.today()
    year = int(todays_date.year)
    df['Year'] = year
    df['Day'] = df['Day'].astype(int)
    df['Date'] = compose_date(df['Year'], days=df['Day'])
    # df.loc[-1,'Date'] = df.loc[-2,'Date']
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

    local_offset = 320.85

    df['Level'] = df['Value/Valeur'].astype(float).fillna(0.0) + local_offset

    return df


# get the required data
df_historical = get_historical_level_data()
# df_precip = get_precipitation_data()
df_recent = get_recent_level_data()

# condition the data to prepare for display
df_recent['Date'] = pd.to_datetime(df_recent['Date'])
df_recent['Day'] = df_recent['Date'].dt.dayofyear - 1
# df_recent['Level'] = df_recent['Value/Valeur'].astype(float).fillna(0.0)
groups = df_recent.groupby(['Day'])['Level'].mean()
group_list = groups.to_list()
day_list = df_historical['Date'].to_list()[:len(group_list)]

x_list = df_historical['Month'].to_list()[:len(group_list)]
# y_list = df_precip['Total Precip (mm)'].to_list()

# create plotly plots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.8, 0.2])

fig.append_trace(go.Line(x=df_historical['Date'], y=df_historical['Top of High'], name='Top of High Water Zone', line_color='Red'), row=1, col=1)
fig.append_trace(go.Line(x=df_historical['Date'], y=df_historical['Top of Normal'], name='Top of Normal Operating Zone', line_color='Yellow'), row=1, col=1)
fig.append_trace(go.Scatter(x=df_historical['Date'], y=df_historical['Bottom of Low'], name='Bottom of Low Water Zone', line=dict(color='Red', dash='dash')), row=1, col=1)
fig.append_trace(go.Scatter(x=df_historical['Date'], y=df_historical['Bottom of Normal'], name='Bottom of Normal Operating Zone', line=dict(color='Yellow', dash='dash')), row=1, col=1)
fig.append_trace(go.Scatter(x=df_historical['Date'], y=df_historical['Best Practice'], name='Best Practice', line=dict(color='Green', dash='dash')), row=1, col=1)
fig.append_trace(go.Line(x=df_historical['Date'], y=df_historical['Target'], name='Target Operating Level', line_color='Green'), row=1, col=1)

fig.append_trace(go.Scatter(x=day_list, y=group_list, name='Lake Bernard Mean Daily Levels', marker=dict(
    color='Blue',
    size=4,
)), row=1, col=1)

# fig.append_trace(
#         go.Line(x=df_historical['Date'], y=df_precip['Total Precip (mm)'].to_list(), name='Precipitation'),
#         row=2,
#         col=1
#     )

# plot via streamlit
st.plotly_chart(fig)
