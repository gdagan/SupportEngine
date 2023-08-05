from flask import Flask, render_template, request

app = Flask(__name__)

# Ticket data dictionary (example data)
tickets = {
    1: {
        'category': 'Hardware',
        'priority': 'High',
        'description': 'Issue with monitor',
        'status': 'Open'
    },
    2: {
        'category': 'Software',
        'priority': 'Medium',
        'description': 'Application crash',
        'status': 'Open'
    }
}

@app.route('/edit_ticket', methods=['GET', 'POST'])
def edit_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        if ticket_id not in tickets:
            return f"Ticket with ID {ticket_id} does not exist."

        category = request.form['category']
        # Update ticket data
        tickets[ticket_id]['category'] = category
        priority = request.form['priority']
        tickets[ticket_id]['priority'] = priority
        description = request.form['description']
        tickets[ticket_id]['description'] = description
        tickets[ticket_id]['status'] = request.form['status']

        return f"Ticket with ID {ticket_id} updated successfully!"
    ticket_id = int(request.args.get('id'))
    if ticket_id not in tickets:
        return "Ticket not found."
    ticket = tickets[ticket_id]
    return render_template('edit_ticket.html', ticket=ticket)

if __name__ == '__main__':
    app.run()
