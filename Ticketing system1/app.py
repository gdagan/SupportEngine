from flask import Flask, json, jsonify, render_template, request, redirect, session, url_for, flash
import sqlite3  # to use SQL in Python
import pandas as pd
from datetime import datetime
import uuid  # to generate random reset tokens
from flask_mail import Mail, Message
import os

app = Flask(__name__)
mail = Mail(app)

app.secret_key = 'your_secret_key'  # Set a secret key for session encryption
session = {'username': None}
db_path = './tickets_database.db'  # Path to the database file


# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'manageengine77@gmail.com'  # Your Gmail email address
app.config['MAIL_PASSWORD'] = 'Applepie99'  # Your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'manageengine77@gmail.com'
mail = Mail(app)

@app.route('/test_email')
def test_email():
    try:
        # Create a test email message
        subject = 'Test Email'
        recipients = ['ghicer@gmail.com']  # Replace with a recipient's email address
        message_body = 'This is a test email from your Flask application.'

        message = Message(subject=subject,
                          recipients=recipients,
                          body=message_body)

        # Send the test email
        mail.send(message)

        return 'Test email sent successfully!'
    except Exception as e:
        return f'Error sending test email: {str(e)}'



def get_tickets(ticket_id=None,username=None):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    if ticket_id is not None:
        sql_query = f"SELECT * FROM tickets WHERE id = {ticket_id}"
        return cursor.execute(sql_query).fetchall()
        
    if username is None:
        return cursor.execute("SELECT * FROM tickets").fetchall()
    
    query = f"SELECT * FROM tickets where AssignedTo like \'{username}\'"
    return cursor.execute(query).fetchall()
    
def get_comments(ticket_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    sql_query = f"SELECT * FROM comments WHERE ticket_id = {ticket_id}"
    return cursor.execute(sql_query).fetchall()

def get_categories():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return cursor.execute("SELECT Distinct Category FROM tickets").fetchall()

def get_technicians():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return cursor.execute("SELECT * FROM technician").fetchall()

def get_users():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return cursor.execute("SELECT Distinct AssignedTo FROM tickets").fetchall()

def get_assets():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return cursor.execute("SELECT * FROM asset_management").fetchall()
        

# Tech Login route
@app.route('/')
@app.route('/tech_login', methods=['GET', 'POST'])
def tech_login():
    if request.method != 'POST':
        return render_template('tech_login.html')
    username = request.form['username']
    password = request.form['password']

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    sql_query = """
                    SELECT
                        *
                    FROM 
                      technician
                    """

    technicians = cursor.execute(sql_query).fetchall()

    # Check if the technician credentials are valid
    for technician in technicians:
        if technician[-2] == username and technician[-1] == password:
            session['username'] = username
            return redirect('/technician_dashboard')
    flash('Invalid credentials')
    return render_template('tech_login.html', error='Invalid credentials')


def format_time(cols):
    cby = cols[0]
    return cby if cby is None else str(cby).split('.')[0]
    

# # Technician Dashboard route
@app.route('/technician_dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['username'] is None:
        return redirect('/tech_login')
    username = session['username']
    
    assignedTo = None
    if request.method == 'POST':
    
        value = request.form.to_dict()['TicketList']
        
        if value == "MyTickets":
            assignedTo = username

    tickets = get_tickets(username=assignedTo)
    df_tickets = pd.DataFrame(tickets, columns=['id', 'desc', 'reqName', 'assto', 'dby', 'cat', 'pri', 'cby', 'stat', 'attach', 'act'])
    df_tickets['cby'] = df_tickets[['cby']].apply(format_time,axis=1)
 
    
    num_all = df_tickets.shape[0]
    num_high = df_tickets[df_tickets['pri'] == 'high'].shape[0]
    num_open = df_tickets[df_tickets['stat'] == 'open'].shape[0]
    num_closed = df_tickets[df_tickets['stat'] == 'Closed'].shape[0]
    
    overalls = {
        'All Tikcets': num_all,
        'All High Priority Tickets': num_high,
        'All Open Tickets': num_open,
        'All Closed Ticket': num_closed,
    }
    
    overalls_text = f'''
        'All Tikcets': {num_all},
        'All High Priority Tickets': {num_high},
        'All Open Tickets': {num_open},
        'All Closed Ticket': {num_closed},  
    '''

    return render_template('technician_dashboard.html', username=username, tickets=df_tickets.values.tolist(), overalls=overalls_text)


### Logout route
@app.route('/tech_logout')
def logout():
    session['username'] = None
    return redirect('/tech_login')


### User portal route

@app.route('/user_portal', methods=['GET','POST'])
def user_portal():
    
    # Check if the user is authenticated
    if request.method != 'POST':
        return render_template('user_portal.html')
    
    
     # Send an email notification to the user
    subject = 'Ticket Logged'
    recipients = [request.form['email']]  # Get the user's email from the form
    message_body = 'Your ticket has been logged successfully.'

    message = Message(subject=subject,
                      recipients=recipients,
                      body=message_body)
    mail.send(message)
    
    # Handle form data
    ticket_data = {
        'created_date': datetime.now(),
        'requestername': request.form['name'],
        'category': request.form['category'],
        'priority': request.form['priority'],
        'description': request.form['description']   
        
    }

    try:
        db_path = "tickets_database.db"  # Path to the database file
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
    
    except Exception as e:
        print("Error:", e)  # Print the error for debugging
        return jsonify({"error":'An error occurred while submitting the ticket'})


    new_ticket = Ticket(
        createddate = datetime.now(),
        requestername= ticket_data['requestername'],
        category=ticket_data['category'],
        priority=ticket_data['priority'],
        description=ticket_data['description'],
        status='open',
        attachments= 'null',
     
    )

    sql_query = "INSERT INTO tickets (createddate, category, priority, description, status, attachments, requesterName) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql_query, ( 
              
    new_ticket.createddate,
    new_ticket.category,
    new_ticket.priority,
    new_ticket.description,
    new_ticket.status,
    new_ticket.attachments,
    new_ticket.requestername   
    ))
    
    connection.commit()
    connection.close()

    response_message = "Ticket submitted successfully!"
    #return render_template('technician_dashboard.html')
    return jsonify({
        "status":True,
        "message":response_message}), 200
  


