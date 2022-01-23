# Handles execution of the actions to the led strip


from collections.abc import Callable
import string


class LedAction:
    identifier: string
    ledFunction: any
    def __init__(self, identifier:string, ledFunction:Callable[[], None]):
        self.identifier = identifier
        
    # kills the current action
    def abort():
        
    # starts the current led action
    def start(self):
        
