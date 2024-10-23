from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Create a Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'
#not working
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rajkumarsain'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'employeetypingtest'

# Initialize MySQL
mysql = MySQL(app)
 
# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in the database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['user_type'] = account['user_type']
           # Redirect based on user_type
            if account['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif account['user_type'] == 'examiner':
                return redirect(url_for('examiner_dashboard'))
            elif account['user_type'] == 'participant':
                return redirect(url_for('participant_dashboard'))
            else:
                msg = 'Invalid user type!'
        else:
            # Account does not exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

# Route for the admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    # Check if the user is logged in and is admin
    if 'loggedin' in session and session['user_type'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

# Route for the examiner dashboard
@app.route('/examiner_dashboard')
def examiner_dashboard():
    # Check if the user is logged in and is admin
    if 'loggedin' in session and session['user_type'] == 'examiner':
        return render_template('examiner_dashboard.html')
    else:
        return redirect(url_for('login'))
    
# Route for the participant dashboard
@app.route('/participant_dashboard')
def participant_dashboard():
    # Check if the user is logged in and is admin
    if 'loggedin' in session and session['user_type'] == 'participant':
        return render_template('participant_dashboard.html')
    else:
        return redirect(url_for('login'))

#Route to handle the form submission after typing by participant
@app.route('/save_text', methods=['POST'])
def save_text():
    typed_text = request.form['typed_text']
    # You can save the text to a file or database here
    return redirect(url_for('participant_dashboard'))


# Route for logging out
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
