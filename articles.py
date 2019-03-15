from flask import Flask, jsonify, request, make_response, g, Response
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
        db.close()

# Add article with authentication
@app.route("/addArticle", methods=['POST'])
@auth.login_required
def addArticle():
    if (request.method == 'POST'):
        try:
            db = get_db()
            c = db.cursor()
            jsonData = request.get_json()
            updateTime = datetime.datetime.now()
            email = request.authorization.username
            url = "127.0.0.1:5000/articles/"

            if not jsonData['title'] or not jsonData['content']:
                return jsonify({'Message': 'Missing data'})
            else:

                c.execute("insert into article (title, content, email, createTime, updateTime, url) values (:title, :content, :email, :createTime, :updateTime, :url)",{"title":jsonData['title'], "content":jsonData['content'], "email":email, "createTime":updateTime, "updateTime":updateTime, "url":url})
                last = c.lastrowid
                #c.execute("select article_id from article desc 1")
                #article_id = c.fetchone[0]
                url = "127.0.0.1:5000/articles/" + str(last)
                c.execute("update article set url = (:url) where article_id = (:last)",{"url":url, "last":last})

                db.commit()
                c.execute("select article_id from article order by createTime DESC")
                aID = c.fetchone()
                print(aID)
                response = Response(status = 201, mimetype = 'application/json')
                response.headers['location'] = 'http://127.0.0.1:5000/articles/'+str(aID[0])

        except sqlite3.Error as e:
                print(e)
                response = Response(status=409, mimetype='application/json')

        return (response)

# Fetch all articles
@app.route("/fetchArticle/<title>", methods=['GET'])
@auth.login_required
def fetchArticle(title):
    if (request.method == 'GET'):
        try:
            db = get_db()
            c = db.cursor()
            updateTime = datetime.datetime.now()
            email = request.authorization.username
            print(title)

            c.execute("select article_id, title, content, createTime, updateTime from article where title = (:title)", {'title':title})
            userArticle = c.fetchone()
            db.commit()

            if not userArticle:
                response = Response(status = 404, mimetype = 'application/json')
            else:
                return jsonify(userArticle)


        except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype = 'application/json')

    return response


# Edit article - last modified timestamp
@app.route("/editArticle", methods=['PATCH'])
@auth.login_required
def editArticle():
    if (request.method == 'PATCH'):
        db = get_db()
        c = db.cursor()
        email = request.authorization.username
        updateTime = datetime.datetime.now()

        try:
            jsonData = request.get_json()
            if not jsonData['title']:
                response = Response(status = 405, mimetype = 'application/json')

            else:
                c.execute("select * from users where email = (:email)", {'email':email})
                userId = c.fetchone()[0]
                print(userId)

                print("hi")
                c.execute("select * from article")
                print(c.fetchone())
                print("before")

                c.execute("update article set title = (:newTitle), content = (:newContent), updateTime = (:updateTime) where email = (:email) and title = (:title)", {'email':email, 'title':jsonData['title'], 'newTitle':jsonData['newTitle'], 'updateTime':updateTime, 'newContent':jsonData['newContent']})
                print("after")
                db.commit()
                response = Response(status=200, mimetype='application/json')
        except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype='application/json')

    return response

# Delete article
@app.route("/deleteArticle", methods=['DELETE'])
@auth.login_required
def deleteArticle():
    if (request.method == 'DELETE'):
        try:
            db = get_db()
            c = db.cursor()
            jsonData = request.get_json()
            updateTime = datetime.datetime.now()
            email = request.authorization.username
            if not email or not jsonData['title']:
                response = Response(status=404, mimetype='application/json')

            else:

                c.execute("delete from article where email = (:email) and title = (:title)",
                    {'email':email, 'title':jsonData['title']})

                db.commit()
                response = Response(status=200, mimetype='application/json')

        except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype='application/json')

    return response

# Retrieve Recent article
@app.route("/recentArticle", methods=['GET'])
#@auth.login_required
def recentArticle():
        try:
            db = get_db()
            c = db.cursor()
            jsonData = request.args.get('mostRecent')
            c.execute("select title, content from article order by createTime desc limit (:jsonData)", {"jsonData":jsonData})
            userArticle = c.fetchall()

            if userArticle == ():
                return Response(status=404, mimetype='application/json')
            else:
                return jsonify(userArticle)

            db.commit()

        except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype='application/json')
        return response

# Retrive metadata for the nth most recent article
@app.route("/metaArticle", methods=['GET'])
def metaArticle():
    try:
        db = get_db()
        c = db.cursor()
        jsonData = request.args.get('mostRecent')
        c.execute("select title, content, email, createTime, url from article order by createTime desc limit (:jsonData)", {"jsonData":jsonData})
        recentArticles = c.fetchall()

        if recentArticles == ():
            return Response(status = 404, mimetype='application/json')
        else:
            return jsonify(recentArticles)

    except sqlite3.Error as e:
            print(e)
            response = Response(status=409, mimetype='application/json')

    return response


# User Verification
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

# List all articles
@app.route("/display", methods=['GET'])
@auth.login_required
def display():
    message = {"meaning_of_life": 42}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)
