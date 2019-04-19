from flask import Flask,request, g
from flask import jsonify
import json
import sqlite3
import datetime
from DatabaseInstance import get_db
# from authentication import *

DATABASE = './articles.db'

app = Flask(__name__)

#insert articles
@app.route('/articles',methods = ['POST'])
def insertArticle():
    if request.method == 'POST':
        data = request.get_json(force = True)
        executionState:bool = False
        try:
            cur = get_db(DATABASE).cursor()
            current_time= datetime.datetime.now()
            # uid = request.authorization["username"] Not required
            # pwd = request.authorization["password"] Not required
            cur.execute("INSERT INTO articles(title,author,content,date_created,date_modified) VALUES (:title, :author, :content, :date_created, :date_modified)",{"title":data['title'],"author":data['author'],"content": data['content'], "date_created":current_time,"date_modified":current_time })
            last_inserted_row = cur.lastrowid
            url_article=("http://127.0.0.1:5200/articles/"+str(last_inserted_row)+"")
            cur.execute("UPDATE articles set url=? where article_id=?",(url_article,last_inserted_row))
            if(cur.rowcount >=1):
                    executionState = True
            get_db(DATABASE).commit()
        except:
            get_db(DATABASE).rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data insert sucessfully"), 201
            else:
                return jsonify(message="Failed to insert data"), 409


# Get invidiual article
@app.route('/articles', methods= ['GET'])
def show():
    cur = get_db(DATABASE).cursor()
    article_id = request.args.get('article_id')

    try:
        if article_id is not None:
            #cur.execute("SELECT * from articles WHERE article_id = " + article_id)
            cur.execute("SELECT * from articles WHERE article_id="+article_id)
            row = cur.fetchone()
    except:
        get_db(DATABASE).rollback()
        return jsonify(message="Fail to retrieve from db"), 409
    finally:
        if row is None:
            return jsonify(message="Article not found"), 404

        return jsonify(row), 200

#get latest n article and get all article
@app.route('/articles',methods = ['GET'])
def list():
    if request.method == 'GET': # try except
        limit = request.args.get('limit') if request.args.get('limit') else 5
        executionState:bool = True
        cur = get_db(DATABASE).cursor()
        print(limit)

        try:
            # Get the n most recent articles
            if limit is not None :
                cur.execute("select * from articles order by date_created desc limit :limit",  {"limit":limit})
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n", 204
                return jsonify(row), 200

            if limit is None and article_id is None :
                cur.execute('''Select * from articles''')
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n", 204
                return jsonify(row), 200

            if article_id is not None :
                cur.execute("SELECT * from  articles WHERE article_id="+article_id)
                row = cur.fetchall()
                if list(row) == []:
                    return "No such value exists\n", 204
                return jsonify(row), 200

        except:
            get_db(DATABASE).rollback()
            executionState = False
        finally:
            if executionState == False:
                return jsonify(message="Fail to retrieve from db"), 409
            else:
                return jsonify(row), 200

# get meta data for n most recent
@app.route('/articles/metadata',methods = ['GET'])
def metaList():
    if request.method == 'GET': # try except
        limit = request.args.get('limit') if request.args.get('limit') else 10
        executionState:bool = True
        cur = get_db(DATABASE).cursor()

        try:
            if limit is not None:
                cur.execute("select title,author,date_created,date_modified from articles order by date_created desc limit :limit", {"limit":limit})
                row = cur.fetchall()

                if len(row) == 0:
                    return "No such value exists\n", 204
                return jsonify(row), 200

        except:
            get_db(DATABASE).rollback()
            executionState = False
        finally:
            if executionState == False:
                return jsonify(message="Fail to retrieve from db"), 409
            else:
                return jsonify(row), 200

# update article
@app.route('/articles/<id>',methods = ['PUT'])
def updateArticle(id):
    if request.method == 'PUT':
        cur = get_db(DATABASE).cursor()
        executionState:bool = True

        try:
            data = request.get_json(force = True)
            tmod = datetime.datetime.now()
            cur.execute("select * from articles where article_id=?",(data['article_id'],))
            res=cur.fetchall()
            if len(res) >0:
                cur.execute("UPDATE articles set content=?,date_modified=? where article_id=? and author=?", (data['content'],tmod,data['article_id'], id))
                if(cur.rowcount >=1):
                    executionState = True
                get_db(DATABASE).commit()
            else:
                return jsonify(message="Article does not exist"), 409
        except:
            get_db(DATABASE).rollback()
            print("Error in update")
        finally:
            if executionState == True:
                return jsonify(message="Updated article successfully"), 201
            else:
                return jsonify(message="Failed to update Article"), 409

#delete article by article id
@app.route('/articles/<id>', methods = ['DELETE'])
def deleteArticle(id):
    if request.method == 'DELETE':
        cur = get_db(DATABASE).cursor()
        executionState:bool = False
        try:
            data = request.get_json(force=True)
            cur.execute("select * from articles where article_id=?",(data['article_id'],))
            res=cur.fetchall()
            if len(res) > 0:
                cur.execute("UPDATE articles where article_id= :article_id and author= :author AND EXISTS(SELECT 1 FROM articles WHERE author=:author)",{"article_id":data['article_id'], "author":author})
                row = cur.fetchall()
                if cur.rowcount >= 1:
                    executionState = True
                get_db(DATABSE).commit()

        except:
            get_db(DATABASE).rollback()
            print("Error")
        finally:
            if executionState == True:
                return jsonify(message="Deleted article successfully"), 200
            else:
                return jsonify(message="Failed to delete Article"), 409


if __name__ == '__main__':
    app.run(debug=True)
    app.run(DATABASE='articles.db')
