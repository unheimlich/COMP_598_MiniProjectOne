import numpy as np
__author__ = 'andrew'

class Preprocessor:

    def __init__(self):

        self.mu = 0
        self.sigma = 0
        self.S = 0
        self.V = 0


    #ToDo: learn principal components and principal eigen values
    def train(self,X):

        self.mu = np.nanmean(X, axis=0, dtype=np.float64)
        self.sigma = np.nanstd(X, axis=0, dtype=np.float64)

        D = (X - self.mu)/self.sigma

        u, s, v = np.linalg.svd(D, full_matrices=0)

        idx = s >= np.finfo(np.float).resolution*D.shape[0]

        self.S = np.diag(s[idx])
        self.V = v[:, idx]

    def center(self, X):

        return X - self.mu

    def standardize(self, X):

        return (X - self.mu)/self.sigma

    #ToDo: enable
    def whiten(self, X):

        s = (X - self.mu)/self.sigma

        return np.linalg.lstsq(np.sqrt(self.S), np.dot(self.V.T, s.T))[0].T