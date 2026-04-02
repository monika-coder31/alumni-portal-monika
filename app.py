from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import csv
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alumni_portal_secret_2026_change_in_prod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    email = db.Column(db.String(100))
    year = db.Column(db.Integer)

@app.route('/')
def index():
    search = request.args.get('search', '')
    alumni_list = Alumni.query
    if search:
        alumni_list = alumni_list.filter(
            db.or_(
                Alumni.name.contains(search),
                Alumni.company.contains(search)
            )
        )
    alumni = alumni_list.all()
    return render_template('index.html', alumni=alumni, search=search)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'ai123' and password == 'ai123':
            session['logged_in'] = True
            flash('Login successful! Welcome to Admin Dashboard.')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please login first!')
        return redirect(url_for('login'))
    alumni = Alumni.query.all()
    return render_template('index.html', alumni=alumni, show_admin=True)

@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['name']
    company = request.form['company']
    email = request.form['email']
    year = int(request.form['year'])
    new_alumni = Alumni(name=name, company=company, email=email, year=year)
    db.session.add(new_alumni)
    db.session.commit()
    flash('Alumni record added successfully!')
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        alumni.name = request.form['name']
        alumni.company = request.form['company']
        alumni.email = request.form['email']
        alumni.year = int(request.form['year'])
        db.session.commit()
        flash('Record updated!')
        return redirect(url_for('dashboard'))
    return render_template('edit.html', alumni=alumni)

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    flash('Record deleted!')
    return redirect(url_for('dashboard'))

@app.route('/export')
def export():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    alumni = Alumni.query.all()
    si = BytesIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Company', 'Email', 'Grad Year'])
    cw.writerows([[a.id, a.name, a.company, a.email, a.year] for a in alumni])
    output = si.getvalue()
    return ('alumni.csv', 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=alumni_export.csv'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))

@app.cli.command()
def initdb():
    db.create_all()
    if Alumni.query.filter_by(name='Ravi Kumar').first() is None:
        sample_data = [
            Alumni(name='Ravi Kumar', company='TCS', email='ravi.tcs@example.com', year=2020),
            Alumni(name='Priya Sharma', company='Google', email='priya.google@example.com', year=2019),
            Alumni(name='Amit Patel', company='Infosys', email='amit.infosys@example.com', year=2021)
        ]
        db.session.bulk_save_objects(sample_data)
        db.session.commit()
        print("Sample data added!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Uncomment below to add sample data locally: initdb()
    app.run(debug=True)
