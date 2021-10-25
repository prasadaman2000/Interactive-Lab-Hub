from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def get_value(self):
        pass

class CapacitorButton(Button):
    # boardObj and idx
    def __init__(self, **kwargs):
        self.board = kwargs['boardObj']
        self.idx = kwargs['idx']
    
    def get_value(self):
        return not self.board[self.idx].value
