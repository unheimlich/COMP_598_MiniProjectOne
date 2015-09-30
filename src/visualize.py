__author__ = 'andrew'
import matplotlib.pyplot as plt

def scatter(t,y,title):

    yM = y.max();
    tM = t.max();

    fig = plt.figure()
    ax = plt.gca()
    ax.set_ylim(100,yM)
    ax.set_xlim(1,tM)

    ax.scatter(t,y , c='blue', alpha=0.75, edgecolors='none')

    ax.set_yscale('log')
    ax.set_xscale('log')

    plt.xlabel('Shares')
    plt.ylabel('Predicted Shares')

    plt.title(title)

    ax.plot([1,10,100,1000,10000,100000,1e6],[1,10,100,1000,10000,100000,1e6], c='red')