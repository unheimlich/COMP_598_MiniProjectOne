import pandas as pd


def readDataOne(filename):

    DS = pd.read_csv(filename)
    X = DS.values[:, 1:60]
    t = DS.values[:, 60]

    return X, t