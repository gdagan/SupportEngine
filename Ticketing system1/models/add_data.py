import sqlite3



""" create a database connection to a SQLite database """

conn = sqlite3.connect('tickets_database.db')
c = conn.cursor()


# Create the tables
c.execute('insert into tickets (id, category, technician_name, priority, description, status, attachments, comments) VALUES ("1", "Hardware", "John Smith", "High", "My computer is broken", "Open", "None", "None")')
c.execute('insert into tickets (id, category, technician_name, priority, description, status, attachments, comments) VALUES ("2", "Software", "John Smith", "High", "my outlook will not load", "Open", "None", "None")')
c.execute('insert into tickets (id, category, technician_name, priority, description, status, attachments, comments) VALUES ("3", "Hardware", "John Smith", "High", "my password is not working ", "Open", "None", "None")')


# Commit the changes and close the database connection
conn.commit()
conn.close()
