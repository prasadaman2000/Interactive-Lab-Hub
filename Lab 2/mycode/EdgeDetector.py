class EdgeDetector:
    def __init__(self, button):
        self.state = button.value
        self.button = button

    def neg_edge(self):
        has_edge = not self.button.value and self.state
        self.state = self.button.value
        return has_edge