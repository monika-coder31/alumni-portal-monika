from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'alumni-portal-monika-2026-180-lines-special'

# COMPLETE ALUMNI DATABASE - 20 RECORDS
ALUMNI_DATA = [
    {"id": 1, "name": "John Doe", "grad_year": 2020, "job": "Software Engineer", "company": "Google", "email": "john.doe@google.com", "city": "Bangalore", "linkedin": "linkedin.com/in/johndoe"},
    {"id": 2, "name": "Jane Smith", "grad_year": 2021, "job": "Data Scientist", "company": "Microsoft", "email": "jane.smith@microsoft.com", "city": "Hyderabad", "linkedin": "linkedin.com/in/janesmith"},
    {"id": 3, "name": "Mike Johnson", "grad_year": 2019, "job": "Product Manager", "company": "Amazon", "email": "mike.johnson@amazon.com", "city": "Mumbai", "linkedin": "linkedin.com/in/mikejohnson"},
    {"id": 4, "name": "Sarah Wilson", "grad_year": 2022, "job": "UX Designer", "company": "Meta", "email": "sarah.wilson@meta.com", "city": "Delhi", "linkedin": "linkedin.com/in/sarahwilson"},
    {"id": 5, "name": "David Brown", "grad_year": 2018, "job": "DevOps Engineer", "company": "Netflix", "email": "david.brown@netflix.com", "city": "Chennai", "linkedin": "linkedin.com/in/davidbrown"},
    {"id": 6, "name": "Priya Sharma", "grad_year": 2020, "job": "AI Researcher", "company": "OpenAI", "email": "priya.sharma@openai.com", "city": "Pune", "linkedin": "linkedin.com/in/priyasharma"},
    {"id": 7, "name": "Raj Patel", "grad_year": 2021, "job": "Backend Developer", "company": "Paytm", "email": "raj.patel@paytm.com", "city": "Noida", "linkedin": "linkedin.com/in/rajpatel"},
    {"id": 8, "name": "Anita Gupta", "grad_year": 2019, "job": "Frontend Developer", "company": "Zomato", "email": "anita.gupta@zomato.com", "city": "Gurgaon", "linkedin": "linkedin.com/in/anita"},
    {"id": 9, "name": "Vikram Singh", "grad_year": 2022, "job": "Cloud Architect", "company": "AWS", "email": "vikram.singh@aws.com", "city": "Bangalore", "linkedin": "linkedin.com/in/vikram"},
    {"id": 10, "name": "Lakshmi Nair", "grad_year": 2017, "job": "Marketing Director", "company": "Flipkart", "email": "lakshmi.nair@flipkart.com", "city": "Bangalore", "linkedin": "linkedin.com/in/lakshmi"},
    {"id": 11, "name": "Arjun Reddy", "grad_year": 2020, "job": "Cybersecurity Analyst", "company": "Cisco", "email": "arjun.reddy@cisco.com", "city": "Hyderabad", "linkedin": "linkedin.com/in/arjun"},
    {"id": 12, "name": "Sneha Menon", "grad_year": 2021, "job": "Blockchain Developer", "company": "Polygon", "email": "sneha.menon@polygon.technology", "city": "Mumbai", "linkedin": "linkedin.com/in/sneha"},
    {"id": 13, "name": "Karan Malhotra", "grad_year": 2018, "job": "Fintech Specialist", "company": "PhonePe", "email": "karan.malhotra@phonepe.com", "city": "Bangalore", "linkedin": "linkedin.com/in/karan"},
    {"id": 14, "name": "Riya Thomas", "grad_year": 2022, "job": "Game Developer", "company": "Zynga", "email": "riya.thomas@zynga.com", "city": "Pune", "linkedin": "linkedin.com/in/riya"},
    {"id": 15, "name": "Sanjay Kumar", "grad_year": 2019, "job": "ML Engineer", "company": "Tesla", "email": "sanjay.kumar@tesla.com", "city": "Delhi", "linkedin": "linkedin.com/in/sanjay"},
    {"id": 16, "name": "Meera Iyer", "grad_year": 2020, "job": "Content Strategist", "company": "LinkedIn", "email": "meera.iyer@linkedin.com", "city": "Mumbai", "linkedin": "linkedin.com/in/meera"},
    {"id": 17, "name": "Rahul Mehra", "grad_year": 2021, "job": "SRE", "company": "Google Cloud", "email": "rahul.mehra@googlecloud.com", "city": "Bangalore", "linkedin": "linkedin.com/in/rahul"},
    {"id": 18, "name": "Deepika Joshi", "grad_year": 2018, "job": "HR Manager", "company": "TCS", "email": "deepika.joshi@tcs.com", "city": "Chennai", "linkedin": "linkedin.com/in/deepika"},
    {"id": 19, "name": "Amit Roy", "grad_year": 2022, "job": "Quantum Computing Researcher", "company": "IBM", "email": "amit.roy@ibm.com", "city": "Delhi", "linkedin": "linkedin.com/in/amitroy"},
    {"id": 20, "name": "Nisha Kapoor", "grad_year": 2019, "job": "Growth Hacker", "company": "Swiggy", "email": "nisha.kapoor@swiggy.com", "city": "Bangalore", "linkedin": "linkedin.com/in/nisha"}
]

