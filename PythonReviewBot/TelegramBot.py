from telegram.ext import MessageHandler, Filters, Updater
from SearchFunctions import *


class DialogBot:

    def __init__(self, token):
        self.updater = Updater(token)
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)
        self.handlers = {}

    def run(self):
        self.updater.start_polling()

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
                information = search(message)
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

