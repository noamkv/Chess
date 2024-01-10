class Square:
    def __init__(self, occupied=None):
        self.occupied = None  # None means empty

    def is_empty(self):
        return self.occupied is None
