
# coding: utf-8

from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.i18n import (
    intents as its,
)

from .states import *
from .triggers import *

from bernard.platforms.telegram.layers import (
    BotCommand
)


transitions = [
    Tr(
        dest=S001xStart,
        factory=trg.Equal.builder(BotCommand('/start')),
    ),
    Tr(
        dest=S002xGuessANumber,
        factory=trg.Equal.builder(BotCommand('/play')),
    ),
    Tr(
        dest=S003xGuessAgain,
        origin=S002xGuessANumber,
        factory=Number.builder(is_right=False),
    ),
    Tr(
        dest=S003xGuessAgain,
        origin=S003xGuessAgain,
        factory=Number.builder(is_right=False),
    ),
    Tr(
        dest=S004xCongrats,
        origin=S003xGuessAgain,
        factory=Number.builder(is_right=True),
    ),
    Tr(
        dest=S004xCongrats,
        origin=S002xGuessANumber,
        factory=Number.builder(is_right=True),
    ),
    Tr(
        dest=S002xGuessANumber,
        origin=S004xCongrats,
        factory=trg.Choice.builder('again'),
    ),
]