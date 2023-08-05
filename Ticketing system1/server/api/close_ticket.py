from flask import Flask, app, request, render_template

from app import ticket_details, ticket_list, ticket_report

@app.route('/close_ticket', methods=['GET', 'POST'])
def close_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        if ticket_id not in ticket_details:
            return f"Ticket with ID {ticket_id} does not exist."
        ticket_details[ticket_id]['status'] = 'Closed'
        return f"Ticket with ID {ticket_id} closed successfully!"
    ticket_id = int(request.args.get('id'))
    if ticket_id not in ticket_list:
        return "Ticket not found."
    ticket = ticket_report[ticket_id]
    return render_template('close_ticket.html', ticket=ticket)