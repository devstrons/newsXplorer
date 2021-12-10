import os
from quart import Quart, render_template, url_for
from utils import get_hacker_news, get_news

app = Quart(__name__)


@app.route("/news/<category>")
async def news_page(category):
    data = await get_news(category)
    hacker_posts = await get_hacker_news()
    return await render_template(
        "new.html",
        data=data,
        title=data[0]["title"],
        hacker_posts=hacker_posts,
    )


@app.route("/")
@app.route("/home")
async def home():
    data = await get_news()
    hacker_posts = await get_hacker_news()
    return await render_template(
        "new.html",
        data=data,
        title="General news",
        hacker_posts=hacker_posts,
    )


if __name__ == "__main__":
    # app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
    app.run(debug=True, port=os.environ["PORT"], host="0.0.0.0")
