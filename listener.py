class Listener:
    def __init__(self, condition, function):
        self.condition = condition
        self.function = function
        self.dead = False

    def condition_met(self, game):
        return self.condition(game)

    def invoke(self):
        self.dead = True
        return self.function()
