# Third Party
import pytest
# Project
from fixtures import test_questions
from src.CatTrainer import CatTrainer


def test_train_questions(test_questions):
    test_trainer = CatTrainer()
