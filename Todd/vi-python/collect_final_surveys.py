"""
This script is for my own sanity in collecting all the final survey positions and ideal positions into their
own respective csv files so that they can easily be ran in final_survey_plot.py
Mostly based off Zach's survey python script to get the data: https://github.com/zachschillaci27/Surveys
"""
import collections
import pandas as pd
import numpy as np
import glob
import re
import sys


def StringtoFlt(string):
    flt = None
    if "\n" in string:
        string.replace("\n", "")
    if "=" in string:
        string = string[string.find("=") + 1:]
    try:
        flt = float(string)
    except ValueError:
        print("Cannot convert string to float!")
    return flt


class Module:

    def __init__(self, module_file):
        self.dimensions = ['X', 'Y']

        with open(module_file) as f_in:
            self.lines = list(filter(None, (line.rstrip() for line in f_in)))

        indA, indB, indC, indD = 0, 0, 0, 0
        for ind, line in enumerate(self.lines):
            if "CornerA" in line:
                indA = ind + 1
            elif "CornerB" in line:
                indB = ind + 1
            elif "CornerC" in line:
                indC = ind + 1
            elif "CornerD" in line:
                indD = ind + 1

        self.corners = collections.OrderedDict()
        self.corners['A'] = self.lines[indA: indB - 1]
        self.corners['B'] = self.lines[indB: indC - 1]
        self.corners['C'] = self.lines[indC: indD - 1]
        self.corners['D'] = self.lines[indD:]

        self.stages = []
        for line in self.corners['A']:
            stage = line[line.find("_") + 1: line.find("=") - 1]
            if stage not in self.stages:
                self.stages.append(stage)

        xdf, ydf, zdf = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
        for corner, coords in self.corners.items():
            xvals, yvals, zvals = [], [], []
            for i in range(len(self.stages)):
                xvals.append(StringtoFlt(coords[(3 * i)]))
                yvals.append(StringtoFlt(coords[(3 * i) + 1]))
                zvals.append(StringtoFlt(coords[(3 * i) + 2]))
            xdf[corner] = xvals
            ydf[corner] = yvals
            zdf[corner] = zvals

        self.xdf = pd.DataFrame(xdf, index=self.stages)
        self.ydf = pd.DataFrame(ydf, index=self.stages)
        self.zdf = pd.DataFrame(zdf, index=self.stages)

    def get_values_for_files(self):
        x_vals = self.xdf.to_numpy()
        y_vals = self.ydf.to_numpy()
        z_vals = self.zdf.to_numpy()

        xyz_ideals = np.vstack((x_vals[0, :], y_vals[0, :], z_vals[0, :])).T
        xyz_measurements = np.vstack((x_vals[-1, :], y_vals[-1, :], z_vals[-1, :])).T

        return xyz_ideals, xyz_measurements


def get_module_number(module_file):
    return int(re.search(r'(\d+)', module_file).group(0))


if __name__ == '__main__':

    ideal_values = []
    measurement_values = []
    module_files = glob.glob(sys.argv[1]+'\\*.txt')
    module_files.sort(key=get_module_number)
    print(module_files)

    for file in module_files:
        m = Module(file)

        module_ideals, module_measurements = m.get_values_for_files()

        ideal_values.append(module_ideals)
        measurement_values.append(module_measurements)

    data_ideals = np.vstack(ideal_values)
    data_measurements = np.vstack(measurement_values)

    np.savetxt(sys.argv[2] + 'Ideals.csv', data_ideals, fmt='%.6f', delimiter=',')
    np.savetxt(sys.argv[2] + 'Survey.csv', data_measurements, fmt='%.6f', delimiter=',')
