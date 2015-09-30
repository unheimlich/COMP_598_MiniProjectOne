import numpy as np
import scipy.stats as stats

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

        shape = 0.892974489438055
        scale = 3.802326072910595e+03

        #w = np.zeros((t.shape[0],1))

        #for i in range(t.shape[0]):
            #w[i] = stats.gamma.pdf(t[i], shape, scale=scale)

        #w = w/w.max()

        #Xtw = (X*w).T
        Xtw = X.T

        I = np.eye(self.numVars+1)

        S = self.Lambda*I + np.dot(Xtw,X);

        self.w = np.linalg.lstsq(S,np.dot(Xtw,t))[0]

    def optimizeGradientDescent(self, X, t):

        self.initWeights()
        self.evalLoss(X, t)

        dLoss = -1

        #shape = 0.892974489438055
        #scale = 3.802326072910595e+03

       #w = np.zeros((t.shape[0],1))

        #for i in range(t.shape[0]):
          #  w[i] = stats.gamma.pdf(t[i], shape, scale=scale)

       # w = w/sum(w)

        #Xtw = (X*w).T
        Xtw = X.T

        S = np.dot(Xtw,X)
        T = np.dot(Xtw,t)

        iters = 0.

        max_iters = 10000.

        while (dLoss < -1e-1) and (iters < max_iters):

            lr = self.alpha

            iters += 1

            last_w = self.w
            last_loss = self.loss

            dE = (np.dot(S, self.w) - T)/self.numObs + self.Lambda*self.w

            self.w -= lr*dE

            self.evalLoss(X, t)

            dLoss = self.loss - last_loss

            print(dLoss)

            if dLoss > 0:

                self.w = last_w

    def evalLoss(self, X, t):

        self.loss = 0.5*sum((t - np.dot(X,self.w))**2) + 0.5*self.Lambda*np.dot(self.w.T, self.w)

    def evalError(self,X,t):

        y = np.dot(X,self.w)

        #self.loss = np.mean(np.abs(t-y), axis=0, dtype=np.float64)
        self.loss = np.sqrt(np.mean((t - y)**2, axis=0, dtype=np.float64),dtype=np.float64)

    def initWeights(self):

        hi = np.sqrt(12)/(self.numVars+1)
        lo = -hi

        self.w = np.random.uniform(lo, hi, [self.numVars+1,])
        self.w[0] = 0

