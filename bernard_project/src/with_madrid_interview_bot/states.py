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
    layers as tgr
)

from .store import (
    cs, VIDEO_NAME, DISPLAY_SIZE
)

import time
import io
from PIL import (
    Image
)

from .components import (
    FrameXBisector
)

def get_current_frame_from_payload(payload):
    limit_left = int(payload['left'])
    limit_right = int(payload['right'])
    return int((limit_left + limit_right) / 2)

def get_image_from_bisector_response(bisector_response):
    pil_img = Image.open(io.BytesIO(bisector_response))
    pil_img.thumbnail(DISPLAY_SIZE)
    buf = pil_img.tobytes()
    size = pil_img.width, pil_img.height


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
        bisector = FrameXBisector(VIDEO_NAME)
        limit_left = 0
        limit_right = bisector.count
        current_frame = int((limit_left + limit_right) / 2)
        bisector.index = current_frame
        context.update({
            'current_frame': current_frame,
            'limit_left': limit_left,
            'limit_right': limit_right
        })
        results = [
            tgr.InlineQueryResultArticle(
                identifiers={'id': 1},
                input_stack=lyr.Stack(layers=[tgr.InlineQueryResultArticle]),
                title="current frame",
                description="TEST",
                thumb_url="https://www.clker.com//cliparts/3/m/v/Y/E/V/small-red-apple-hi.png",
                thumb_width=480,
                thumb_height=360
            )
        ]
        self.send(
            lyr.Text(t('DID_ROCKET_LAUNCH', frame_number=current_frame)),
            tgr.AnswerInlineQuery(
                results=results,
                cache_time=0,
            ))
        self.send(
            
            lyr.Text(t('DID_ROCKET_LAUNCH', frame_number=current_frame)),
            tgr.InlineKeyboard([
                [tgr.InlineKeyboardCallbackButton(
                    text='Yes',
                    payload={'increaseFrame': True}
                )],
                [tgr.InlineKeyboardCallbackButton(
                    text='No',
                    payload={'increaseFrame': False}
                )]
            ]),
        )


class S003xGuessAgain(WithMadridInterviewBotState):
    """
    If the user gave a number that is wrong, we give an indication whether that
    guess is too low or too high.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-again')
    @cs.inject()
    async def handle(self, context) -> None:
        # bisector = FrameXBisector(VIDEO_NAME)
        current_frame = int((context.get('limit_left') + context.get('limit_right')) / 2)
        # bisector.index = current_frame
        context['current_frame'] = current_frame
        results = [
            tgr.InlineQueryResultArticle(
                title="current frame",
                thumb_url="https://www.clker.com//cliparts/3/m/v/Y/E/V/small-red-apple-hi.png",
                thumb_width=480,
                thumb_height=360
            )
        ]
        self.send(
            tgr.AnswerInlineQuery(
                results=results,
                cache_time=0,
                is_personnal=True,
            ),
            lyr.Text(t('DID_ROCKET_LAUNCH', frame_number=current_frame)),
            tgr.InlineKeyboard([
                [tgr.InlineKeyboardCallbackButton(
                    text='Yes',
                    payload={'increaseFrame': True}
                )],
                [tgr.InlineKeyboardCallbackButton(
                    text='No',
                    payload={'increaseFrame': False}
                )]
            ]),
        )


class S004xCongrats(WithMadridInterviewBotState):
    """
    Congratulate the user for finding the number and propose to find another
    one.
    """

    @page_view('/bot/congrats')
    @cs.inject()
    async def handle(self, context) -> None:
        current_frame = context.get('current_frame')
        self.send(
            lyr.Text(t('FOUND', frame_number=current_frame)),
            lyr.Text(t.DO_YOU_WANT_AGAIN),
            
        )