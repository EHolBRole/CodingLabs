import string

from bottle import (
    route, run, template, request, redirect
)

import nltk
import sqlalchemy.exc
from scraputils import get_news
from db import News, session, fill
from bayes import NaiveBayesClassifier


def prepare(s):
    translator = str.maketrans("", "", string.punctuation)
    s = s.translate(translator)
    tokens = nltk.word_tokenize(s)
    return tokens


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    s = session()
    label = request.GET.get("label", None)
    id = request.GET.get("id", None)
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.add(row)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    s = session()
    recent_news = get_news(url="https://news.ycombinator.com/newest", n_pages=1)
    authors = [news["author"] for news in recent_news]
    titles = s.query(News.title).filter(News.author.in_(authors)).subquery()
    existing_news = s.query(News).filter(News.title.in_(titles)).all()
    for news in recent_news:
        if not existing_news or news not in existing_news:
            fill(news)
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    s = session()
    labeled = s.query(News).filter(News.label != None).all()
    x = [row.title for row in labeled]
    y = [row.label for row in labeled]
    x = [prepare(title) for title in x]
    x_train, y_train = x[: round(len(labeled) * 0.7)], y[: round(len(labeled) * 0.7)]
    x_test, y_test = x[round(len(labeled) * 0.7) :], y[round(len(labeled) * 0.7) :]
    model = NaiveBayesClassifier(1)
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))
    unlabeled = s.query(News).filter(News.label == None).all()
    x_class = [prepare(row.title) for row in unlabeled]
    predictions = model.predict(x_class)
    classified_news = []
    second_priority = []
    third_priority = []
    for i, row in enumerate(unlabeled):
        if predictions[i] == "good":
            classified_news.append(row)
        elif predictions[i] == "maybe":
            second_priority.append(row)
        else:
            third_priority.append(row)
    classified_news.extend(second_priority)
    classified_news.extend(third_priority)
    return template('news_template', rows=classified_news)


@route("/recommendations")
def recommendations():
    s = session()
    news = s.query(News).filter().all()
    X = [i.title for i in news]
    b = NaiveBayesClassifier(1)
    y = b.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return template('news_template', rows=news)


@route("/")
def root():
    redirect('/news')


if __name__ == "__main__":
    run(host="localhost", port=8080)

