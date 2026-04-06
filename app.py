from flask import Flask, render_template_string, request, session, redirect, jsonify
import os
import hashlib
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'alumni-crud-admin-search-2026-final-public-view'

DATA_FILE = 'alumni.json'

def load_alumni():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        data = [
            {"id": 1, "name": "John Doe", "grad": "2020", "company": "Google", "role": "Engineer", "email": "john@google.com"},
            {"id": 2, "name": "Jane Smith", "grad": "2021", "company": "Microsoft", "role": "Data Scientist", "email": "jane@microsoft.com"},
            {"id": 3, "name": "Mike Johnson", "grad": "2019", "company": "Amazon", "role": "Product Manager", "email": "mike@amazon.com"},
            {"id": 4, "name": "Sarah Wilson", "grad": "2022", "company": "Meta", "role": "UX Designer", "email": "sarah@meta.com"},
            {"id": 5, "name": "David Brown", "grad": "2018", "company": "Netflix", "role": "DevOps", "email": "david@netflix.com"}
        ]
        save_alumni(data)
        return data

def save_alumni(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

users = {"admin": hashlib.md5("admin123".encode()).hexdigest()}
alumni_data = load_alumni()

CSS = '''
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:Arial,sans-serif;background:#f0f2f5;padding:20px;}
.container{max-width:1400px;margin:auto;}
.header{background:#4267b2;color:white;padding:30px;border-radius:10px;text-align:center;}
.nav{display:flex;gap:15px;justify-content:center;margin:30px 0;flex-wrap:wrap;}
.nav a{background:#1877f2;color:white;padding:12px 24px;text-decoration:none;border-radius:25px;font-weight:bold;}
.login-box,.admin-only{max-width:500px;margin:50px auto;background:white;padding:40px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);}
.logout{float:right;background:#e74c3c;color:white;padding:10px 20px;text-decoration:none;border-radius:8px;font-weight:bold;}
.search-box{max-width:600px;margin:20px auto;text-align:center;}
.search-input{width:70%;padding:15px;font-size:16px;border:2px solid #ddd;border-radius:30px;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
.btn{padding:12px 30px;background:#28a745;color:white;border:none;border-radius:8px;cursor:pointer;font-size:16px;margin:5px;transition:all 0.3s;}
.btn:hover{transform:translateY(-2px);box-shadow:0 5px 15px rgba(0,0,0,0.2);}
.btn-danger{background:#dc3545;}
.table{width:100%;border-collapse:collapse;margin:20px 0;background:white;border-radius:15px;overflow:hidden;box-shadow:0 5px 20px rgba(0,0,0,0.1);}
.table th{background:#f8f9fa;padding:18px;font-weight:bold;text-align:left;border-bottom:3px solid #4267b2;}
.table td{padding:15px;border-bottom:1px solid #eee;}
.table tr:hover{background:#f8f9fa;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:25px;margin:30px 0;}
.card{background:white;padding:30px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.1);transition:all 0.3s;}
.card:hover{transform:translateY(-5px);box-shadow:0 20px 40px rgba(0,0,0,0.2);}
.form-group{margin:20px 0;}
.form-group label{display:block;margin-bottom:8px;font-weight:bold;color:#333;font-size:16px;}
.form-group input{width:100%;padding:15px;border:2px solid #e1e5e9;border-radius:10px;font-size:16px;transition:border-color 0.3s;}
.form-group input:focus{outline:none;border-color:#4267b2;box-shadow:0 0 0 3px rgba(66,103,178,0.1);}
.message{padding:15px;margin:20px 0;border-radius:10px;text-align:center;font-weight:bold;}
.message.success{background:#d4edda;color:#155724;border:1px solid #c3e6cb;}
.message.error{background:#f8d7da;color:#721c24;border:1px solid #f5c6cb;}
.public-badge{background:#17a2b8;color:white;padding:5px 12px;border-radius:20px;font-size:14px;margin-left:10px;}
</style>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        if username in users and users[username] == password:
            session['user'] = username
            session['is_admin'] = True
        return redirect('/')
    
    if 'user' in session and session.get('is_admin'):
        recent = alumni_data[-3:] if alumni_data else []
        cards = ''
        for alum in recent:
            cards += f'''
            <div class="card">
                <h3>{alum['name']}</h3>
                <p><strong>Grad {alum['grad']} • {alum['role']} @ {alum['company']}</strong></p>
                <p>{alum['email']}</p>
                <a href="/admin/edit/{alum['id']}" class="btn" style="background:#17a2b8;">Edit</a>
            </div>'''
        return f'''<!DOCTYPE html><html><head><title>🏛️ Alumni Portal - Admin</title>{CSS}</head><body>
        <div class="container">
        <div class="header">
            <h1>🎓 Alumni Portal Dashboard</h1>
            <p>Hello <strong>{session['user']}</strong>! | <a href="/logout" class="logout">Logout</a></p>
        </div>
        <div class="nav">
            <a href="/">🏠 Dashboard</a>
            <a href="/alumni">👥 Public Alumni <span class="public-badge">Public</span></a>
            <a href="/admin/add">➕ Add Alumni</a>
            <a href="/admin">⚙️ Admin Panel</a>
        </div>
        <div class="message success">Total Alumni: {len(alumni_data)} | Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
        <h2 style="text-align:center;margin:40px 0;color:#333;">Recent Alumni</h2>
        <div class="grid">{cards}</div>
        </div></body></html>'''
    
    return f'''<!DOCTYPE html><html><head><title>🎓 Alumni Portal</title>{CSS}</head><body>
    <div class="container">
    <div class="header">
        <h1>🏛️ Welcome to Alumni Portal</h1>
        <p>Connect with graduates • View alumni success stories • Admin login below</p>
    </div>
    <div class="login-box">
        <h2 style="margin-bottom:25px;text-align:center;">🔐 Admin Login (Optional)</h2>
        <form method="POST">
            <div class="form-group">
                <label>Admin Username:</label>
                <input type="text" name="username" placeholder="admin" required>
            </div>
            <div class="form-group">
                <label>Admin Password:</label>
                <input type="password" name="password" placeholder="admin123" required>
            </div>
            <button type="submit" class="btn" style="width:100%;background:#4267b2;">Admin Login</button>
        </form>
        <div style="text-align:center;margin-top:25px;color:#666;">
            <p><strong>No login needed to view alumni →</strong> <a href="/alumni" style="color:#1877f2;font-weight:bold;">View Alumni Directory</a></p>
            <p><small>Demo: admin / admin123</small></p>
        </div>
    </div>
    <div style="text-align:center;margin-top:50px;">
        <a href="/alumni" class="btn" style="background:#28a745;font-size:18px;padding:15px 40px;">👥 View Public Alumni Directory</a>
    </div>
    </div></body></html>'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/alumni')
