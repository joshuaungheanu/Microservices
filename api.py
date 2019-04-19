from flask import jsonify
import requests
import pprint
import datetime
from rfeed import *



class Slash(Extension):
    def get_namespace(self):
        return {"xmlns:slash" : "http://purl.org/rss/1.0/modules/slash/"}

class SlashItem(Serializable):
    def __init__(self, content):
        Serializable.__init__(self)
        self.comments = content

    def publish(self, handler):
        Serializable.publish(self, handler)
        self._write_element("slash:comments", self.comments)



from flask import Flask
app = Flask(__name__)
@app.route('/metarticle')
def metarticle():

    r = requests.get('http://127.0.0.1:5200/articles/metadata')
    # r = requests.get('http://127.0.0.1/article?metadata=10')    #no server number when load balancer is used

    arr=r.json()

    item1=[]
    for i in range(0, 10):
        date_time_str = str(arr[i][2])
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

        item = Item(
            title = arr[i][0],
            author = arr[i][1],
            pubDate= date_time_obj,
            link=arr[i][3])
        item1.append(item)

    feed = Feed(
        title = "Latest 10 article",
        link = "http://www.example.com/rss",
        description = "This feed returns a summary feed listing the title, author, date, and link for the 10 most recent articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = item1)

    return (feed.rss())

@app.route('/comments/<article_id>')
def comments(article_id):

    r = requests.get('http://127.0.0.1:5100/comment/'+article_id)

    arr=r.json()

    item1=[]
    for i in range(0, 10):
        item = Item(
            title = arr[i][0],
            comments = arr[i][0],
            pubDate= datetime.datetime.now(),
            )
        item1.append(item)

    feed = Feed(
        title = "Top comments for article",
        link = "http://www.example.com/rss",
        description = "Top comments for article",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = item1)

    return (feed.rss())


@app.route('/fullfeed/<article_id>')
def fullfeed(article_id):

    r = requests.get('http://127.0.0.1:5200/articles?article_id='+article_id)
    re=r.json()

    r = requests.get('http://127.0.0.1:5300/tags/'+article_id)
    tag=r.json()
    l=len(tag)
    cat=[]

    r = requests.get('http://127.0.0.1:5100/comment?article_id='+article_id)
    comment_count=r.json()


    item1=[]
    date_time_str = str(re[4])
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    for i in range(0,l):
        ca=tag[i]
        cat.append((' '.join(ca)))


    item = Item(
        title = re[1],
        author = re[2],
        description = re[3],
        pubDate= date_time_obj,
        link=re[6],
        extensions = [SlashItem(comment_count)])
    item1.append(item)

    feed = Feed(
        title = "Full Feed Article",
        link = "http://www.example.com/rss",
        description = "A full feed containing the full text for each article, its tags as RSS categories, and a comment count",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        extensions = [Slash()],
        items = item1)

    return (feed.rss())
