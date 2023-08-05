from flask import Flask, render_template, request

app = Flask(__name__)

# User data dictionary (example data)
users = {
    1: {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'role': 'admin'
    },
    2: {
        'name': 'Jane Smith',
        'email': 'janesmith@example.com',
        'role': 'user'
    }
}

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = int(request.form['user_id'])

    if user_id not in users:
        return f"User with ID {user_id} does not exist."
    del users[user_id]
    return f"User with ID {user_id} deleted successfully!"

if __name__ == '__main__':
    app.run()
