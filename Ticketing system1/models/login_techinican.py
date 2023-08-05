from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Technician data dictionary (example data)
technicians = {
    'john': 'password123',
    'jane': 'password456'
}

@app.route('/login_technician', methods=['GET', 'POST'])
def login_technician():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in technicians and technicians[username] == password:
            # Technician login successful, redirect to dashboard or desired page
            return redirect('/dashboard')
        else:
            return "Invalid username or password. Please try again."

    return render_template('login_technician.html')

@app.route('/dashboard')
def dashboard():
    # Check if technician is logged in, otherwise redirect to login page
    # Add logic to display technician's dashboard

    
    
    
    
    return "Technician Dashboard"

if __name__ == '__main__':
    app.run()
