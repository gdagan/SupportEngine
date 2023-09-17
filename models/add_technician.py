#add a technician to the database
import sqlite3

conn = sqlite3.connect('tickets_database.db')
c = conn.cursor()


c.execute('''
          insert into technician (teamID, FirstName, LastName, email, password)
          
          VALUES (1, 'John', 'Smith', 'ghicer@gmail.com', 'password')
          
            ''')

conn.commit()

