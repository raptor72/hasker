from celery import shared_task
from hasker.utils import recalculate_answers, recalculate_question
import logging


@shared_task()
def rec_answers():
    answers = recalculate_answers()
    logging.warning(f'recalculete {answers} answers')
    return answers


@shared_task()
def rec_questions():
    questions = recalculate_question()
    logging.warning(f'recalculete {questions} questions')
    return questions
