from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "<div><p>Hello, Flask!</p></div>"

@app.route('/bye')
def bye():
    return "Bye, Flask!"

@app.route('/user/<username>')
def user(username):
    return f"Hello, {username}!"

@app.route('/user/<username>/<int:age>')
def user_with_age(username, age):
    return f"Hello, {username}! You are {age} years old."

@app.route("/flask")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)