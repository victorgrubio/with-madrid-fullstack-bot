from bernard import (
    layers as lyr,
)
from bernard.engine.triggers import (
    BaseTrigger,
)

from .store import (
    cs,
)


class Frame(BaseTrigger):
    """
    This trigger will try to interpret what the user sends as a number. If it
    is a number, then it's compared to the number to guess in the context.
    The `is_right` parameter allows to say if you want the trigger to activate
    when the guess is right or not.
    """

    def __init__(self, request, is_right):
        super().__init__(request)
        self.is_right = is_right
        self.left = None
        self.right = None

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        number = context.get('current_frame')

        if not number:
            return .0

        try:
            self.left = context.get('limit_left')
            self.right = context.get('limit_right')
            increase_frame = bool(self.request.get_layer(lyr.Postback).payload['increaseFrame'])
            if increase_frame:
                self.left = context.get('current_frame')
                context['limit_left'] = context.get('current_frame')
            else:
                self.right = context.get('current_frame')
                context['limit_right'] = context.get('current_frame')
            
        except (KeyError, ValueError, TypeError):
            return .0
        
        print({'CURRENT': context.get('current_frame'), 'LEFT': self.left, 'RIGHT': self.right})
        is_right = self.left + 2 >= self.right
        if is_right and increase_frame:
            context['current_frame'] += 1
        elif is_right and not increase_frame:
            context['current_frame'] -= 1
        

        return 1. if is_right == self.is_right else .0