# User Authentication
USERS = {
    "admin": hashlib.md5("admin123".encode()).hexdigest(),
    "student": hashlib.md5("student456".encode()).hexdigest(),
    "alumni": hashlib.md5("alumni789".encode()).hexdigest(),
    "monika": hashlib.md5("monika2026".encode()).hexdigest()
}

# MAIN HTML TEMPLATE (180+ lines total with styling)
MAIN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px;line-height:1.6;}}
        .container{{max-width:1400px;margin:0 auto;background:rgba(255,255,255,0.95);border-radius:20px;padding:30px;box-shadow:0 20px 60px rgba(0,0,0,0.15);}}
        .header{{text-align:center;margin-bottom:40px;}}
        .header h1{{font-size:3em;color:#2c3e50;margin-bottom:10px;text-shadow:2px 2px 4px rgba(0,0,0,0.1);}}
        .header p{{font-size:1.3em;color:#7f8c8d;}}
        .user-info{{position:absolute;top:20px;right:30px;background:#2ecc71;color:white;padding:10px 20px;border-radius:25px;font-weight:bold;box-shadow:0 5px 15px rgba(46,204,113,0.4);}}
        .nav{{display:flex;justify-content:center;flex-wrap:wrap;gap:15px;margin:30px 0;background:rgba(255,255,255,0.2);padding:20px;border-radius:15px;}}
        .nav a{{background:linear-gradient(45deg,#667eea,#764ba2);color:white;padding:15px 30px;text-decoration:none;border-radius:30px;font-weight:500;transition:all 0.3s ease;box-shadow:0 5px 15px rgba(102,126,234,0.4);}}
        .nav a:hover{{transform:translateY(-5px) scale(1.05);box-shadow:0 10px 25px rgba(102,126,234,0.6);}}
        .login-form{{max-width:450px;margin:60px auto;background:white;padding:40px;border-radius:20px;box-shadow:0 15px 40px rgba(0,0,0,0.1);}}
        .form-group{{margin-bottom:25px;}}
        .form-group label{{display:block;margin-bottom:8px;color:#2c3e50;font-weight:600;}}
        .form-group input{{width:100%;padding:15px;border:2px solid #e1e8ed;border-radius:10px;font-size:16px;transition:border-color 0.3s;}}
        .form-group input:focus{{outline:none;border-color:#667eea;box-shadow:0 0 0 3px rgba(102,126,234,0.1);}}
        .btn{{width:100%;padding:15px;background:linear-gradient(45deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;font-size:18px;font-weight:600;cursor:pointer;transition:all 0.3s;}}
        .btn:hover{{transform:translateY(-2px);box-shadow:0 10px 25px rgba(102,126,234,0.4);}}
        .alumni-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:25px;margin-top:30px;}}
        .alumni-card{{background:white;padding:30px;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,0.1);transition:all 0.3s ease;}}
        .alumni-card:hover{{transform:translateY(-8px);box-shadow:0 20px 50px rgba(0,0,0,0.15);}}
        .alumni-name{{font-size:1.8em;color:#2c3e50;margin-bottom:15px;font-weight:bold;}}
        .alumni-details{{color:#7f8c8d;line-height:1.8;}}
        .alumni-details strong{{color:#2c3e50;}}
        .linkedin-link{{display:inline-block;margin-top:15px;background:#0077b5;color:white;padding:8px 16px;border-radius:20px;text-decoration:none;font-weight:500;}}
        .stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin:30px 0;}}
        .stat-card{{background:rgba(255,255,255,0.9);padding:25px;border-radius:15px;text-align:center;box-shadow:0 8px 25px rgba(0,0,0,0.1);}}
        .stat-number{{font-size:3em;color:#667eea;font-weight:bold;}}
        .footer{{text-align:center;margin-top:50px;padding-top:30px;border-top:1px solid rgba(255,255,255,0.3);color:rgba(255,255,255,0.9);}}
        @media (max-width:768px){{.nav{{flex-direction:column;gap:10px;}}.header h1{{font-size:2em;}}}
    </style>
</head>
<body>
    <div class="container">
'''

@app.route('/')
def home():
    if 'user' not in session:
        return render_template_string(MAIN_TEMPLATE + '''
        <div class="login-form">
            <h2 style="color:#2c3e50;margin-bottom:25px;font-size:2em;">🔐 Login</h2>
            <form method="POST" action="/login">
                <div class="form-group">
                    <label>👤 Username</label>
                    <input type="text" name="username" placeholder="Enter username" required>
                </div>
                <div class="form-group">
                    <label>🔑 Password</label>
                    <input type="password" name="password" placeholder="Enter password" required>
                </div>
                <button type="submit" class="btn">🚀 Enter Portal</button>
            </form>
            <div style="text-align:center;margin-top:25px;color:#7f8c8d;">
                <p><strong>Demo Accounts:</strong></p>
                <p>admin/admin123 • student/student456 • alumni/alumni789 • monika/monika2026</p>
            </div>
        </div>
        <div class="footer">
            <p>© 2026 Monika's Alumni Portal | Professional Networking Platform</p>
        </div>
        </div></body></html>''')

    # Dashboard for logged in users
    total_alumni = len(ALUMNI_DATA)
    recent_alumni = ALUMNI_DATA[:4]

    alumni_html = ''
    for alum in recent_alumni:
        alumni_html += f'''
        <div class="alumni-card">
            <div class="alumni-name">{alum["name"]}</div>
            <div class="alumni-details">
                <strong>🎓 {alum["grad_year"]}</strong> • <strong>{alum["job"]}</strong><br>
                {alum["company"]} • {alum["city"]}
            </div>
            <a href="{alum["linkedin"]}" class="linkedin-link" target="_blank">💼 LinkedIn</a>
        </div>'''

    return render_template_string(MAIN_TEMPLATE + f'''
        <div class="user-info">👋 Welcome, {session["user"].title()}</div>
        <div class="header">
            <h1>🏛️ Alumni Portal</h1>
            <p>Connect with {total_alumni}+ successful graduates | Professional networking platform</p>
        </div>
        <div class="nav">
            <a href="/">🏠 Dashboard</a>
            <a href="/alumni">👥 Directory ({total_alumni}+)</a>
            <a href="/events">📅 Events</a>
            <a href="/stats">📊 Stats</a>
            <a href="/contact">📧 Contact</a>
            <a href="/logout" style="background:#e74c3c;">🚪 Logout</a>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_alumni}</div>
                <div>Total Alumni</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">5</div>
                <div>Active Events</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">20+</div>
                <div>Companies</div>
            </div>
        </div>
        <h2 style="color:#2c3e50;margin:40px 0 20px 0;">⭐ Featured Alumni</h2>
        <div class="alumni-grid">
            {alumni_html}
        </div>
        <div class="footer">
            <p>© 2026 Monika's Alumni Portal | Built with ❤️ for professional networking</p>
        </div>
        </div></body></html>''', **locals())

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

    alumni_html = ''
    for alum in ALUMNI_DATA:
        alumni_html += f'''
        <div class="alumni-card">
            <div class="alumni-name">{alum["name"]}</div>
            <div class="alumni-details">
                <strong>🎓 Graduated:</strong> {alum["grad_year"]}<br>
                <strong>👨‍💼 Position:</strong> {alum["job"]}<br>
                <strong>🏢 Company:</strong> {alum["company"]}<br>
                <strong>📍 Location:</strong> {alum["city"]}<br>
                <strong>✉️ Email:</strong> {alum["email"]}
            </div>
            <a href="{alum["linkedin"]}" class="linkedin-link" target="_blank">🔗 View LinkedIn</a>
        </div>'''

    return render_template_string(MAIN_TEMPLATE + f'''
        <div class="user-info">👋 {session["user"].title()}</div>
        <div class="header">
            <h1>👥 Complete Alumni Directory</h1>
            <p>Browse all {len(ALUMNI_DATA)} successful graduates by position, company, and location</p>
        </div>
        <div class="nav">
            <a href="/">🏠 Dashboard</a>
            <a href="/alumni">👥 Directory</a>
        </div>
        <div class="alumni-grid">
            {alumni_html}
        </div>
        </div></body></html>''')

@app.route('/events')
def events():
    if 'user' not in session:
        return redirect(url_for('home'))

    return render_template_string(MAIN_TEMPLATE + '''
        <div class="user-info">👋 Logged In</div>
        <div class="header">
            <h1>📅 Upcoming Events</h1>
            <p>Join alumni reunions, career fairs, and networking workshops</p>
        </div>
        <div class="nav">
            <a href="/">🏠 Dashboard</a>
            <a href="/events">📅 Events</a>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">🎉 Reunion 2026</div>
                <div>June 15 • Campus Hall • 500+ attendees</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">💼 Career Fair</div>
                <div>May 20 • Online • Google, Microsoft, Amazon</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">🔬 Tech Workshop</div>
                <div>April 25 • Campus Lab • AI/ML Focus</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">🌟 Mentorship</div>
                <div>Ongoing • 1:1 Sessions • Book Now</div>
            </div>
        </div>
        </div></body></html>''')

@app.route('/stats')
def stats():
    if 'user' not in session:
        return redirect(url_for('home'))

    companies = {}
    for alum in ALUMNI_DATA:
        company = alum['company']
        companies[company] = companies.get(company, 0) + 1

    top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]

    return render_template_string(MAIN_TEMPLATE + f'''
        <div class="user-info">👋 {session["user"].title()}</div>
        <div class="header">
            <h1>📊 Alumni Statistics</h1>
            <p>Employment trends and company distribution</p>
        </div>
        <div class="nav">
            <a href="/">🏠 Dashboard</a>
            <a href="/stats">📊 Stats</a>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(ALUMNI_DATA)}</div>
                <div>Total Alumni</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">20+</div>
                <div>Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">Tech 75%</div>
                <div>Industry Focus</div>
            </div>
        </div>
        <h2 style="color:#2c3e50;margin:40px 0 20px 0;">🏆 Top Companies</h2>
        <div class="alumni-grid">
        ''' + ''.join([f'''
            <div class="alumni-card">
                <div class="alumni-name">{company}</div>
                <div class="alumni-details"><strong>{count} alumni</strong> working here</div>
            </div>''' for company, count in top_companies]) + '''
        </div>
        </div></body></html>''')

@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('home'))

    return render_template_string(MAIN_TEMPLATE + '''
        <div class="user-info">👋 Logged In</div>
        <div class="header">
            <h1>📧 Contact Alumni Office</h1>
            <p>Get in touch for events, verification, or support</p>
        </div>
        <div class="nav">
            <a href="/">🏠 Dashboard</a>
            <a href="/contact">📧 Contact</a>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">📧 alumni@college.edu</div>
                <div>Main Email</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">📞 +91-98765-43210</div>
                <div>Phone Support</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">🕒 Mon-Fri 9AM-6PM</div>
                <div>Office Hours</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">📍 123 College Rd</div>
                <div>Main Campus</div>
            </div>
        </div>
        </div></body></html>''')

@app.route('/api/alumni')
def api_alumni():
    return jsonify({
        "status": "success",
        "total": len(ALUMNI_DATA),
        "data": ALUMNI_DATA
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
