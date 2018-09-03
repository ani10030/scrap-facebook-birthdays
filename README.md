# scrap-facebook-birthdays
<p>
A bunch of Python scripts to perform the task in the order as below :<br>
<span style="margin-left: 25px;">1. Scrap Facebook, fetch my facebook friend birthdays and insert into database.</span><br>
<span style="margin-left: 25px;">2. Fetch birthdays from database and send SMS reminder</span><br>
<span style="margin-left: 25px;">3. Send SMS reminder for today's birthday(s)</span>
</p>
<p>
<b>import_birthdays.py</b> 	:	Script to import birthday data from Facebook<br>
<b>birthday_reminder.py</b> 	:	Script to check for todays' birthdays and notify user with SMS<br>
</p>
<p>
Scripts are developed with Python 2.7 and below libraries are REQUIRED for this script to work.<br>
Use pip to install any missing library.<br>
Example Usage : <pre>pip install requests</pre>
</p>
<p>
Libraries Used :<br>
<span style="margin-left: 25px;">1. MySQLdb</span><br>
<span style="margin-left: 25px;">2. requests</span><br>
<span style="margin-left: 25px;">3. smtplib</span><br>
</p>