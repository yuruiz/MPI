#! /usr/bin/python
import math
import sys
import csv
import random
from operator import itemgetter

MAX_ITER = 100000

MIN_DIFF = 8


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

    setSize = len(dataset)

    print setSize

    for x in xrange(k):
        index = 0
        while True:
            index = random.randrange(setSize)
            if validCentroid(dataset[index], centroids):
                break
        centroids.append(dataset[index])

    return centroids

def validCentroid(strand, centroids):
    for centroid in centroids:
        if diff(centroid, strand) <= MIN_DIFF:
            return False
    return True

def diff(str1, str2):
    strlen = len(str1)
    diffcount = 0

    for x in xrange(strlen):
        if str1[x] != str2[x]:
            diffcount += 1

    return diffcount


def calCentroid(dataset, labels, k):
    numFeature = len(dataset[0])

    clusterList = [[] for x in xrange(k)]

    for x in xrange(len(dataset)):
        clusterList[labels[x]].append(list(dataset[x]))

    CharMap = ['A', 'C', 'G', 'T']
    centroids = []

    for x in xrange(k):
        centroid = ''
        components = zip(*clusterList[x])
        for y in xrange(numFeature):
            charCount = []
            charCount.append(components[y].count('A'))
            charCount.append(components[y].count('C'))
            charCount.append(components[y].count('G'))
            charCount.append(components[y].count('T'))

            centroid += CharMap[charCount.index(max(charCount))]
        centroids.append(centroid)

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
            templist.append(diff(data, centroid))
        labellist.append(min(enumerate(templist), key=itemgetter(1))[0])
    return labellist

def usage():
    print "Usage: %s <k> <datafilename>" % sys.argv[0]



if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit(0)

    k = int(sys.argv[1])
    filename = sys.argv[2]

    datasets = []
    with open(filename, 'rb') as datafile:
        datalines = csv.reader(datafile)
        for dataline in datalines:
            datasets.extend(dataline)

    centroids = kmeas(k, datasets)
    print centroids


