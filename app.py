import re, requests
from datetime import datetime, timedelta  
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def get_article_summaries(keywords, top=None):

    print('')
    print(f'SEARCH FOR: {keywords}')
    # Get the news articles from the last 7 days
    after = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = "https://www.google.com/search?q=" + keywords + " after:" + after

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    url = 'https://www.google.com' + soup.find_all("a")[2].attrs['href']
    i = 0
    end = 3 if top else 1
    while i < end and url:
        i += 1
        [matching_articles, url] = get_articles(url, top)

        # Loop through the matching articles, summarize, and print them
        for article in matching_articles:
            article['summary'] = get_summary(article['url'])
            print_article(article)

def get_articles(url, top):
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
        result = get_article(article)
        matching_articles.append(result)

    all_a = soup.find_all("a")
    next = list(filter(lambda x: x.text == 'Next >' or x.text == '>', all_a))
    if next:
        next_tag = next.pop()
        url = 'https://www.google.com' + next_tag.attrs['href']
    else:
        url = None

    return [matching_articles, url]

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

def get_summary(url):
    summary_url = 'https://smmry.com/sm_portal.php?&SM_TOKEN=4208879900&SM_POST_SAVE=0&SM_REDUCTION=-1&SM_CHARACTER=-1&SM_LENGTH=5&SM_URL=' + url
    res = str(requests.get(summary_url).content)
    res = re.sub(r'\[SM_a\]', "<span id=\"sm_flash_", res)
    res = re.sub(r'\[SM_b\]', "\" onclick=\"sm_flash_process('", res)
    res = re.sub(r'\[SM_c\]', "', this,", res)
    res = re.sub(r'\[SM_d\]', ")\" onmouseover=\"sm_flash_add('", res)
    res = re.sub(r'\[SM_e\]', "', this, ", res)
    res = re.sub(r'\[SM_f\]', ");\" onmouseout=\"sm_flash_remove('", res)
    res = re.sub(r'\[SM_g\]', ");\">", res)
    res = re.sub(r'\[SM_h\]', "</span>", res)
    res = re.sub(r'\[SM_i\]', "<span style=\"background-color:", res)
    res = re.sub(r'\[SM_j\]', "rgb(255, ", res)
    res = re.sub(r'\[SM_k\]', ", 0)\"> ", res)
    res = re.sub(r'\[SM_l\]', "<br><br>", res)
    res = re.sub(r'\[SM_m\]', "<sm_break><sm_break>", res)
    res = re.sub(r'\[SM_n\]', "rgb(75, ", res)
    res = res.split('SM_DIVIDE')[3]
    summary_soup = BeautifulSoup(res, "html.parser")
    summary_text = summary_soup.text
    return summary_text

def print_article(article):
    print("")
    print("Title:", f'[{article["date"]}] {article["title"]}')
    print("Text:", article['text'].replace(article['title'], ''))
    print("URL:", article['url'])
    print("SUMMARY:", article['summary'])

get_article_summaries('"Brian Green"', 3)
get_article_summaries('"Mark Graves"', 3)
get_article_summaries('"Jason Thacker"', 3)
get_article_summaries('"Michael Sacasas"', 3)
get_article_summaries('"Nicoleta Acatrinei"', 3)
get_article_summaries('"Gretchen Huizinga"', 3)
get_article_summaries('"Mois Navon"', 3)
get_article_summaries('"Michael Paulus"', 3)
get_article_summaries('"Cory Labrecque"', 3)
get_article_summaries('"Elias Kruger"', 3)
get_article_summaries('"Trish Shaw"', 3)
get_article_summaries('"Joanna Ng"', 3)
get_article_summaries('moral impact of "generative AI"')