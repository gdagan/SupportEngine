from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Set a secret key for session encryption



# Login route
@app.route('/technician_login', methods=['GET', 'POST'])
def technician_login():
    if request.method != 'POST':
        return render_template('technician_dashboard.html')
    username = request.form['username']
    password = request.form['password']

    db_path = './tickets_database.db'  # please download 'olist.db' from the Courseworks
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    sql_query = """
                    SELECT
                        *
                    FROM 
                      technician
                    """

    technicians = cursor.execute(sql_query).fetchall()
    print(technicians)
    print(request)
    # Check if the technician credentials are valid
    for technician in technicians:
        if technician['username'] == username and technician['password'] == password:
            session['username'] = username
            return redirect('/technician_dashboard.html')

    # return render_template('login.html', error='Invalid credentials')

# # Dashboard route
# @app.route('/technician_dashboard')
# def dashboard():
#     if 'username' not in session:
#         return redirect('/login')
#     # Fetch technician-specific data based on the logged-in technician's username
#     username = session['username']
   
#     tickets = get_technician_tickets(username)

#     return render_template('technician_dashboard.html', username=username, tickets=tickets)

# # Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


# Ticket data dictionary (example data)
tickets = {}
ticket_id = 1


@app.route('/view_tickets')
def view_tickets():
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/view_ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    if ticket_id not in tickets:
        return "Ticket not found."
    ticket = tickets[ticket_id]
    return render_template('view_ticket.html', ticket=ticket)

@app.route('/view_ticket')
def view_ticket_query():
    ticket_id = int(request.args.get('id'))
    if ticket_id not in tickets:
        return "Ticket not found."
    ticket = tickets[ticket_id]
    return render_template('view_ticket.html', ticket=ticket)

@app.route('/view_tickets/<int:ticket_id>')
def view_ticket_redirect(ticket_id):
    return view_ticket(ticket_id)

@app.route('/view_tickets')
def view_tickets_redirect():
    return view_tickets()


@app.route('/')
def root():
    return render_template('technician_login.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/edit_user')
def edit_user():
    return render_template('edit_user.html')

@app.route('/delete_user')
def delete_user():
    return render_template('delete_user.html')

@app.route('/search_user')
def search_user():
    return render_template('search_user.html')
@app.route('/add_ticket')
def add_ticket():
    return render_template('add_ticket.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

# @app.route('/technician_login')
# def technician_login():
#     return render_template('technician_login.html')

@app.route('/main')
def main():
    return render_template('main.html')

    
    
    
# @app.route('/search_ticket')
# def search_ticket():
#     return render_template('search_ticket.html')

# @app.route('/close_ticket')
# def close_ticket():
#     return render_template('close_ticket.html')

@app.route('/assets_management')
def assets_management():
    return render_template('assets_management.html')

@app.route('/kb_faq')
def kb_faq():
    return render_template('kb_faq.html')

@app.route('/technician_dashboard')
def technician_dashboard():
    return render_template('technician_dashboard.html')

@app.route('/ticket_details')
def ticket_details():
    return render_template('ticket_details.html')

# @app.route('/ticket_list')
# def ticket_list():
#     return render_template('ticket_list.html')

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/ticket_list')
def ticket_list():
    return render_template('ticket_list.html')

@app.route('/ticket_report')
def ticket_report():
    return render_template('ticket_report.html')

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
      app.run(host="0.0.0.0", debug=True)

    