def alumni():
    search = request.args.get('search', '')
    filtered = alumni_data
    if search:
        filtered = [a for a in alumni_data if search.lower() in a['name'].lower() or search.lower() in a['company'].lower()]
    
    rows = ''
    for alum in filtered:
        admin_actions = ''
        if 'user' in session and session.get('is_admin'):
            admin_actions = f'''
            <td>
                <a href="/admin/edit/{alum['id']}" class="btn" style="background:#17a2b8;">Edit</a>
                <a href="/admin/delete/{alum['id']}" class="btn btn-danger" onclick="return confirm('Delete {alum['name']}?')">Delete</a>
            </td>'''
        else:
            admin_actions = '<td><span class="public-badge">Public View</span></td>'
        
        rows += f'''
        <tr>
            <td><strong>{alum['name']}</strong></td>
            <td>{alum['grad']}</td>
            <td>{alum['company']}</td>
            <td>{alum['role']}</td>
            <td>{alum['email']}</td>
            {admin_actions}
        </tr>'''
    
    admin_panel = ''
    if 'user' in session and session.get('is_admin'):
        admin_panel = '''
        <div style="margin-top:30px;">
            <a href="/admin/add" class="btn" style="background:#28a745;">➕ Add New Alumni</a>
        </div>'''
    
    return f'''<!DOCTYPE html><html><head><title>👥 Alumni Directory</title>{CSS}</head><body>
    <div class="container">
    <div class="header">
        <h1>📋 Alumni Directory ({len(filtered)} of {len(alumni_data)})</h1>
        <p>Publicly accessible • <a href="/" style="color:#fff;">← Home</a>
        {' | <a href="/logout" class="logout" style="margin-left:20px;">Logout</a>' if 'user' in session else ''}
        </p>
    </div>
    <div class="search-box">
        <form method="GET">
            <input type="text" name="search" placeholder="🔍 Search name or company..." class="search-input" value="{search}">
            <button type="submit" class="btn">Search</button>
        </form>
    </div>
    <table class="table">
        <thead><tr>
            <th>Name</th>
            <th>Grad Year</th>
            <th>Company</th>
            <th>Role</th>
            <th>Email</th>
            <th>Actions</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table>
    {admin_panel}
    </div></body></html>'''

