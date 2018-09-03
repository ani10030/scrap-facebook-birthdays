import MySQLdb
import requests,urllib

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import timedelta
import datetime

import os

def db_connect(query_string,query_type):
	# Your MySQL db details. Host, username, password, database name
	db = MySQLdb.connect("123.456.789.000","username","password,","db_name")
	cursor=db.cursor()
	if query_type == 'SELECT':
		cursor.execute(query_string)
		data=cursor.fetchall()
	elif query_type == 'UPDATE' or query_type == 'INSERT':
		try:
			cursor.execute(query_string)
			db.commit()
			data = 'SUCCESS'
		except:
			db.rollback()
			data = 'FAILURE'
	
	db.close()
	return data

def calendar_download():
	try:
		print '-- Opening calendar URL --'

		# Get your URL from facebook and replace below
		url = 'https://www.facebook.com/ical/b.php?uid=100001111111111&key=ABCDEFGHIJKLMNOP'

		#Open downloaded calendar file
		data = requests.get(url)
		#Append all data into a single continuous string
		text_data = data.content
		print '-- Calendar data fetched successfully from URL --'
		return text_data
	except Exception,e:
		error_mail('Error occured in calendar_download() - Error Message : '+str(e))

def fetch_birthdays(text_data):
	try:
		print ' '
		print '-- Creating birthday list --'
		text = text_data.split('BEGIN:VEVENT')
		#Initializing value for id.
		id = 1000
		#This list element is a list of lists and will store all birthdays as individual lists
		birthday_list=[]
		#Looping through each birthday
		for i in range(1,len(text)):
			#Fetching each birthday as a element of list
			lines=text[i].split('\r\n')
			#Fetching DTSTART element of calendar file
			dtstart=(lines[1].split(':'))[1]
			#Splitting DTSTART into YYYY MM DD components
			bday_year = dtstart[0:4]
			bday_month = dtstart[4:6]
			bday_date = dtstart[6:8]
			#Fetching SUMMARY element of calendar file
			summary = lines[2].split(':')[1].split("'s birthday")[0]
			name = summary.split(' ')
			#Fetch first, middle, last names and their space(' ') adjustments
			if len(name)==0:
				pass
			elif len(name)==1:
				first_name = name[0]
				middle_name = ''
				last_name = ''
			elif len(name)==2:
				first_name = name[0]
				middle_name = ' '
				last_name = name[1]
			elif len(name)==3:
				first_name = name[0]
				middle_name = ' '+name[1]+' '
				last_name = name[2]
			else:
				first_name = name[0]
				middle_name = ' '+name[1]+' '
				last_name = ''
				for j in range(2,len(name)):
					last_name+=name[j]+' '
				last_name=last_name[0:-1]
			#Fetch uid element from calendar file
			uid = lines[5].split(':')[1].split('@facebook.com')[0]
			profile_id = uid[1:]
			
			#Creating a list for this birthday
			line_data_list = [id+i,bday_year,bday_month,bday_date,first_name,middle_name,last_name,profile_id]
			#Adding this list to parent birthday list
			birthday_list.append(line_data_list)

		print '-- Birthday List created successfully --'
		return birthday_list
	except Exception,e:
		error_mail('Error occured in fetch_birthdays() - Error Message : '+str(e))

def insert_in_db(birthdays,query_type):
	# Your MySQL db details. Host, username, password, database name
	db = MySQLdb.connect("123.456.789.000","username","password,","db_name")
	cursor=db.cursor()
	if query_type == 'SELECT':
		cursor.execute('')
		data=cursor.fetchall()
	elif query_type == 'UPDATE' or query_type == 'INSERT':
		try:
			count = 0
			print ' '
			print '-- Insert calendar data into database --'
			for i in birthdays:
				insert_query = """INSERT INTO table(year,month,day,first_name,middle_name,last_name,profile_id) VALUES('"""+i[1]+"""','"""+i[2]+"""','"""+i[3]+"""','"""+i[4]+"""','"""+i[5]+"""','"""+i[6]+"""','"""+i[7]+"""') ON DUPLICATE KEY UPDATE year = '"""+i[1]+"""'"""
				cursor.execute(insert_query)
				count+=1
				if count%50==0:
					db.commit()
					print '>> '+str(count)+' records commited successfully'
			db.commit()
			data = 'SUCCESS'
			print '>> '+str(count)+' records commited successfully'
			print '-- Calendar data inserted successfully into database --'
		except Exception,e:
			db.rollback()
			data = 'FAILURE'
			error_mail('Error occured in insert_in_db() - Error Message : '+str(e))
		finally:
			db.close()
			return data

