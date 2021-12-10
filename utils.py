import json
import requests
import httpx
import asyncio
from pprint import pprint

story_url = "https://hacker-news.firebaseio.com/v0/item/"
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
n_hacker_posts = 14


def make_news_posts(articles: list) -> list:
    data = []

    for article in articles:
        pprint(article)
        post = {}
        try:
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
        except TypeError as e:
            pprint(e)
            print("*"*32)
        data.append(post)
    return data


async def get_news(category="general"):
    url = f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/in.json"
    articles = httpx.get(url).json()["articles"][:3]
    pprint(articles)
    data = make_news_posts(articles)
    return data


# make urls
def make_hacker_urls(story_ids: list[str]) -> str:
    for story_id in story_ids:
        yield f"{story_url}{story_id}.json"


def get_hacker_ids(stories_n) -> list[str]:
    story_ids = httpx.get(top_stories_url).json()
    return story_ids[:stories_n]


# get story data
def get_hacker_post(story_url) -> dict:
    data = httpx.get(story_url).json()
    return data


async def get_hacker_news() -> list[dict]:
    hacker_posts = []
    hacker_ids = get_hacker_ids(n_hacker_posts)
    # for url in make_hacker_urls(hacker_ids):
    #     hacker_posts.append(get_hacker_post(url))
    async with httpx.AsyncClient() as client:
        tasks = (client.get(url) for url in make_hacker_urls(hacker_ids))
        reqs = await asyncio.gather(*tasks)

    hacker_posts = [req.json() for req in reqs]
    return hacker_posts
