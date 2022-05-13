# Native
import os
import re
from contextlib import suppress
from requests import get as get_http_code
from requests.exceptions import RequestException
# Third-Party
from prettyconf import Configuration
from prettyconf.loaders import Environment, EnvFile

project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
#TODO: fix slashes with proper pathing
env_file = f"{project_path}/config/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])


class Question:
    def __init__(self, question_json):
        # text with html links separated out
        scrubbed_text = Question.separate_html(question_json['question'])
        self.text = ''
        self.valid_links = []
        if type(scrubbed_text) == str:
            self.text = scrubbed_text
        # if there are valid html links included in question text
        elif type(scrubbed_text) == list:
            self.text = scrubbed_text[0]
            self.valid_links = scrubbed_text[1:]
        self.value = question_json['value']
        self.category = question_json['category']
        self.answer = question_json['answer']
        self.date = question_json['air_date']

    @staticmethod
    def separate_html(question_text):
        """
        separates html links from questions. returns a tuple of the question text and link if link is valid,
        otherwise just returns the text
        """
        with suppress(RequestException):
            # scrub newline chars from question text
            question_text = re.sub(r'\n', '', question_text)
            # valid links to return
            valid_links = []
            # use regex to check in case link syntax got mangled
            regex_links = re.findall(r'http://.*?\"', question_text)
            # remove trailing quotes
            regex_links = [link[:-1] for link in regex_links]
            # scrub out html from question
            question_text = re.sub(r'<.*?>', '', question_text)
            if regex_links:
                for link in regex_links:
                    # slice up the link to remove extra quotes
                    if get_http_code(link).status_code in [200, 301, 302]:
                        valid_links.append(link)
            # clean up extra whitespace (change spaces w/more than one space to
            # a single space)
            question_text = re.sub(r'\s{2,}', ' ', question_text)
            # remove leading and trailing spaces
            question_text = question_text.strip()
            # only return links if they're valid, otherwise we just want the
            # scrubbed text
            if valid_links:
                return [question_text] + valid_links
            else:
                return question_text
