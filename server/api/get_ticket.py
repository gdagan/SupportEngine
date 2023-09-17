from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('tickets.db')
cursor = conn.cursor()

# API endpoint to get ticket details by ID
@app.route('/api/ticket/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    if ticket := cursor.fetchone():
        ticket_data = {
            'id': ticket[0],
            'category': ticket[1],
            'priority': ticket[2],
            'description': ticket[3],
            'status': ticket[4],
            'attachments': ticket[5].split(','),
            'comments': ticket[6].split(',')
        }
        return jsonify(ticket_data)
    else:
        return jsonify({'error': 'Ticket not found'}), 404

# API endpoint to update ticket details by ID
@app.route('/api/ticket/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = request.get_json()
    cursor.execute("""
        UPDATE tickets
        SET category = ?, priority = ?, description = ?, status = ?, attachments = ?, comments = ?
        WHERE id = ?
    """, (
        ticket.get('category'),
        ticket.get('priority'),
        ticket.get('description'),
        ticket.get('status'),
        ','.join(ticket.get('attachments', [])),
        ','.join(ticket.get('comments', [])),
        ticket_id
    ))
    conn.commit()
    if cursor.rowcount > 0:
        return jsonify(ticket)
    else:
        return jsonify({'error': 'Ticket not found'}), 404
