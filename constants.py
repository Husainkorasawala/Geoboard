import json
import numpy as np

"""
    Reading Files saved in sample.json
"""
with open('sample.json') as data:
    dataDict = dict(json.load(data))

# All the Constant Values Used in the program is kept here
N = 10
X = np.zeros((N, N), dtype=int)
BYELLOW = '\033[43m'
CBLACK = '\033[30m'
CRED = '\033[41m'
CGREEN = '\033[42m'
CEND = '\033[0m'
COORDS = []
SHAPES = dataDict
