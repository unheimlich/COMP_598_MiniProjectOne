import pandas as pd
import numpy as np
import math
from src.LinearRegressor import LinearRegressor as LR
from src.LinearRegressor import Preprocessor as PP
__author__ = 'suzin'


def separateTestSet(f, x):
    #'data\PartOne\OnlineNewsPopularity.csv'
    ds = pd.read_csv(f)
    
    # leave out x*100% as a test set
    testindices = np.random.randint(0,ds.shape[0]-1,np.floor(ds.shape[0]/x)) #get a random set of indices, size n/5
    # create new csv's, test set set aside
    ds.iloc[testindices].to_csv(f.replace(".csv","")+"_test.csv", index=False)  
    ds.drop(testindices).to_csv(f.replace(".csv","")+"_training.csv", index=False)    


def kfoldlabel(f, k):
    
    dataset = pd.read_csv(f.replace(".csv","")+"_training.csv")  #read the training set data

    n = dataset.shape[0]                        #gets the number of samples in the dataset
    l = list(range(0,n))                        #List of integers
    np.random.shuffle(l)                           # shuffle
    dataset['kset'] = np.nan                    #add a column indicated which of the k subsets it is
    
    for i in range(0,k):
        chunk = l[int(math.ceil(i*n/k)):int(math.ceil((i+1)*n/k)-1)]    #get the next block of random indices
        dataset.loc[chunk,'kset'] = i+1       #label 'kset' column
        
    dataset.to_csv(f.replace(".csv","")+"_training_"+str(k)+"-fold.csv")


def runcrossval(optimization, regularization, learningrate, preprocessing):

    ds = pd.read_csv('data/PartOne/OnlineNewsPopularity_training_5-fold.csv')
    X = ds.values[:, 2:61]
    t = ds.values[:, 61]

    I = ds.values[:, 62]
    y = np.zeros(X.shape[0])

    lr = LR.LinearRegressor()

    if preprocessing is '':

        D = X

    elif preprocessing is 'center':

        pp = PP.Preprocessor()
        pp.train(X)
        D = pp.center(X)

    elif preprocessing is 'standardize':

        pp = PP.Preprocessor()
        pp.train(X)
        D = pp.standardize(X)

    elif preprocessing is 'whiten':

        pp = PP.Preprocessor()
        pp.train(X)
        D = pp.whiten(X)



    train_error = 0

    for i in range(1,6):
        lr.train(D[I != i, :], t[I != i], optimization, learningrate, regularization)
        y[I == i] = lr.predict(D[I == i, :])
        train_error += lr.loss

    valid_error = np.mean(np.abs(y-t),axis=0,dtype=np.float64)
    train_error = train_error/5

    return train_error, valid_error
