from flask import Flask, render_template_string, request, session, redirect
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'alumni-portal-2026-final'

users = {"admin": hashlib.md5("admin123".encode()).hexdigest()}
alumni_data = [
    {"name": "John Doe", "year": "2020", "company": "Google", "role": "Engineer"},
    {"name": "Jane Smith", "year": "2021", "company": "Microsoft", "role": "Data Scientist"},
    {"name": "Mike Johnson", "year": "2019", "company": "Amazon", "role": "Product Manager"},
    {"name": "Sarah Wilson", "year": "2022", "company": "Meta", "role": "UX Designer"},
    {"name": "David Brown", "year": "2018", "company": "Netflix", "role": "DevOps"}
]

MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Alumni Portal - Monika</title>
    <style>
        * {margin:0;padding:0;box-sizing:border-box;}
        body {font-family:Arial;background:#f0f2f5;padding:20px;}
        .container {max-width:1200px;margin:auto;}
        .header {background:#4267b2;color:white;padding:30px;border-radius:10px;text-align:center;}
        .nav {display:flex;gap:15px;justify-content:center;margin:20px 0;flex-wrap:wrap;}
        .nav a {background:#1877f2;color:white;padding:12px 24px;text-decoration:none;border-radius:25px;}
        .login {max-width:400px;margin:50px auto;background:white;padding:30px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
        .grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;}
        .card {background:white;padding:20px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
        .logout {float:right;background:#e74c3c;color:white;padding:8px 16px;text-decoration:none;border-radius:5px;}
    </style>
</head>
<body>
<div class="container">
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return render_template_string(MAIN_TEMPLATE + '''
        <div class="login">
            <h2>🏛️ Alumni Portal Login</h2>
            <form method="POST" action="/login">
                <p>Username: <input type="text" name="username" style="width:100%;padding:10px;margin:5px 0;" required></p>
                <p>Password: <input type="password" name="password" style="width:100%;padding:10px;margin:5px 0;" required></p>
                <button type="submit" style="width:100%;padding:12px;background:#1877f2;color:white;border:none;border-radius:5px;">Login</button>
            </form>
            <p style="text-align:center;margin-top:15px;color:#666;">Demo: admin / admin123</p>
        </div>
        </div></body></html>''')
    
    return render_template_string(MAIN_TEMPLATE + f'''
    <div class="header">
        <h1>🎓 Alumni Portal</h1>
        <p>Welcome {session["user"]}! <a href="/logout" class="logout">Logout</a></p>
    </div>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/alumni">Alumni Directory</a>
        <a href="/events">Events</a>
    </div>
    <h2 style="text-align:center;color:#333;margin:30px 0 20px 0;">Recent Alumni</h2>
    <div class="grid">
    ''', **locals())

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    if username in users and users[username] == password:
        session['user'] = username
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/alumni')
def alumni():
    if 'user' not in session: return redirect('/')
    
    cards = ''
    for alum in alumni_data:
        cards += f'''
        <div class="card">
            <h3>{alum["name"]}</h3>
            <p><strong>Graduation:</strong> {alum["year"]} | <strong>{alum["role"]} @ {alum["company"]}</strong></p>
        </div>'''
    
    return render_template_string(MAIN_TEMPLATE + f'''
    <div class="header">
        <h1>👥 Complete Alumni Directory</h1>
        <a href="/" class="logout">← Home</a>
    </div>
    <div class="grid">{cards}</div>
    </div></body></html>''')

@app.route('/events')
def events():
    if 'user' not in session: return redirect('/')
    
    return render_template_string(MAIN_TEMPLATE + '''
    <div class="header">
        <h1>📅 Upcoming Events</h1>
        <a href="/" class="logout">← Home</a>
    </div>
    <div class="grid">
        <div class="card">
            <h3>🎉 Alumni Reunion 2026</h3>
            <p>📅 June 15, 2026 | 🏫 Main Campus</p>
            <p>Join us for networking & memories!</p>
        </div>
        <div class="card">
            <h3>💼 Career Fair</h3>
            <p>📅 May 20, 2026 | 🌐 Online</p>
            <p>Top companies hiring alumni!</p>
        </div>
    </div>
    </div></body></html>''')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
