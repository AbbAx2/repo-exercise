# insecure_code.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Example of SQL Injection vulnerability
@app.route('/search')
def search():
    query = request.args.get('query')
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{query}'")  # SQL Injection
    result = cursor.fetchall()
    return str(result)

# Example of Cross-Site Scripting (XSS) vulnerability
@app.route('/xss', methods=['GET', 'POST'])
def xss():
    if request.method == 'POST':
        username = request.form['username']
        return render_template_string(f'<h1>Hello {username}</h1>')  # XSS vulnerability
    return '''
        <form method="POST">
            <input type="text" name="username" />
            <input type="submit" value="Submit" />
        </form>
    '''

# Example of Insecure Direct Object Reference (IDOR) vulnerability
@app.route('/profile/<user_id>')
def profile(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # IDOR vulnerability
    result = cursor.fetchall()
    return str(result)

# Example of Broken Authentication vulnerability
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")  # Broken Authentication
    result = cursor.fetchall()
    if result:
        return 'Login successful'
    else:
        return 'Invalid credentials'

# Example of Security Misconfiguration vulnerability
@app.route('/admin')
def admin():
    # Imagine this is an unprotected route for admin users
    return 'Welcome to the admin panel'

if __name__ == '__main__':
    app.run(debug=True)
