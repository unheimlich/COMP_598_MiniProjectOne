import pandas as pd
import numpy as np
import math
from src.LinearRegressor import LinearRegressor as LR
from src.LinearRegressor import Preprocessor as PP
__author__ = 'suzin'


def separateTestSet(f, x):                      # separates the original data set into x*100% test set and (1-x)100% training set.
    #'data\PartOne\OnlineNewsPopularity.csv'
    ds = pd.read_csv(f)
    
    testindices = np.random.randint(0,ds.shape[0]-1,np.floor(ds.shape[0]/x)) # get a random set of indices, size n/x

    ds.iloc[testindices].to_csv(f.replace(".csv","")+"_test.csv", index=False)  # create a new test set csv
    ds.drop(testindices).to_csv(f.replace(".csv","")+"_training.csv", index=False) # create a new training set csv


def kfoldlabel(f, k):                           # Divides the training set into k equal-sized subsets by 
                                                # adding a column of integers 1-k at the end indicating
                                                # to which of the k subset each example belongs.

    dataset = pd.read_csv(f.replace(".csv","")+"_training.csv")  #read the training set data

    n = dataset.shape[0]                        # gets the number of samples in the dataset
    l = list(range(0,n))                        # makes a list of integers from 0 to n-1
    np.random.shuffle(l)                        # shuffle
    dataset['kset'] = np.nan                    # add a blank column
    
    for i in range(0,k):
        chunk = l[int(math.ceil(i*n/k)):int(math.ceil((i+1)*n/k)-1)]    #get the next block of random indices
        dataset.loc[chunk,'kset'] = i+1         #label 'kset' column
        
    dataset.to_csv(f.replace(".csv","")+"_training_"+str(k)+"-fold.csv")


def runcrossval(optimization, regularization, learningrate, preprocessing):

    ds = pd.read_csv('data/PartTwo/DailyMailArticlePopularity_training_5-fold.csv')
    X = ds.values[:, 2:31]
    t = ds.values[:, 31]

    I = ds.values[:, 32]
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

    return train_error, valid_error, y, t

def test(optimization, regularization, learningrate, preprocessing):

    ds = pd.read_csv('data/PartOne/OnlineNewsPopularity_training.csv')
    X_train = ds.values[:, 1:30]
    t_train = ds.values[:, 30]
    #t_train = ds.as_matrix(60)

    ds = pd.read_csv('data/PartOne/OnlineNewsPopularity_test.csv')
    X_test = ds.values[:, 1:30]
    t_test = ds.values[:, 30]

    lr = LR.LinearRegressor()

    if preprocessing is '':

        D_test = X_test
        D_train = X_train

    elif preprocessing is 'center':

        pp = PP.Preprocessor()
        pp.train(X_train)
        D_test = pp.center(X_test)
        D_train = pp.center(X_train)

    elif preprocessing is 'standardize':

        pp = PP.Preprocessor()
        pp.train(X_train)
        D_test = pp.standardize(X_test)
        D_train = pp.standardize(X_train)

    elif preprocessing is 'whiten':

        pp = PP.Preprocessor()
        pp.train(X_train)
        D_test = pp.whiten(X_test)
        D_train = pp.whiten(X_train)

    lr.train(D_train, t_train, optimization, learningrate, regularization)

    y = lr.predict(D_test)

    test_error = np.mean(np.abs(y-t_test),axis=0,dtype=np.float64)

    return test_error, lr.w, y, t_test, lr.w
