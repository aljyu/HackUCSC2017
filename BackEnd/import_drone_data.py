#!/usr/bin/python

#from pexpect import pxssh
#import pysftp
import paramiko
import os
import csv
import sys
import time

DRONE_CONTENT = []

# SSH into Drone
def ssh_drone():
    HOST = "unix.ucsc.edu"
    USER = ""
    PASS = ""
    PORT = 22
    # Try to connect to the host.
    # Retry a few times if it fails.
    i = 1
    while True:
        print "Trying to connect to %s (%i/30)" % (HOST, i)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(HOST, port=PORT, username=USER, password=PASS)
            print "Connected to %s" % host
            break
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % HOST
            sys.exit(1)
        except:
            print "Could not SSH to %s, waiting for it to start" % HOST
            i += 1
            time.sleep(2)
        # If we could not connect within time limit
        if i == 30:
            print "Could not connect to %s. Giving up" % HOST
            sys.exit(1)    
    # Send the command (non-blocking)
    stdin, stdout, stderr = ssh.exec_command("ls -l")
    # Wait for the command to terminate
    while not stdout.channel.exit_status_ready():
        # Only print data if there is data to read in the channel
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                # Print data from stdout
                print stdout.channel.recv(1024),
    # Disconnect from the host
    print "Command done, closing SSH connection"
    ssh.close()        

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
    #drone_content = [['45ADGS324D', '34242','54325','Found'],['45FDSS324D', '3423212','5442342325','Not Found']]
    #store_local_db(drone_content)
    ssh_drone()

if __name__=="__main__":
    Main()
