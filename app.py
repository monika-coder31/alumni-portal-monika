from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
import csv
import io
import os
from collections import Counter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'college123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def index():
    return render_template('hero.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        # College email + common password check
        if ('@college.edu' in email or '@student.ac.in' in email) and password == 'college123':
            session['logged_in'] = True
            session['email'] = email
            flash('✅ Welcome to Admin Dashboard!')
            return redirect(url_for('dashboard'))
        flash('❌ Invalid college email or password!')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    alumni_list = Alumni.query.all()
    
    # Pie chart data
    companies = [alum.company for alum in alumni_list]
    company_counts = Counter(companies)
    years = [alum.grad_year for alum in alumni_list]
    year_counts = Counter(years)
    
    return render_template('dashboard.html', 
                         alumni=alumni_list, 
                         company_data=company_counts,
                         year_data=year_counts,
                         total=len(alumni_list))

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        alumni = Alumni(
            name=request.form['name'],
            email=request.form['email'],
            grad_year=int(request.form['grad_year']),
            job_title=request.form['job_title'],
            company=request.form['company']
        )
        db.session.add(alumni)
        db.session.commit()
        flash('✅ Alumni added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add.html')

# Other routes remain same...
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    flash('✅ Alumni deleted!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
