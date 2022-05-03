import os
from flask import Flask, render_template, request
import requests
from sawo import createTemplate, verifyToken
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
# using flask = True generates flask template
    
load = ''
loaded = 0

def setPayload(payload):
    global load
    load = payload

def setLoaded(reset=False):
    global loaded
    if reset:
        loaded = 0
    else:
        loaded += 1

createTemplate("./templates/partials",flask=True)

story_url = "https://hacker-news.firebaseio.com/v0/item/"
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
stories_n = 2


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

@app.route("/login")
def login_page():
    setLoaded()
    setPayload(load if loaded<2 else '')
    sawo = {
        "auth_key": API_KEY,
        "to": "login",
        "identifier": "email"
    }
    return render_template("login.html", sawo=sawo, load=load)


@app.route("/login", methods=["POST", "GET"])
def login():
    payload = json.loads(request.data)["payload"]
    setLoaded(True)
    setPayload(payload)
    status = 200 if(verifyToken(payload)) else 404
    return {"status": status}


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
            post[
                "youtube"
            ] = f"https:/youtube.com/embed/{post['sourceUrl'].split('=')[-1]}"
        data.append(post)
    return data


def get_news_url(category="general"):
    return f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/in.json"


def get_posts(url):
    articles = requests.get(url).json()["articles"]
    data = make_posts(articles)
    return data


# make urls
def make_urls(story_ids: list[str]) -> str:
    for story_id in story_ids:
        url = f"{story_url}{story_id}.json"
        yield url


def get_hacker_ids(stories_n) -> list[str]:
    story_ids = requests.get(top_stories_url).json()
    return story_ids[:stories_n]


# get story data
def get_story(story_url) -> dict:
    data = requests.get(story_url).json()
    return data


def get_hacker_posts() -> list[dict]:
    hacker_posts = []
    hacker_ids = get_hacker_ids(stories_n)
    for url in make_urls(hacker_ids):
        hacker_posts.append(get_story(url))
    return hacker_posts


if __name__ == "__main__":
    # app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
    app.run(debug=True)