def error_mail(failure_msg):
	print ' '
	print '[X] '+failure_msg+' [X]'
	print ' '
	me = 'Mail-Failure<test-mail@gmail.com>'
	you = 'test-mail@gmail.com'
	print '-- Sending error e-mail to < '+you+' > --'
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Failure in updating Birthday Calendar"
	msg['From'] = me
	msg['To'] = you

	html = """\
	<html>
		<head></head>
		<link href="https://fonts.googleapis.com/css?family=Lobster+Two|Alegreya+SC" rel="stylesheet">
		<body style="font-family: 'Alegreya SC', serif;">
			<h1 style = "font-family: 'Lobster Two', cursive;color:#D9534F;"><q style="margin-left: 20px;">Updating Birthday Calendar Failed </q></h1>
			---------------------------------------------------
			<p>Hi</p>
			<p>Some error has occured while updating the birthday calendar data in database.</p>
			<p style="font:red;"><b>Error Message : """+failure_msg+"""</b></p>
			<p>Please check.</p>
			---------------------------------------------------</br>
		<footer style="color: #000;font-family: 'Alegreya SC', serif;font-weight: bolder;">
				<p>Thanks</p>
			</footer>
			<pre style="text-align: center;">This mail was sent to you at <footer style="color: #000;font-family: 'Alegreya SC', serif;">{time}</footer></pre>
		</body>
	</html>""".format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))

	part1 = MIMEText(html, 'html')
	msg.attach(part1)

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(me, you, msg.as_string())
		print '-- Error e-mail sent successfully--'
		return "Success"
	except:
		return "Error"

def success_mail(previous_count,new_count,new_members_html):
	me = 'Birthday-Calendar<test-mail@gmail.com>'
	you = 'test-mail@gmail.com'
	print ' '
	print '-- Sending success e-mail to < '+you+' > --'
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Birthday Calendar updated successfully !"
	msg['From'] = me
	msg['To'] = you

	html = """\
	<html>
		<head></head>
		<link href="https://fonts.googleapis.com/css?family=Lobster+Two|Alegreya+SC" rel="stylesheet">
		<body style="font-family: 'Alegreya SC', serif;">
			<h1 style = "font-family: 'Lobster Two', cursive;color:#D9534F;"><q style="margin-left: 20px;">Birthday Calendar Updated Successfully </q></h1>
			---------------------------------------------------
			<p>Hi</p>
			<p>The birthday calendar data in database has been updated successfully.</p>
			<p>***********************</p>
			<p>Previous Count : {previous_count}</p>
			<p>New Count :  {new_count}</p>
			<p>***********************</p>
			<p>New members in the birthday calendar :</br>
			<table style="font-family: 'Alegreya SC', serif; border-collapse: collapse; width: 60%;">
  				<tr>
  					<th style="border: 1px solid #000; text-align: left; padding: 8px; background-color : #dfdfdf;">
  						Member Name
  					</th>
  					<th style="border: 1px solid #000; text-align: left; padding: 8px; background-color : #dfdfdf;">
  						Profile URL
  					</th>
  				</tr>
  				{new_members_html}
  			</table>
			</p>
			---------------------------------------------------</br>
		<footer style="color: #000;font-family: 'Alegreya SC', serif;font-weight: bolder;">
				<p>Thanks</p>
			</footer>
			<pre style="text-align: center;">This mail was sent to you at <footer style="color: #000;font-family: 'Alegreya SC', serif;">{time}</footer></pre>
		</body>
	</html>""".format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'), previous_count = previous_count, new_count = new_count, new_members_html = new_members_html)

	part1 = MIMEText(html, 'html')
	msg.attach(part1)

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(me, you, msg.as_string())
		return "Success"
	except:
		return "Error"

