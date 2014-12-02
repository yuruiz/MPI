#! /usr/bin/python
import sys
import csv
import random

def strandGen(dna, varlen, size):
    dnaLen = len(dna)
    indexToChange = random.sample(xrange(dnaLen), varlen)

    retStrands = []
    for y in xrange(size):
        retStrand = ''
        for x in xrange(dnaLen):
            if x in indexToChange:
                retStrand += random.choice('ACGT'.replace(dna[x], ''))
            else:
                retStrand += dna[x]
        retStrands.append(retStrand)

    return retStrands

def usage():
    print "Usage: %s <config file path> <output file>", sys.argv[0]
    print "config file line example: "
    print "original Strand, differencelen, centroid size"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit(0)

    centroids = []
    variance = []
    count = []
    filename = sys.argv[1]
    outputname = sys.argv[2]

    with open(filename, 'rb') as centroidfile:
        centroidlines = csv.reader(centroidfile)
        for centroidline in centroidlines:
            if len(centroidline) != 3:
                continue
            centroids.append(centroidline[0])
            variance.append(int(centroidline[1]))
            count.append(int(centroidline[2]))

    print centroids
    print variance
    print count
    outputdata = []
    for x in xrange(len(centroids)):
        outputdata.extend(strandGen(centroids[x], variance[x], count[x]))

    outputfile = open(outputname, 'w')
    for line in outputdata:
        outputfile.write(line+'\n')