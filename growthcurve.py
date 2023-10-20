#!/usr/bin/env python

"""
Program: Plot growth curves.
Author: Emil Karlsson
Date: 2023-10-20
Usage: graphGC.py data.csv

Expected raw data format is one
row per time point and one column
per replicate. Header must contain
the following column names:

time, dilution, blank, alpha, beta, gamma, epsilon, zeta, eta

Possible improvements:
- Allow an arbitrary number of replicates.
- Allow arbitrary replicate labels.
- Allow different conversion factors (300000 or 100000).
"""


import sys
import pandas as pd
import matplotlib.pyplot as plt

def readindata(datafile):
    """
    Read in the raw data csv.
    """
    return pd.read_csv(datafile)


def subtractblank(df):
    """
    Subtract away blank controls.
    """
    replicates = ['alpha', 'beta', 'gamma', 'epsilon', 'zeta', 'eta']
    for replicate in replicates:
        df[replicate + "-blank"] = df[replicate].sub(df['blank'])
    return df


def fluorescencetocells(df):
    """
    Convert from fluorescence values to cells.
    """
    conversionfactor = 300000
    replicates = ['alpha-blank', 'beta-blank', 'gamma-blank', 'epsilon-blank', 'zeta-blank', 'eta-blank']
    for replicate in replicates:
        df[replicate + "-cells"] = df[replicate].multiply(conversionfactor)
    return df

def dilutionadjust(df):
    """
    Adjust for dilutions.
    """
    replicates = ['alpha-blank-cells', 'beta-blank-cells', 'gamma-blank-cells', 'epsilon-blank-cells', 'zeta-blank-cells', 'eta-blank-cells']
    for replicate in replicates:
        df[replicate + "-adjust"] = df[replicate].multiply(df["dilution"])
    return df


def makegraph(df):
    """
    Make line graph from processed data.
    """
    replicates = ['alpha-blank-cells-adjust', 'beta-blank-cells-adjust',
    'gamma-blank-cells-adjust', 'epsilon-blank-cells-adjust', 'zeta-blank-cells-adjust', 'eta-blank-cells-adjust']
    for replicate in replicates:
        plt.plot(df["time"], df[replicate],label=replicate.split('-')[0])
    plt.title('Growth curve')
    plt.legend(loc='best')
    plt.xlabel('Time (hours)')
    plt.ylabel('Cell density (cells/ml)')
    plt.savefig("growthcurves_python.pdf", format="pdf")


pd.set_option('display.max_columns', None)
my_data = readindata(sys.argv[1])
my_data = subtractblank(my_data)
my_data = fluorescencetocells(my_data)
my_data = dilutionadjust(my_data)
makegraph(my_data)