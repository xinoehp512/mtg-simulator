class Target:

    def __init__(self, legality_function, object):
        self.legality_function = legality_function
        self.object = object

    def is_legal(self, game, player, source):
        return self.legality_function(game, self.object, player, source)

    def __str__(self) -> str:
        return str(self.object)

    __repr__ = __str__
