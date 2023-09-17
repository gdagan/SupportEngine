from flask import Flask, request, render_template, app
from app import tickets

@app.route('/reopen_ticket', methods=['GET', 'POST'])
def reopen_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        if ticket_id not in tickets:
            return f"Ticket with ID {ticket_id} does not exist."
        tickets[ticket_id]['status'] = 'Open'
        return f"Ticket with ID {ticket_id} reopened successfully!"
    ticket_id = int(request.args.get('id'))
    if ticket_id not in tickets:
        return "Ticket not found."
    ticket = tickets[ticket_id]
    return render_template('reopen_ticket.html', ticket=ticket)