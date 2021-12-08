import json
import requests

story_url = "https://hacker-news.firebaseio.com/v0/item/"
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
stories_n = 14


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


def get_hacker_news() -> list[dict]:
    hacker_posts = []
    hacker_ids = get_hacker_ids(stories_n)
    for url in make_urls(hacker_ids):
        hacker_posts.append(get_story(url))
    return hacker_posts


def get_news(category="general"):
    url = get_news_url(category)
    return get_posts(url)