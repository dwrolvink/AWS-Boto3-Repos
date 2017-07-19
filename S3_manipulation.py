import os
import boto3

#
# S3 Manipulation.py
# ------------------
# Create bucket, upload a file to it, 
# set that file to public, return the download link for that file
#
#

bucket_name = 'bb1mb'
file_name = 'bla.jpg'
file_folder_location = 'C:\\Users\\dwrol\\Desktop\\temp\\'

# Nice UI function
def PrintResult(response):
	if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
		print ' - Done'
	else:
		print ' - Failed'
		print response['ResponseMetadata']
	print ''
	

############# Header #######################

# Clear the screen
os.system("cls")

# Mission objective
print 'S3-M4N!PUL4T0R3000 by DWR' + "\n"

print 'Objectives:'
print ' - Create bucket "' + bucket_name + '"'
print ' - Upload file "' + file_name + '"'
print ' - Set file to public'
print ' - Print out file link'
print ''


############# Init ################################
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')



#####++++++++ ROLL UP ++++++++#######
############# Create Bucket #######################
# Create a bucket using a client
print 'Creating bucket...'
response = s3_client.create_bucket(Bucket=bucket_name)
PrintResult(response)
exit()



############# List Buckets #######################
# # Print out bucket names
# print 'Buckets:'
# for bucket in s3_resource.buckets.all():
    # print(bucket.name)
# print ''

############ Upload file #################
# Upload a new file in the new bucket
data = open(file_folder_location+file_name, 'rb') # read-only (r), load bites (b)
s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data)

############ List Objects + extra ########################
# # List all objects in the new bucket
# print 'Items in ' + bucket_name + ":"
# for object in s3_resource.Bucket(bucket_name).objects.all():
    # print(object)
# print ''

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

# UI feedback
if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
	print ' - Done'
else:
	print ' - Failed'
	print response['ResponseMetadata']
print ''

########### List ########################
# # Get file acl (check)
# print 'ACL of ' + file_name + ':'
# result = s3_client.get_object_acl(Bucket=bucket_name, Key=file_name)
# print(result)
# print ''

# Print out file link
print 'Download link ' + file_name + ':'
print 'https://s3.amazonaws.com/' + bucket_name + '/' + file_name

####++++++ ROLL DOWN ++++#####
print 'Deleting bucket...'
bucket = s3_resource.Bucket(bucket_name)
for key in bucket.objects.all():
	key.delete()
bucket.delete()
print ' - Done'




