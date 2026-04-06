from flask import Flask, render_template_string, request, session, redirect, jsonify
import os
import hashlib
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'alumni-crud-admin-search-2026-final'

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
.logout{float:right;background:#e74c3c;color:white;padding:8px 16px;text-decoration:none;border-radius:5px;}
.search-box{max-width:600px;margin:20px auto;text-align:center;}
.search-input{width:70%;padding:12px;font-size:16px;border:1px solid #ddd;border-radius:25px;}
.btn{padding:12px 24px;background:#28a745;color:white;border:none;border-radius:5px;cursor:pointer;font-size:16px;}
.table{width:100%;border-collapse:collapse;margin:20px 0;background:white;border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
.table th{background:#f8f9fa;padding:15px;font-weight:bold;text-align:left;}
.table td{padding:12px;border-bottom:1px solid #eee;}
.table tr:hover{background:#f8f9fa;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;}
.card{background:white;padding:20px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
.form-group{margin:15px 0;}
.form-group label{display:block;margin-bottom:5px;font-weight:bold;}
.form-group input{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;}
.modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:#00000080;}
.modal-content{background:white;margin:5% auto;padding:30px;border-radius:10px;width:90%;max-width:500px;}
.close{position:absolute;right:20px;top:15px;font-size:28px;cursor:pointer;}
</style>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return f'''<!DOCTYPE html><html><head><title>Login</title>{CSS}</head><body>
        <div class="container">
        <div style="max-width:400px;margin:100px auto;background:white;padding:40px;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
            <h2 style="text-align:center;margin-bottom:30px;">🔐 Alumni Portal Login</h2>
            <form method="POST" action="/login">
                <div class="form-group"><label>Username:</label><input type="text" name="username" required style="width:100%;padding:12px;"></div>
                <div class="form-group"><label>Password:</label><input type="password" name="password" required style="width:100%;padding:12px;"></div>
                <button type="submit" class="btn" style="width:100%;background:#1877f2;">Login</button>
            </form>
            <p style="text-align:center;margin-top:20px;color:#666;">Demo: <strong>admin / admin123</strong></p>
        </div></div></body></html>'''
    
    search = request.form.get('search', '') if request.method == 'POST' else ''
    filtered = [a for a in alumni_data if not search or search.lower() in a['name'].lower() or search.lower() in a['company'].lower()]
    
    cards = ''
    for alum in filtered[:6]:
        cards += f'''
        <div class="card">
            <h3>{alum['name']}</h3>
            <p><strong>{alum['grad']} • {alum['role']} @ {alum['company']}</strong></p>
            <p>{alum['email']}</p>
        </div>'''
    
    return f'''<!DOCTYPE html><html><head><title>Alumni Portal</title>{CSS}</head><body>
    <div class="container">
    <div class="header">
        <h1>🎓 Alumni Portal</h1>
        <p>Welcome <strong>{session['user']}</strong>! <a href="/logout" class="logout">Logout</a></p>
    </div>
    <div class="nav">
        <a href="/">🏠 Home</a>
        <a href="/alumni">👥 Alumni ({len(alumni_data)})</a>
        <a href="/admin">⚙️ Admin Panel</a>
    </div>
    <form method="POST" class="search-box">
        <input type="text" name="search" placeholder="🔍 Search by name or company..." class="search-input" value="{search}">
        <button type="submit" class="btn">Search</button>
    </form>
    <h2 style="text-align:center;margin:30px 0;color:#333;">Featured Alumni</h2>
    <div class="grid">{cards}</div>
    </div></body></html>'''

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
    search = request.args.get('search', '')
    filtered = alumni_data
    if search:
        filtered = [a for a in alumni_data if search.lower() in a['name'].lower() or search.lower() in a['company'].lower()]
    
    rows = ''
    for alum in filtered:
        rows += f'''
        <tr>
            <td>{alum['name']}</td>
            <td>{alum['grad']}</td>
            <td>{alum['company']}</td>
            <td>{alum['role']}</td>
            <td>{alum['email']}</td>
            <td><a href="/admin/edit/{alum['id']}" class="btn" style="background:#ffc107;">Edit</a> 
                <a href="/admin/delete/{alum['id']}" class="btn" style="background:#dc3545;" onclick="return confirm('Delete?')">Delete</a></td>
        </tr>'''
    
    return f'''<!DOCTYPE html><html><head><title>Alumni Directory</title>{CSS}</head><body>
    <div class="container">
    <div class="header"><h1>📋 Alumni Directory</h1><a href="/" class="logout">← Home</a></div>
    <div style="background:white;padding:20px;border-radius:10px;margin:20px 0;">
        <div style="display:flex;gap:10px;align-items:center;margin-bottom:20px;">
            <input type="text" placeholder="🔍 Search..." value="{search}" onkeyup="searchAlumni(this.value)" style="flex:1;padding:12px;border:1px solid #ddd;border-radius:5px;">
            <a href="/admin/add" class="btn" style="background:#28a745;">➕ Add New</a>
        </div>
        <table class="table">
            <thead><tr><th>Name</th><th>Grad Year</th><th>Company</th><th>Role</th><th>Email</th><th>Actions</th></tr></thead>
            <tbody id="alumniTable">{rows}</tbody>
        </table>
    </div></div>
    <script>
    function searchAlumni(query) {{
        window.location.href = '/alumni?search=' + encodeURIComponent(query);
    }}
    </script></body></html>'''

@app.route('/admin')
def admin():
    if 'user' not in session or session['user'] != 'admin': return redirect('/')
    return f'''<!DOCTYPE html><html><head><title>Admin Panel</title>{CSS}</head><body>
    <div class="container">
    <div class="header"><h1>⚙️ Admin Panel</h1><a href="/" class="logout">← Home</a></div>
    <div class="nav">
        <a href="/admin/add">➕ Add Alumni</a>
        <a href="/alumni">📋 View All</a>
    </div>
    <div class="grid">
        <div class="card"><h3>Total Alumni: {len(alumni_data)}</h3></div>
        <div class="card"><h3>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</h3></div>
    </div>
    </div></body></html>'''

@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add():
    if 'user' not in session or session['user'] != 'admin': return redirect('/')
    
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
    
    return f'''<!DOCTYPE html><html><head><title>Add Alumni</title>{CSS}</head><body>
    <div class="container">
    <div class="header"><h1>➕ Add New Alumni</h1><a href="/admin" class="logout">← Admin</a></div>
    <form method="POST" style="max-width:600px;margin:auto;background:white;padding:40px;border-radius:10px;">
        <div class="form-group"><label>Name:</label><input type="text" name="name" required></div>
        <div class="form-group"><label>Grad Year:</label><input type="text" name="grad" required></div>
        <div class="form-group"><label>Company:</label><input type="text" name="company" required></div>
        <div class="form-group"><label>Role:</label><input type="text" name="role" required></div>
        <div class="form-group"><label>Email:</label><input type="email" name="email" required></div>
        <button type="submit" class="btn" style="width:100%;background:#28a745;">Save Alumni</button>
    </form></div></body></html>'''

@app.route('/admin/edit/<int:alum_id>', methods=['GET', 'POST'])
def admin_edit(alum_id):
    if 'user' not in session or session['user'] != 'admin': return redirect('/')
    
    alum = next((a for a in alumni_data if a['id'] == alum_id), None)
    if not alum: return redirect('/admin')
    
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
    <div class="header"><h1>✏️ Edit {alum['name']}</h1><a href="/admin" class="logout">← Admin</a></div>
    <form method="POST" style="max-width:600px;margin:auto;background:white;padding:40px;border-radius:10px;">
        <div class="form-group"><label>Name:</label><input type="text" name="name" value="{alum['name']}" required></div>
        <div class="form-group"><label>Grad Year:</label><input type="text" name="grad" value="{alum['grad']}" required></div>
        <div class="form-group"><label>Company:</label><input type="text" name="company" value="{alum['company']}" required></div>
        <div class="form-group"><label>Role:</label><input type="text" name="role" value="{alum['role']}" required></div>
        <div class="form-group"><label>Email:</label><input type="email" name="email" value="{alum['email']}" required></div>
        <button type="submit" class="btn" style="width:100%;background:#17a2b8;">Update</button>
    </form></div></body></html>'''

@app.route('/admin/delete/<int:alum_id>')
def admin_delete(alum_id):
    if 'user' not in session or session['user'] != 'admin': return redirect('/')
    global alumni_data
    alumni_data = [a for a in alumni_data if a['id'] != alum_id]
    save_alumni(alumni_data)
    return redirect('/alumni')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
