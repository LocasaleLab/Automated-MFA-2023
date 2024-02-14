import itertools as it
import warnings
from collections import defaultdict, abc
import gzip
import pickle
import pathlib
import os
import copy
import multiprocessing as mp
import argparse
import enum


class ValueEnum(enum.Enum):
    def __str__(self):
        return self.value

    def startswith(self, substr):
        return self.value.startswith(substr)
