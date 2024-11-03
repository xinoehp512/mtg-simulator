
import random


class Zone:
    def __init__(self, name, privacy, assigned_player=None):
        self.name = name
        self.privacy = privacy
        self.assigned_player = assigned_player
        self.objects = []

    @property
    def size(self):
        return len(self.objects)

    def is_empty(self):
        return len(self.objects) == 0

    def add_objects(self, objects):
        self.objects.extend(objects)

    def shuffle(self):
        random.shuffle(self.objects)

    def pop(self):
        return self.objects.pop()

    def remove(self, object):
        self.objects.remove(object)

    def get_by_criteria(self, criteria):
        return [obj for obj in self.objects if criteria(obj) and obj.is_alive]

    def remove_by_criteria(self, criteria):
        self.removed_objects = self.get_by_criteria(criteria)
        self.objects = [obj for obj in self.objects if not criteria(obj)]
        return len(self.removed_objects) > 0
