from requests import get
from bs4 import BeautifulSoup


def link_finder(soup_text):
    if 'No results found.' in str(soup_text):
        return None
    else:
        for h in soup_text.findAll('h1'):
            link = h.find('a')
            if link:
                founded_link = link['href']
                return founded_link


def information_finder(link):
    if link:
        new_req = get(link)
        soup = BeautifulSoup(new_req.text, "lxml")
        found_article = link.split('/')[4]
        found_article = found_article.split('_')
        for paragraph in soup.findAll('p'):
            check_for_paragraph = 1
            for word in found_article:
                if word not in str(paragraph) and word.lower() not in str(paragraph):
                    check_for_paragraph = 0
                    break
            if '<b>' in str(paragraph) and check_for_paragraph:
                ret_text = str(paragraph)[3:len(str(paragraph)) - 4] + \
                           '\n\n' + 'For more detail information you can go to this site:\n' + link
                return ret_text

    else:
        return 'I\'m sorry, but i can\'t find anything for your request'


def search(request):
    req = get('https://starwars.fandom.com/wiki/Special:Search?query=' + request)
    soup = BeautifulSoup(req.text, "lxml")
    founded_link = link_finder(soup)
    return information_finder(founded_link)
