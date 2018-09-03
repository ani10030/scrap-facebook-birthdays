# scrap-facebook-birthdays
A bunch of Python scripts to perform the task in the order as below :
	1. Scrap Facebook, fetch my facebook friend birthdays and insert into database.
	2. Fetch birthdays from database and send SMS reminder
	3. Send a SMS reminder for today's birthday(s)

import_birthdays.py 	:	Script to import birthday data from Facebook
birthday_reminder.py 	:	Script to check for todays' birthdays and notify user with SMS

Scripts are developed with Python 2.7 and below libraries are REQUIRED for this script to work.
Use pip to install any missing library.
Example Usage : pip install requests

Libraries Used :
	1. MySQLdb
	2. requests
	3. smtplib