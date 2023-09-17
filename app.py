from flask import Flask, json, jsonify, render_template, request, redirect, session, url_for, flash, send_from_directory
import sqlite3  # to use SQL in Python
import pandas as pd
from datetime import datetime
import uuid  # to generate random reset tokens
from flask_mail import Mail, Message
import os
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt 
import pypandoc




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


def send_email(recipient, subject, body):
    msg = Message(subject, recipients=[recipient], body=body)
    mail.send(msg)

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

def get_requests_by_technician(technician_email):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    sql_query = """ 
        SELECT COUNT(*) FROM tickets WHERE AssignedTo = ?
        """
    return cursor.execute(sql_query,(technician_email,)).fetchone()[0]


def get_tickets_by_status(stat):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = f"SELECT * FROM tickets where status = '{stat}'"
    return cursor.execute(query).fetchall()

def get_tickets_by_department(dep):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = f"SELECT * FROM tickets where department = '{dep}'"
    return cursor.execute(query).fetchall()

def get_tickets_priority(pri):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = f"SELECT * FROM tickets where priority = '{pri}'"
    return cursor.execute(query).fetchall()

def create_ticket(createddate, description, priority, category, requestername):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    sql_query = """
        INSERT INTO tickets (createddate, description, priority, category, requestername)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(sql_query, (createddate, description, priority, category, requestername))
    connection.commit()
    return cursor.execute("SELECT * FROM tickets WHERE id = ?", (cursor.lastrowid,)).fetchone()


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

def format_time(cols):
    dby = cols[0]
    return dby if dby is None else str(dby).split('.')[0]

# # Technician Dashboard route
@app.route('/technician_dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['username'] is None:
        return redirect('/tech_login')
    username = session['username']
    
    # Get the current date and format it as a string
    current_date = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    
    status = None 
   
   
    
    ticket_filtering = {
        'options' : ['All Tickets', 'My Tickets', 'Closed Tickets', 'Open Tickets', 'Hold Tickets', 'Unassigned Tickets'],
        'selected': 'All Tickets'
    }     
    
    if request.method == 'POST':
        form_data = request.form.to_dict()
        value = form_data.get('TicketList')
        
        if value == "Unassigned":
            tickets = get_tickets_by_status('unassigned')
            ticket_filtering['selected'] = 'Unassigned Tickets'
        if value == "My":
            assignedTo = session['username']
            tickets = get_tickets(username=assignedTo)
            ticket_filtering['selected'] = 'My Tickets'
        elif value == "Closed":
            tickets = get_tickets_by_status('closed')
            ticket_filtering['selected'] = 'Closed Tickets'
        elif value == "Open":
            tickets = get_tickets_by_status('open')
            ticket_filtering['selected'] = 'Open Tickets'
        elif value == "Hold":
            tickets = get_tickets_by_status('hold')
            ticket_filtering['selected'] = 'Hold Tickets'
        else:
            tickets = get_tickets()
            ticket_filtering['selected'] = 'All Tickets'
    else:
        tickets = get_tickets()

    df_tickets = pd.DataFrame(tickets, columns=['id', 'desc', 'reqName', 'assto', 'dby', 'cat', 'pri', 'cby', 'stat', 'attach', 'dep','act'])
    df_tickets['cby'] = df_tickets[['cby']].apply(format_time,axis=1)
    df_tickets['dby'] = df_tickets[['dby']].apply(format_time,axis=1)


    num_all = df_tickets.shape[0]
    num_high = df_tickets[df_tickets['pri'].str.lower() == 'high'].shape[0]
    num_open = df_tickets[df_tickets['stat'].str.lower() == 'open'].shape[0]
    num_closed = df_tickets[df_tickets['stat'].str.lower() == 'closed'].shape[0]
    num_hold = df_tickets[df_tickets['stat'].str.lower() == 'hold'].shape[0]
    num_unassigned = df_tickets[df_tickets['assto'].str.lower() == 'unassigned'].shape[0]
    
    

    overalls = {
        'All Tikcets': num_all,
        'All High Priority Tickets': num_high,
        'All Open Tickets': num_open,
        'All Closed Ticket': num_closed,
        'All Hold Tickets': num_hold,
        'All Unassigned Tickets': num_unassigned,
    }

    overalls_text = f'''
        'All Tikcets': {num_all},
        'All High Priority Tickets': {num_high},
        'All Open Tickets': {num_open},
        'All Closed Ticket': {num_closed},  
        'All Hold Tickets': {num_hold},
        'All Unassigned Tickets': {num_unassigned},
    '''
    


    return render_template('technician_dashboard.html', username=username, tickets=df_tickets.values.tolist(), overalls=overalls_text, current_date=current_date,ticket_filtering=ticket_filtering)


### Logout route
@app.route('/tech_logout')
def logout():
    session['username'] = None
    return redirect('/tech_login')


### User portal route

@app.route('/user_portal', methods=['GET','POST'])
def user_portal():
    
    # Check if the user is authenticated
    if session.get('username') is None:  # If the user is not logged in
        return redirect('/user_login')   
        
    if request.method != 'POST':
        return render_template('user_portal.html')
    
    #Handle form data
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

    sql_query = "INSERT INTO tickets (createddate, category, priority, description, status,resolveddate attachments, requesterName) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
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
    
    # Check if the user credentials are valid
    for user in users:
        if user[-3] == username and user[-1] == password:
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
        cursor.execute(sql_query, (category, priority, assignedto, status, ticket_id))
        connection.commit()
        connection.close()

        return redirect(url_for('view_ticket', ticket_id=ticket_id))  # Redirect after updating
    
    
    
    ticket = get_tickets(ticket_id)
    options_pri = ['high', 'medium', 'low']
    options_status = ['open', 'closed','hold','pending','unassigned']
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
    def __init__(self, category, priority, description, status,dueby, attachments, createddate,requestername):
       
        self.createddate = createddate
        self.category = category
        self.priority = priority
        self.description = description
        self.status = status
        self.attachments = attachments
        self.requestername = requestername
        self.dueby = dueby 

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

    if attachment := request.files.get('attachment'):
        attachment.save(os.path.join('static/attachments', attachment.filename))
        ticket_data['attachments'] = 'static/attachments' + attachment.filename
    else:
        ticket_data['attachments'] = 'none'
        
# Define SLA timeframes based on priority

    sla_timeframes = {
        'high': timedelta(hours=4),
        'medium': timedelta(hours=36),
        'low': timedelta(hours=72)
    }

    # Calculate the dueby date based on priority
    dueby = ticket_data['created_date'] + sla_timeframes.get(ticket_data['priority'], timedelta(hours=24))

    try:
        db_path = "tickets_database.db"  # Path to the database file
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

    except Exception as e:
        print("Error:", e)  # Print the error for debugging
        return jsonify({"error": 'An error occurred while submitting the ticket'})

    new_ticket = Ticket(
        createddate = datetime.now(),
        requestername= ticket_data['requestername'],
        category=ticket_data['category'],
        priority=ticket_data['priority'],
        description=ticket_data['description'],
        status='open',
        attachments= 'static/attachments' + attachment.filename,
        dueby = dueby

    )

    sql_query = "INSERT INTO tickets (createddate, category, priority, description, status, attachments, requesterName, dueby, AssignedTo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql_query, ( 

    new_ticket.createddate,
    new_ticket.category,
    new_ticket.priority,
    new_ticket.description,
    new_ticket.status,
    new_ticket.attachments,
    new_ticket.requestername,
    new_ticket.dueby,
    'unassigned'

    ))

    connection.commit()
    connection.close()

    response_message = "Ticket submitted successfully!"

    return jsonify({
        "status":True,
        "message":response_message}), 200
  

# main dashboard route
@app.route('/main')
def main():
    # Query the database to retrieve the required data for the report
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Query to get requests by technician
    sql_requests_by_technician = """
        SELECT AssignedTo, COUNT(*) as request_count
        FROM tickets
        WHERE status IN ('open', 'pending', 'hold', 'unassigned')
        GROUP BY AssignedTo
    """
    cursor.execute(sql_requests_by_technician)
    requests_by_technician = cursor.fetchall()
   

    # Query to get tickets by status
    sql_tickets_by_status = """
        SELECT status, COUNT(*) as ticket_count
        FROM tickets
        GROUP BY status
    """
    cursor.execute(sql_tickets_by_status)
    tickets_by_status = cursor.fetchall()

    # Query to get tickets by priority
    sql_tickets_by_priority = """
        SELECT priority, COUNT(*) as ticket_count
        FROM tickets
        GROUP BY priority
    """
    cursor.execute(sql_tickets_by_priority)
    tickets_by_priority = cursor.fetchall()
    
    # query tickets by category
    sql_tickets_by_category = """
        SELECT category, COUNT(*) as ticket_count
        FROM tickets
        GROUP BY category
    """
    cursor.execute(sql_tickets_by_category)
    tickets_by_category = cursor.fetchall()
    
   
       
    connection.close()

    plt.figure(figsize=(10,10))
    data = []
    keys = []
    for item in requests_by_technician:
        data.append(item[1])
        keys.append(item[0])
    palette_color = sns.color_palette('bright')
    plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%') 
    plt.savefig('static/stats/requests_by_technician.png', bbox_inches='tight')

    plt.figure(figsize=(10,10))
    data.clear()
    keys.clear()
    for item in tickets_by_status:
        data.append(item[1])
        keys.append(item[0])
    palette_color = sns.color_palette('bright')
    plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%') 
    plt.savefig('static/stats/tickets_by_status.png', bbox_inches='tight')
   
    plt.figure(figsize=(10,10))
    data.clear()
    keys.clear()
    for item in tickets_by_priority:
        data.append(item[1])
        keys.append(item[0])
    palette_color = sns.color_palette('bright')
    plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%') 
    plt.savefig('static/stats/tickets_by_priority.png', bbox_inches='tight')
    
    plt.figure(figsize=(10,10))
    data.clear()
    keys.clear()
    for item in tickets_by_category:
        data.append(item[1])
        keys.append(item[0])
    palette_color = sns.color_palette('bright')
    plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%') 
    plt.savefig('static/stats/tickets_by_category.png', bbox_inches='tight')   
    
      
    
    # Process the data and generate the report
    return render_template(
        'main.html',
        requests_by_technician=requests_by_technician,
        tickets_by_status=tickets_by_status,
        tickets_by_priority=tickets_by_priority, 
        tickets_by_category=tickets_by_category,
       
    )

 

# class Asset:
#     def __init__(self, asset_name, asset_tag, asset_type, location, model):
#         self.asset_name = asset_name
#         self.location = location
#         self.asset_type = asset_type
#         self.asset_tag = asset_tag
#         self.model = model
  
# @app.route('/assets_management', methods=['GET', 'POST'])
# def assets_management():
#     # Check if the user is authenticated
#     if session.get('username') is None:  # If the user is not logged in
#         return redirect('/tech_login')
    
       
#     db_path = "tickets_database.db"  # Path to the database file
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     if request.method != 'POST':
#         render_template('assets_list.html')
        
#         # Handle form data
#         asset_data = {
#         'asset_name' : request.form['asset_name'],
#         'location' : request.form['location'],  
#         'asset_type' : request.form['asset_type'] , 
#         'asset_tag' : request.form['asset_tag'],   
#         'model' : request.form['model']           
        
#         } 
        
#         try:
#             db_path = "tickets_database.db"  # Path to the database file
#             connection = sqlite3.connect(db_path)
#             cursor = connection.cursor()
            
#         except Exception as e:
#             print("Error:", e)
#             return jsonify({"error": 'An error occurred while submitting the ticket'})
        
#         new_asset = Asset(
#         asset_name = asset_data['asset_name'],
#         location = asset_data['location'],
#         asset_type = asset_data['asset_type'],
#         asset_tag = asset_data['asset_tag'],
#         model = asset_data['model']
                
#         )
        
#         # Update the asset in the database
#         sql_query = "INSERT INTO asset_management (asset_name, location, asset_type, asset_tag, model) VALUES (?, ?, ?, ?, ?)"
#         cursor.execute(sql_query, (
        
#         new_asset.asset_name,
#         new_asset.location,
#         new_asset.asset_type,
#         new_asset.asset_tag,
#         new_asset.model
                   
#         ))
        
#         connection.commit()
#         connection.close()
        
       
#         # response_message = "Asset submitted successfully!"
#         # return jsonify({
#         # "status":True,
#         # "message":response_message}), 200
        
#     return render_template('assets_management.html')
    

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        # Handle form data to add a new asset to the database
        asset_name = request.form['asset_name']
        asset_tag = request.form['asset_tag']
        asset_type = request.form['asset_type']
        location = request.form['location']
        model = request.form['model']

        # Insert the new asset into the database
        connection = sqlite3.connect(db_path)  # Use your database path
        cursor = connection.cursor()
        cursor.execute("INSERT INTO asset_management (asset_name, location, asset_type, asset_tag, model) VALUES (?, ?, ?, ?, ?)",
                       (asset_name, asset_tag, asset_type, location, model))
        connection.commit()
        connection.close()

    # Fetch the list of assets from the database
    connection = sqlite3.connect(db_path)  # Use your database path
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM asset_management")
    asset_management = cursor.fetchall()
    connection.close()

    return render_template('add_asset.html', asset_management=asset_management)


@app.route('/delete_asset/<int:asset_id>', methods=['GET', 'POST'])
def delete_asset(asset_id):
    if session.get('username') is None:
        return redirect('/tech_login')
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Check if the ticket exists
    cursor.execute("SELECT * FROM asset_management WHERE id = ?", (asset_id,))
    asset = cursor.fetchone()
    
    if not asset:
        connection.close()
        return jsonify({"error": "Asset not found"}), 404
    
    # Delete the ticket from the database
    cursor.execute("DELETE FROM asset_management WHERE id = ?", (asset_id,))
    connection.commit()
    connection.close()
    
    return jsonify({"message": "Asset deleted successfully"}), 200


@app.route('/assets_list')
def assets_list():
    return render_template('assets_list.html')
    



# API route for resolving a ticket
@app.route('/resolve_ticket/<int:ticket_id>', methods=['GET'])
def resolve_ticket(ticket_id):
    if session.get('username') is None:  # If the user is not logged in
        return redirect('/tech_login')
    
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    
    # Check if the ticket exists
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    if not ticket:
        connection.close()
        return jsonify({"error": "Ticket not found"}), 404
    
    # print(ticket[8])
    
    # Check if the ticket is already resolved
    if ticket[8] == 'Resolved':
        connection.close()
        return jsonify({"error": "Ticket is already resolved"}), 400

    # Update the ticket status to 'Resolved' and set the resolution date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE tickets SET status = ?, resolveddate = ? WHERE id = ?",
                   ('Resolved', current_datetime, ticket_id))
    connection.commit()
    connection.close()

    # return jsonify({"message": "Ticket resolved successfully"}), 200
    

    return redirect(url_for('dashboard'))  # Redirect after updating

## FAQ route
@app.route('/kb_faq')   
def kb_faq():
    # Convert the Word document to HTML
    # html_content = convert_word_to_html(
    #     'static/kb_articles/Adding another mailbox to your profile.doc'
        
    #     )
    
    return render_template('kb_faq.html')

## ticket details route
@app.route('/ticket_details')
def ticket_details():
    return render_template('ticket_details.html')


@app.route('/ticket_list')
def ticket_list():  # sourcery skip: avoid-builtin-shadow
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    all = get_tickets()
    
    return render_template('ticket_list.html' , all=all)

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')



@app.route('/ticket_report')
def ticket_report():
    # Query the database to retrieve the required data for the report
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Query to get requests by technician
    sql_requests_by_technician = """
        SELECT AssignedTo, COUNT(*) as request_count
        FROM tickets
        WHERE status IN ('open', 'pending', 'hold', 'unassigned')
        GROUP BY AssignedTo
    """
    cursor.execute(sql_requests_by_technician)
    requests_by_technician = cursor.fetchall()

    # Query to get tickets by status
    sql_tickets_by_status = """
        SELECT status, COUNT(*) as ticket_count
        FROM tickets
        GROUP BY status
    """
    cursor.execute(sql_tickets_by_status)
    tickets_by_status = cursor.fetchall()

    # Query to get tickets by priority
    sql_tickets_by_priority = """
        SELECT priority, COUNT(*) as ticket_count
        FROM tickets
        GROUP BY priority
    """
    cursor.execute(sql_tickets_by_priority)
    tickets_by_priority = cursor.fetchall()
    
    # query tickets by category
    sql_tickets_by_category = """
        SELECT category, COUNT(*) as ticket_count
        FROM tickets
        GROUP BY category
    """
    cursor.execute(sql_tickets_by_category)
    tickets_by_category = cursor.fetchall()
    

    connection.close()

    # Process the data and generate the report
    return render_template(
        'ticket_report.html',
        requests_by_technician=requests_by_technician,
        tickets_by_status=tickets_by_status,
        tickets_by_priority=tickets_by_priority,
        tickets_by_category=tickets_by_category
    )



@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')


# @app.route('/test_email')
# def test_email():
#     try:
#         # Create a test email message
#         subject = 'Test Email'
#         recipients = ['ghicer@gmail.com']  # Replace with a recipient's email address
#         message_body = 'This is a test email from your Flask application.'

#         message = Message(subject=subject,
#                           recipients=recipients,
#                           body=message_body)

#         # Send the test email
#         mail.send(message)

#         return 'Test email sent successfully!'
#     except Exception as e:
#         return f'Error sending test email: {str(e)}'


@app.route('/display_kb')
def display_kb():
    filename = 'vlaning ports.doc'
        
    return send_from_directory('static', filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
   
