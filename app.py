from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai123secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Alumni Model
class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# Login check
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login first!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def index():
    search = request.args.get('search', '')
    alumni = Alumni.query
    if search:
        alumni = alumni.filter(
            db.or_(
                Alumni.name.contains(search),
                Alumni.company.contains(search),
                Alumni.job_title.contains(search)
            )
        )
    alumni_list = alumni.order_by(Alumni.name).all()
    total = len(alumni_list)
    return render_template('index.html', alumni=alumni_list, search=search, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'ai123':
            session['logged_in'] = True
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        flash('Wrong password!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logged out!')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        alumni = Alumni(
            name=request.form['name'],
            grad_year=int(request.form['grad_year']),
            job_title=request.form['job_title'],
            company=request.form['company']
        )
        db.session.add(alumni)
        db.session.commit()
        flash('Alumni added!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        alumni.name = request.form['name']
        alumni.grad_year = int(request.form['grad_year'])
        alumni.job_title = request.form['job_title']
        alumni.company = request.form['company']
        db.session.commit()
        flash('Alumni updated!')
        return redirect(url_for('index'))
    return render_template('edit.html', alumni=alumni)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    flash('Alumni deleted!')
    return redirect(url_for('index'))

@app.route('/export')
@login_required
def export():
    alumni_list = Alumni.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Name', 'Grad Year', 'Job Title', 'Company'])
    for alumni in alumni_list:
        cw.writerow([alumni.name, alumni.grad_year, alumni.job_title, alumni.company])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/sample')
@login_required
def sample():
    sample_data = [
        ('Ravi Kumar', 2020, 'Software Engineer', 'TCS'),
        ('Priya Sharma', 2021, 'Data Scientist', 'Google'),
        ('Arun Patel', 2019, 'ML Engineer', 'Microsoft')
    ]
    for name, year, title, company in sample_data:
        if not Alumni.query.filter_by(name=name).first():
            alumni = Alumni(name=name, grad_year=year, job_title=title, company=company)
            db.session.add(alumni)
    db.session.commit()
    flash('Sample data added!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai123secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Alumni Model
class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# Login check
def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login first!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def index():
    search = request.args.get('search', '')
    alumni = Alumni.query
    if search:
        alumni = alumni.filter(
            db.or_(
                Alumni.name.contains(search),
                Alumni.company.contains(search),
                Alumni.job_title.contains(search)
            )
        )
    alumni_list = alumni.order_by(Alumni.name).all()
    total = len(alumni_list)
    return render_template('index.html', alumni=alumni_list, search=search, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'ai123':
            session['logged_in'] = True
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        flash('Wrong password!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logged out!')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        alumni = Alumni(
            name=request.form['name'],
            grad_year=int(request.form['grad_year']),
            job_title=request.form['job_title'],
            company=request.form['company']
        )
        db.session.add(alumni)
        db.session.commit()
        flash('Alumni added!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        alumni.name = request.form['name']
        alumni.grad_year = int(request.form['grad_year'])
        alumni.job_title = request.form['job_title']
        alumni.company = request.form['company']
        db.session.commit()
        flash('Alumni updated!')
        return redirect(url_for('index'))
    return render_template('edit.html', alumni=alumni)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    flash('Alumni deleted!')
    return redirect(url_for('index'))

@app.route('/export')
@login_required
def export():
    alumni_list = Alumni.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Name', 'Grad Year', 'Job Title', 'Company'])
    for alumni in alumni_list:
        cw.writerow([alumni.name, alumni.grad_year, alumni.job_title, alumni.company])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/sample')
@login_required
def sample():
    sample_data = [
        ('Ravi Kumar', 2020, 'Software Engineer', 'TCS'),
        ('Priya Sharma', 2021, 'Data Scientist', 'Google'),
        ('Arun Patel', 2019, 'ML Engineer', 'Microsoft')
    ]
    for name, year, title, company in sample_data:
        if not Alumni.query.filter_by(name=name).first():
            alumni = Alumni(name=name, grad_year=year, job_title=title, company=company)
            db.session.add(alumni)
    db.session.commit()
    flash('Sample data added!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