# ### Root route
# @app.route('/')
# def root():
#     return redirect('tech_login')


### About route
@app.route('/about')
def about():
    return render_template('about.html')


### Contact us route
@app.route('/contact_us')
def contact_us():
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    if request.method == 'POST':
        comment_text = request.form['comment']
        
    return render_template('contact_us.html')


### User login route
@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method != 'POST':
        return render_template('user_login.html')
    username = request.form['username']
    password = request.form['password']

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    sql_query = """
                    SELECT
                        *
                    FROM 
                      users
                    """

    users = cursor.execute(sql_query).fetchall()
    for users in users:
        if users[-2] == username and users[-1] == password:
            session['username'] = username
            return redirect('/user_portal')
    flash('Invalid credentials')
    return render_template('user_login.html', error='Invalid credentials')
    

# # Generate a random reset token for the user and store it in the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
sql_query = """
                    SELECT
                        *
                    FROM 
                      users
                    """
users = cursor.execute(sql_query).fetchall()

def generate_reset_token(email):
    reset_token = str(uuid.uuid4())
    users[email]['reset_token'] = reset_token
    return reset_token

# Check if the reset token is valid and associated with the user
def is_valid_reset_token(email, reset_token):
    return users.get(email) and users[email]['reset_token'] == reset_token

### Reset password route
@app.route('/reset_password/<string:reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    if request.method != 'POST':
        return render_template('reset_password.html', reset_token=reset_token)
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if email not in users or not is_valid_reset_token(email, reset_token):
        return 'Invalid reset token or email'
    if new_password != confirm_password:
        return 'Passwords do not match'

    # Expire the reset token
    users[email]['reset_token'] = None
    return 'Password reset successful!'

#### Edit ticket route
# @app.route('/edit_ticket', methods=['GET', 'POST'])
@app.route('/edit_ticket/<int:ticket_id>', methods=['GET','POST'])
def edit_ticket(ticket_id= True):    # sourcery skip: avoid-builtin-shadow
    if session.get('username') is None:  # If the user is not logged in
        return redirect('/tech_login')
    
    db_path = "tickets_database.db"  # Path to the database file
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

  
           
    if request.method == 'POST':
 
      # Handle form data
        category = request.form['category']
        priority = request.form['priority']
        status = request.form['status']
        assignedto = request.form['AssignedTO'] 

   
            
        #Update the ticket in the database
        sql_query = (
            "UPDATE tickets SET "
            "category = ?, priority = ?, AssignedTO = ?, "
            "status = ?"
            "WHERE id = ?"
        )
        cursor.execute(sql_query, (category, priority,assignedto, status, ticket_id))
        connection.commit()
        connection.close()

        return redirect(url_for('view_ticket', ticket_id=ticket_id))  # Redirect after updating
    
    
    
    ticket = get_tickets(ticket_id)
    options_pri = ['high', 'medium', 'low']
    options_status = ['open', 'closed','pending']
    options_cat = get_categories()
    options_users = get_users()
    
    
    context = {
        'ticket': ticket,
        'options_pri': options_pri,
        'options_status': options_status,
        'options_cat': options_cat,
        'options_users': options_users,
    }
    
    return render_template('edit_ticket.html', context=context)   


@app.route('/view_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def view_ticket(ticket_id):
    if session.get('username') is None:
        return redirect('/tech_login')
   
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if request.method == 'POST':
        text = request.form['comment'].strip()  # Remove leading/trailing whitespace
        author = session['username']

        # Validate the comment text
        if not text:
            flash('Comment text cannot be empty', 'error')
        else:
            now = datetime.now()
            # Insert the comment into the database
            sql_query = "INSERT INTO comments (author, text, date, time, ticket_id) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (author, text, now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), ticket_id))
            connection.commit()


    tickets = get_tickets(ticket_id)
    comments = get_comments(ticket_id)


    return render_template('view_ticket.html', tickets=tickets, comments=comments, author=session['username'])



## add user route
@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

## edit user route
@app.route('/edit_user')
def edit_user():
    return render_template('edit_user.html')

## delete user route
@app.route('/delete_user')
def delete_user():
    return render_template('delete_user.html')

## search user route
@app.route('/search_user')
def search_user():
    return render_template('search_user.html')

## admin login route
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

##admin dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


## submit ticket route
class Ticket:
    def __init__(self, category, priority, description, status, attachments, createddate,requestername):
       
        self.createddate = createddate
        self.category = category
        self.priority = priority
        self.description = description
        self.status = status
        self.attachments = attachments
        self.requestername = requestername

@app.route('/submit_ticket', methods=['GET', 'POST'])
def submit_ticket():
    # Check if the user is authenticated
    if session.get('username') is None:  # If the user is not logged in
        return redirect('/tech_login')

    if request.method != 'POST':
        return render_template('submit_ticket.html')
    # Handle form data
    ticket_data = {
        'created_date': datetime.now(),
        'requestername': request.form['name'],
        'category': request.form['category'],
        'priority': request.form['priority'],
        'description': request.form['description']
      
        
    }

    try:
        db_path = "tickets_database.db"  # Path to the database file
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
    
    except Exception as e:
        print("Error:", e)  # Print the error for debugging
        return jsonify({"error":'An error occurred while submitting the ticket'})


    new_ticket = Ticket(
        createddate = datetime.now(),
        requestername= ticket_data['requestername'],
        category=ticket_data['category'],
        priority=ticket_data['priority'],
        description=ticket_data['description'],
        status='open',
        attachments= 'null',
     
    )

    sql_query = "INSERT INTO tickets (createddate, category, priority, description, status, attachments, requesterName) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql_query, ( 
              
    new_ticket.createddate,
    new_ticket.category,
    new_ticket.priority,
    new_ticket.description,
    new_ticket.status,
    new_ticket.attachments,
    new_ticket.requestername   
    ))
    
    connection.commit()
    connection.close()

    response_message = "Ticket submitted successfully!"
    #return render_template('technician_dashboard.html')
    return jsonify({
        "status":True,
        "message":response_message}), 200
  

