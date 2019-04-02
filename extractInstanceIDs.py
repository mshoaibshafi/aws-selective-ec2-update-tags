

import sys


def extractInstanceIDs(file):
	inst_ids_list = []
	with open(file,"r") as f:
		for line in f.readlines(): 
			# split by commas
			# Only works if all instances IDs are on a single line
			inst_ids_list = line.split(',')
		return inst_ids_list
	


