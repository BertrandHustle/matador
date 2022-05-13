# Native
import random
# Third Party
import spacy
# Project
from src.Question import Question


class CatTrainer:
    def __init__(self):
        self.nlp = spacy.blank('en')
        self.category = self.nlp.create_pipe('textcat')
        self.category.add_label('History')
        self.nlp.add_pipe('textcat')

    def train_questions(self, questions):
        self.nlp.begin_training()

        for itn in range(100):
            random.shuffle()
