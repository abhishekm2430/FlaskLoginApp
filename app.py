from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/testpython'
db = SQLAlchemy(app)



class Report(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  sender = db.Column(db.String(80))
  recipient = db.Column(db.String(80))
  message = db.Column(db.String(200))
  open_count = db.Column(db.Integer)
db.create_all()



mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "email id",
    "MAIL_PASSWORD": "gmail password"
}




class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz1'),
    User(2, 'user2', 'abcxyz2'),
    User(3, 'user3', 'abcxyz3'),
    User(4, 'user4', 'abcxyz4'),
    User(5, 'user5', 'abcxyz5'),
    User(6, 'user6', 'abcxyz6'),
    User(7, 'user7', 'abcxyz7'),
    User(8, 'user8', 'abcxyz8'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

app.config.update(mail_settings)
mail = Mail(app)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"
 



@app.route('/login', methods=['GET','POST'])
def do_admin_login():
  if(request.method == 'POST'):
    username = request.form['username']
    password = request.form['password']

    user = username_table.get(username, None)
     if(user == None):
        return jsonify({"msg": "Invalid username or password"}), 401
     elif(user.password != password):
        return jsonify({"msg": "Invalid password"}), 401
     else:
        session['logged_in'] = True
        session['current_user'] = username
        return redirect("http://localhost:5000/compose")
    else:
        flash('wrong password!')
  else:
    return render_template('login.html')




@app.route('/compose', methods = ['GET','POST'])
def compose():
  if not session.get('logged_in'):
        return render_template('login.html')
  if(request.method == 'POST'):
    reciever = request.form['to']
    messg = request.form['messg']
    record = Report(sender=session.get('current_user'), recipient=reciever, message = messg, open_count = 0)
    db.session.add(record)
    db.session.commit()
    unique_id = record.id 

    if __name__ == '__main__':
      with app.app_context():
        msg = Message(subject="Hello", sender=session.get('current_user'), recipients=[reciever], body=messg) 
        msg.html = render_template('emails.html', reciever = reciever, messg = messg, unique_id = unique_id)
        mail.send(msg)
    return redirect("http://localhost:5000/compose")
  else:
    return render_template('compose.html')



 
@app.route('/report', methods = ['GET'])
def report():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    user = session.get('current_user')
    res = Report.query.filter_by(sender = user).all()
    return render_template('report.html', res = res)


@app.route('/tracking')
def tracking():
  unique_id = request.args.get('unique_id')
  row1 = Report.query.filter_by(id = unique_id)
  row1.open_count = row1.open_count + 1;
  db.session.commit()

  return "return a small image of size 1 X 1"


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()