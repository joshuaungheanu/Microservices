DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Article;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Comment;

CREATE TABLE USERS (
    email TEXT PRIMARY KEY UNIQUE,
    name TEXT,
    password TEXT,
    createTime DATETIME,
    updateTime DATETIME)
);

CREATE TABLE Article (
  article_nameid INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  email TEXT NOT NULL,
  article_url TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updateTime DATETIME,
  FOREIGN KEY (id) REFERENCES Article(id)
);

CREATE TABLE Tag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_name VARCHAR NOT NULL,
  article_url TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updateTime DATETIME,
  UNIQUE(tag,article_url),
  FOREIGN KEY (id) REFERENCES Article(id)
);

CREATE TABLE Comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  article_id INTEGER NOT NULL,
  author, TEXT NOT NULL DEFAULT 'John Doe',
  comment VARCHAR NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updateTime DATETIME,
  FOREIGN KEY (article_id) REFERENCES Article(id)
);

INSERT INTO Tag (tag, article_url)
VALUES ('me', (SELECT article_url FROM Article WHERE title = 'Allo About Me')),
('story', (SELECT article_url FROM Article WHERE title = 'Title 2')),
('random', (SELECT article_url FROM Article WHERE title = 'Title 2'));

INSERT INTO Comment (comment, article_id, author)
VALUES ('Article 1', (SELECT artId FROM Article WHERE title = 'Author'), 'default'),
('Comment about article', (SELECT article_id FROM Article WHERE title = 'Article Title 1'), 'default'),
('Comment about article', (SELECT article_id FROM Article WHERE title = 'Article Title 2'), 'default'),
('Comment about article', (SELECT article_id FROM Article WHERE title = 'Article Title 3'), 'default');
