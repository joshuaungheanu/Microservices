import sqlite3

# Establishing database connection
conn = sqlite3.connect("blogdatabase.db")
c = conn.cursor()

c.execute(""" Create table if not exists users (
                    email TEXT PRIMARY KEY UNIQUE,
                    name TEXT,
                    password TEXT,
                    createTime DATETIME,
                    updateTime DATETIME) """)

c.execute(""" Create table if not exists article (
                    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT,
                    email TEXT,
                    createTime DATETIME,
                    updateTime DATETIME,
                    url TEXT,
                    FOREIGN KEY (email) REFERENCES users(email)) """)

c.execute(""" Create table if not exists comment (
                    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comment_content TEXT,
                    author TEXT,
                    articleId INTEGER,
                    createTime DATETIME,
                    updateTime DATETIME,
                    FOREIGN KEY (articleId) REFERENCES article(articleId)) """)

c.execute(""" Create table if not exists tagHead (
                    tagId INTEGER PRIMARY KEY AUTOINCREMENT,
                    tagName TEXT,
                    tagFrequency TEXT,
                    createTime DATETIME,
                    updateTime DATETIME) """)

c.execute(""" Create table if not exists tag_detail (
                    articleId INTEGER,
                    tags TEXT,
                    createTime DATETIME,
                    updateTime DATETIME,
                    FOREIGN KEY (articleId) REFERENCES article(articleId)) """)

conn.commit()
conn.close()
