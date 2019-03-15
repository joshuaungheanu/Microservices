from flask import Flask, jsonify, request, Response, g
import sqlite3, json
from flask_api import status
import datetime
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt

app = Flask(__name__)
auth = HTTPBasicAuth()

DATABASE = 'microdatabase.db'

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

@auth.login_required

# Add a new comment to an article
@app.route("/article/<int:articleId>/comment", methods=['POST'])
def comment(articleId):

    cur = db.connection.cursor()
    username = None
    comment = request.form.get('comment')
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    cur.execute("SELECT article_id FROM article WHERE article_id = ? ", (articleId,))
    returnObject = cur.fetchone()
    if(returnObject):
        if(username is not None):
            insertComment = (comment, articleId, username)
            if(checkAuth(username, password) == True):
                cur.execute("INSERT INTO comment (comment_content, articleId, author) VALUES (?, ?, ?)", insertComment)
                db.connection.commit()
                cur.execute("SELECT comment_id FROM comment where comment_content = ? AND articleId = ?", (comment, articleId))
                commentId = cur.fetchone()[0]
                db.connection.commit()
                return jsonify({'articleId' : articleId, 'comment_id' : commentId}), 201
            else:
                return jsonify('Credentials not found'), 409
        else:
            insertComment = (comment, articleId)
            cur.execute("INSERT INTO Comment (comment, artId) VALUES (?, ?)", insertComment)
            db.connection.commit()
            cur.execute("SELECT commentId FROM comment where comment = ? AND artId = ?", (comment, articleId))
            commentId = cur.fetchone()[0]
            db.connection.commit()
            return jsonify({'articleId' : articleId, 'comment_id' : commentId}), 201
    else:
        return jsonify('articleId was not found'), 404

# Delete an individual comment
@app.route("/article/comment/<int:commentId>", methods=['DELETE'])
def deleteComment(commentId):
    cur = db.connection.cursor()
    if (request.authorization):
        username = request.authorization.username
        password = request.authorization.password
    else:
        return jsonify('Unauthorized request'), 401
    cur.execute("SELECT * FROM comment WHERE comment_id = ? ", (commentId,))
    returnObject = cur.fetchone()
    if(returnObject):
        if(checkAuth(username, password) == True):
            cur.execute("SELECT author FROM comment WHERE comment_id = ? ", (commentId,))
            author = cur.fetchone()[0]
            if(author == username):
                cur.execute("DELETE FROM comment WHERE comment_id = ?", (commentId,))
                db.connection.commit()
                return jsonify('comment deleted'), 200
            else:
                return jsonify('You are not authorized to delete this comment'), 409
        else:
            return jsonify('Credentials not found'), 409
    else:
        return jsonify('comment_id was not found'), 404

# Return the total amount of comments on a given article
@app.route("/article/<string:articleId>/comments", methods=['GET'])
def getNumOfComments(articleId):
    cur = db.connection.cursor()
    cur.execute("SELECT article_id FROM article WHERE article_id = ? ", (articleId,))
    returnObject = cur.fetchone()
    if(returnObject):
        cur.execute("SELECT * FROM comment WHERE articleId = ?", (articleId,))
        comments= cur.fetchall()
        return jsonify(len(comments)), 200
    else:
        return jsonify('articleId was not found'), 404

#4 Return the nth most recent comment based on the URL
@app.route("/article/<string:articleId>/comments/<int:n>", methods=['GET'])
def getNComments(articleId, n):
    cur = db.connection.cursor()
    nComments = (articleId, n)
    cur.execute("SELECT article_id FROM article WHERE article_id = ? ", (articleId,))
    returnObject = cur.fetchone()
    if(returnObject):
        cur.execute("SELECT comment_content FROM comment WHERE articleId = ? ORDER BY created DESC LIMIT ?", nComments)
        comments = cur.fetchall()
        returnComments = {}
        for comment in comments:
            returnComments['comment'] = comment[0]
        return jsonify(returnComments), 200
    else:
        return jsonify('articleId was not found'), 404

if(__name__ == '__main__'):
    app.run(debug=True)
