# import the dropbox library
import dropbox
import time

# read the acces token
access_token = open('app_token.txt').read()
print(access_token)

# Authenticate to Dropbox account

db = dropbox.Dropbox(access_token)

print('Successfully authenticated to Dropboxed owned by ' + db.users_get_current_account().name.display_name)

while True:
    db.files_download_to_file('heartdata.txt', '/IoT Project/heartdata.txt')
    db.files_download_to_file('stepsdata.txt', '/IoT Project/stepsdata.txt')
    db.files_download_to_file('activity.txt', '/IoT Project/activity.txt')
    time.sleep(25)
    
