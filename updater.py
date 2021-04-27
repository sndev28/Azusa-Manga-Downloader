import requests
import sys

version_code = sys.argv[1]

new_version_code = requests.get('https://drive.google.com/uc?export=download&id=1BKHZ1c_S6xVWwf_LE_prBqGa8X3M6BVH').text

if new_version_code != version_code:
    print('Downloading update!')

else:
    print('No available update!')
    
