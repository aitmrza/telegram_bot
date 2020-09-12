import requests
from bottle import Bottle, response, request as bottle_request

from secret_token import token


class BotHandlerMixin:
    BOT_URL = None

    def get_chat_id(self, data):
        """Метод извлечения chat_id из запроса telegram бота"""
        chat_id = data['message']['chat']['id']
        return chat_id

    def get_message(self, data):
        """Метод извлечения message_id из запроса telegram бота"""
        message_text = data['message']['text']
        return message_text

    def send_message(self, prepared_data):
        """Подготовленные данные должны быть в формате json, которые включают как минимум chat_id и text."""
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):
    BOT_URL = f'https://api.telegram.org/bot{token}/'

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method='POST')

    def change_text_message(self, text):
        """Метод переворота текста сообщения"""
        return text[::-1]

    def prepare_data_for_answer(self, data):
        message = self.get_message(data)
        answer = self.change_text_message(message)
        chat_id = self.get_chat_id(data)
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }
        return json_data

    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)
        return response


if __name__ == '__main__':
    app = TelegramBot()
    app.run(host='localhost', port=8090)
