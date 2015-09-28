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
            self.evalError(X, t)

        elif optimization is 'GradientDescent':

            self.optimizeGradientDescent(X, t)
            self.evalError(X, t)


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
        self.evalError(X, t)

        dLoss = -1

        S = np.dot(X.T,X)
        T = np.dot(X.T,t)


        iters = 0.

        max_iters = 10000.

        while (dLoss < -1e-3) and (iters < max_iters):

            #lr = self.alpha*(2**-(iters/30))
            lr = self.alpha

            iters += 1

            last_w = self.w
            last_loss = self.loss

            dE = (np.dot(S ,self.w) - T + self.Lambda*self.w)/self.numObs

            #I = np.random.choice(range(0, self.numObs), [self.numObs,],replace=0)
            #Xs = X[I]
            #ts = t[I]

            #y = np.dot(Xs, self.w)

            #for i in range(0, self.numObs-1):
                #self.w += self.alpha*(ts[i] - y[i])*Xs[i, :].T

            self.w -= lr*dE

            self.evalError(X, t)

            dLoss = self.loss - last_loss

            print(dLoss)

            if dLoss > 0:

                self.w = last_w

    def evalLoss(self, X, t):

        #e = np.power(np.power(t - np.dot(X, self.w), 2.0), 0.5)

        self.loss = 0.5*sum(t - np.dot(X,self.w)) + 0.5*self.Lambda*np.dot(self.w.T,self.w)

        #self.loss = np.mean(e, axis=0, dtype=np.float64)

    def evalError(self,X,t):

        y = np.dot(X,self.w)

        self.loss = np.mean(np.abs(t-y), axis=0, dtype=np.float64)

    def initWeights(self):

        hi = np.sqrt(12)/self.numVars+1
        #hi = 50
        lo = -hi

        self.w = np.random.uniform(lo, hi, [self.numVars+1,])
        self.w[0] = 0

