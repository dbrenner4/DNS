#!/usr/bin/env python
"""
Integration Team
 
DynECT API

9-CS-IGT Importing bulk zone files with the DynECT API in the Python Language.

Created by Jonathan Schultz - Integration Intern - Integration Team

Created 9/6/2012
Last Update 9/11/2012
"""

# Importing libraries.
import sys, os, time
from dynect.DynectDNS import DynectRest

# Calling the DynectRest Method.
rest_iface = DynectRest()

# Inputs from user for login to the DynECT API.
customer = raw_input("Enter your Customer Name: ")
username = raw_input("Enter your Username: ")
password = raw_input("Enter your password: ")
    
# Declaring the credentials for logging into the DynECT API.
login_arg = {
    'customer_name': customer,
    'user_name': username,
    'password': password,
    }
    
# Sending the POST command to the DynECT API for login proposes.
response = rest_iface.execute('/Session/', 'POST', login_arg)
    
# Checking to see if the Login to the DynECT API is successful.
if response['status'] != 'success':
    sys.exit("Incorrect credentials")
elif response['status'] == 'success':
    print 'Login Successful to DynECT API.'

# Inputs from user to path to Zone Files.
path = raw_input("Enter your path to your Zone Files: ")

# Going through the Zone Files Directory.
for zoneFileName in os.listdir(path):

    zone_path = os.path.join(path, zoneFileName)

    # Opening the Zone File.
    zone = open(zone_path, "r")
    
    # Reading in the Zone File.
    zone_file = zone.read()
    
    # Setting the arguments for the /ZoneFile/ Argument.
    zone_arg = {
            "file": zone_file
            }
    
    # Reading the Zone name from the Zone File.
    zone = open(zone_path, "r")
    
    # Reading the Zone File.
    zone_line = zone.readline()

    # Getting the first line of the Zone File.
    zone_line1 = zone_line[1:]

    # Removing the @ORIGIN from the first line of the Zone File.
    zone_line2 = zone_line1[7:]

    # Removing the period at the end of the first line in the Zone File.
    zone_name = zone_line2[:-2]
    
    # Creating the Zone File name.
    zone_name_arg = '/ZoneFile/%s' % zone_name

    zone_file1 = rest_iface.execute(zone_name_arg, 'POST', zone_arg)

    count1 = 0

    while(zone_file1['status'] != 'success') and (count1 < 10):
        print "Waiting for DynECT API..."
        # Sending the the POST command to the DynECT API for login proposes.
        zone_file1 = rest_iface.execute(zone_name_arg, 'POST', zone_arg)
        time.sleep(10)
    
    #Checking if the Zone was created successful.
    if zone_file1['status'] != 'success':
        print 'Zone %s Not Created' % zone_name
    elif zone_file1['status'] == 'success':
        print 'Zone %s Created' % zone_name

    # Closing the Zone File.
    zone.close()

# Reading in each Zone File in the Zone File Directory.   
for zoneFileName in os.listdir(path):

    # Setting the Publish Argument to True.
    publish_arg = {
            "publish": True
            }

    zone_path = os.path.join(path, zoneFileName)
    
    # Opening the Zone File for the Zone name.
    zone = open(zone_path, "r")

    # Reading in the line.
    zone_line = zone.readline()

    # Taking out the first line.
    zone_line1 = zone_line[1:]

    # Removing the @ORIGIN from the first line
    zone_line2 = zone_line1[7:]
    
    # Removing the period at the end of the first line.
    zone_name  = zone_line2[:-2]

    # Creating the Zone Publish Name Argument.
    zone_pub_name = '/Zone/%s' % zone_name

    # Sending the PUT command to the DynECT API.
    publish_zone = rest_iface.execute(zone_pub_name, 'PUT', publish_arg)
    
    # If the API needs time to catch up.
    count = 0

    while(publish_zone['status'] != 'success') and (count < 10):
        print "Waiting for the DynECT API..."
        count = count + 1
        # The Script will sleep for 30 seconds.
        time.sleep(30)
        # Execute the the PUT command again to the DynECT API.
        publish_zone = rest_iface.execute(zone_pub_name, 'PUT', publish_arg)

    # Checking to see if the Zone was Published.
    if publish_zone['status'] != 'success':
        print 'Zone %s Not Published' % zone_name
    elif publish_zone['status'] == 'success':
        print 'Zone %s is Published' % zone_name
    
    # Closing the Zone File.
    zone.close()

# Closing the connection to the DynECT API.
rest_iface.execute('/Session/', 'DELETE')
