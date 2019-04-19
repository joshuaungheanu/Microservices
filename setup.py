import sqlite3

sqlite_file = 'users.db'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('users.db', timeout=10)
print("Successfully connected")

# users denormalization table
conn.execute('''CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY NOT NULL,
password TEXT NOT NULL,
display_name TEXT NOT NULL,
date_created DATE NOT NULL,
email_id TEXT NOT NULL,
is_active INTEGER NOT NULL )''')
print("Table successfully created")

# Create Unique username
conn.execute ('CREATE INDEX IF NOT EXISTS user_index ON users (username) ')

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

sqlite_file = 'articles.db'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('articles.db', timeout=10)
print("Successfully connected")

# article denormalization table
conn.execute('''CREATE TABLE IF NOT EXISTS articles(
article_id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
author INTEGER NOT NULL,
content TEXT NOT NULL,
date_created DATE,
date_modified DATE,
url TEXT )''')
print("Table successfully created")

# create author INDEX
conn.execute ('CREATE INDEX IF NOT EXISTS author_index ON articles (author) ')

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

sqlite_file = 'tags.db'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('tags.db', timeout=10)
print("Successfully connected")

# tags denormalization table
conn.execute('''CREATE TABLE IF NOT EXISTS tags(
tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
tag_name TEXT ) ''')
print("Table successfully created")

conn.execute('''CREATE TABLE IF NOT EXISTS tag_article_mapping (
tag_id INTEGER,
article_id INTEGER )''')

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

sqlite_file = 'comments.db'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect('comments.db', timeout=10)
print("Successfully connected")

# comments denormalization table
conn.execute('''CREATE TABLE IF NOT EXISTS comments(
comment_id INTEGER PRIMARY KEY NOT NULL,
article_id INTEGER,
comment TEXT,
username INTEGER,
display_name TEXT NOT NULL,
timestamp DATE )''')
print("Table successfully created")

# create author INDEX
conn.execute ('CREATE INDEX IF NOT EXISTS display_index ON comments (display_name) ')

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
