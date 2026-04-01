import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from io import BytesIO
import csv

app = Flask(__name__)
app.secret_key = 'ai1232026'

# Heroku: Use postgres, Local: SQLite
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)

ADMIN_PASSWORD = "ai123"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

with app.app_context():
    db.create_all()

def get_stats():
    alumni = Alumni.query.all()
    years, companies = {}, {}
    for a in alumni:
        years[a.grad_year] = years.get(a.grad_year, 0) + 1
        companies[a.company] = companies.get(a.company, 0) + 1
    return {
        'total': len(alumni),
        'years': dict(sorted(years.items())),
        'companies': dict(sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5])
    }

# ALL YOUR ROUTES (same as Day 4 - login, index, add, edit, delete, seed, export)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search = request.form.get('search', '') if request.method == 'POST' else ''
    alumni = Alumni.query.all()
    if search:
        alumni = [a for a in alumni if search.lower() in a.name.lower() or 
                 search.lower() in a.company.lower() or str(a.grad_year).startswith(search)]
    stats = get_stats()
    return render_template('index.html', alumni=alumni, search=search, stats=stats)

@app.route('/export')
@login_required
def export():
    alumni = Alumni.query.all()
    si = BytesIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Grad Year', 'Job Title', 'Company'])
    for a in alumni:
        cw.writerow([a.id, a.name, a.grad_year, a.job_title, a.company])
    si.seek(0)
    return send_file(si, mimetype='text/csv', as_attachment=True, download_name='alumni_data.csv')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        alumni = Alumni(
            name=request.form['name'].strip(),
            grad_year=int(request.form['grad_year']),
            job_title=request.form['job_title'].strip(),
            company=request.form['company'].strip()
        )
        db.session.add(alumni)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        alumni.name = request.form['name'].strip()
        alumni.grad_year = int(request.form['grad_year'])
        alumni.job_title = request.form['job_title'].strip()
        alumni.company = request.form['company'].strip()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', alumni=alumni)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/seed')
@login_required
def seed():
    sample_data = [
        ('Ravi Kumar', 2025, 'AI Engineer', 'Google'),
        ('Priya Singh', 2024, 'Data Scientist', 'Microsoft'),
        ('Arjun Reddy', 2023, 'ML Engineer', 'Amazon'),
        ('Sneha Patel', 2026, 'Software Developer', 'TCS'),
        ('Vikram Joshi', 2022, 'DevOps Engineer', 'Infosys')
    ]
    for name, year, job, company in sample_data:
        if not Alumni.query.filter_by(name=name).first():
            alumni = Alumni(name=name, grad_year=year, job_title=job, company=company)
            db.session.add(alumni)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)