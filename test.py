import string
import pandas as pd
import pymssql


while True:
	print("Search Listings type s; Book Listing type b; Write Review type w; Quit type q")
	t = raw_input (">")
	if t=='q':
		break 
	if t=='s':
		min = raw_input("please enter minimum price:")
		while True:
			try:
				min=float(min)
				break
			except ValueError: 
				min = raw_input("Not a float, please enter minimum price:")

		max = raw_input("please enter maximum price:")
		while True:
			try:
				max=float(max)
				break
			except ValueError: 
				max = raw_input("Not a float, please enter maximum price:")
		bed_room=raw_input("please enter number of bedrooms:")
		bed_room=unicode(bed_room,'utf-8')
		while ~bed_room.isnumeric():
			try:
				bed_room=int(bed_room)
				break
			except ValueError: 
				bed_room = raw_input("Not a integer, please enter number of bedrooms:")
				bed_room=unicode(bed_room,'utf-8')
		start=raw_input("please enter start date:")
		while True:
			try:
				start=pd.to_datetime(start)
				break
			except ValueError: 
				start = raw_input("Not a valide date, please enter start date:")
		end=raw_input("please enter end date:")
		while True:
			try:
				end=pd.to_datetime(end)
				break
			except ValueError: 
				end = raw_input("Not a valide date, please enter end date:")
		##
		conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
		cur = conn.cursor()
		cur.execute('SELECT id,name,description,number_of_bedrooms, price from helpdesk')
		df=pd.DataFrame(columns=['id','name','description','number_of_bedrooms', 'price'])
		row = cur.fetchone()
		while row:
    		#print (("SQL Server standard login name= %s") %  (row[0]))
    		df=df.append({'id':row[0],'name':row[1],'description':row[2],'number_of_bedrooms':row[3], 'price':row[4]})
			# from Python version 3: print is a function, not a statement.
    		row = cur.fetchone()
    	print(row)
		conn.close()
		##
	num=unicode(num,'utf-8')
	if num.isnumeric():
		break


	 id, name, first 25 characters of description, number of bedrooms, price












