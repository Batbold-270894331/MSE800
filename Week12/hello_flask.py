from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/bye')
def bye():
    return "Bye, Flask!"

@app.route('/user/<username>')
def user(username):
    return f"Hello, {username}!"

if __name__ == "__main__":
    app.run(debug=True)