from flask import Flask, render_template
import feedparser

app = Flask(__name__)

FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(FEEDS[publication])
    first_article = feed['entries'][0]
    return render_template("home.html", articles=feed['entries'])

                           #article=first_article)

                           #title=first_article.get("title"), published=first_article.get("published"),
                           #summary=first_article.get("summary"))



if __name__ == '__main__':
    app.run(port=5000, debug=True)

