class Player:
    def __init__(self, name, color, is_turn: bool):
        self.name = name
        self.color = color
        self.is_turn = is_turn

    def switch_turn(self):
        self.is_turn = not self.is_turn

    def __str__(self):
        return f"name: {self.name} \ncolor:{self.color}"
