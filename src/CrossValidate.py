import pandas as pd
import numpy as np
import math
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
        chunk = l[math.ceil(i*n/k):math.ceil((i+1)*n/k)-1]    #get the next block of random indices
        dataset.loc[chunk,'kset'] = i+1       #label 'kset' column
        
    dataset.to_csv(f.replace(".csv","")+"_training_"+str(k)+"-fold.csv")
