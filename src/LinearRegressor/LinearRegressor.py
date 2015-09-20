__author__ = 'andrew'

import numpy as np

class LinearRegressor:

    def __init__(self):

        self.alpha = 0.0
        self.w = 0.0
        self.Lambda = 0.0
        self.loss = 1.0
        self.numObs = 0
        self.numVars = 0
        self.optimization = 'LeastSquares'

    def train(self, X, T, optimization, learningRate, regularization):

        self.alpha = learningRate
        self.Lambda = regularization

        [self.numObs, self.numVars] = X.shape

        X = np.concatenate((np.matrix(np.ones([self.numObs, 1])), X), axis=1)

        if optimization is 'LeastSquares':

            self.optimizeLeastSquares(X, T)

        elif optimization is 'GradientDescent':

            self.optimizeGradientDescent(X, T)


    def predict(self, X):

        y = 1

        return y

    def getWeights(self):

        return self.w

    def getTrainingError(self):

        return self.loss

    def getLearingRate(self):

        return self.alpha

    def getRegularizationConstant(self):

        return self.Lambda

    def optimizeLeastSquares(self, X, T):

        xt = X.transpose()
        s = np.linalg.inv(xt*X)

        self.w = s*xt*T

    def optimizeGradientDescent(self, X, T):

        w = self.w

        return w

    def evalLoss(self, X, T):

        e = np.array(T - X*self.w)**2

        self.loss = 0.5*e.sum(axis=0)

    def initWeights(self):

        hi = np.sqrt(12)/self.numVars+1
        lo = -hi

        self.w = np.matrix(np.random.uniform(lo, hi, [self.numVars+1, 1]))

