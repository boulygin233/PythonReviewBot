from telegram.ext import MessageHandler, Filters, Updater
from requests import get
from bs4 import BeautifulSoup


class DialogBot:

    def __init__(self, token):
        self.updater = Updater(token)
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)
        self.handlers = {}

    def link_finder(self, soup_text):
        if 'No results found.' in str(soup_text):
            return None
        else:
            for h in soup_text.findAll('h1'):
                link = h.find('a')
                if link:
                    founded_link = link['href']
                    return founded_link

    def information_finder(self, link):
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

    def search(self, request):
        req = get('https://starwars.fandom.com/wiki/Special:Search?query=' + request)
        soup = BeautifulSoup(req.text, "lxml")
        founded_link = self.link_finder(soup)
        return self.information_finder(founded_link)

    def handle_message(self, bot, update):
        chat_id = update.message.chat_id
        message = update.message.text
        if chat_id in self.handlers:
            if self.handlers[chat_id] == 'Not started':
                bot.sendMessage(chat_id,
                                'Hi, I\'m <b>StarWarsBot</b>, and I can find any'
                                'information about Star Wars for you request.',
                                'HTML')
                bot.sendMessage(chat_id, 'What are you want? I understand only <b>\'exit\'</b> and <b>\'find\'</b>',
                                'HTML')
                self.handlers[chat_id] = 'Waiting for command'
            elif self.handlers[chat_id] == 'Waiting for command':
                if message.lower() == 'exit':
                    bot.sendMessage(chat_id, 'Goodbye. May the force be with you!')
                    self.handlers[chat_id] = 'Not started'
                elif message.lower() == 'find':
                    bot.sendMessage(chat_id, 'Input your request:')
                    self.handlers[chat_id] = 'Waiting for request'
                else:
                    bot.sendMessage(chat_id, 'Sorry, I don\'t understand you.')
            elif self.handlers[chat_id] == 'Waiting for request':
                information = self.search(message)
                bot.sendMessage(chat_id, information, 'HTML')
                bot.sendMessage(chat_id,
                                'What are you want? I understand only <b>\'exit\'</b> and <b>\'find\'</b>',
                                'HTML')
                self.handlers[chat_id] = 'Waiting for command'
        else:
            self.handlers[chat_id] = 'Not started'
            bot.sendMessage(chat_id,
                            'Hi, I\'m <b>StarWarsBot</b>, and I can find any'
                            'information about Star Wars for you request.',
                            'HTML')
            bot.sendMessage(chat_id, 'What are you want? I understand only <b>\'exit\'</b> and <b>\'find\'</b>',
                            'HTML')
            self.handlers[chat_id] = 'Waiting for command'

    def run(self):
        self.updater.start_polling()
