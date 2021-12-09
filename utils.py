import json
import requests

story_url = "https://hacker-news.firebaseio.com/v0/item/"
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
n_hacker_posts = 14


def make_news_posts(articles: list) -> list:
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


def get_news(category="general"):
    url = f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/in.json"
    articles = requests.get(url).json()["articles"]
    data = make_news_posts(articles)
    return data


# make urls
def make_hacker_urls(story_ids: list[str]) -> str:
    for story_id in story_ids:
        yield f"{story_url}{story_id}.json"


def get_hacker_ids(stories_n) -> list[str]:
    story_ids = requests.get(top_stories_url).json()
    return story_ids[:stories_n]


# get story data
def get_hacker_post(story_url) -> dict:
    data = requests.get(story_url).json()
    return data


def get_hacker_news() -> list[dict]:
    hacker_posts = []
    hacker_ids = get_hacker_ids(n_hacker_posts)
    for url in make_hacker_urls(hacker_ids):
        hacker_posts.append(get_hacker_post(url))
    return hacker_posts