## main dashboard route
@app.route('/main')
def main():
    overalls = "<p>Overall statistics...</p>"

    # Fetch ticket metrics from the database
    db_connection = sqlite3.connect('tickets_database.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT id, category, priority, status  FROM tickets")
    ticket_metrics = db_cursor.fetchall()

    # Fetch chart data from the database 
    db_cursor.execute("SELECT id, category, priority, status  FROM tickets")
    chart_data = db_cursor.fetchall()

    db_connection.close()

    return render_template('main.html', overalls=overalls, ticket_metrics=ticket_metrics, chart_data=chart_data)


## search ticket route
@app.route('/search_ticket')
def search_ticket():
    return render_template('search_ticket.html')

## close ticket route
@app.route('/close_ticket')
def close_ticket():
    return render_template('close_ticket.html')

## assets management route
@app.route('/assets_management', methods=['GET', 'POST'])
def assets_management():  # sourcery skip: avoid-builtin-shadow
  # Check if the user is authenticated
    if session.get('username') is None:  # If the user is not logged in
        return redirect('/tech_login')
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if request.method == 'POST':
        print(request.form)
        # Handle form data
        asset_name = request.form['asset_name']
        location = request.form['location']
        type = request.form['type']
        asset_tag = request.form['asset_tag']
        model = request.form['model']

        #Update the ticket in the database
        sql_query = "INSERT INTO asset_management (asset_name, location, type, asset_tag, model) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql_query, (asset_name, location, type, asset_tag, model ))
        connection.commit()
        connection.close()
        
    return render_template('assets_management.html')

## FAQ route
@app.route('/kb_faq')
def kb_faq():
    return render_template('kb_faq.html')

## ticket details route
@app.route('/ticket_details')
def ticket_details():
    return render_template('ticket_details.html')


@app.route('/ticket_list')
def ticket_list():
    return render_template('ticket_list.html')

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')


@app.route('/ticket_report')
def ticket_report():
    # Query the database to retrieve ticket data
    db_path = "tickets_database.db"  # Path to the database file
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    sql_query = "SELECT * FROM tickets where status = 'open'"
    sql_query = "SELECT * FROM tickets where category = 'Hardware'"
    sql_query = "SELECT * FROM tickets where priority = 'high'"
    sql_query = "SELECT * FROM tickets where status = 'closed'"
    sql_query = "SELECT * FROM tickets where category = 'Software'"
    sql_query = "SELECT * FROM tickets where priority = 'low'"
    sql_query = "SELECT * FROM tickets where status = 'open'"
    
    
    tickets = cursor.execute(sql_query).fetchall()

    connection.close()

    return render_template('ticket_report.html', tickets=tickets)



@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
   
