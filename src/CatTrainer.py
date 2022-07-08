# Native
import random
# Third Party
import spacy
# Project
from src.Question import Question


class CatTrainer:
    def __init__(self):
        self.nlp = spacy.blank('en')
        self.textcat = self.nlp.add_pipe('textcat')
        self.textcat.add_label('History')
        self.textcat.add_label('Not History')

    def train_questions(self, questions: list[Question]):
        self.nlp.begin_training()

        # text of the questions themselves
        question_content = [self.nlp(q.text) for q in questions]

        for question in self.textcat.pipe(question_content, batch_size=10):
            pass

        return question_content
