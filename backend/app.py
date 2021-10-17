from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shivanshagg18@gmail.com'
app.config['MAIL_PASSWORD'] = 'GAInTheHouse'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/", methods=['GET'])
def home():
    return render_template("project.html")

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/assess", methods=['GET'])
def assess():
    return render_template("assess.html")

@app.route("/form", methods=['POST'])
def post():
    print(request.form.get("First"))
    print(request.form.get("Last"))
    return render_template("assess.html")

app.run(port=5000)
