import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    # PUT YOUR CODE HERE
    html = parser.table.findAll("table")[1].findAll("tr")
    for i in range(0, len(html), 3):
        try:
            current_news = {
                "title": html[i].findAll("a")[1].string,
                "author": html[i + 1].find("a").string,
                "url": html[i].findAll("a")[1].get("href"),
                "points": int(html[i + 1].findAll("span")[1].string.split()[0]),
                "comments": html[i + 1].findAll("a")[-1].string.split()[0],
            }
            news_list.append(current_news)
        except IndexError:
            continue
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    url = parser.table.findAll("table")[1].findAll("tr")[-1].contents[2].find("a").get("href")
    return url
    # PUT YOUR CODE HERE


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

