# Native
import json
import os
from random import randint
# Third-Party
from prettyconf import Configuration
from prettyconf.loaders import Environment, EnvFile

project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
#TODO: fix slashes with proper pathing
env_file = f"{project_path}/config/.env"
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])


class Question:
    def __init__(self, question_json_filepath: str = None):
        self.question_json_filepath = question_json_filepath or config('QUESTIONS_JSON_FILEPATH')

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

    def get_random_question(self):
        # gets random question from given json file
        total_bytes = os.stat(self.question_json_filepath).st_size
        question_json_string = ''
        with open(self.question_json_filepath) as questions_json:
            questions_json.seek(randint(0, total_bytes))
            cur_char = questions_json.read(1)
            # this only works because this is a 1-dimensional json
            if cur_char != '{':
                while cur_char != '{':
                    # read until we get to the start of a question json object
                    cur_char = questions_json.read(1)
            question_json_string += cur_char
            while cur_char != '}':
                cur_char = questions_json.read(1)
                question_json_string += cur_char
        return json.loads(question_json_string)

    @staticmethod
    def get_average_question_len():
        with open(config('QUESTIONS_JSON_FILEPATH')) as questions_json:
            question_json = json.loads(questions_json.read())
            pass

