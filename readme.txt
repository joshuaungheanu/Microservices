Project 1 CPSC 476

Project Name: Blog
Team: Shamant Bhimangoud Naik
           Joshua Ungheanu

Libraries Used:
Hashing Libraries	: sha256_crypt
RDBMS		: SQLite3
Authorization: 	: flask_basicauth
Python framework      : Flask

Structure:
	- users.py
	- comments.py
	- tags.py
	- articles.py
	- test_users.tavern.yaml
	- test_articles.tavern.yaml
	- test_comments.tavern.yaml
	- test_tags.tavern.yaml
	- microdatabase.db
	- db.py
	- Procfile


Micro-Service : User
users.py


Functionality: Create new user
Url: http://localhost:5000/addUser
Method:POST
Curl command example: curl -i -H "Content-Type: application/json" -X POST -d '{"email":"aaa@gmail.com","name":"aaa","password":"aaa"}' http://127.0.0.1:5000/addUser
Input variables :
	email : email is a unique key
	name : name of the user
	password : Password which will be hashed and stored in the database
	

Functionality: Delete existing user
Url: http://127.0.0.1:5000/deleteUser
Method: DELETE
Login by entering the email and password.
Curl command example: curl -i -u aaa@gmail.com:aaa -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/deleteUser
Input variables :
	email : email will be fetched from authentication data
Functionality: Change existing user’s password
Url: http://127.0.0.1:5000/updatePassword
Method: PATCH
Login by entering the user id and password.
Curl command example : curl -i -u eee@gmail.com:eee -H "Content-Type: application/json" -X PATCH -d '{"newPassword":"eeee"}' http://127.0.0.1:5000/updatePassword
Input variables :
	newPassword: new password to be changed


Micro-service: Articles
articles.py


Functionality: Post a new article
Url: http://127.0.0.1:5000/addArticle
Method: POST
Curl command example: curl -i -u xxx@gmail.com:xxx -H "Content-Type: application/json" -X POST -d '{"title":"xxx_blog","content":"blog of xxx"}' http://127.0.0.1:5000/addArticle
Input variables:
	title: Title for the blog
	content: Content for the blog


Functionality: Retrieve an individual article
Url: http://127.0.0.1:5000/fetchArticle
Method: GET
Curl command example:curl -i -u xxx@gmail.com:xxx -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/fetchArticle/xxx_blog
Login by entering the user id and password.
Input variables:
	title : Provide title for retrieving article


Functionality: Edit an individual article. The last-modified timestamp should be updated.
Url: http://127.0.0.1:5000/editArticle
Method: PATCH
Curl command example: curl -i -u xxx@gmail.com:xxx -H "Content-Type: application/json" -X PATCH -d '{"title":"xxx_blog","newTitle":"xxx_XXX","newContent":"this is new content"}' http://127.0.0.1:5000/editArticle
Login by entering the user id and password.
Input variables :
	title: Provide title to edit
	newTitle: Title to be replaced
	newContent: Content to be replaced








Functionality: Retrieve the entire contents (including article text) for the n most recent articles
Url: http://127.0.0.1:5000/recentArticle
Method: GET
Curl command example: curl -i -u aaa@gmail.com:aaa -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/recentArticle?mostRecent=3
Input variables:
	mostRecent : Retrieve all data of article.


Functionality: Retrieve metadata for the n most recent articles, including title, author, date, and URL
Url: http://127.0.0.1:5000/metaArticle
Method: GET
Curl command example: curl -i -u aaa@gmail.com:aaa -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/metaArticle?mostRecent=3
Input variables:
	mostRecent: Retrieve metadata of given number


Micro-service: Comments
comments.py

Functionality: Add a new comment
Url: http://127.0.0.1:5000/article/<int:articleId>/comment"
Method: POST
Require login credentials
Curl command example: curl -POST http://127.0.0.1:5000/article/2/comment -d '{"article_id":2,"comment":"#comment goes here"}
Input variables:
	comment_context: your comment entered here
	article_id: Article Id associated with comment


Functionality: Delete a comment 
Url: http://127.0.0.1:5000/article/comment/<int:commentId>
Method: DELETE
Require login credentials
Curl command example: curl -X DELETE http://127.0.0.1:5000/article/comment -d '{"article_id":2,"comment":"#comment goes here"}
Input variables:
	Comment_id : Id is associated to the comment that will delete


Functionality: Retrieve the nth number of comments
Url: http://127.0.0.1:5000 /article/<string:articleId>/comment
Method: GET
Curl command example: curl -GET http://127.0.0.1:5000/article/2/comment -d '{"article_id"}
Require login credentials
Input variables :
	Article_id: all comments associate with article id.







Functionality: Retrieve n recent comment of an individual article
Url: http://127.0.0.1:5000 /article/<string:articleId>/comment/<int:n>
Method: GET
Curl command example: curl -GET http://127.0.0.1:5000/article/3/comment/1 -d '{"article_id":1}

Require login credentials
Input variables :
	Article_id: most recent comment associate with article id.

Functionality: Update an existing comment
Url: http://127.0.0.1:5000/article/<int:articleId>/comment"
Method: PUT
Curl command example: curl -PUT http://127.0.0.1:5000/article/2/comment -d '{"article_id":2,"comment":"#comment goes here"}
Require login credentials
Input variables :
	comment_contect: updated comment.
	comment_id: comment id associated to a specific comment.



Micro-service: Tags
tags.py

Functionality: Add a tag to a new URL
Url: http://127.0.0.1:5000/tags
Method: POST
Require login credentials
Curl command example: curl -POST http://127.0.0.1:5000/tags -d '{"article_id":2,"tag_name":"#comment goes here"} 

Input variables:
	article_id: Article Id associated with tag
	tag_name: tags name



Functionality: Delete a tag with the URL 
Url: http://127.0.0.1:5000/tags
Method: DELETE
Require login credentials
Curl command example: Curl command example: curl -X DELETE http://127.0.0.1:5000/tags -d '{"article_id":1,"tag_name":"#URL"} 



Input variables:
	article_id: Article Id associated with tag
	tag_name: tags name



Functionality: Retrieve tag for an individual URL
Url: http://127.0.0.1:5000 /tags
Method: GET
Require login credentials
Curl command example: curl -GET http://127.0.0.1:5000/tags/5 

Input variables :
	article_id: tags associate with article id.



Functionality: Retrieve a list of URL by a given tag
Url: http://127.0.0.1:5000 /tags
Method: GET
Require login credentials
Curl command example: curl -GET http://127.0.0.1:5000/tags?tag=%20URL
Input variables :
	tag_name: tags name 


