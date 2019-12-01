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
        start=input("please enter start date(YYYY-MM-YY):")
        while True:
            try:
                start=pd.to_datetime(start)
                break
            except ValueError: 
                start = input("Not a valide date, please enter start date:")
        end=input("please enter end date(YYYY-MM-YY):")
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
        AND L.number_of_bedrooms=%s AND C.available=1
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
                    if (id in df['id'].values):
                        break
                    else:
                         id = input("Id not in the listing, Please enter the id you would like to book:")
                else:
                    id = input("Please enter a numeric id:")
            name=input('please enter your name:')
            number_of_guests=input('please enter number_of_guests:')
            while True:
                if number_of_guests.isnumeric():
                   break;
                else: 
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
            conn.commit()
            conn.close()
    if (t=='w'):
        name=input('please enter your booking name(Capital sensitive):')
        conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
        cur = conn.cursor()
        SQLCommand ='''
        SELECT * from Bookings B
        WHERE B.guest_name=%s
        '''
        cur.execute(SQLCommand,str(name))
        print('processing:\n')
        df=pd.DataFrame(columns=['id','listing_id','guest_name','stay_from','stay_to','number_of_guests'])
        #row = cur.fetchone()
        for row in cur:
            #print (("SQL Server standard login name= %s") %  (row[0]))
            df=df.append({'id':row[0],'listing_id':row[1],'guest_name':row[2],'stay_from':row[3], 'stay_to':row[4],'number_of_guests':row[5]},ignore_index=True)
        conn.close()
        if df.empty:
            print('No result found\n')
        else:    
            print(df)
            id = input("Please enter the listing id you would like to book:")
            while True:
                if id.isnumeric():
                    id = int(id)
                    if (id in df['listing_id'].values):
                        break
                    else:
                         id = input("Id not in the listing, Please enter the id you would like to review:")
                else:
                    id = input("Please enter a numeric id:")
            user_name= input("Please enter your name:")
            date=input("Please enter current date:")
            while True:
                try:
                    date=pd.to_datetime(date)
                    break
                except ValueError: 
                    date = input("Not a valide date, please enter date:")
            review=input("Please enter your comments:")
            ##get the key
            conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
            cur = conn.cursor()
            SQLCommand ='''
            SELECT max(R.id) from Review R
            '''
            cur.execute(SQLCommand,Value)
            for row in cur:
                key=row[0];
            key=key+1
            conn.close()
            ###
            conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_xza185', password='JT3rG3HthGtMbg3A', database='xza185354')
            cur = conn.cursor()
            SQLCommand ='''
            INSERT INTO Review
            (id, listing_id, comments, guest_name)
            VALUES(%s,%s,%s,%s)
            '''
            Value=(str(key),str(id),str(review),str(user_name))
            try:
                cur.execute(SQLCommand,Value)
            except pymssql.OperationalError as e:
            	print("AN Error has been caught.")
            	print('Message = ',e.message)
            	print('the review was not stored')
            conn.commit()
            conn.close()
    else:
    	print('Not a valid input')



















