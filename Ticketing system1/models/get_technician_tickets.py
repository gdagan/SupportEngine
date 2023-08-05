# from sqlite3 import Cursor
# from tkinter import _Cursor






# def get_technician_tickets(username):
#     # Get the tickets from the database
#     Cursor.execute("SELECT * FROM tickets WHERE technician = ?", (username,))
#     tickets = _Cursor.fetchall()

#     # Format the tickets into a list of dictionaries
#     formatted_tickets = []
#     for ticket in tickets:
#         formatted_ticket = {
#             'id': ticket[0],
#             'category': ticket[1],
#             'priority': ticket[2],
#             'status': ticket[3]
#         }
#         formatted_tickets.append(formatted_ticket)

#     return formatted_tickets
