

import sys


def extractInstanceIDs(file):
	inst_ids_list = []
	with open(file,"r") as f:
		for line in f.readlines(): 
			# split by commas
			# Only works if all instances IDs are on a single line
			# If there are multiple instance IDs and separated by ','
			# The last entry in the list coming up with '\n', so do rstrip to erase '\n' before splitting
			print (line)
			if ',' in line:
				inst_ids_list = line.rstrip('\n').split(',')
			else:
				# If there is only one instance ID in the file then split by '\n'
				inst_ids_list = line.rstrip('\n').split('\n')
		return inst_ids_list
	


