from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1><p>Welcome to your Flask app.</p>'

@app.route('/hello/<name>')
def greet(name):
    return f'<h1>Hello, {name}!</h1><p>Thanks for visiting.</p>'

if __name__ == '__main__':
    app.run(debug=True)