@app.route('/admin/add', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'user' not in session or not session.get('is_admin'):
        return redirect('/alumni')
    
    if request.method == 'POST':
        new_id = max([a['id'] for a in alumni_data], default=0) + 1
        new_alum = {
            "id": new_id,
            "name": request.form['name'],
            "grad": request.form['grad'],
            "company": request.form['company'],
            "role": request.form['role'],
            "email": request.form['email']
        }
        alumni_data.append(new_alum)
        save_alumni(alumni_data)
        return redirect('/admin')
    
    return f'''<!DOCTYPE html><html><head><title>⚙️ Admin Panel</title>{CSS}</head><body>
    <div class="container">
    <div class="header">
        <h1>⚙️ Admin Control Panel</h1>
        <a href="/" class="logout">← Dashboard</a>
    </div>
    <div class="admin-only">
        <h3>➕ Add New Alumni</h3>
        <form method="POST">
            <div class="form-group">
                <label>Name:</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>Grad Year:</label>
                <input type="text" name="grad" required>
            </div>
            <div class="form-group">
                <label>Company:</label>
                <input type="text" name="company" required>
            </div>
            <div class="form-group">
                <label>Role:</label>
                <input type="text" name="role" required>
            </div>
            <div class="form-group">
                <label>Email:</label>
                <input type="email" name="email" required>
            </div>
            <button type="submit" class="btn" style="width:100%;background:#28a745;">Add Alumni</button>
        </form>
    </div>
    </div></body></html>'''

@app.route('/admin/edit/<int:alum_id>', methods=['GET', 'POST'])
def admin_edit(alum_id):
    if 'user' not in session or not session.get('is_admin'):
        return redirect('/alumni')
    
    alum = next((a for a in alumni_data if a['id'] == alum_id), None)
    if not alum:
        return redirect('/alumni')
    
    if request.method == 'POST':
        alum['name'] = request.form['name']
        alum['grad'] = request.form['grad']
        alum['company'] = request.form['company']
        alum['role'] = request.form['role']
        alum['email'] = request.form['email']
        save_alumni(alumni_data)
        return redirect('/alumni')
    
    return f'''<!DOCTYPE html><html><head><title>Edit Alumni</title>{CSS}</head><body>
    <div class="container">
    <div class="header">
        <h1>✏️ Edit {alum['name']}</h1>
        <a href="/alumni" class="logout">← Alumni</a>
    </div>
    <form method="POST" class="admin-only">
        <div class="form-group">
            <label>Name:</label>
            <input type="text" name="name" value="{alum['name']}" required>
        </div>
        <div class="form-group">
            <label>Grad Year:</label>
            <input type="text" name="grad" value="{alum['grad']}" required>
        </div>
        <div class="form-group">
            <label>Company:</label>
            <input type="text" name="company" value="{alum['company']}" required>
        </div>
        <div class="form-group">
            <label>Role:</label>
            <input type="text" name="role" value="{alum['role']}" required>
        </div>
        <div class="form-group">
            <label>Email:</label>
            <input type="email" name="email" value="{alum['email']}" required>
        </div>
        <button type="submit" class="btn" style="width:100%;background:#17a2b8;">Update Alumni</button>
    </form>
    </div></body></html>'''

@app.route('/admin/delete/<int:alum_id>')
def admin_delete(alum_id):
    if 'user' not in session or not session.get('is_admin'):
        return redirect('/alumni')
    
    global alumni_data
    alumni_data = [a for a in alumni_data if a['id'] != alum_id]
    save_alumni(alumni_data)
    return redirect('/alumni')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
