# Log into an ArcGIS Online Organization and find all the disabled users.
# Count the number of items owned by each disabled user and print a list.
# 
# Requires: ArcGIS API for Python (https://developers.arcgis.com/python/)
#           Python 3.x
#
from arcgis.gis import GIS
from getpass import getpass
from operator import attrgetter

# Get username and password
username = input('Username: ')
password = getpass(prompt='Password: ')

# Connect to ArcGIS Online
try:
    gis = GIS("https://arcgis.com/", username, password)
except:
    print(sys.exc_info()[0])
    exit(1)

# Get a list of all users
try:
    all_users = gis.users.search(None, max_users=500)
except:
    print(sys.exc_info()[0])
    exit(1)

# Use list comprehension to create a subset list of disabled users
disabled_users = [user for user in all_users if user.disabled == True]

# Items are either in a folder or not. The latter are called root items. There can only be one folder level, so only one level needs to be traversed.
for user in sorted(disabled_users, key=attrgetter('lastName', 'firstName')):
    print(user.fullName + " (" + user.username + ")")

    # user.items() returns a list of root items.
    # Exception will occur if logged in user doesn't have permission to access user.items()
    try:
        total_items = len(user.items())
    except:
        print(sys.exc_info()[0])
        exit(1)

    print("Root items: %s" % str(total_items))
    # user.folders returns a list of folders
    folders = user.folders
    print("Folders: %s" % str(len(folders)))
    for folder in folders:
        # The folder parameter on user.items() returns a list of items in the given folder
        folder_items = len(user.items(folder = folder))
        print("Folder " + folder["title"] + " items:" + str(folder_items))
        total_items += folder_items

    print("Total items: %s" % str(total_items))
    print("=" * 25)

print("Total number of disabled users: %s" % str(len(disabled_users)))

exit(0)