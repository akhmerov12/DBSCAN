import numpy as np
from sklearn.manifold import TSNE
import numpy.random as random
from  numpy.core.fromnumeric import *
import matplotlib.pyplot as plt

def calDist(X1 , X2 ):
   sum = 0
   for x1 , x2 in zip(X1 , X2):
       sum += (x1 - x2) ** 2
   return sum ** 0.5

def getNeibor(data , dataSet , e):
   res = []
   for i in range(shape(dataSet)[0]):
       if calDist(data , dataSet[i])<e:
           res.append(i)
   return res

def DBSCAN(dataSet , e , minPts):
   coreObjs = {}
   C = {}
   n = shape(dataSet)[0]
   for i in range(600):
       neibor = getNeibor(dataSet[i] , dataSet , e)
       if len(neibor)>=minPts:
           coreObjs[i] = neibor
   oldCoreObjs = coreObjs.copy()
   k = 0
   notAccess = list(range(n))
   while len(coreObjs)>0:
       OldNotAccess = []
       OldNotAccess.extend(notAccess)
       cores = coreObjs.keys()
       randNum = random.randint(0,len(cores))
       cores=list(cores)
       core = cores[randNum]
       queue = []
       queue.append(core)
       notAccess.remove(core)
       while len(queue)>0:
           q = queue[0]
           del queue[0]
           if q in oldCoreObjs.keys() :
               delte = [val for val in oldCoreObjs[q] if val in notAccess]
               queue.extend(delte)
               notAccess = [val for val in notAccess if val not in delte]
       k += 1
       C[k] = [val for val in OldNotAccess if val not in notAccess]
       for x in C[k]:
           if x in coreObjs.keys():
               del coreObjs[x]
   #C[k + 1] = [val for val in notAccess]
   return C

def loadDataSet(filename):
   dataSet = []
   fr = open(filename)
   i = 0
   for line in fr.readlines():
       curLine = line.strip().split(", ")
       fltLine = map(float, curLine)
       dataSet.append(list(fltLine))
       i += 1
   return dataSet

def draw(C , dataSet):
   color = ['black', 'grey', 'red', 'navy', 'maroon', 'coral', 'gold', 'khaki', 'olive', 'deeppink', 'lightseagreen', 'silver', 'yellow',
            'green', 'lime', 'blue', 'beige',  'aqua', 'teal', 'orchid', 'skyblue', 'slateblue', 'magenta', 'lavender', 'cornflowerblue', 'violet']
   for i in C.keys():
       X = []
       Y = []
       datas = C[i]
       for j in range(len(datas)):
           X.append(dataSet[datas[j]][0])
           Y.append(dataSet[datas[j]][1])
       plt.scatter(X, Y, marker='o', color=color[i % len(color)], label=i)
   plt.legend(loc='upper right')
   plt.show()

def count_accuracy(C):
   first_cluster = 0
   second_cluster = 0
   third_cluster = 0
   for i in C.keys():
       print(len(C[i]))
       first_cluster_counter = 0
       second_cluster_counter = 0
       third_cluster_counter = 0
       for j in range(len(C[i])):
           if C[i][j] < 200:
               first_cluster_counter += 1
           elif C[i][j] >= 400:
               third_cluster_counter += 1
           else:
               second_cluster_counter += 1
       if first_cluster_counter > third_cluster_counter and first_cluster_counter > second_cluster_counter:
           first_cluster += first_cluster_counter
       elif third_cluster_counter > first_cluster_counter and third_cluster_counter > second_cluster_counter:
           third_cluster += third_cluster_counter
       else:
           second_cluster += second_cluster_counter
       print(first_cluster / 2)
       print(second_cluster / 2)
       print(third_cluster / 2)

def main():
    big = []
    small = np.load('new_data_big_6.npy')
    C = DBSCAN(small, 4.1, 4)
    count_accuracy(C)
    draw(C, small)

if __name__ == '__main__':
    main()
