#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, random, math, time
from multiprocessing import Pool
import math



class Example(object):
    map = []

    def __init__(self, x, y, fl=2):
        self.X_S = x
        self.Y_S = y
        self.fl = fl
        self.generate(x, y, fl)

    def generate(self, x, y, fl):
        for i in range(y):
            self.map.append([])
            for j in range(x):
                self.map[i].append({"busy": not bool(random.getrandbits(fl))})
                if self.map[i][j]["busy"]:
                    self.map[i][j]["staf"] = random.getrandbits(4)


def runtest(obj, a=0, b=1):
    for j in range(len(obj)):
        if obj[j]["busy"]:
            obj[j] = math.factorial(j)

    obj[0]=a
    
    return(obj)



if __name__ == '__main__':
    start_time = time.time()
    print("Let's start")

    wld = Example(1640, 1640)
    TREADS = 4
    Multi=True
    pool = Pool(processes=TREADS)

 
    # for i in range(len(wld.map)):
    #     print(wld.map[i])
    # print(" \n")

    
    if Multi:
        arguments = [(wld.map[i],i,TREADS) for i in range(len(wld.map))]
        wld.map = pool.starmap(runtest,arguments)

    else:
        for i in range(len(wld.map)):
            wld.map[i]=runtest(wld.map[i],i)
    


    print("--- %s seconds ---" % (time.time() - start_time))

# -------Print wld.map--------test for correct order
    print("\n Last result")
    for i in range(len(wld.map)):
        if i!=wld.map[i][0]: print("NO SYNC!!!! ",i,wld.map[i][0])
