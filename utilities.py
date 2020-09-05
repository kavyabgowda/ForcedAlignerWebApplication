####Author: Kavya Bhadre Gowda######

# Copyright (c) 2011-2014 Kyle Gorman and Michael Wagner
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import bisect
import logging
import os
import yaml

SP = "sp"
SIL = "sil"
TEMP = "temp"
MISSING = "missing.txt"
OOV = "OOV.txt"
DICT = "dict"
HMMDEFS = "hmmdefs"
MACROS = "macros"
PROTO = "proto"
VFLOORS = "vFloors"

ALIGNED = "aligned.mlf"
SCORES = "scores.csv"

# samplerates which appear to be HTK-compatible (all divisors of 1e7)
SAMPLERATES = [4000, 8000, 10000, 12500, 15625, 16000, 20000, 25000,
               31250, 40000, 50000, 62500, 78125, 80000, 100000, 125000,
               156250, 200000]
def mkdir_p(dirname):
    os.makedirs(dirname, exist_ok=True)


def resolve_opts(argDict):
    with open(argDict.get('configuration'), "r") as source:
        try:
            opts = yaml.load(source, Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            logging.error("Error in configuration file: %s", err)
            exit(1)

    opts["dictionary"] = argDict.get('dictionary')
    try:
        sr = opts["samplerate"]
        print(sr)
    except KeyError:
        logging.error("Samplerate (-s) not specified.")
        exit(1)
    if sr not in SAMPLERATES:
        i = bisect.bisect(SAMPLERATES, sr)
        if i == 0:
            pass
        elif i == len(SAMPLERATES):
            i = -1
        elif SAMPLERATES[i] - sr > sr - SAMPLERATES[i - 1]:
            i = i - 1
        # else keep `i` as is
        sr = SAMPLERATES[i]
        logging.warning("Using {} Hz as samplerate".format(sr))
    opts["samplerate"] = sr
    return opts

def opts2cfg(filename, opts):
    with open(filename, "w") as sink:
        for (setting, value) in opts.items():
            print("{!s} = {!s}".format(setting, value), file=sink)


def splitname(fullname):
    (dirname, filename) = os.path.split(fullname)
    (basename, ext) = os.path.splitext(filename)
    return (dirname, basename, ext)