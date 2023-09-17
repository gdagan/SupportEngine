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

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        if user_id not in users:
            return f"User with ID {user_id} does not exist."

        name = request.form['name']
        # Update user data
        users[user_id]['name'] = name
        email = request.form['email']
        users[user_id]['email'] = email
        users[user_id]['role'] = request.form['role']

        return f"User with ID {user_id} updated successfully!"
    user_id = int(request.args.get('id'))
    if user_id not in users:
        return "User not found."
    user = users[user_id]
    return render_template('edit_user.html', user=user)

if __name__ == '__main__':
    app.run()
