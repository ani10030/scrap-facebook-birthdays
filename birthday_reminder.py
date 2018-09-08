import MySQLdb
from datetime import timedelta
import datetime
import sms_with_api

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

def todays_birthdays():
	try:
		select_query = '''SELECT CONCAT(first_name,middle_name,last_name)
		 FROM 
		 WHERE CONVERT(year, UNSIGNED INTEGER) = ''' + str(int(format(datetime.datetime.now(),'%Y'))) + '''
		   AND CONVERT(month, UNSIGNED INTEGER) = ''' + str(int(format(datetime.datetime.now(),'%m'))) + '''
		   AND CONVERT(day, UNSIGNED INTEGER) = ''' + str(int(format(datetime.datetime.now(),'%d')))+'''
		   AND sms = 'Y' '''
		print '-- Fetching birthdays from database --'
		
		birthday_data = db_connect(select_query,'SELECT')
		print '[OK]- Birthdays fetched successfully -[OK]\n'

		birthday_count = len(birthday_data)
		if birthday_count == 0:
			print 'No birthdays today !'
		else:
			message = ":\n>> Today's Birthdays <<\n\n"
			x = 1
			for i in birthday_data:
				message = message+str(x)+'. '+i[0]+'\n'
				x+=1
			print message
			phone = '1234567890' #Recipient mobile number
			sms_status = sms_with_api.send_sms([phone,message])
			if sms_status == 'SUCCESS':
				print 'SMS sent successfully !'
			else:
				print '[X]- Error sending SMS -[X]'
	except Exception,e:
		print '[X]- Some error occured -[X] : '+str(e)

todays_birthdays()