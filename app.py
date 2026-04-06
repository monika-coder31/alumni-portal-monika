from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'alumni-portal-complete-189-lines'

ALUMNI_DATA = [
    {"id": 1, "name": "John Doe", "grad_year": 2020, "job": "Software Engineer", "company": "Google", "email": "john@email.com"},
    {"id": 2, "name": "Jane Smith", "grad_year": 2021, "job": "Data Scientist", "company": "Microsoft", "email": "jane@email.com"},
    {"id": 3, "name": "Mike Johnson", "grad_year": 2019, "job": "Product Manager", "company": "Amazon", "email": "mike@email.com"},
    {"id": 4, "name": "Sarah Wilson", "grad_year": 2022, "job": "UX Designer", "company": "Meta", "email": "sarah@email.com"},
    {"id": 5, "name": "David Brown", "grad_year": 2018, "job": "DevOps", "company": "Netflix", "email": "david@email.com"}
]

USERS = {
    "admin": hashlib.md5("admin123".encode()).hexdigest(),
    "student": hashlib.md5("student456".encode()).hexdigest()
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title>Alumni Portal</title>
<style>
body {{ font-family: Arial; background: #f0f2f5; margin: 0; padding: 20px; }}
.container {{ max-width: 1200px; margin: auto; }}
.header {{ background: #4267B2; color: white; padding: 20px; text-align: center; border-radius: 10px; }}
.nav {{ display: flex; gap: 10px; justify-content: center; margin: 20px 0; flex-wrap: wrap; }}
.nav a {{ background: #1877F2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
.login {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
.card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
.logout {{ float: right; background: #e74c3c; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; }}
</style>
</head>
<body>
<div class="container">
'''

@app.route('/')
def home():
    if 'user' not in session:
        return render_template_string(HTML_TEMPLATE + '''
        <div class="login">
            <h2>Login - Alumni Portal</h2>
            <form method="POST" action="/login">
                Username: <input type="text" name="username" required><br><br>
                Password: <input type="password" name="password" required><br><br>
                <button type="submit">Login</button>
            </form>
            <p><small>admin/admin123 | student/student456</small></p>
        </div>
        </body></html>''')
    
    return render_template_string(HTML_TEMPLATE + f'''
    <div class="header">
        <h1>🏛️ Alumni Portal</h1>
        <p>Welcome {session["user"]}! <a href="/logout" class="logout">Logout</a></p>
    </div>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/alumni">Alumni</a>
        <a href="/events">Events</a>
    </div>
    <h2>Recent Alumni</h2>
    <div class="grid">
    ''', **locals())

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    
    if username in USERS and USERS[username] == password:
        session['user'] = username
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/alumni')
def alumni():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    alumni_html = '<div class="grid">'
    for a in ALUMNI_DATA:
        alumni_html += f'''
        <div class="card">
            <h3>{a["name"]}</h3>
            <p>Grad: {a["grad_year"]} | {a["job"]} @ {a["company"]}</p>
            <p>{a["email"]}</p>
        </div>'''
    alumni_html += '</div>'
    
    return render_template_string(HTML_TEMPLATE + f'''
    <div class="header">
        <h1>👥 Alumni Directory</h1>
        <a href="/" class="logout">← Back</a>
    </div>
    {alumni_html}
    </body></html>''')

@app.route('/events')
def events():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    return render_template_string(HTML_TEMPLATE + '''
    <div class="header">
        <h1>📅 Events</h1>
        <a href="/" class="logout">← Back</a>
    </div>
    <div class="grid">
        <div class="card">
            <h3>Reunion 2026</h3>
            <p>June 15th - Campus Hall</p>
        </div>
        <div class="card">
            <h3>Career Fair</h3>
            <p>May 20th - Online</p>
        </div>
    </div>
    </body></html>''')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
"""
lines = len(full_code.strip().split('\n'))
print(f"Total lines in app.py: {lines}")

with open("output/alumni_portal_complete_app.py", 'w') as f:
    f.write(full_code)

print("File saved as output/alumni_portal_complete_app.py")
