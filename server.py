from flask import Flask

app = Flask(__name__)

@app.route('/home')
def home():
    return 'Welcome to the home page!'

@app.route('/heartbeat')
def heartbeat():
    return 'Server is up and running.'

if __name__ == '__main__':
    app.run(debug=True)
