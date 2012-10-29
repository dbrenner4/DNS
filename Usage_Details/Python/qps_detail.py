#! /usr/bin/env python
''' 
   An example script which will print the usage for a specific zone, 
   fqdn or print for all fqdn broken down by fqdn
   
   The credentials are read out of a configuration file in the same 
   directory named credentials.cfg in the format:
   
   [Dynect]
   user : user_name
   customer : customer_name
   password: password
   
   Usage: %python suz.py [-s|-r|-z|-g|-n] [options]

   Options:
	  -h, --help            show this help message and exit
	  -a, --all             Output all hostnames with QPS (default)
	  -z ZONE, --zone=ZONE  Return the QPS for a specific zone
	  -f FQDN, --fqdn=FQDN  Return the QPS for a specific fqdn (hostname)
	  -c FILE, --csv=FILE   File to output data to in csv format
	  -s START, --start=START
				Start date for QPS (ie: 2012-09-30). The start time
				begins on 00:00:01
	  -e END, --end=END     End date for QPS (ie: 2012-09-30). The end time
				finshes at 23:59:59 				

  The library is available at: 
  https://github.com/dyninc/Dynect-API-Python-Library			
'''

import sys
import datetime
import time
import ConfigParser
from optparse import OptionParser
from DynectDNS import DynectRest 
import csv

dynect = DynectRest()


def login(cust, user, pwd):
    '''	
    This method will do a dynect login

    @param cust: customer name
    @type cust: C{str}
    
    @param user: user name
    @type user: C{str}
    
    @param pwd: password
    @type pwd: C{str}
    @return: The function will exit the script on failure to login
    @rtype: None
    
    '''
    arguments = {
            'customer_name':  cust,
            'user_name':  user,  
            'password':  pwd,
    }
    
    response = dynect.execute('/Session/', 'POST', arguments)
    
    if response['status'] != 'success':
        sys.exit("Incorrect credentials")

def displayUsage(start, end, zone=None, fqdn=None, file=None):
    '''	
    Print the usage and write the csv file if needed
    
    @param start: start date for queries
    @type start: C{str}
    
    @param end: end date for queries
    @type end: C{str}
    
    @param zone: pass in a zone to display just the usage for that zone
    @type zone: C{str}
    
    @param zone: pass in an fqdn to display just the usage for that fqdn
    @type zone: C{str}
    
    @return: 
    @rtype: None
    
    '''
    
    # create our argument list
    args = None
    if fqdn != None:
        args = { 'start_ts' :  start, 'end_ts' : end, 'breakdown' : 'hosts', 'hosts' : [fqdn] }
    elif zone != None:
        args = { 'start_ts' :  start, 'end_ts' : end, 'breakdown' : 'hosts', 'zones' : [zone] }
    else:
        args = { 'start_ts' :  start, 'end_ts' : end, 'breakdown' : 'hosts'}
	
    # Perform action
    response = dynect.execute('/QPSReport/', 'POST', args)
    if response['status'] != 'success':
        print 'Failed to return results!'
        print response['msgs']
        return False
	
	
    # if we are writing out a csv, let's open it up to write
    if file != None:
        queryWriter = csv.writer(open(file, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
    # break the csv out by line so we can aggregate it by zone or fqdn
    lines = response['data']['csv'].split('\n')
    start = True
    hostnames = {}
    for line in lines:
        element = line.split(',')
        # if it's the first row,, just save the columns
        if start:
            start = False
            queryWriter.writerow([element[2] , element[1]])
            print element[2]  +'\t\t' + element[1]
        else:	
            #else aggregate them by hostname
            if len(element) > 1:
                if element[1] in hostnames:
                    hostnames[element[1]] = hostnames[element[1]] + int(element[2])
                else:
                    hostnames[element[1]] = int(element[2])
		
    # now print everything out				
    for host, queries in hostnames.iteritems():
        print  str(queries) + '\t\t' + host
        if file != None:
            queryWriter.writerow([str(queries) , host])


usage = "usage: %python suz.py [-s|-r|-z|-g|-n] [options]"
parser = OptionParser(usage=usage)
parser.add_option("-a", "--all", action="store_true", dest="all", default=False, help="Output all hostnames with QPS (default)")
parser.add_option("-z", "--zone", dest="zone", help="Return the QPS for a specific zone")
parser.add_option("-f", "--fqdn", dest="fqdn", help="Return the QPS for a specific fqdn (hostname)")
parser.add_option("-c", "--csv", dest="file", help="File to output data to in csv format")
parser.add_option("-s", "--start", dest="start", help="Start date for QPS (ie: 2012-09-30). The start time begins on 00:00:01")
parser.add_option("-e", "--end", dest="end", help="End date for QPS (ie: 2012-09-30). The end time finshes at 23:59:59")
(options, args) = parser.parse_args()


if options.start == None or options.end == None:
    parser.error("You must enter a start and end date")

# now read in the DynECT user credentials
config = ConfigParser.ConfigParser()
try:
    config.read('credentials.cfg')
except:
    sys.exit("Error Reading Config file")


login(config.get('Dynect', 'customer', 'none'), config.get('Dynect', 'user', 'none'), config.get('Dynect', 'password', 'none'))

# get the dates into arrays
dt_start = options.start.split('-')
dt_end = options.end.split('-')

# now create datetime objects from the dates
tm_start = datetime.datetime(int(dt_start[0]), int(dt_start[1]), int(dt_start[2]), 0, 0, 0)
tm_end = datetime.datetime(int(dt_end[0]), int(dt_end[1]), int(dt_end[2]), 23, 59, 59)

# call the display function with the start and end time and any other options
displayUsage(time.mktime(tm_start.timetuple()), time.mktime(tm_end.timetuple()), options.zone, options.fqdn, options.file)

# Log out, to be polite
dynect.execute('/Session/', 'DELETE')
