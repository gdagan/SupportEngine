from flask import Flask, app, render_template, request
from app import ticket_details, ticket_list, ticket_report


@app.route('/search_ticket', methods=['GET', 'POST'])
def search_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        if ticket_id not in ticket_details:
            return f"Ticket with ID {ticket_id} does not exist."
        ticket = ticket_list[ticket_id]
        return render_template('search_ticket.html', ticket=ticket)
    ticket_id = int(request.args.get('id'))
    if ticket_id not in ticket_report:
        return "Ticket not found."
    ticket = ticket[ticket_id]
    return render_template('search_ticket.html', ticket=ticket)