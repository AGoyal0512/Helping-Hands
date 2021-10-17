from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'HelpingHands00018@gmail.com'
app.config['MAIL_PASSWORD'] = 'Datathon_18'
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
    first = request.form.get("First")
    last = request.form.get("Last")
    subject = "Patient: " + first + " " + last
    msg = Message(subject, sender = 'HelpingHands0018@gmail.edu', recipients = [request.form.get("email")])
    msg.body = "Patient's number: " + request.form.get("Phone")
    msg.body = msg.body + "\n" + "Patient's response: " + request.form.get("text")
    mail.send(msg)
    return render_template("assess.html")

app.run(port=5000)
