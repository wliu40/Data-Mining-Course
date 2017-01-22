from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

''' input the row number and column number, 
    fun() will compute the value of gamma
    row represents the number of random points generated;
    col represents the dimensions
'''
def fun(row, col):
    arr = np.random.randint(0, 100, size = (row, col))
    max_value = np.iinfo(np.uint32).min
    min_value = np.iinfo(np.uint32).max
    gamma = 0
    for i in range(row):
        for j in range(i+1, row):
            #dis = np.sqrt(sum(np.square(arr[i]-arr[j])))
            dis = sum(np.absolute(arr[i]-arr[j]))
            if dis > max_value:
                max_value = dis
            if dis < min_value:
                min_value = dis
                
    try:        
        gamma = np.log10((max_value-min_value)/float(min_value))
    except ZeroDivisionError:
        print 'Division is zero!'

    return gamma

def main():    
    dims = np.arange(2,100,10)
    ns = np.arange(10,1100,100)

    row_cnt = len(dims)
    col_cnt = len(ns)
    gammas = np.zeros((row_cnt, col_cnt), float)  
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(ns, dims)
    
    for i in range(col_cnt):
        for j in range(row_cnt):
            gammas[j][i] = fun(X[j][i],Y[j][i])

    surf = ax.plot_surface(X, Y, gammas, rstride=1, cstride=1, cmap=cm.coolwarm,
                     linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_zlim(-1.01, 1.01)
    ax.set_title('gamma as function of n and d')
    ax.set_xlabel('points count')
    ax.set_ylabel('dimensions')
    ax.set_zlabel('gamma value')
    plt.show()


if __name__ == '__main__':
    main()