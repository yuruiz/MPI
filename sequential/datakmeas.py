#! /usr/bin/python
import math
import sys
import csv
import random
from operator import itemgetter

MAX_ITER = 100000

# Kmeas calculation
def kmeas(k, dataset):

    if dataset == None:
        return None

    # Get the Feature Number of the dataset
    numFeature = len(dataset[0])

    # Pick random centroids set from the dataset value range
    centroids = generateCentroid(dataset, k)

    iterCount = 0
    lastCentroids = None

    # Start Iteration, Iteration would stop if the stop condition is satisfied
    while not stopIteration(centroids, lastCentroids, iterCount):

        # Count the Iteration number
        iterCount += 1
        lastCentroids = centroids

        # Assign data in dataset to each centroid
        labels = assignLable(dataset, centroids)

        # Calculate new centroid based on current data assignment
        centroids = calCentroid(dataset, labels, k)

    return centroids


def generateCentroid(dataset, k):
    centroids = []
    maxCom = []
    minCom = []


    numFeature = len(dataset[0])

    components = zip(*dataset)

    # Get the value range for each feature
    for component in components:
        maxCom.append(int(max(component)))
        minCom.append(int(min(component)))

    # Generate random centroids
    for x in xrange(k):
        centroid = []
        for y in xrange(numFeature):
            centroid.append(random.uniform(minCom[y], maxCom[y]))

        centroids.append(centroid)

    return centroids


def calCentroid(dataset, labels, k):
    numFeature = len(dataset[0])
    clusterList = [[0 for y in xrange(numFeature)] for x in xrange(k)]
    clusterCount = [0 for x in xrange(k)]
    centroids = [[0 for y in xrange(numFeature)] for x in xrange(k)]

    # Calculate the sum of the data in each cluster in each dimension
    for x in xrange(len(dataset)):
        cluster = clusterList[labels[x]]
        data = dataset[x]
        clusterCount[labels[x]] += 1
        for y in xrange(numFeature):
            cluster[y] += data[y]

    # Calculate the average of each cluster data as the new centroid
    for x in xrange(k):
        for y in xrange(numFeature):
            if clusterCount[x] == 0:
                break
            centroids[x][y] = clusterList[x][y] / clusterCount[x]

    return centroids

# if Iteration counts beyond MAX_ITER or the current centroids are equal to
# old centroids, then stop the Iteration
def stopIteration(centroids, lastCentroids, iterCount):
    if iterCount > MAX_ITER:
        return True

    return centroids == lastCentroids

# Assign Data to the centroid of closest distance
def assignLable(dataset, centroids):

    labellist = []

    for data in dataset:
        templist = []
        for centroid in centroids:
            templist.append(calDist(data, centroid))
        labellist.append(min(enumerate(templist), key=itemgetter(1))[0])
    return labellist


def usage():
    print "Usage: %s <k> <datafilename>" % sys.argv[0]


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
    for centroid in centroids:
        print centroid


