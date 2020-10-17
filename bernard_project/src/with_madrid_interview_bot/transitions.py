
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
        dest=S002xFirstLaunchingFrame,
        factory=trg.Equal.builder(BotCommand('/play')),
    ),
    Tr(
        dest=S003xIsRocketLaunchedInFrame,
        origin=S002xFirstLaunchingFrame,
        factory=Frame.builder(is_search_finished=False),
    ),
    Tr(
        dest=S003xIsRocketLaunchedInFrame,
        origin=S003xIsRocketLaunchedInFrame,
        factory=Frame.builder(is_search_finished=False),
    ),
    Tr(
        dest=S004xCongrats,
        origin=S003xIsRocketLaunchedInFrame,
        factory=Frame.builder(is_search_finished=True),
    ),
    Tr(
        dest=S004xCongrats,
        origin=S002xFirstLaunchingFrame,
        factory=Frame.builder(is_search_finished=True),
    ),
    Tr(
        dest=S002xFirstLaunchingFrame,
        origin=S004xCongrats,
        factory=trg.Choice.builder('again'),
    ),
]