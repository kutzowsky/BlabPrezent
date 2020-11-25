import mechanicalsoup

from .MarkupParser import MarkupParser


class BlabWebsiteClient:
    def __init__(self, base_url='https://blabler.pl', markup_parser=MarkupParser()):
        self.base_url = base_url

        self.browser = None
        self.markup_parser = markup_parser

        self.username = ''
        self.password = ''

    def login(self, username, password):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.username = username
        self.password = password

        self.browser.open(f'{self.base_url}/logowanie.html')

        self.browser.select_form(nr=0)
        self.browser['name'] = username
        self.browser['pass'] = password

        response = self.browser.submit_selected()
        if response.status_code != 200:
            self.browser = None
            raise Exception(f'Login error. HTTP response status code: {response.status_code}')

    def send_message(self, message_text):
        self._check_login()

        self.browser.open(f'{self.base_url}/dash/{self.username}.html')

        self.browser.select_form(nr=0)
        self.browser['text'] = message_text
        self.browser.submit_selected()

    def get_secretary_messages(self, page_number=1):
        self._check_login()

        page = self.browser.open(f'{self.base_url}/sekretarz.html?pg={page_number}')
        page_soup = page.soup
        message_html_elements = self.markup_parser.get_message_html_elements(page_soup)

        messages = [self._get_message_from(html_element) for html_element in message_html_elements]
        non_empty_messages = filter(lambda message: message != {}, messages)
        return list(non_empty_messages)

    def _get_message_from(self, html_element):
        people = self.markup_parser.get_message_people(html_element)

        if not people:  # system messages are not supported
            return {}

        text = self.markup_parser.get_message_text(html_element)
        timestamp = self.markup_parser.get_message_timestamp(html_element)

        message = {'text': f'{people} {text}',
                   'timestamp': timestamp}

        return message

    def _check_login(self):
        if not self.browser:
            raise Exception('Please log in first')
