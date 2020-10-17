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
    cs, VIDEO_NAME, BASE_VIDEO_API_URL
)

import time
import io
from httpx import Client
from os import(
    getenv
)

from urllib.parse import quote, urljoin

from .components import (
    FrameXBisector
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


class S002xFirstLaunchingFrame(WithMadridInterviewBotState):
    """
    Show the middle frame of the video transmission and check
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-a-number')
    @cs.inject()
    async def handle(self, context) -> None:
        
        bisector = FrameXBisector(VIDEO_NAME)
        limit_left = 0
        limit_right = bisector.count
        current_frame = int((limit_left + limit_right) / 2)
        context.update({
            'current_frame': current_frame,
            'limit_left': limit_left,
            'limit_right': limit_right
        })

        image_url = urljoin(BASE_VIDEO_API_URL,
                    f'video/{quote(VIDEO_NAME)}/frame/{quote(f"{current_frame}")}/')
        self.send(
            lyr.Markdown(t('DID_ROCKET_LAUNCH', frame_number=current_frame, image_url=image_url)),
            tgr.InlineKeyboard([
                [tgr.InlineKeyboardCallbackButton(
                    text='Yes',
                    payload={'decreaseFrame': True}
                )],
                [tgr.InlineKeyboardCallbackButton(
                    text='No',
                    payload={'decreaseFrame': False}
                )]
            ]),
        )


class S003xIsRocketLaunchedInFrame(WithMadridInterviewBotState):
    """
    If the search has not finished, we have to keep updating the boundaries
    and send new images to the user. 
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-again')
    @cs.inject()
    async def handle(self, context) -> None:
        # Update the frame
        current_frame = int((context.get('limit_left') + context.get('limit_right')) / 2)
        context['current_frame'] = current_frame
        
        image_url = urljoin(BASE_VIDEO_API_URL,
                    f'video/{quote(VIDEO_NAME)}/frame/{quote(f"{current_frame}")}/')
        
        self.send(
            lyr.Markdown(t('DID_ROCKET_LAUNCH', frame_number=current_frame, image_url=image_url)),
            tgr.InlineKeyboard([
                [tgr.InlineKeyboardCallbackButton(
                    text='Yes',
                    payload={'decreaseFrame': True}
                )],
                [tgr.InlineKeyboardCallbackButton(
                    text='No',
                    payload={'decreaseFrame': False}
                )]
            ]),
        )


class S004xCongrats(WithMadridInterviewBotState):
    """
    Congratulate the user for finding the frame where the rocket was launched
    """

    @page_view('/bot/congrats')
    @cs.inject()
    async def handle(self, context) -> None:
        current_frame = context.get('current_frame')
        self.send(
            lyr.Text(t('FOUND', frame_number=current_frame)),
            lyr.Text(t.DO_YOU_WANT_AGAIN),
            
        )