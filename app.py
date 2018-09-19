from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from werkzeug.security import safe_str_cmp

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
#u = username_table.get("user9",None)
#if(u == None):
#  print("No such username")
#else:
 # print(u.password)
#print(userid_table)

app = Flask(__name__)
app.debug = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

@app.route('/login', methods=['GET','POST'])
def login():
   if(request.method=='POST'):
     username = request.json.get('username', None)
     password = request.json.get('password', None)
     #username = request.form['username']
     #password = request.form['password']
     user = username_table.get(username, None)
     if(user == None):
        return jsonify({"msg": "Invalid username or password"}), 401
     elif(user.password != password):
        return jsonify({"msg": "Invalid password"}), 401
     
     ret = {
            'access_token':create_access_token(identity = username) }
     return jsonify(ret), 200
   return render_template('login.html')



@app.route('/protected', methods=['GET'])    
@jwt_required
def protected():

  current_user = get_jwt_identity()
  return jsonify({'status':200,'Logged in as':current_user}), 200
 
@app.route('/welcome')
def welcome():
  return render_template('welcome.html')

if __name__ == '__main__':
    app.run()