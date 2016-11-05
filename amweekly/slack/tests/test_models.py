from django.core.exceptions import ValidationError

from amweekly.slack.tests.factories import SlashCommandFactory

import pytest

pytest.mark.unit


def test_slash_command_raises_with_invalid_token(settings):
    settings.SLACK_TOKENS = ''

    with pytest.raises(ValidationError):
        SlashCommandFactory()
