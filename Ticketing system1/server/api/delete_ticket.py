from flask import Flask, app, render_template, request

from app import ticket_details, ticket_list, ticket_report

@app.route('/delete_ticket', methods=['GET', 'POST'])
def delete_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        if ticket_id not in ticket_report:
            return f"Ticket with ID {ticket_id} does not exist."
        del ticket_details[ticket_id]
        return f"Ticket with ID {ticket_id} deleted successfully!"
    ticket_id = int(request.args.get('id'))
    if ticket_id not in ticket_list:
        return "Ticket not found."
    ticket = ticket[ticket_id]
    return render_template('delete_ticket.html', ticket=ticket)