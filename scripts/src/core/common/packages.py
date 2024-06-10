import itertools as it
import copy
import time
import warnings
from collections import defaultdict, Counter
from queue import PriorityQueue

import numpy as np
from scipy.special import comb as scipy_comb
from scipy import linalg as scipy_linalg
from scipy import optimize

np_float_type = 'float64'
np_int_type = 'int32'

try:
    import os
except ModuleNotFoundError:
    os = None
