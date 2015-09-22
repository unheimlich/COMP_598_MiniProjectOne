import pandas as pd


def readDataOne(filename):

    DS = pd.read_csv(filename)
    X = DS.values[:,1:59]
    t = DS.values[:,60]

    return X, t