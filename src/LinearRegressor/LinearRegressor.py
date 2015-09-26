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

        X = np.concatenate((np.ones([self.numObs, 1]), X), axis=1)

        if optimization is 'LeastSquares':

            self.optimizeLeastSquares(X, t)
            self.evalLoss(X, t)

        elif optimization is 'GradientDescent':

            self.optimizeGradientDescent(X, t)


    def predict(self, X):

        [self.numObs, self.numVars] = X.shape

        X = np.concatenate((np.ones([self.numObs, 1]), X), axis=1)

        y = np.dot(X,self.w)

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

        I = np.eye(self.numVars+1)

        # Q, R = np.linalg.qr(X)
        #
        # R = self.Lambda*I + R
        #
        # self.w = np.linalg.lstsq(R,np.dot(Q.T,t))[0]

        S = self.Lambda*I + np.dot(X.T,X);

        self.w = np.linalg.lstsq(S,np.dot(X.T,t))[0]

    def optimizeGradientDescent(self, X, t):

        self.initWeights()
        self.evalLoss(X, t)

        dLoss = -1

        S = np.dot(X.T,X)
        T = np.dot(X.T,t)


        iters = 0.0

        while dLoss < -1e-1:

            lr = self.alpha*(2**-(iters/4))

            iters += 1

            last_w = self.w
            last_loss = self.loss

            dE = (np.dot(S ,self.w) - T + self.Lambda*self.w)/self.numObs

            #y = np.dot(X, self.w)

            #for i in range(0, self.numObs-1):
                #self.w += self.alpha*(t[i] - y[i])*X[i, :].T

            self.w -= lr*dE

            self.evalLoss(X, t)

            dLoss = self.loss - last_loss

            print(dLoss)

            if dLoss > 0:

                self.w = last_w

    def evalLoss(self, X, t):

        e = np.power(np.power(t - np.dot(X, self.w), 2.0), 0.5)

        self.loss = np.mean(e, axis=0, dtype=np.float64)

    def initWeights(self):

        hi = np.sqrt(12)/self.numVars+1
        lo = -hi

        self.w = np.random.uniform(lo, hi, [self.numVars+1,])

