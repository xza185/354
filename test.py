import string
import pandas as pd
import pymssql

def first_25(d):
    if len(d)<=25:
        return d
    else:
        return d[0:25]


while True:
    print("Search Listings type s; Book Listing type b; Write Review type w; Quit type q")
    t = input(">")
    if t=='q':
        break 
    if t=='s':
        min = input("please enter minimum price:")
        while True:
            try:
                min=float(min)
                break
            except ValueError: 
                min = input("Not a float, please enter minimum price:")

        max = input("please enter maximum price:")
        while True:
            try:
                max=float(max)
                break
            except ValueError: 
                max = input("Not a float, please enter maximum price:")
        bed_room=input("please enter number of bedrooms:")
        while ~bed_room.isnumeric():
            try:
                bed_room=int(bed_room)
                break
            except ValueError: 
                bed_room = input("Not a integer, please enter number of bedrooms:")
        start=input("please enter start date:")
        while True:
            try:
                start=pd.to_datetime(start)
                break
            except ValueError: 
                start = input("Not a valide date, please enter start date:")
        end=input("please enter end date:")
        while True:
            try:
                end=pd.to_datetime(end)
                break
            except ValueError: 
                end = input("Not a valide date, please enter end date:")
        day=end-start
        ##
        conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
        cur = conn.cursor()
        SQLCommand ='''
        SELECT L.id,L.name,L.description,L.number_of_bedrooms, R.Total_price from
        (SELECT L.id,sum(C.price) as Total_price from Listings L, Calendar C 
        WHERE L.id=C.listing_id AND C.date>=%s AND C.date<=%s 
        AND L.number_of_bedrooms=%s
        Group by L.id
        Having count(*)>%s) R, Listings L
        WHERE R.id=L.id AND
        R.Total_price>=%s AND R.Total_price<=%s 
        '''

        Value=(str(start)[0:10],str(end)[0:10],str(bed_room),str(day.days),str(min),str(max))
        cur.execute(SQLCommand,Value)
        print('processing:\n')
        df=pd.DataFrame(columns=['id','name','description','number_of_bedrooms', 'Total_price'])
        #row = cur.fetchone()
        for row in cur:
            #print (("SQL Server standard login name= %s") %  (row[0]))
            df=df.append({'id':row[0],'name':row[1],'description':row[2],'number_of_bedrooms':row[3], 'Total_price':row[4]},ignore_index=True)
            # from Python version 3: print is a function, not a statement.
            #row = cur.fetchone()
        conn.close()
        df['description']=df['description'].apply(first_25)
        if df.empty:
            print('No result found\n')
        else:    
            print(df)
            id = input("Please enter the id you would like to book:")
            while True:
            	if id.isnumeric():
            		id = int(id)
            		if id in df['id'].values:
            			break
            		else:
            		   id = input("Id not in the listing, Please enter the id you would like to book:")
                id = input("Please enter a numeric id:")
            name=input('please enter your name:')
            number_of_guests=input('please enter number_of_guests:')
            while ~number_of_guests.isnumeric(): 
                number_of_guests = input("Not a integer, please enter number_of_guests:")
            conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
            cur = conn.cursor()
            SQLCommand ='''
            SELECT COUNT(*) FROM Bookings
            '''
            cur.execute(SQLCommand)
            for row in cur:
            	key=row[0];
            conn.close()
            conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
            cur = conn.cursor()
            SQLCommand ='''
            INSERT INTO Bookings
            (id, listing_id, guest_name, stay_from, stay_to, number_of_guests)
            VALUES(%s,%s,%s,%s,%s,%s)
            '''
            Value=(str(key),str(id),str(name),str(start),str(end),str(number_of_guests))
            cur.execute(SQLCommand,Value)
            conn.close()

            














