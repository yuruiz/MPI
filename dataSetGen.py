#! /usr/bin/python
import random
import sys
import csv

def generate(mu, sigma, num):
    ret = []
    for x in xrange(num):
        temp = []
        for x in mu:
            temp.append(random.gauss(x, sigma))
        print temp
        ret.append(temp)

    # print ret
    return ret

def usage():
    print "Usage: %s <config file path> <output file>", sys.argv[0]
    print "config file line example: "
    print "x_coordinate, y_coordinate, sigma, centroid size"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit(0)

    centroids = []
    sigma = []
    count = []
    filename = sys.argv[1]
    outputname = sys.argv[2]

    with open(filename, 'rb') as centroidfile:
        centroidlines = csv.reader(centroidfile)
        for centroidline in centroidlines:
            if len(centroidline) != 4:
                continue
            centroids.append([int(centroidline[0]), int(centroidline[1])])
            sigma.append(float(centroidline[2]))
            count.append(int(centroidline[3]))

    outputdata = []
    for x in xrange(len(centroids)):
        outputdata.extend(generate(centroids[x], sigma[x], count[x]))

    with open(outputname, 'wb') as outputfile:
        output = csv.writer(outputfile)
        output.writerows(outputdata)