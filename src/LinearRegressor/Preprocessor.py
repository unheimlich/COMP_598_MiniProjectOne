import numpy as np
__author__ = 'andrew'

class Preprocessor:

    def __init__(self):

        self.mu = 0
        self.sigma = 0
        self.L = 0
        self.V = 0


    #ToDo: learn principal components and principal eigen values
    def train(self,X):

        self.mu = np.nanmean(X, axis=0, dtype=np.float64)
        self.sigma = np.nanstd(X, axis=0, dtype=np.float64)

    def center(self, X):

        return X - self.mu

    def standardize(self, X):

        return (X - self.mu)/self.sigma

    #ToDo: enable
    def whiten(self, X):

        S = (X - self.mu)/self.sigma
        return S