def update_manual_rows():
	try:
		select_query = '''SELECT profile_id FROM table WHERE CONVERT(year, UNSIGNED INTEGER) <= ''' + str(int(format(datetime.datetime.now()+timedelta(hours=12.5),'%Y'))) + '''
		 AND CONVERT(month, UNSIGNED INTEGER) <= ''' + str(int(format(datetime.datetime.now()+timedelta(hours=12.5),'%m'))) + '''
		 AND CONVERT(day, UNSIGNED INTEGER) < ''' + str(int(format(datetime.datetime.now()+timedelta(hours=12.5),'%d')))
		manual_rows = db_connect(select_query,'SELECT')
		manually_added_birthdays = []
		for i in manual_rows:
			manually_added_birthdays.append(i[0])
		if manually_added_birthdays != []:
			update_query = """UPDATE table SET year = '""" + str(int(format(datetime.datetime.now()+timedelta(hours=12.5),'%Y')) + 1) + """',segment2 = DATE(DATE_ADD(SYSDATE(), INTERVAL '12:30' HOUR_MINUTE))
			 WHERE profile_id IN (""" + str(manually_added_birthdays)[1:-1] + """)"""
			updation_status = db_connect(update_query,'UPDATE')
			return updation_status
		else:
			print '-- No rows eligible for manual updation --'
			return 'SUCCESS'
	except Exception,e:
		error_mail('Error occured in update_manual_rows() - Error Message : '+str(e))
try:
	select_query = """SELECT IFNULL(MAX(ID),1000) FROM table_calendar_updates"""
	max_id = db_connect(select_query,'SELECT')[0][0]
	id = max_id+1

	date = format(datetime.datetime.now()+datetime.timedelta(hours=12.5),'%d-%b-%y')
	timestamp = format(datetime.datetime.now()+datetime.timedelta(hours=12.5),'%H:%M:%S')
	insert_query = "INSERT INTO table_calendar_updates(id,updated_on,timestamp,previous_count) VALUES ("+str(id)+",'"+date+"','"+timestamp+"',(SELECT count(1) FROM table))"
	db_connect(insert_query,'INSERT')

	text_data = calendar_download()
	if text_data[0:5] == 'Sorry':
		print 'Looks like the facebook key to fetch birthday calendar has expired - Error Message : '+text_data
		error_mail('Looks like the facebook key to fetch birthday calendar has expired - Error Message : '+text_data)
		print '\nUpdating error message in table_calendar_updates table'
		text_data = text_data.replace("'","`")
		update_query = """UPDATE table_calendar_updates SET
								 new_count = (SELECT COUNT(1) FROM table),
								 insert_status = 'ERROR',
								 update_status = 'ERROR',
								 segment1 = '"""+text_data[0:250]+"' WHERE id = "+str(id)
		status = db_connect(update_query,'UPDATE')
		print 'Update Status for table_calendar_updates table = '+status
		print '\nExiting from the program ...'
		exit()

	birthdays = fetch_birthdays(text_data)
	insert_status = insert_in_db(birthdays,'INSERT')
	update_status = update_manual_rows()

	if (insert_status == 'SUCCESS') and (update_status == 'SUCCESS'):
		count_query = """SELECT previous_count,(SELECT COUNT(1) FROM table) FROM table_calendar_updates WHERE updated_on = '"""+date+"""'"""
		count_values = db_connect(count_query,'SELECT')
		previous_count = count_values[0][0]
		new_count = count_values[0][1]

		new_members_query = """SELECT CONCAT(b.first_name,b.middle_name,b.last_name) name,b.profile_id
  								FROM table_calendar_updates bcu,
       								 birthdays b
 							   WHERE bcu.updated_on = DATE_FORMAT(b.segment1,'%d-%b-%y')
   								 AND bcu.updated_on = '"""+date+"""'"""
   		new_members = db_connect(new_members_query,'SELECT')
   		new_members_html = ''
   		for i in new_members:
   			new_members_html = new_members_html+'''\n
   			<tr>
            	<th style="border: 1px solid #000; text-align: left; padding: 8px;">
                	'''+i[0]+'''
                </th>
                <th style="border:1px solid #000">
                	<a href="www.facebook.com/'''+i[1]+'''">'''+i[1]+'''</a>
                </th>
            </tr>
   			'''
		success_mail(str(previous_count),str(new_count),new_members_html)
		print ' '
		print 'Insert Status : '+insert_status
		print 'Update Status : '+update_status
	else:
		print ' '
		print '*** Some Error has occured in the program ***'
		print 'Insert Status : '+insert_status
		print 'Update Status : '+update_status
	update_query = "UPDATE table_calendar_updates SET insert_status = '"+insert_status+"',update_status = '"+update_status+"',new_count = (SELECT COUNT(1) FROM table) WHERE id = "+str(id)
	db_connect(update_query,'UPDATE')
	
	print '--- Completed ---'
except Exception,e:
	print ' '
	print 'FAILURE'
	print 'Error Message - '+str(e)