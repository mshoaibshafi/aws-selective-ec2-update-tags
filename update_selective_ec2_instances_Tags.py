# This program will read list of ec2 instances' IDs from the file and will add or update tags if needed

import boto3,sys,os
from pprint import pprint 
from extractTagKeysValues import extractTagKeysValues
from extractInstanceIDs import extractInstanceIDs

ec2 = boto3.client('ec2')
response = ec2.describe_instances()

# Data File : instance IDs file
# Contains : instances' IDs separated by commas
# Requirement : instances IDs must be on a single line

# Filename : instance-ids.file.txt or instance-ids.file.txt.sample
# Process : read instances ID one by one and update tags 
# For example : 
#				i-233lkadkw,i-ouoiu2ldadaf



# Data File : Tags key value file
# Purpose : all the tags and their prospective values are in the file with a syntax "tag_name = tag_value1,tag_value2,tag_value3 ...."
# Filename : tags.file.txt or tags.file.txt.sample
# Process : Read all Tags from the file, split by "=" and then by "," and create a list
# For example :
# 	account = production,dev,qa
# 	output list :
# 	account = [production,dev,qa]


# Only works with a single line of instances IDs
# TODO : allow to add instances' IDs on multiple comma separated lines

# instance_IDs_Data_file = "instance-ids.file.txt.sample" # Sample file included with Git
instance_IDs_Data_file = "instance-ids.file.txt"		# Your own file not in Git

# Tag_Data_file = "tags.file.txt.sample"	# Sample file included with Git
Tag_Data_file = "tags.file.txt"				# Your own file not in Git


# Check if Both Data Files exist before proceed further 

if not(os.path.isfile(instance_IDs_Data_file)):
	print ("\nData File Error ..... ")
	print ("\n\"{}\" >>>> Doesn't exist".format(instance_IDs_Data_file))
	print ("\nCreate this file and add ec2 instance IDs separated by comma on a single line ")
	print ("\n")
	sys.exit()

if not(os.path.isfile(Tag_Data_file)):
	print ("\nDate File Error ..... ")
	print ("\n\"{}\" >>>> Doesn't exist".format(Tag_Data_file))
	print ("Create this file and add Tag information")
	print ("\nFor example:")
	print ("\taccount = production,dev,qa")
	print ("\tstate = permanent,temporary")
	print ("\n")
	sys.exit()

Tag_Keys_Values = {}
# Call the function to extract Tags Key pair value from the tags.file.txt file
Tag_Keys_Values = extractTagKeysValues(Tag_Data_file)

# Convert instances-id.file into a list
Instance_IDs_List = []
Instance_IDs_List = extractInstanceIDs(instance_IDs_Data_file)

instanceTagDict = {}
for reservation in (response["Reservations"]):
	for instance in reservation["Instances"]:
		# Clear the instanceTagDict before using it otherwise it will show wrong / stale values 
		instanceTagDict.clear()

		# Verify if the instance ID is in the list, if yes then allow to update tags otherwise skip
		for i in range(0,len(Instance_IDs_List)):
			if instance["InstanceId"] == Instance_IDs_List[i]:
				# If instance ID matches
				# List current Tags of the instance
				for i in range(0,len(instance["Tags"])):
					instanceTagDict[instance["Tags"][i]['Key']] = instance["Tags"][i]['Value']
				# Display all current Tags
				print("\n------- instance ID {}".format(instance["InstanceId"]))
				pprint (instanceTagDict)
				resp = input ("\nDo you want to add Tags for this instance {}  ( y or yes ): ".format(instance["InstanceId"]))
				if resp.lower() == 'y' or resp.lower() == "yes":
					for k in Tag_Keys_Values.keys():
						print("Pick up a value for {} tag".format(k))
						for i in range(0,len(Tag_Keys_Values[k])):
							print ("{}: {}".format(i,Tag_Keys_Values[k][i]))
						print ("{}: {}".format(i+1,"skip"))
						resp_2 = int(input(": "))
						if resp_2 != i+1:
							ec2.create_tags(Resources=[instance["InstanceId"]], Tags=[{'Key':k, 'Value':Tag_Keys_Values[k][resp_2]}])
				else:
					# Clear the instanceTagDict before using it otherwise it will show wrong / old values 
					instanceTagDict.clear()
					continue
				input("Press Any Key to Continue ... \n")
			else:
				continue
