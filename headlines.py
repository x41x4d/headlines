from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route("/")
def get_news() -> "html":
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])

                           #article=first_article)

                           #title=first_article.get("title"), published=first_article.get("published"),
                           #summary=first_article.get("summary"))



if __name__ == '__main__':
    app.run(port=5000, debug=True)

