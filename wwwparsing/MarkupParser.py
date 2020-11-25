import datetime


class MarkupParser:
    @staticmethod
    def get_message_html_elements(page_html):
        message_div_style = 'margin: 2px; border: 1px solid #BBB; border-radius: 3px; padding: 1px; margin-bottom: ' \
                            '7px; background-color: #fefefe; '
        return page_html.find_all('div', style=message_div_style)

    @staticmethod
    def get_message_people(html_element):
        people_element_style = 'font-size: 14pt; color: #999; padding-bottom: 3px;'
        people_element = html_element.find('div', style=people_element_style)

        if not people_element:
            return ''

        return people_element.text.strip().replace('»', '>>')

    @staticmethod
    def get_message_text(html_element):
        message_text_element_style = 'font-size: 12pt;'
        message_text_element = html_element.find('span', style=message_text_element_style)

        if not message_text_element:
            return ''

        return message_text_element.text.strip()

    @staticmethod
    def get_message_timestamp(html_element):
        timestamp_element = html_element.find('a', href=lambda href: href and ('/pm/' in href or '/dm/' in href))

        if not timestamp_element:
            return ''

        timestamp_text = timestamp_element.text.strip()
        timestamp_datetime = datetime.datetime.strptime(timestamp_text, '%Y/%m/%d %H:%M:%S')  # 2020/11/19 23:50:19

        return timestamp_datetime
