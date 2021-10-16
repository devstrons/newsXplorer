from flask import Flask, render_template, url_for
import requests
from pprint import pprint as p

app = Flask(__name__)


@app.route("/news/<category>")
def news_page(category):
    url = f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/in.json"
    articles = requests.get(url).json()["articles"]
    data = make_posts(articles)
    return render_template("new.html", data=data, title=articles[0]["title"])


@app.route("/")
@app.route("/home")
def home():
    url = f"https://saurav.tech/NewsAPI/top-headlines/category/general/in.json"
    articles = requests.get(url).json()["articles"]
    data = make_posts(articles)
    return render_template("home.html", data=data, title="General news")


def make_posts(articles: list) -> list:
    data = []

    for article in articles[2:6]:
        post = {}
        post["title"] = article["title"]
        post["description"] = article["description"]
        post["sourceName"] = article["source"]
        post["imgUrl"] = article["urlToImage"]
        post["sourceUrl"] = article["url"]
        post["time"] = article["publishedAt"]
        if "youtube" in post["sourceName"]["name"].lower():
            post["youtube"] = f"https:/youtube.com/embed/{post['sourceUrl'].split('=')[-1]}"
        data.append(post)
    return data


if __name__ == "__main__":
    # app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
    app.run(debug=True)
