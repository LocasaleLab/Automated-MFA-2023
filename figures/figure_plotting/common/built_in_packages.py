import enum
import copy
import gzip
import pickle
import logging
import warnings
import itertools as it
from dataclasses import dataclass
from typing import List, Tuple, Dict


class FigureName(enum.Enum):
    test = 'test'
    simple_test = 'simple_test'
    figure_1 = '1'
    figure_2 = '2'
    figure_3 = '3'
    figure_4 = '4'
    figure_5 = '5'
    figure_s1 = 's1'
    figure_s2 = 's2'
    figure_s3 = 's3'
    figure_s4 = 's4'
    figure_s5 = 's5'
    figure_s6 = 's6'
    figure_s7 = 's7'

    def __str__(self):
        return self.value

