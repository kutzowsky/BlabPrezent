#!/usr/bin/env python

import pickle
import time
import logging

from wwwparsing import BlabWebsiteClient
from config import configreader
from messaging import messagehandler


class WebsiteParsingBot:
    def __init__(self):
        self.website_client = BlabWebsiteClient()
        self.username = ''
        self.logger = logging.getLogger()
        self.latest_message_file_name = 'latest_message.p'

    def login(self, username, password):
        self.username = username
        self.website_client.login(username, password)

    def mark_last_message_as_latest(self):
        messages = self.website_client.get_secretary_messages()
        messages_to_bot = list(filter(lambda message: not message['text'].startswith(self.username), messages))
        latest_message = messages_to_bot[0]
        pickle.dump(latest_message, open(self.latest_message_file_name, 'wb'))

    def start_listening(self, sleep_seconds=60.0):
        self.logger.info(f'Listening started. Sleep timeout set to: {sleep_seconds}s')

        while True:
            try:
                self._handle_new_messages()
            except KeyboardInterrupt:
                break
            except Exception as exc:
                self.logger.error(f'Error occurred. Waiting {sleep_seconds}s before retry.', exc)
            finally:
                time.sleep(sleep_seconds)

    def _send_message(self, message_text):
        self.website_client.send_message(message_text)

    def _get_new_messages(self):
        previous_latest_message = pickle.load(open(self.latest_message_file_name, 'rb'))

        messages_to_bot = self._get_messages_newer_than(previous_latest_message)

        if not messages_to_bot:
            self.logger.info('No new messages')
            return []

        self.logger.info(f'New messages: {len(messages_to_bot)}')

        latest_message = messages_to_bot[0]
        pickle.dump(latest_message, open(self.latest_message_file_name, "wb"))

        return messages_to_bot

    def _get_messages_newer_than(self, given_message):
        page = 1
        messages = []
        while given_message not in messages:
            messages += self.website_client.get_secretary_messages(page)
            page += 1

            if page > 10:
                raise Exception('To many pages back. Something wrong happened!')

        messages_to_bot = list(filter(lambda message: not message['text'].startswith(self.username), messages))
        given_message_index = messages_to_bot.index(given_message)

        return messages_to_bot[:given_message_index]

    def _handle_new_messages(self):
        new_messages = self._get_new_messages()

        for message in new_messages:
            full_text = message['text']
            self.logger.debug(f'Got message:  {full_text}')

            answer = messagehandler.handle(full_text)
            if answer is not None:
                self.logger.debug(f'Sending answer:  {answer}')
                self._send_message(answer)

            time.sleep(1)   # small delay just in case to keep message spam protection happy


def _set_logger():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('bot.log')
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


if __name__ == '__main__':
    _set_logger()

    logger.info('Started')

    bot_configuration = configreader.get_bot_configuration()

    bot = WebsiteParsingBot()
    bot.login(bot_configuration.website_login, bot_configuration.website_password)

    # bot.mark_last_message_as_latest()

    bot.start_listening()

