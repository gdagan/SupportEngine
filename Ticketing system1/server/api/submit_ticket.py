from flask import Flask, render_template, request
from app import ticket_details

app = Flask(__name__)


@app.route('/submit_ticket', methods=['GET', 'POST'])
def submit_ticket():
    if request.method == 'POST':
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']

        global ticket_id
        ticket_details[ticket_id] = {
            'category': category,
            'priority': priority,
            'description': description,
            'status': 'Open'
        }
        ticket_id += 1

        return f"Ticket submitted successfully! Ticket ID: {ticket_id - 1}"

    return render_template('submit_ticket.html')