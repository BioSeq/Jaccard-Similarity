#!/usr/bin/env python
#
# spearmanCorrelation.py
# Author: Hannah DeBaets
# Date Created: 1/23/15
# Last Modified: 1/25/15
#
# EG: Invoke the script using: ./spearmanCorrelation.py Classification1 Classification2


from sys import argv
from sys import exit
from scipy import stats

classyFile1 = argv[1]
classyFile2 = argv[2]
lvl = 'Species'
minPct = float(0.1)

def main():
	if len(argv) != 3:
		usage()
	dictionary1 = accumulateApproved(classyFile1, lvl, minPct)
	dictionary2 = accumulateApproved(classyFile2, lvl, minPct)
	#print "Dictionary1", dictionary1
	#print "Dictionary2", dictionary2
	sample2 = addExtras(dictionary1, dictionary2, classyFile2)
	sample1 = addExtras(dictionary2, dictionary1, classyFile1)
	#print "Sample1", sample1
	#print "Sample2", sample2
	list1, list2 = makeLists(sample1, sample2)
	#print list1
	#print list2
	#print "List1", list1
	#print "List2", list2
	print stats.spearmanr(list1, list2)
	exit(0)


#prints usage and exits nonzero
def usage():
	print "USAGE:", argv[0], "Classification 1, Classification2"
	exit(1)

#create dictionaries of items above the lower percentage limit
#takes calssification file as input, with set level (genus, species, etc.)
#and minimum percent (1.0 = 1%, 0.5 = 0.5%)
#creates a dictionary of {genus or species: percentage present in sample}
def accumulateApproved(classyFile, lvl, minPct):
	sample = {}
	with open(classyFile, 'r') as filer:
		for line in filer:
			line = line.strip()
			col = line.split("\t")[2:]
			if col[0].startswith(lvl) and float(col[3])>=minPct:
				if col[1] != "Unclassified":
					sample[col[1]] = [col[3]]
	return sample

#adds groups that are present in the sample, but are at pcts less than the min
#value. Does not add groups that are not present in the sample, or have 0%.
def addExtras(sample1, sample2, classyFile2):
	for key in sample1:
		if key not in sample2:
			with open(classyFile2, 'r') as filer:
				for line in filer:
					line = line.strip()
					col = line.split("\t")[2:]
					if col[0].startswith(lvl) and col[1] == key:
						sample2[col[1]] = [col[3]]
	return sample2


#creates the lists that are representative of the classifications
#list1 = [pct0, pct1, pct2, pct3]  list2 = [pct0, pct1, pct2, pct3]
#pct0 for both relates to one group, pct1 relates to another, MUST MATCH
def makeLists(sample1, sample2):
	list1 = []
	list2 = []
	for key in sample1:
		if key in sample2:
			list1.append(sample1[key])
			list2.append(sample2[key])
		if key not in sample2:
			list1.append(sample1[key])
			list2.append(['0'])
	if len(list1) != len(list2):
		for key in sample2:
			if key not in sample1:
				list1.append(0)
				list2.append(sample2[key])
	return list1, list2
	



if __name__ == '__main__':
        main()