import requests
import argparse
import glob
import os
import sys
from config import api_token, instance, working_dir, file_ext

# config - moved to a seperate config file, keeping it here in case of a changed mind.
#api_token = ''
#instance = ''
#working_dir = ''
#file_ext = ["png", "jpg", "jpeg", "gif"]

# defaults - not meant to be changed, but it could in theory work
unique_categories = False

if api_token == '':
    print('please set an api token!')
    sys.exit()
if instance == '':
    print('please set an instance!')
    sys.exit()

# command line argument(s)
parser = argparse.ArgumentParser(description='simple script for uploading emojis en masse to some types of fedi instances')
parser.add_argument('--category', help='the name of the category the emojis will belong to. (default: empty string, aka uncategorized)')
parser.add_argument('--directory', help='set a directory for the script to run in (default: current working dir)')
args = parser.parse_args()


# parsing category - if no category is set, then making sure that the category is set 1-by-1 per emojo
if args.category != None:
    if args.category == 'u':
        unique_categories = True
    else:
        category = args.category
else:
    category = ''
    
if args.directory != None:
    working_dir = args.directory
elif working_dir == '':
    working_dir = os.getcwd()
    
    

# testing
#print(args.category)

# i love dealing with trailing slashes
if not instance.endswith('/'):
    instance += '/'

# getting the list of images in the working directory
file_list = []
for ext in file_ext:
    file_list += glob.glob(os.path.join(working_dir, '*.' + ext))

# turning the images into a dictionary with name (key) and path (value)
emojos = {}
for emojo in file_list:
    dummy, ext = os.path.splitext(emojo)
    name = os.path.basename(emojo).replace(ext, '')
    emojos[name] = emojo

# confirmation prompt
print('the following files will be uploaded to ' + instance + ':')
for k,v in emojos.items():
    print(k + ' (' + v + ')')
if not unique_categories:
    print('they will be in the ' + category + ' category')
else:
    print('u\'ll be specifying a category seperately for each emojo.')
ans = input('is that oki with u :3 [y]')
if ans.lower() == 'y' or ans == '':
    print('yayyy')
else:
    print('ruh roh')
    sys.exit()
    
# uploading process. if they are unique categories, make sure that a category is reselectable without typing.

# initialize
if unique_categories:
    categories = {}

# upload function
def upload(emojo_name, image_path, cat):
    global api_token
    error = ''
    print(emojo_name)
    with open(image_path, 'rb') as img:
        print('uploading ' + emojo_name + '...')
        # i'm too lazy to rename the json variable to indicate it's not json being sent - yet i'm not too lazy to make this comment. curious.
        request_json = {'shortcode': emojo_name}
        if cat != '':
            request_json['category'] = cat
        
        # this was me fucking around and failing
        """files = {'image': img}
        response = requests.post(
        url= instance + "api/v1/admin/custom_emojis",
        headers={"Authorization": "Bearer " + api_token, 'content-type': "multipart/form-data"},
        json=request_json,
        files=files
        )"""
        
        # thanks to https://stackoverflow.com/questions/47162039/sending-image-over-post-request-with-python-requests
        files= {'image': (os.path.basename(image_path),img,'multipart/form-data',{'Expires': '0'}) }
        with requests.Session() as s:
            r = s.post(instance + "api/v1/admin/custom_emojis", headers={"Authorization": "Bearer " + api_token} ,files=files, data=request_json)
            print('response:')
            print(r.status_code)
            print(r.text)
            if r.status_code != 200:
                error = str(r.status_code) + ': ' + r.text

        #print('response:')
        #print(response.status_code)
        #print(response.text)
    return error

errors = {}
# loop it all
cat_i = 1
for k, v in emojos.items():
    if unique_categories:
        # build a categories dict so categories are easily reusable
        print()
        print('choose a category for ' + k + '.')
        if cat_i > 1:
            print('you can select one of the following as categories now by typing a number:')
            for e_i, e_cat in categories.items():
                print(str(e_i) + ': ' + e_cat)
        cat = input('you can also quit if you type \'exit\'. ') # cat egory meow
        if cat.lower() == 'exit':
            sys.exit()
        elif cat.isdigit():
            cat = categories[int(cat)]
        else:
            categories[cat_i] = cat
            cat_i += 1
    else:
        cat = category
    error = upload(k, v, cat)
    if error != '':
        errors[k] = error
print()
print('the following errors have occured:')
for k, v in errors.items():
    print(k + ': ' + v)
