from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from datetime import datetime
import json
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Complete Alumni Database
ALUMNI_DATA = [
    {"id": 1, "name": "John Doe", "grad_year": 2020, "job": "Software Engineer", "company": "Google", "email": "john.doe@email.com"},
    {"id": 2, "name": "Jane Smith", "grad_year": 2021, "job": "Data Scientist", "company": "Microsoft", "email": "jane.smith@email.com"},
    {"id": 3, "name": "Mike Johnson", "grad_year": 2019, "job": "Product Manager", "company": "Amazon", "email": "mike.j@email.com"},
    {"id": 4, "name": "Sarah Wilson", "grad_year": 2022, "job": "UX Designer", "company": "Meta", "email": "sarah.w@email.com"},
    {"id": 5, "name": "David Brown", "grad_year": 2018, "job": "DevOps Engineer", "company": "Netflix", "email": "david.b@email.com"}
]

# Users for login
USERS = {
    "admin": hashlib.md5("admin123".encode()).hexdigest(),
    "student": hashlib.md5("student456".encode()).hexdigest()
}

# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Alumni Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 30px; text-align: center; }
        .header h1 { color: #333; font-size: 2.5em; margin-bottom: 10px; }
        .nav { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 20px; }
        .nav a { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; transition: all 0.3s; }
        .nav a:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .login-form { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 400px; margin: 50px auto; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: bold; color: #333; }
        .form-group input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; transition: border-color 0.3s; }
        .form-group input:focus { outline: none; border-color: #667eea; }
        .btn { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; width: 100%; transition: all 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .alumni-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; margin-top: 30px; }
        .alumni-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: all 0.3s; }
        .alumni-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
        .alumni-name { font-size: 1.5em; font-weight: bold; color: #333; margin-bottom: 10px; }
        .alumni-info { color: #666; line-height: 1.6; }
        .logout { position: absolute; top: 20px; right: 20px; background: #ff4757; color: white; padding: 10px 20px; border-radius: 20px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        {% if session.user %}
        <a href="/logout" class="logout">Logout</a>
        <div class="header">
            <h1>🏫 Alumni Portal</h1>
            <p>Welcome back, {{ session.user }}!</p>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/alumni">Alumni Directory</a>
                <a href="/events">Events</a>
                <a href="/contact">Contact</a>
            </div>
        </div>
        {% else %}
        <div class="login-form">
            <h2>Login to Alumni Portal</h2>
            <form method="POST" action="/login">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
            <p style="text-align: center; margin-top: 20px;">
                Demo: admin/admin123 | student/student456
            </p>
        </div>
        {% endif %}
        
        {% if show_message %}
        <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin: 20px 0;">
            {{ show_message }}
        </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

ALUMNI_TEMPLATE = '''
<div class="alumni-grid">
    {% for alumni in alumni_list %}
    <div class="alumni-card">
        <div class="alumni-name">{{ alumni.name }}</div>
        <div class="alumni-info">
            <strong>Graduation:</strong> {{ alumni.grad_year }}<br>
            <strong>Job:</strong> {{ alumni.job }}<br>
            <strong>Company:</strong> {{ alumni.company }}<br>
            <strong>Email:</strong> {{ alumni.email }}
        </div>
    </div>
    {% endfor %}
</div>
'''

EVENTS_TEMPLATE = '''
<div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h2>📅 Upcoming Events</h2>
    <div style="display: grid; gap: 20px; margin-top: 20px;">
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #667eea;">
            <h3>Alumni Reunion 2026</h3>
            <p><strong>Date:</strong> June 15, 2026</p>
            <p><strong>Location:</strong> Campus Auditorium</p>
            <p>Join us for networking and memories!</p>
        </div>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #764ba2;">
            <h3>Career Fair</h3>
            <p><strong>Date:</strong> May 20, 2026</p>
            <p><strong>Location:</strong> Online</p>
            <p>Top companies hiring alumni!</p>
        </div>
    </div>
</div>
'''

@app.route('/')
def home():
    if 'user' not in session:
        return render_template_string(HOME_TEMPLATE)
    return render_template_string(HOME_TEMPLATE + ALUMNI_TEMPLATE, alumni_list=ALUMNI_DATA[:3], session=session)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    
    if username in USERS and USERS[username] == password:
        session['user'] = username
        return redirect(url_for('home'))
    return render_template_string(HOME_TEMPLATE, show_message="Invalid credentials!", session=session)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/alumni')
def alumni():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template_string(HOME_TEMPLATE + ALUMNI_TEMPLATE, alumni_list=ALUMNI_DATA, session=session)

@app.route('/events')
def events():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template_string(HOME_TEMPLATE + EVENTS_TEMPLATE, session=session)

@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template_string('''
    ''' + HOME_TEMPLATE + '''
    <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h2>📧 Contact Us</h2>
        <p><strong>Email:</strong> alumni@yourcollege.edu</p>
        <p><strong>Phone:</strong> +1-234-567-8900</p>
        <p><strong>Address:</strong> 123 College St, City, State 12345</p>
    </div>
    ''', session=session)

@app.route('/api/alumni')
def api_alumni():
    return jsonify(ALUMNI_DATA)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from datetime import datetime
import json
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Complete Alumni Database
ALUMNI_DATA = [
    {"id": 1, "name": "John Doe", "grad_year": 2020, "job": "Software Engineer", "company": "Google", "email": "john.doe@email.com"},
    {"id": 2, "name": "Jane Smith", "grad_year": 2021, "job": "Data Scientist", "company": "Microsoft", "email": "jane.smith@email.com"},
    {"id": 3, "name": "Mike Johnson", "grad_year": 2019, "job": "Product Manager", "company": "Amazon", "email": "mike.j@email.com"},
    {"id": 4, "name": "Sarah Wilson", "grad_year": 2022, "job": "UX Designer", "company": "Meta", "email": "sarah.w@email.com"},
    {"id": 5, "name": "David Brown", "grad_year": 2018, "job": "DevOps Engineer", "company": "Netflix", "email": "david.b@email.com"}
]

# Users for login
USERS = {
    "admin": hashlib.md5("admin123".encode()).hexdigest(),
    "student": hashlib.md5("student456".encode()).hexdigest()
}

# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Alumni Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 30px; text-align: center; }
        .header h1 { color: #333; font-size: 2.5em; margin-bottom: 10px; }
        .nav { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 20px; }
        .nav a { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; transition: all 0.3s; }
        .nav a:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .login-form { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 400px; margin: 50px auto; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: bold; color: #333; }
        .form-group input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; transition: border-color 0.3s; }
        .form-group input:focus { outline: none; border-color: #667eea; }
        .btn { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; width: 100%; transition: all 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .alumni-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; margin-top: 30px; }
        .alumni-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: all 0.3s; }
        .alumni-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
        .alumni-name { font-size: 1.5em; font-weight: bold; color: #333; margin-bottom: 10px; }
        .alumni-info { color: #666; line-height: 1.6; }
        .logout { position: absolute; top: 20px; right: 20px; background: #ff4757; color: white; padding: 10px 20px; border-radius: 20px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        {% if session.user %}
        <a href="/logout" class="logout">Logout</a>
        <div class="header">
            <h1>🏫 Alumni Portal</h1>
            <p>Welcome back, {{ session.user }}!</p>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/alumni">Alumni Directory</a>
                <a href="/events">Events</a>
                <a href="/contact">Contact</a>
            </div>
        </div>
        {% else %}
        <div class="login-form">
            <h2>Login to Alumni Portal</h2>
            <form method="POST" action="/login">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
            <p style="text-align: center; margin-top: 20px;">
                Demo: admin/admin123 | student/student456
            </p>
        </div>
        {% endif %}
        
        {% if show_message %}
        <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin: 20px 0;">
            {{ show_message }}
        </div>
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

ALUMNI_TEMPLATE = '''
<div class="alumni-grid">
    {% for alumni in alumni_list %}
    <div class="alumni-card">
        <div class="alumni-name">{{ alumni.name }}</div>
        <div class="alumni-info">
            <strong>Graduation:</strong> {{ alumni.grad_year }}<br>
            <strong>Job:</strong> {{ alumni.job }}<br>
            <strong>Company:</strong> {{ alumni.company }}<br>
            <strong>Email:</strong> {{ alumni.email }}
        </div>
    </div>
    {% endfor %}
</div>
'''

EVENTS_TEMPLATE = '''
<div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h2>📅 Upcoming Events</h2>
    <div style="display: grid; gap: 20px; margin-top: 20px;">
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #667eea;">
            <h3>Alumni Reunion 2026</h3>
            <p><strong>Date:</strong> June 15, 2026</p>
            <p><strong>Location:</strong> Campus Auditorium</p>
            <p>Join us for networking and memories!</p>
        </div>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #764ba2;">
            <h3>Career Fair</h3>
            <p><strong>Date:</strong> May 20, 2026</p>
            <p><strong>Location:</strong> Online</p>
            <p>Top companies hiring alumni!</p>
        </div>
    </div>
</div>
'''

@app.route('/')
def home():
    if 'user' not in session:
        return render_template_string(HOME_TEMPLATE)
    return render_template_string(HOME_TEMPLATE + ALUMNI_TEMPLATE, alumni_list=ALUMNI_DATA[:3], session=session)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    
    if username in USERS and USERS[username] == password:
        session['user'] = username
        return redirect(url_for('home'))
    return render_template_string(HOME_TEMPLATE, show_message="Invalid credentials!", session=session)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/alumni')
def alumni():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template_string(HOME_TEMPLATE + ALUMNI_TEMPLATE, alumni_list=ALUMNI_DATA, session=session)

@app.route('/events')
def events():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template_string(HOME_TEMPLATE + EVENTS_TEMPLATE, session=session)

@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template_string('''
    ''' + HOME_TEMPLATE + '''
    <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h2>📧 Contact Us</h2>
        <p><strong>Email:</strong> alumni@yourcollege.edu</p>
        <p><strong>Phone:</strong> +1-234-567-8900</p>
        <p><strong>Address:</strong> 123 College St, City, State 12345</p>
    </div>
    ''', session=session)

@app.route('/api/alumni')
def api_alumni():
    return jsonify(ALUMNI_DATA)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
