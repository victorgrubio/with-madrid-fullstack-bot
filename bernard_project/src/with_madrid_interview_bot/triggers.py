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
    This trigger will try to interpret what the user sends as a specific action 
    to increase or decrease the limits of the bisection search.
    The `is_search_finished` parameter allows to say if you want the trigger to activate
    when the frame search is finished or not.
    """

    def __init__(self, request, is_search_finished):
        super().__init__(request)
        self.is_search_finished = is_search_finished
        self.left = None
        self.right = None

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
        number = context.get('current_frame')

        if not number:
            return .0

        try:
            # Get values from context
            self.left = context.get('limit_left')
            self.right = context.get('limit_right')
            # Get the update action from the decrease frame element in payload as boolean
            decrease_frame = bool(self.request.get_layer(lyr.Postback).payload['decreaseFrame'])
            if decrease_frame:
                # Update the right limit of the bisection search
                self.right = context.get('current_frame')
                context['limit_right'] = context.get('current_frame')
            else:
                # Update the left limit of the bisection search
                self.left = context.get('current_frame')
                context['limit_left'] = context.get('current_frame')
            
        except (KeyError, ValueError, TypeError):
            return .0

        # If we sum 2 and surpass the limit, we already now the number
        is_search_finished = self.left + 2 >= self.right
        # If the result is secure and next action is decrease, then is previous frame
        if is_search_finished and decrease_frame: 
            context['current_frame'] -= 1
        # If the result is secure and next action is increase, then is next frame
        elif is_search_finished and not decrease_frame:
            context['current_frame'] += 1
        

        return 1. if is_search_finished == self.is_search_finished else .0