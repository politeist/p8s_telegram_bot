import random

from dataclasses import dataclass
from typing import Optional, List

from telegram.ext import CallbackContext, CommandHandler, PollHandler
from telegram import (
    Poll,
    ParseMode,
    Update
)
from loader import LoaderApps
from utils import logger
from db.sqlite import DbConnection

ERRORS_STICKERS = [
    "CAACAgQAAxkBAAECSxdgmsm5LY9-QMotvNFbWBDRWpP88gAC7QEAAheqxwABXETOigPW7vUfBA", # Homer
    "CAACAgEAAxkBAAECSxlgmsnoWr1UGxHoOXVYB8vZzcCcmgACDQADh0KUClSrGCL_QP4FHwQ", # Faustop
    "CAACAgIAAxkBAAECSyFgmsqEtNwfZ752FY7retG3EffwxAAClAADF64RA0kNX5l8ULvFHwQ" # Spidy
    ""
]

CORRECT_STICKERS = [
    "CAACAgEAAxkBAAECSxtgmspEPOmHYamBj1VjTUn1Bk2rOwAC_gIAAodClAr5Fn2X7dW5ax8E", # Faustop
    "CAACAgEAAxkBAAECSx1gmspe7ZC0zEwmNJ-snGQYtjS3hwACywYAAodClArep0IMdrL2KB8E", # Faustop
    "CAACAgEAAxkBAAECSx9gmspgNmFkAU16Xtv6gYMl9whT3gACyQYAAodClApOHAsKsaPAMx8E", # Faustop
    "CAACAgIAAxkBAAECSyNgmsqWukeX43lBS2MpMK7cK_FfhwACrQADF64RA9lQTvLyFpnjHwQ" # Don't know the name
]


@dataclass
class Question:
    question_id: int
    question: str
    question_options: List[str]
    correct_option_id: int
    is_multiple_answers: bool
    extra_args: Optional[str] = None
    message_id: Optional[str] = None
    explanation_parse_mode: Optional[str] = ParseMode.MARKDOWN_V2


class PersistQuiz:
    _QUESTIONS: List[Question] = []

    @classmethod
    def clean(cls) -> None:
        cls._QUESTIONS = []

    @classmethod
    def questions(cls) -> list:
        _questions = []
        for question in cls._QUESTIONS:
            _questions.append(question)
        return _questions

    @classmethod
    def add_question(cls, **kwargs) -> dict:
        question = Question(**kwargs)
        cls._QUESTIONS.append(question)
        return question

    @classmethod
    def get_question(cls, question_id: int) -> dict:
        for question in cls._QUESTIONS:
            if question.__dict__.get('question_id') == question_id:
                return question
        return {}


get_quiz_id = PersistQuiz.get_question
register_question = PersistQuiz.add_question


def cmd_quiz(update: Update, context: CallbackContext):
    """Send a predefined poll"""
    db = DbConnection()
    result = db.query('SELECT * from quiz_db order by RANDOM() limit 1;')[0]
    question = register_question(**result)

    if len(question.question) > 300:
        update.message.reply_text(question.question)
        text = "What the folloing options?"
    else:
        text = question.question

    args = {
        'question': text,
        'options': question.question_options.split('\n'),
        'type':Poll.QUIZ,
        'correct_option_id': question.correct_option_id,
        'allows_multiple_answers': question.is_multiple_answers,
        'explanation_parse_mode': ParseMode.MARKDOWN_V2
    }
    if args['allows_multiple_answers']:
        args['correct_option_id'] = args['correct_option_id'].split(',')
        args['type'] = Poll.REGULAR

    message = update.effective_message.reply_poll(**args)
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {
            "chat_id": update.effective_chat.id,
            "question_id": question.question_id,
            "message_id": message.message_id
        }
    }
    context.bot_data.update(payload)


def receive_quiz_answer(update: Update, context: CallbackContext) -> None:
    """ Close quiz once participants took it """
    correct_answers = []

    if update.poll.is_closed:
        return
    try:
        for idx, opt in enumerate(update.poll.options):
            if opt.voter_count:
                correct_answers.append(idx)

        quiz_data = context.bot_data[update.poll.id]
        question = get_quiz_id(quiz_data["question_id"])

        if type(question.correct_option_id) == int:
            correct_ids = [question.correct_option_id]

        if type(question.correct_option_id) == str:
            correct_ids = [int(x) for x in question.correct_option_id.split(',')]

        if correct_answers and correct_answers == correct_ids:
            context.bot.send_sticker(
                quiz_data["chat_id"],
                random.choice(CORRECT_STICKERS)
            )

        else:
            context.bot.send_sticker(
                quiz_data["chat_id"],
                random.choice(ERRORS_STICKERS)
            )
        context.bot.send_message(
            chat_id=quiz_data["chat_id"],
            text=question.extra_args
        )
    # this means this poll answer update is from an old poll, we can't stop it then
    except KeyError:
        return
    context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])


@LoaderApps.handler
def quiz_me():
    """
        /quizMe - Generate sample quiz (It quiz!)
    """
    return CommandHandler("quizMe", cmd_quiz)


@LoaderApps.handler
def quiz_response():
    return PollHandler(
        receive_quiz_answer,
        pass_chat_data=True,
        pass_user_data=True
    )
