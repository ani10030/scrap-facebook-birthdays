# scrap-facebook-birthdays
<p>
Python scripts to perform the task in the order as below :<br>
1. Scrap Facebook, fetch my Facebook friend birthdays and insert into database.<br>
2. Fetch birthdays from database and send SMS reminder<br>
</p>
<p>
<b>import_birthdays.py</b>		:	Script to import birthday data from Facebook<br>
<em>Note : You will need to get the URL for your Facebook account's calendar file. <a href="https://www.anirudhsethi.in/blog/tech/import-facebook-birthdays-as-calendar/" target="_blank">Click here to know how to retrieve your calendar file.</a></em><br>
<em>This script will take care of adding only new birthdays to your database from the calendar file. Also, if there are any updates in the calendar file to the existing data, it will be handled by this script</em><br><br>
<b>birthday_reminder.py</b> 	:	Script to check for today's birthdays and notify user with SMS<br>
<em>Note : This script uses Fast2SMS API to send SMS. You will need to setup your API key on Fast2SMS before sending SMS. <a href="https://github.com/ani10030/sms-with-api">Click here to see the code for <b>sms_with_api.py</b></a></em>
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
