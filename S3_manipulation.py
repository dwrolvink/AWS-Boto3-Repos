import os, sys
import boto3

#
# S3 Manipulation.py
# ------------------
# Create bucket, upload a file to it, 
# set that file to public, return the download link for that file
#
#


# Setup settings
bucket_name = 'bb1mb'
file_name = 'par.png'
file_folder_location = 'C:\\Users\\dwrol\\Desktop\\temp\\'
# Setup bucket with file, or delete bucket ("create', "destroy")
RunMode = "notSet"


# Load CMD variables
if len(sys.argv) > 1:
	RunMode = sys.argv[1]
	
if RunMode not in ['create', 'destroy']:
	print "\n ERROR: \n - Add runmode argument after filename <create, destroy> (e.g.: python file.py create)"
	exit()
	
# Nice UI function
def PrintResult(response, newline=True):
	httpCode = response['ResponseMetadata']['HTTPStatusCode']
	if (httpCode == 200):
		print ' - Done'
	else:
		if httpCode == 204:
			print ' - 204: dryRun response'
			print ' - Done'
			
		elif httpCode > 200 and httpCode < 300:
			print response['ResponseMetadata']
			print ' - Done' 
			
		else:
			print response['ResponseMetadata']
			print ' - Failed'
			
	if(newline):
		print ''
	

############# Header #######################

# Clear the screen
os.system("cls")

# Mission objective
print 'S3-M4N!PUL4T0R3000 by DWR' + "\n"

print 'Run mode:'
print ' - {} \n'.format(RunMode.capitalize())

print 'Objectives:'
if RunMode == 'create':
	print ' - Create bucket "' + bucket_name + '"'
	print ' - Upload file "' + file_name + '"'
	print ' - Set file to public'
	print ' - Print out file link'
else:
	print ' - Delete bucket "{}" and all it\'s children'.format(bucket_name)
print ''


############# Init ################################
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')



#####++++++++ ROLL UP ++++++++#######
if RunMode == 'create':
	############# Create Bucket #######################
	# Create a bucket using a client
	print 'Creating bucket...'
	response = s3_client.create_bucket(Bucket=bucket_name)
	PrintResult(response)



	############# List Buckets #######################
	# Print out bucket names
	print 'Buckets:'
	for bucket in s3_resource.buckets.all():
		print ' - {}'.format(bucket.name)
	print ''

	############ Upload file #################
	# Upload a new file in the new bucket
	print 'Uploading file....'
	data = open(file_folder_location+file_name, 'rb') # read-only (r), load bites (b)
	response = s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data)
	if response:
		print ' - {}'.format(response)
		print ' - Done \n'
	else:
		print ' - Failed'

	############ List Objects + extra ########################
	# # List all objects in the new bucket
	print 'Items in ' + bucket_name + ":"
	for object in s3_resource.Bucket(bucket_name).objects.all():
		print ' - {}'.format(object.key)
	print ''

	# # Get bucket acl
	# print 'ACL of ' + bucket_name + ':'
	# result = s3_client.get_bucket_acl(Bucket=bucket_name)
	# print(result)
	# print ''

	# # Get file acl
	# print 'ACL of ' + file_name + ':'
	# result = s3_client.get_object_acl(Bucket=bucket_name, Key=file_name)
	# print(result)
	# print ''

	############ Edit file ###################
	# Set uploaded file to public
	print 'Setting ' + file_name + ' to public...'
	response = s3_client.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=file_name)
	PrintResult(response)

	########### List ########################
	# # Get file acl (check)
	# print 'ACL of ' + file_name + ':'
	# result = s3_client.get_object_acl(Bucket=bucket_name, Key=file_name)
	# print(result)
	# print ''

	# Print out file link
	print 'Download link ' + file_name + ':'
	print 'https://s3.amazonaws.com/' + bucket_name + '/' + file_name + '\n'

####++++++ ROLL DOWN ++++#####
elif RunMode == 'destroy':
	print 'Deleting bucket...'
	bucket = s3_resource.Bucket(bucket_name)
	for key in bucket.objects.all():
		key.delete()
	response = bucket.delete()
	PrintResult(response)




