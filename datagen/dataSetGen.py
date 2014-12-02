#! /usr/bin/python
import random
import math
import sys
import csv

CENTROID_INTERVAL = 5
CENTROID_RANGE = 50

def distance(point1, point2):
    numFeature = len(point1)

    SquareSum = 0

    for x in xrange(numFeature):
        SquareSum += (point1[x] - point2[x])**2

    return math.sqrt(SquareSum)

def centroidValid(point, centroids):
    for centroid in centroids:
        if distance(point, centroid) < CENTROID_INTERVAL:
            return False
    return True

def genCentroid():
    centroid = []
    centroid.append(random.uniform(CENTROID_RANGE * -1, CENTROID_RANGE))
    centroid.append(random.uniform(CENTROID_RANGE * -1, CENTROID_RANGE))
    return centroid

def getCentroid(k):
    sigma = []
    centroids = []

    for x in xrange(k):
        while True:
            centroid = genCentroid()
            if centroidValid(centroid, centroids):
                break
        centroids.append(centroid)
        sigma.append(random.gauss(CENTROID_INTERVAL, 1))

    return centroids, sigma


def generate(mu, sigma, num):
    ret = []
    for x in xrange(num):
        temp = []
        for x in mu:
            temp.append(random.gauss(x, sigma))
        # print temp
        ret.append(temp)

    # print ret
    return ret

def usage():
    print "Usage: %s <k> <Num> <output file>" % sys.argv[0]
    print "k: number of centroid"
    print "Num: number of points each centroid"

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
        exit(0)

    centroids = []
    sigma = []
    count = []
    k = int(sys.argv[1])
    Num = int(sys.argv[2])
    outputname = sys.argv[3]

    centroids, sigma = getCentroid(k)

    outputdata = []
    for x in xrange(len(centroids)):
        outputdata.extend(generate(centroids[x], sigma[x], Num))

    with open(outputname, 'wb') as outputfile:
        output = csv.writer(outputfile)
        output.writerows(outputdata)

    with open("Centroid_" + outputname, 'wb') as centroidOutputfile:
        Centroidoutput = csv.writer(centroidOutputfile)
        Centroidoutput.writerows(centroids)