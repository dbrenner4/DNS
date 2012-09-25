
This is the bulk import of zone files script. This script will run through a folder of zone files create the zones through DynECT API and bulk publish the files. The script runs on the command line. Here are the steps to run the script.

1.) Create a folder called BulkZones.<br />
2.) Create a sub folder in BulkZones called dynect.<br />
3.) Download the DynectDNS.py __init__.py, and setup.py from here - https://github.com/dyninc/Dynect-API-Python-Library <br />
4.) Put the DynectDNS.py __init__.py and setup.py scrips in the dynect folder.<br />
5.) Put the BulkImportZoneFiles.py script in the BulkZones folder.<br />
6.) Create a folder and put the zone files you want to import inside the folder. (Remember the path you will need to enter the path in the script.<br />
7.) run $ python BulkImportZoneFiles.py <br />
8.) The script will ask for your company name, username, and password to log into DynECT.<br />
9.) If you correctly enter your credentials the script will ask you for the path to your zone files.<br />
10.) The script will run and tell you what zones were created or not created and if your zones were published or not.<br />
