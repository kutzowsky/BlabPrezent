#!/usr/bin/env python

import pickle
import time
import logging
import os.path

from src.wwwparsing import BlabWebsiteClient
from src.config import settings
from src.messaging import MessageHandler


class WebsiteParsingBot:
    def __init__(self):
        self.website_client = BlabWebsiteClient()
        self.username = ''
        self.logger = logging.getLogger()
        self.checkpoint_file_path = 'message_checkpoint.pickle'
        self.message_handler = MessageHandler(settings.General.participant_list_open)

    def login(self, username, password):
        self.username = username
        self.website_client.login(username, password)

    def try_create_latest_message_file(self):
        if not os.path.exists(self.checkpoint_file_path):
            logging.info(f"{self.checkpoint_file_path} does not exist. Creating.")

            messages = self.website_client.get_secretary_messages()
            messages_to_bot = list(filter(lambda message: not message['text'].startswith(self.username), messages))
            latest_message = messages_to_bot[0]
            pickle.dump(latest_message, open(self.checkpoint_file_path, 'wb'))

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
        previous_latest_message = pickle.load(open(self.checkpoint_file_path, 'rb'))

        messages_to_bot = self._get_messages_newer_than(previous_latest_message)

        if not messages_to_bot:
            self.logger.info('No new messages')
            return []

        self.logger.info(f'New messages: {len(messages_to_bot)}')

        latest_message = messages_to_bot[0]
        pickle.dump(latest_message, open(self.checkpoint_file_path, "wb"))

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

            answers = self.message_handler.handle(full_text)
            if answers:
                for answer in answers:
                    self.logger.debug(f'Sending answer:  {answer}')
                    self._send_message(answer)
                    time.sleep(1)  # small delay just in case to keep message spam protection happy
