#! /usr/bin/python
import sys
import csv
import random
from operator import itemgetter

MAX_ITER = 100000

MIN_DIFF = 0


def kmeas(k, dataset):

    if dataset == None:
        return None

    # Get the length of DNA strand
    numFeature = len(dataset[0])

    # Pick random centroids set from the DNA strands
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

    setSize = len(dataset)

    # Pick centroids from the Dataset
    for x in xrange(k):
        index = 0
        while True:
            index = random.randrange(setSize)
            # Centroids must be different enough
            if validCentroid(dataset[index], centroids):
                break
        # print dataset[index]
        centroids.append(dataset[index])
    # print "**********"

    return centroids

def validCentroid(strand, centroids):
    for centroid in centroids:
        # if the two Strands too similar, retur False
        if diff(centroid, strand) <= MIN_DIFF:
            return False
    return True

# calculate the difference of the two strand
def diff(str1, str2):
    strlen = len(str1)
    diffcount = 0

    for x in xrange(strlen):
        if str1[x] != str2[x]:
            diffcount += 1

    return diffcount

# Calculate the center of each DNA cluster
def calCentroid(dataset, labels, k):
    numFeature = len(dataset[0])

    clusterList = [[] for x in xrange(k)]

    # Assign the strands of same cluster to the one list
    for x in xrange(len(dataset)):
        clusterList[labels[x]].append(list(dataset[x]))

    CharMap = ['A', 'C', 'G', 'T']
    centroids = []

    # Calculate the Centroids for each cluster
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

    numFeature = len(datasets[0])
    MIN_DIFF = numFeature / 2 + 1

    centroids = kmeas(k, datasets)
    for centroid in centroids:
        print centroid


