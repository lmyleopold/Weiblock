from time import sleep

from weibo_requests import WeiboRequest
from spider import get_keyword, add_reposts


COOKIES_FILE = "../cookies.txt"
MAX_TRY = 10

if __name__ == "__main__":
    cookies = []
    with open(COOKIES_FILE) as f:
        cookies.append(f.readline())

    # Get all posts from a keyword

    wrequest = WeiboRequest(cookies, max_try=MAX_TRY)
    # messages = get_keyword("那些被疫情偷走的时光", wrequest, start_page=1, end_page=20, save=True, repost_pages=10)
    add_reposts(wrequest, 4, repost_pages=20)
