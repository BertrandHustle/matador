# Native
import os
# Third Party
import pytest
# Project
import Question

test_question = Question.Question(os.path.join('fixtures', 'test_questions.json'))


def test_get_average_question_len():
    test_question.get_average_question_len()


def test_get_random_question():
    test_question_json = test_question.get_random_question()
    assert test_question_json
