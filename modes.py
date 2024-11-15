class Mode:
    def __init__(self, target_types, description, id):
        self.target_types = target_types
        self.description = description
        self.id = id

    @property
    def is_targeted(self):
        return self.target_types is not None

    def __str__(self):
        return self.description
    __repr__ = __str__


class ModeChoice:
    def __init__(self, num_select, modes):
        self.modes_required = num_select
        self.modes = modes

    @property
    def mode_number(self):
        return len(self.modes)
