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
    if update.poll.is_closed:
        return
    try:
        quiz_data = context.bot_data[update.poll.id]
        logger.info(f"Data: {quiz_data}, Pool: {update.poll.__dict__}")

        logger.info(f"Upd: {update.__dict__}, cont: {context.__dict__}")
        question = get_quiz_id(quiz_data["question_id"])
        print(question)

        #if update.pool.correct_option_id == get_quiz_id()
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
