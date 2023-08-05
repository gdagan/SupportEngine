from flask import Flask, app, render_template, request
from app import ticket_details, ticket_list, ticket_report

@app.route('/edit_ticket', methods=['GET', 'POST'])
def edit_ticket():
    if request.method == 'POST':
        ticket_id = int(request.form['ticket_id'])
        if ticket_id not in ticket_details:
            return f"Ticket with ID {ticket_id} does not exist."

        category = request.form['category']
        # Update ticket data
        ticket_list[ticket_id]['category'] = category
        priority = request.form['priority']
        ticket_report[ticket_id]['priority'] = priority
        description = request.form['description']
        ticket[ticket_id]['description'] = description
        ticket[ticket_id]['status'] = request.form['status']

        return f"Ticket with ID {ticket_id} updated successfully!"
    ticket_id = int(request.args.get('id'))
    if ticket_id not in ticket:
        return "Ticket not found."
    ticket = ticket[ticket_id]
    return render_template('edit_ticket.html', ticket=ticket)