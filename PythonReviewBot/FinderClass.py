from requests import get
from bs4 import BeautifulSoup


class Finder:
    def link_finder(self, soup_text):
        if 'No results found.' in str(soup_text):
            return None
        else:
            for h in soup_text.findAll('h1'):
                # print(h)
                link = h.find('a')
                if link:
                    founded_link = link['href']
                    break
            return founded_link

    def information_finder(self, founded_link):
        if founded_link:
            new_req = get(founded_link)
            soup = BeautifulSoup(new_req.text, "lxml")
            y = founded_link.split('/')[4]
            y = y.split('_')
            for h in soup.findAll('p'):
                check = 1
                for t in y:
                    if t not in str(h) and t.lower() not in str(h):
                        check = 0
                        break
                if '<b>' in str(h) and check:
                    print('\n', h.text)
                    # display(HTML(str(h)))
                    break
            print('For more detail information you can go to this site:')
            print(founded_link, '\n')
        else:
            print('I\'m sorry, but i can\'t find anything for your request')

    def run(self):
        print('Hi, I\'m StarWarsBot, and I can find any information abou Star Wars for you request.')
        while True:
            print('What are you want? I understand only \'exit\' and \'find\'')
            command = input()
            if command.lower() == 'exit':
                print('Bye')
                break
            elif command.lower() == 'find':
                print('Input your request:')
                request = input()
                req = get('https://starwars.fandom.com/wiki/Special:Search?query=' + request)
                soup = BeautifulSoup(req.text, "lxml")
                founded_link = self.link_finder(soup)
                self.information_finder(founded_link)
            else:
                print('Sorry, I don\'t understand you. Repeat, please:')
