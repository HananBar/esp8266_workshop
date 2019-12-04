# esp8266_workshop
 
This Project is the SW implementation side of an ESP8266 workshop done as a side project.
The Idea was to add a gamification side to the learning experience.
It has 2 main parts
1. Web server containing the workshop's tasks and instructions (HTML+JS)
2. python flask web server listening and waiting to verify each (or at least most) tasks


Current implementation assumes:
1. Webserver is running and the contents of "instructions" folder is in the root you point to when starting the workshop.
2. configuration.yaml holds all configurations - including all the workshop devices MAC addresses.
3. MongoDB is running (run db_access.py once to populate DB)
4. all libraries from 'for_instructor/setup instructions.txt' are installed
5. You can control your AP's settings with<br>
 a. Setup low-band (2.4GHz) SSID as 'intel makers'<br>
 b. Setup high-band (5.2GHz) SSID as a different SSID (we used 'ESP8266 workshop')<br>
 c. DHCP is set to start at 192.168.1.101

Extra assumptions:<br>
1. Since we were running in a corporate environment, the AP wasn't connected to the Internet so we had to provide our own NTP server - done with https://github.com/limifly/ntpserver, and the patch to port it to python3 (https://github.com/limifly/ntpserver/pull/3)

Explanation to 2.4/5.2GHz assumption:
In earlier runs of the workshop we had everyone connected to 2.4GHz which is already crowded in office environments. causing many collisions and retries. having the "management" on a different band made things run better
