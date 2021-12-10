import json
from pathlib import Path
import httpx
import asyncio
import time
from typing import Generator

story_url = "https://hacker-news.firebaseio.com/v0/item/"
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
max_hacker_posts = 14
max_news_posts = 10


def make_news_posts(articles: dict) -> list:
    data = []

    for article in articles:
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


async def get_news(category: str = "general") -> list[dict]:
    if news_cache_exists(category):
        return news_cache_load(category)
    else:
        url = f"https://saurav.tech/NewsAPI/top-headlines/category/{category}/in.json"
        async with httpx.AsyncClient() as client:
            tasks = client.get(url)
            reqs = await asyncio.gather(tasks)
        articles = reqs[0].json()["articles"][:max_news_posts]
        data = make_news_posts(articles)
        news_cache_make(data, category)
    return data


def is_news_recent(cache: Path):
    recent = (time.time() - cache.stat().st_mtime) / 60 < 4
    return recent


def news_cache_make(sd: list[dict], category: str):
    with open(f"news_{category}.json", "w") as fp:
        json.dump(sd, fp)


def news_cache_load(category: str) -> list[dict]:
    with open(f"news_{category}.json", "r") as fp:
        data = json.load(fp)
        return data


def news_cache_exists(category: str) -> bool:
    cache = Path(f"news_{category}.json")
    if cache.exists() and is_news_recent(cache):
        return True
    return False


# make urls
def make_hacker_urls(story_ids: list[str]) -> Generator[str, None, None]:
    for story_id in story_ids:
        yield f"{story_url}{story_id}.json"

    return None


def get_hacker_ids(stories_n: int) -> list[str]:
    story_ids = httpx.get(top_stories_url).json()
    return story_ids[:stories_n]


# get story data
def get_hacker_post(story_url) -> dict:
    data = httpx.get(story_url).json()
    return data


async def get_hacker_news() -> list[dict]:
    if hacker_cache_exists():
        return hacker_cache_load()
    else:
        hacker_posts = []
        hacker_ids = get_hacker_ids(max_hacker_posts)
        async with httpx.AsyncClient() as client:
            tasks = (client.get(url) for url in make_hacker_urls(hacker_ids))
            reqs = await asyncio.gather(*tasks)

        hacker_posts = [req.json() for req in reqs]
        hacker_cache_make(hacker_posts)
    return hacker_posts


def is_hacker_recent(cache: Path):
    recent = (time.time() - cache.stat().st_mtime) / 60 < 4
    return recent


def hacker_cache_make(sd: list[dict]):
    with open("hacker_cache.json", "w") as fp:
        json.dump(sd, fp)


def hacker_cache_load() -> list[dict]:
    with open("hacker_cache.json", "r") as fp:
        data = json.load(fp)
        return data


def hacker_cache_exists() -> bool:
    cache = Path("hacker_cache.json")
    if cache.exists() and is_hacker_recent(cache):
        return True
    return False
