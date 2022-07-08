# Native
import json
import os
# Third Party
import pytest
# Project
from src.Question import Question


@pytest.fixture
def test_questions():
    with open(os.path.join('fixtures', 'test_questions.json')) as test_question_json:
        return [Question(question_json) for question_json in json.load(test_question_json)]
