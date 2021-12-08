import os
from flask import Flask, render_template, url_for
from utils import get_news_url, get_posts, get_hacker_posts
from pprint import pprint as p

app = Flask(__name__)


@app.route("/news/<category>")
def news_page(category):
    url = get_news_url(category)
    data = get_posts(url)
    hacker_posts = get_hacker_posts()
    
    return render_template(
        "new.html",
        data=data,
        title=data[0]["title"],
        hacker_posts=hacker_posts,
    )


@app.route("/")
@app.route("/home")
def home():
    url = get_news_url()
    data = get_posts(url)
    hacker_posts = get_hacker_posts()
    return render_template(
        "new.html",
        data=data,
        title="General news",
        hacker_posts=hacker_posts,
    )


if __name__ == "__main__":
    # app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
    app.run(debug=True, port=os.environ['PORT'],host='0.0.0.0')
