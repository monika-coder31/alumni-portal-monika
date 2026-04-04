from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'alumni2026secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    job = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Admin login required!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'ai123' and request.form['password'] == 'ds2026':
            session['logged_in'] = True
            flash('Welcome Admin!')
            return redirect(url_for('index'))
        flash('Invalid credentials! Demo: ai123/ds2026')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    search = request.form.get('search', '')
    alumni = Alumni.query
    if search:
        alumni = alumni.filter((Alumni.name.contains(search)) | (Alumni.job.contains(search)))
    alumni = alumni.order_by(Alumni.name).all()
    return render_template('index.html', alumni=alumni)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        year = int(request.form['year'])
        job = request.form['job']
        email = request.form['email']
        new_alumni = Alumni(name=name, year=year, job=job, email=email)
        db.session.add(new_alumni)
        db.session.commit()
        flash('Alumni added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    alum = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        alum.name = request.form['name']
        alum.year = int(request.form['year'])
        alum.job = request.form['job']
        alum.email = request.form['email']
        db.session.commit()
        flash('Alumni updated!')
        return redirect(url_for('index'))
    return render_template('edit.html', alum=alum)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    alum = Alumni.query.get_or_404(id)
    db.session.delete(alum)
    db.session.commit()
    flash('Alumni deleted!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=port, debug=True)