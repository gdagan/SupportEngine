from flask import Flask, render_template, request

app = Flask(__name__)

# Sample user ticket data (replace with actual data retrieval logic)
def get_user_tickets(user_id):
    return [
        {
            'id': 'TCK-123',
            'category': 'Hardware',
            'priority': 'High',
            'status': 'Open',
        },
        {
            'id': 'TCK-124',
            'category': 'Software',
            'priority': 'Medium',
            'status': 'In Progress',
        },
        {
            'id': 'TCK-125',
            'category': 'Network',
            'priority': 'Low',
            'status': 'Closed',
        },
    ]

@app.route('/dashboard')
def user_dashboard():
    if user_id := request.args.get('user_id'):
        # Fetch user's ticket information based on the user_id
        tickets = get_user_tickets(user_id)
        return render_template('user_dashboard.html', tickets=tickets)
    else:
        return 'Invalid user ID'

if __name__ == '__main__':
    app.run()
