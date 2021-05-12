import os
from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from features import meets


@patch.dict(os.environ, {"GMEET": "OUr-MEETING_LINK"})
def test_cmd_meet(update, context):
    assert os.environ['GMEET'] == "OUr-MEETING_LINK"
    with patch.object(update.message, "reply_text") as m:
        meets.cmd_meet(update, context)
        m.assert_called_with("OUr-MEETING_LINK")


def test_meets():
    cmd_handler = meets.meet()
    assert isinstance(cmd_handler, CommandHandler)
    assert cmd_handler.callback == meets.cmd_meet
    assert cmd_handler.command == ["meet"]