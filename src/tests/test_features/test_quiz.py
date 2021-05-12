import os
from unittest.mock import patch, MagicMock

import pytest
from telegram.ext import CommandHandler

from db.sqlite import DbConnection
from features import quiz


def test_cmd_quiz(update, context):
    with patch('features.quiz.DB.query', return_value=[{
            'question_id': 1,
            'question': 'chicken or egg what came first?',
            'question_options': 'egg\nchicken\nsalad\nnone',
            'correct_option_id': None,
            'is_multiple_answers': 0}]
        ):
        update = MagicMock()
        quiz.cmd_quiz(update, context)
        update.effective_message.reply_poll.assert_called_with(
            question='chicken or egg what came first?',
            options=['egg', 'chicken', 'salad', 'none'],
            type='quiz',
            correct_option_id=None,
            allows_multiple_answers=0,
            explanation_parse_mode='MarkdownV2'
        )

    big_title = 'chicken or egg what came first? This question needs to explore more than 300 words to see if it will call the reply functions twice, as telegram api has a limit of 300 chars. It shluld be big enough to make the caller send 2 messages, to the quiz, one with the title and another one with the options to select'

    with patch('features.quiz.DB.query', return_value=[{
            'question_id': 1,
            'question': big_title,
            'question_options': 'egg\nchicken\nsalad\nnone',
            'correct_option_id': None,
            'is_multiple_answers': 0}]
        ):
        update = MagicMock()
        quiz.cmd_quiz(update, context)
        update.message.reply_text.assert_called_with(big_title)
        update.effective_message.reply_poll.assert_called_with(
            question='What the following options?',
            options=['egg', 'chicken', 'salad', 'none'],
            type='quiz',
            correct_option_id=None,
            allows_multiple_answers=0,
            explanation_parse_mode='MarkdownV2'
        )


def test_quiz():
    cmd_handler = quiz.quiz_me()
    assert isinstance(cmd_handler, CommandHandler)
    assert cmd_handler.callback == quiz.cmd_quiz
    assert cmd_handler.command == ["quizme"]