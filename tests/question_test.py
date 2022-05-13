# Native
import json
import os
# Third Party
import pytest
# Project
from Question import Question

@pytest.fixture
def test_questions():
    with open(os.path.join('fixtures', 'test_questions.json')) as test_question_json:
        test_questions = []
        for question_json in json.load(test_question_json):
            test_questions.append(Question(question_json))
        return test_questions


def test_test_questions(test_questions):
    print(test_questions)
    for q in test_questions:
        print(q.text, q.category)


