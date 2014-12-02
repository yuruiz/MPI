#! /usr/bin/python
import math
import sys
import csv
import random
from operator import itemgetter

MAX_ITER = 100000


def kmeas(k, dataset):

    if dataset == None:
        return None

    numFeature = len(dataset[0])

    centroids = generateCentroid(dataset, k)

    iterCount = 0
    lastCentroids = None

    while not stopIteration(centroids, lastCentroids, iterCount):
        iterCount += 1
        lastCentroids = centroids

        labels = assignLable(dataset, centroids)

        centroids = calCentroid(dataset, labels, k)

    return centroids


def generateCentroid(dataset, k):
    centroids = []
    maxCom = []
    minCom = []


    numFeature = len(dataset[0])

    components = zip(*dataset)

    for component in components:
        maxCom.append(int(max(component)))
        minCom.append(int(min(component)))

    for x in xrange(k):
        centroid = []
        for y in xrange(numFeature):
            centroid.append(random.randrange(minCom[y], maxCom[y]))

    centroids.append(centroid)

    return centroids

def calCentroid(dataset, labels, k):
    numFeature = len(dataset[0])
    clusterList = [[0 for y in xrange(numFeature)] for x in xrange(k)]
    clusterCount = [0 for x in xrange(k)]
    centroids = [[0 for y in xrange(numFeature)] for x in xrange(k)]

    for x in xrange(len(dataset)):
        cluster = clusterList[labels[x]]
        data = dataset[x]
        clusterCount[labels[x]] += 1
        for y in xrange(numFeature):
            cluster[y] += data[y]

    for x in xrange(k):
        for y in xrange(numFeature):
            if clusterCount[x] == 0:
                break
            centroids[x][y] = clusterList[x][y] / clusterCount[x]

    return centroids

def stopIteration(centroids, lastCentroids, iterCount):
    if iterCount > MAX_ITER:
        return True

    return centroids == lastCentroids

def assignLable(dataset, centroids):

    labellist = []

    for data in dataset:
        templist = []
        for centroid in centroids:
            templist.append(calDist(data, centroid))
        labellist.append(min(enumerate(templist), key=itemgetter(1))[0])
    return labellist

def usage():
    print "Usage: %s <k> <datafilename>"


def calDist(data1, data2):
    disPart = 0

    for x in xrange(len(data1)):
        disPart += (data1[x] - data2[x])**2

    return math.sqrt(disPart)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit(0)

    k = int(sys.argv[1])
    filename = sys.argv[2]

    with open(filename, 'rb') as datafile:
        datalines = csv.reader(datafile)
        datasets = [[float(data) for data in dataline] for dataline in datalines]

    centroids = kmeas(k, datasets)
    print centroids


