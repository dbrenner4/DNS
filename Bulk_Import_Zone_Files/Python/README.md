Dyn Inc, Integration Team Deliverable
"Copyright © 2013, Dyn Inc.
All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
 
* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
 
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
 
* Neither the name of Dynamic Network Services, Inc. nor the names of
  its contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."

____________________________________________________________________________

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
