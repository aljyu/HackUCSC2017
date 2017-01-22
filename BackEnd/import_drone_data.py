#!/usr/bin/python

#from pexpect import pxssh
#import pysftp
import os
import csv

DRONE_CONTENT = []

# SSH into Drone
def ssh_drone():
    HOST = "xxx"
    USER = "xxx"
    PASS = "xxx"
    global DRONE_CONTENT
 #   s = pxssh.pxssh()
 #   if not s.login(HOST, USER, PASS):
 #       s.sendline('ls -l')
 #       s.prompt()
 #       print s.before
 #       s.logout()
 #   with pysftp.Connection(HOST, username=USER, password=PASS) as sftp:
 #       try:
 #           sftp.listdir()
 #       except UnicodeEncodeError as e:
 #           print e
       # with sftp.cd('public'):             # temporarily chdir to public
       #     sftp.put('/my/local/filename')  # upload file to public/ on remote
       #     sftp.get('remote_file')         # get a remote file
    DRONE_CONTENT = CONTENT

# Retrieve MAC Address from Drone
def retrieve_mac():
    # Issue 1: Does not delete entry, continue to pull same value
    PATH = "C:\Users\dnalex\Desktop"
    GEOFILE = "mac_geolocation.csv"
    CONTENT = []
    os.chdir(PATH)
    try:
        with open(GEOFILE, 'rb') as csvfile:
            table = csv.reader(csvfile)
            for row in table:
                CONTENT.append(row)
    except IOError as e:
        print "IOError: " + str(e)
    except Exception as e:
        print "Exception: " + str(e)
    return CONTENT
    
# Store into Local DB/File
# Takes in list with entries pertaining to respective row
def store_local_db(drone_content):
    # Issue 1: Does not account for previous results; i.e. duplicates
    col_names = ['MAC Address', 'Longitude', 'Latitude','Status']
    with open('geo_contents.csv', 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=col_names)
        csvwriter.writeheader()
        for x in drone_content:
            csvwriter.writerow({col_names[0]:x[0],\
                             col_names[1]:x[1],\
                             col_names[2]:x[2],\
                             col_names[3]:x[3]})

# Connect to App Engine SQL
#def connect_sql():
#    @TODO
    
# Send to App Engine SQL
#def send_google_sql():
#    @TODO
    
def Main():
    # 1. SSH into Drone
    # 2. Open Geolocation file
    # 3. Get contents of mac addresses to geo-location
    # 4. Dump contents into local device
    # 5. Connect to App Engine SQL
    # 6. Store into App Engine SQL
    drone_content = [['45ADGS324D', '34242','54325','Found'],['45FDSS324D', '3423212','5442342325','Not Found']]
    store_local_db(drone_content)

if __name__=="__main__":
    Main()