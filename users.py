from flask import Flask, jsonify, request, Response, g
import sqlite3, json
from flask_api import status
import datetime
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt

app = Flask(__name__)
auth = HTTPBasicAuth()

DATABASE = 'microdatabase.db'

# Establish db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print("database closed")
        db.close()

# Create a new user
@app.route("/addUser", methods=['POST'])
def addUser():
    if (request.method == 'POST'):
        try:
            jasonData = request.get_json()
            db = get_db()
            c = db.cursor()
            updateTime = datetime.datetime.now()

            password = sha256_crypt.encrypt((str(jasonData['password'])))
            c.execute("insert into users (email, name, password, createTime, updateTime) values (?,?,?,?,?)",
                    [jasonData['email'], jasonData['name'], password, updateTime, updateTime ])
            db.commit()

            response = Response(status=201, mimetype='application/json')

        except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype='application/json')

    return response

# Password Authentication
@auth.verify_password
def verify(username, password):
    try:
        db = get_db()
        c = db.cursor()
        msg = {}

        c.execute("select password from users where email=(:email)", {'email':username})
        pwd = c.fetchone()
        if pwd is not None:
            p = pwd[0]
            if (sha256_crypt.verify(password,p)):
                return True
            else:
                return False
        else:
            return False

    except sqlite3.Error as e:
        print(e)

    return False

# Delete existing users
@app.route("/deleteUser", methods=['DELETE'])
@auth.login_required
def deleteUser():
    try:
        db = get_db()
        c = db.cursor()
        email = request.authorization.username

        c.execute("delete from users where email=(:email)",{'email':email})
        db.commit()

        response = Response(status=200, mimetype='application/json')

    except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype='application/json')

    return response

# Update/Change User's Password
@app.route("/updatePassword", methods=['PATCH'])
@auth.login_required
def updatePassword():
    try:
        db = get_db()
        c = db.cursor()
        jasonData = request.get_json()
        newPassword = sha256_crypt.encrypt(jasonData['newPassword'])
        email = request.authorization.username
        updateTime = datetime.datetime.now()

        c.execute("update users set password=(:password), updateTime=(:updateTime) where email=(:email)",{'email':email, 'password':newPassword, 'updateTime':updateTime})
        db.commit()
        response = Response(status=200, mimetype='application/json')

    except sqlite3.Error as e:
        print(e)
        response = Response(status=409, mimetype='application/json')

    return response

if __name__ == '__main__':
    app.run(debug=True)
