# Native
import json
import os
# Third Party
import pytest
# Project
from src.Question import Question


@pytest.fixture
def test_questions():
    test_questions = []
    with open(os.path.join('fixtures', 'test_questions.json')) as test_question_json:
        for question_json in json.load(test_question_json):
            test_questions.append(Question(question_json).to_tuple())
    return test_questions