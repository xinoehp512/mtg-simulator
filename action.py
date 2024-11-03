class Action:

    def __init__(self, descriptor, action, results=None, is_priority_holding=True):
        self.descriptor = descriptor
        self.action = action
        self.results = results
        self.is_priority_holding = is_priority_holding

    def invoke(self):
        return self.action()

    def __str__(self):
        return self.descriptor

    __repr__ = __str__
