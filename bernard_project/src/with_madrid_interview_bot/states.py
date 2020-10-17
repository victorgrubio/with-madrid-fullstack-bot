# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.analytics import (
    page_view,
)
from bernard.engine import (
    BaseState,
)
from bernard.i18n import (
    intents as its,
    translate as t,
)
from bernard.platforms.telegram import (
    layers as telegram_layers
)

from .store import (
    cs,
)

class WithMadridInterviewBotState(BaseState):
    """
    Root class for With Madrid Interview Bot.

    Here you must implement "error" and "confused" to suit your needs. They
    are the default functions called when something goes wrong. The ERROR and
    CONFUSED texts are defined in `i18n/en/responses.csv`.
    """

    @page_view('/bot/error')
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    @page_view('/bot/confused')
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """

        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError


class S001xStart(WithMadridInterviewBotState):
    """
    Welcome the user
    """

    @page_view('/bot/start')
    async def handle(self) -> None:
        name = await self.request.user.get_friendly_name()

        self.send(
            lyr.Text(t('WELCOME', name=name))
        )


class S002xGuessANumber(WithMadridInterviewBotState):
    """
    Define the number to guess behind the scenes and tell the user to guess it.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-a-number')
    @cs.inject()
    async def handle(self, context) -> None:
        context['number'] = 50
        self.send(lyr.Text(t.GUESS_A_NUMBER))


class S003xGuessAgain(WithMadridInterviewBotState):
    """
    If the user gave a number that is wrong, we give an indication whether that
    guess is too low or too high.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-again')
    @cs.inject()
    async def handle(self, context) -> None:
        user_number = self.trigger.user_number

        self.send(lyr.Text(t.WRONG))

        if user_number < context['number']:
            self.send(lyr.Text(t.HIGHER))
        else:
            self.send(lyr.Text(t.LOWER))


class S004xCongrats(WithMadridInterviewBotState):
    """
    Congratulate the user for finding the number and propose to find another
    one.
    """

    @page_view('/bot/congrats')
    async def handle(self) -> None:
        self.send(
            lyr.Text(t.CONGRATULATIONS),
            lyr.Text(t.DO_YOU_WANT_AGAIN),
            
        )