#metadata feed (ARticle Post for url)


@requires_auth
def insertarticle():
    if request.method == 'POST':
        data = request.get_json(force = True)
        executionState:bool = False
        try:
            cur = get_db().cursor()
            current_time= datetime.datetime.now()
            is_active_article=1
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("INSERT INTO article(title,author,content,date_created,date_modified,is_active_article) VALUES (:title, :author, :content, :date_created, :date_modified, :is_active_article)",{"title":data['title'],"author":uid,"content": data['content'], "date_created":current_time,"date_modified":current_time,"is_active_article":is_active_article })
            last_inserted_row = cur.lastrowid
            url_article=("http://127.0.0.1:5200/article/"+str(last_inserted_row)+"")
            cur.execute("UPDATE article set url=? where article_id=?",(url_article,last_inserted_row))
            if(cur.rowcount >=1):
                    executionState = True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Instersted Sucessfully"), 201
            else:
                return jsonify(message="Failed to insert data"), 409


#1 get method metadata for articles(article route)

                if metadata is not None:
                          cur.execute("select title,author,date_created,url,content from article  where is_active_article = 1 order by date_created desc limit :metadata", {"metadata":metadata})
                          row = cur.fetchall()
                          if list(row) == []:
                              return "No such value exists\n", 204
                          return jsonify(row), 200

#2 comments (GET route)

@app.route('/comment/<article_id>',methods = ['GET'])
def root(article_id):
    cur = get_db().cursor()
    cur.execute("SELECT comment from comments WHERE article_id="+article_id)
    row = cur.fetchall()
    return jsonify(row)




#3 Full Feed

#article route (GET) via article number in brower link (return all data when article id is given)

@app.route('/article/<article_id>',methods = ['GET'])
def root(article_id):
    cur = get_db().cursor()
    cur.execute("SELECT * from  article WHERE article_id="+article_id)
    row = cur.fetchall()
    return jsonify(row)

#comment route (GET)(return comments when article id is given)
    @app.route('/comment/<article_id>',methods = ['GET'])
    def root(article_id):
        cur = get_db().cursor()
        cur.execute("SELECT comment from comments WHERE article_id="+article_id)
        row = cur.fetchall()
        return jsonify(row)


# tag get route (GET)(return all tag data when article id is given)

@app.route('/tags/<string:article_id>',methods = ['GET'])
def getTagsFromArticle(article_id):
    if request.method == 'GET':
        cur = get_db().cursor()
        cur.execute("SELECT tag_name from tags WHERE tag_id IN (SELECT tag_id from tag_article_mapping WHERE article_id=:article_id )", {"article_id":article_id})
        row = cur.fetchall()
        return jsonify(row), 200
