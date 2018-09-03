# scrap-facebook-birthdays
<p>
A bunch of Python scripts to perform the task in the order as below :<br>
	1. Scrap Facebook, fetch my facebook friend birthdays and insert into database.<br>
	2. Fetch birthdays from database and send SMS reminder<br>
	3. Send a SMS reminder for today's birthday(s)
</p>
<p>
import_birthdays.py 	:	Script to import birthday data from Facebook<br>
birthday_reminder.py 	:	Script to check for todays' birthdays and notify user with SMS<br>
</p>
<p>
Scripts are developed with Python 2.7 and below libraries are REQUIRED for this script to work.<br>
Use pip to install any missing library.<br>
Example Usage : <pre>pip install requests</pre>
</p>
<p>
Libraries Used :<br>
	1. MySQLdb<br>
	2. requests<br>
	3. smtplib<br>
</p>