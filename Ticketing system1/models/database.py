import sqlite3
from sqlite3 import Error


""" create a database connection to a SQLite database """

conn = sqlite3.connect('tickets_database.db')
c = conn.cursor()


# Create the tables
c.execute('''
               
    CREATE TABLE tickets (
        id INTEGER PRIMARY KEY,
        Description TEXT,
        RequesterName TEXT,
        AssignedTo TEXT,
        DueBy TEXT,
        Category TEXT,
        Priority TEXT,
        CreatedDate TEXT,
        Status TEXT,
        Attachments TEXT,
        Comments TEXT)
''')
c.execute('''
    CREATE TABLE users (
        UserID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        Email TEXT,
        Department TEXT)
''')

c.execute('''  

   CREATE TABLE tickettype (
        tickettypeID INTEGER PRIMARY KEY,
        tickettype TEXT)
''')

c.execute('''
    CREATE TABLE ticketstatus (
        ticketstatusID INTEGER PRIMARY KEY,
        ticketstatus TEXT,
        open BOOLEAN,
        closed BOOLEAN)
''')

c.execute('''
    CREATE TABLE ticketdetail (
        ticketdetailID INTEGER PRIMARY KEY,
        ticketID INTEGER,
        technicianID INTEGER)   
''')
c.execute('''
    CREATE TABLE technician(
        technicianID INTEGER PRIMARY KEY,
        teamID INTEGER,
        FirstName TEXT,
        LastName TEXT,
        email TEXT,
        password TEXT)
''')

c.execute('''
    CREATE TABLE team (
        teamID INTEGER PRIMARY KEY,
        email TEXT,
        teamname TEXT)
''')

c.execute('''
    CREATE TABLE ticketpriority (
        ticketpriorityID INTEGER PRIMARY KEY,
        ticketpriority TEXT,
        prioritylevel INTEGER,
        priorityname TEXT,
        PriorityCode TEXT,
        prioritycolor TEXT,
        nextaction TEXT)
''')

c.execute('''
    CREATE TABLE ticketcategory (
        ticketcategoryID INTEGER PRIMARY KEY,
        ticketcategory TEXT)
''')

c.execute('''
   CREATE TABLE description (
        descriptionID INTEGER PRIMARY KEY,
        description TEXT,
        technicianID INTEGER,
        ticketID INTEGER,
        userID INTEGER,
        date TEXT)
''')

c.execute('''
   CREATE TABLE date (
        dateID INTEGER PRIMARY KEY,
        date TEXT,
        technicianID INTEGER,
        ticketID INTEGER,
        userID INTEGER)
''')

c.execute('''
    CREATE TABLE attachement (
        attachementID INTEGER PRIMARY KEY,
        attachement TEXT,
        ticketID INTEGER,
        userID INTEGER,
        date TEXT)             
''')

c.execute('''
    CREATE TABLE admin (
        adminID INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT)
''')

c.execute(''' 
    CREATE TABLE contact_us(
        fname TEXT,
        lname TEXT,
        department TEXT,
        subject TEXT        
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()
