import numpy as np
__author__ = 'andrew'


class LinearRegressor:

    def __init__(self):

        self.alpha = 0.0
        self.w = 0.0
        self.Lambda = 0.0
        self.loss = 1.0
        self.numObs = 0
        self.numVars = 0
        self.optimization = 'LeastSquares'

    def train(self, X, t, optimization, learningRate, regularization):

        self.alpha = learningRate
        self.Lambda = regularization

        [self.numObs, self.numVars] = X.shape

        X = np.concatenate((np.matrix(np.ones([self.numObs, 1])), X), axis=1)

        if optimization is 'LeastSquares':

            self.optimizeLeastSquares(X, t)
            self.evalLoss(X, t)

        elif optimization is 'GradientDescent':

            self.optimizeGradientDescent(X, t)


    def predict(self, X):

        X = np.concatenate((np.matrix(np.ones([self.numObs, 1])), X), axis=1)

        y = X*self.w

        return y

    def getWeights(self):

        return self.w

    def getTrainingError(self):

        return self.loss

    def getLearingRate(self):

        return self.alpha

    def getRegularizationConstant(self):

        return self.Lambda

    def optimizeLeastSquares(self, X, t):

        xt = X.transpose()

        I = np.matrix(np.eye(self.numVars+1))

        C = self.Lambda*I + xt*X;

        S = np.linalg.inv(C)

        self.w = S*xt*t

    def optimizeGradientDescent(self, X, t):

        self.initWeights()
        self.evalLoss(X, t)

        dLoss = -1

        while dLoss < -1e-6:

            last_w = self.w
            last_loss = self.loss

            dE = X.T*X*self.w - X.T*t + self.Lambda*self.w

            self.w -= self.alpha*dE

            self.evalLoss(X, t)

            dLoss = self.loss - last_loss

            print(dLoss)

            if dLoss > 0:

                self.w = last_w

    def evalLoss(self, X, t):

        e = np.array(t - X*self.w)**2

        self.loss = 0.5*e.sum(axis=0)

    def initWeights(self):

        hi = np.sqrt(12)/self.numVars+1
        lo = -hi

        self.w = np.matrix(np.random.uniform(lo, hi, [self.numVars+1, 1]))

