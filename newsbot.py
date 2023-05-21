from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from summarize import summarizeURL


excluded = ['linkedin','tiktok','theknot']

class Newsbot(object):

    @staticmethod
    def article_search(keyword_searches):
        results = ''
        if isinstance(keyword_searches, list):
            for keywords, top in keyword_searches:
                results += Newsbot.get_article_summaries(keywords, top)
        else:
            keywords, top = keyword_searches
            results += Newsbot.get_article_summaries(keywords, top)
        return results

    @staticmethod
    def get_article_summaries(keywords, top=None):
        results = ''
        print('')
        print(f'SEARCH FOR: {" ".join(keywords)}')
        # Get the news articles from the last 7 days
        after = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = "https://www.google.com/search?q=" + " ".join(keywords).replace('_','"') + " after:" + after

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        url = 'https://www.google.com' + soup.find_all("a")[2].attrs['href']
        i = 0
        end = 1 if top else 2
        while i < end and url:
            i += 1
            [matching_articles, url] = Newsbot.get_articles(url, top)
            # Loop through the matching articles, summarize, and print them
            for article in matching_articles:
                is_excluded = list(filter(lambda x: x in article['url'], excluded))
                if len(is_excluded):
                    continue
                if not Newsbot.is_article_keyword_match(article['url'], keywords):
                    continue
                article['summary'] = ''
                # summary = summarizeURL(article['url'], 5)
                # if 'sm_api_content' in summary:
                #     article['summary'] = summary['sm_api_content']
                results += Newsbot.print_article(article)
        return results

    @staticmethod
    def is_article_keyword_match(url, keywords):
        response = requests.get(url).text
        match = False
        for word in keywords:
            if '_' in word:
                is_match = word.replace('_', '') in response
            else:
                is_match = word.replace('"', '').lower() in response.lower()
            is_required = '"' in word
            if is_required:
                match = match and is_match
            else:
                match = match or is_match
        return match

    @staticmethod
    def get_articles(url, top=10):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the news articles on the page
        articles = soup.find_all("h3")
        # Create a list to store the matching articles
        matching_articles = []

        # Loop through the articles
        num_of_articles = len(articles) if top and top > len(articles) else top
        articles_to_get = articles[:num_of_articles] if top else articles
        for article in articles_to_get:
            result = Newsbot.get_article(article)
            matching_articles.append(result)

        all_a = soup.find_all("a")
        next = list(filter(lambda x: x.text == 'Next >' or x.text == '>', all_a))
        if next:
            next_tag = next.pop()
            url = 'https://www.google.com' + next_tag.attrs['href']
        else:
            url = None

        return [matching_articles, url]

    @staticmethod
    def get_article(article):
        title = article.text
        parent = article.parent
        link = None
        text = None
        while parent and link is None:
            if parent.name == 'a':
                parsed_url = urlparse(parent.attrs['href'])
                link = parse_qs(parsed_url.query)['q'][0]
                text = parent.text
                date = text.split('.')[-1]
            parent = parent.parent
        return {'title': title, 'date': date, 'url': link, 'text': text}

    @staticmethod
    def print_article(article):
        article_text = '\n' + \
            f'Title: [{article["date"]}] {article["title"]}' + '\n' + \
            f'Text: {article["text"].replace(article["title"], "")}' + '\n' + \
            f'URL: {article["url"]}]' + '\n'
        if article['summary']:
            article_text = "SUMMARY:", article['summary'] + '\n'
        for line in article_text.split('\n'):
            print(line)
        return article_text
