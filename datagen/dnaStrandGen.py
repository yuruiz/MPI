#! /usr/bin/python
import sys
import csv
import random

STRAND_DIIF_MIN = 0

def strandGen(dna, varlen, size):
    dnaLen = len(dna)

    retStrands = []
    for y in xrange(size):
        retStrand = ''
        indexToChange = random.sample(xrange(dnaLen), varlen)
        for x in xrange(dnaLen):
            if x in indexToChange:
                retStrand += random.choice('ACGT'.replace(dna[x], ''))
            else:
                retStrand += dna[x]
        retStrands.append(retStrand)

    return retStrands

def diff(str1, str2):
    strlen = len(str1)
    diffcount = 0

    for x in xrange(strlen):
        if str1[x] != str2[x]:
            diffcount += 1

    return diffcount

def centroidValid(point, centroids):
    for centroid in centroids:
        if diff(point, centroid) < STRAND_DIIF_MIN:
            return False
    return True

def genCentroid(length):
    centroid = ''

    for x in xrange(length):
        centroid += random.choice('ACGT')

    return centroid

def getCentroid(k, length):
    centroids = []
    variance = []

    for x in xrange(k):
        while True:
            centroid = genCentroid(length)
            if centroidValid(centroid, centroids):
                break
        centroids.append(centroid)
        variance.append(int(random.uniform(STRAND_DIIF_MIN/2, STRAND_DIIF_MIN)))

    return centroids, variance


def usage():
    print "Usage: %s <k> <length> <Num> <output_file>" % sys.argv[0]
    print "k: number of centroid"
    print "length: lengh of strands"
    print "Num: number of strands each centroid"


if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
        exit(0)

    centroids = []
    variance = []
    count = []
    k = int(sys.argv[1])
    length = int(sys.argv[2])
    num = int(sys.argv[3])
    outputname = sys.argv[4]

    STRAND_DIIF_MIN = length / 2

    centroids, variance = getCentroid(k, length)
    outputdata = []
    for x in xrange(len(centroids)):
        outputdata.extend(strandGen(centroids[x], variance[x], num))

    outputfile = open(outputname, 'w')
    for line in outputdata:
        outputfile.write(line+'\n')

    centroidOutputfile = open("Centroid_" + outputname, 'w')

    for line in centroids:
        centroidOutputfile.write(line + '\n')