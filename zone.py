
import random


class Zone:
    def __init__(self, name, privacy, assigned_player=None):
        self.name = name
        self.privacy = privacy
        self.assigned_player = assigned_player
        self._objects = []

    @property
    def size(self):
        return len(self.objects)

    @property
    def objects(self):
        self._objects = [obj for obj in self._objects if obj.is_alive]
        return self._objects

    def is_empty(self):
        return len(self.objects) == 0

    def add_objects(self, objects):
        self._objects.extend(objects)

    def add_objects_to_bottom(self, objects):
        self._objects = objects+self._objects

    def shuffle(self):
        random.shuffle(self._objects)

    def pop(self):
        return self._objects.pop()

    def remove(self, object):
        self._objects.remove(object)

    def get_by_criteria(self, criteria):
        return [obj for obj in self.objects if criteria(obj)]

    def remove_by_criteria(self, criteria):
        self.removed_objects = self.get_by_criteria(criteria)
        self._objects = [obj for obj in self.objects if not criteria(obj)]
        return len(self.removed_objects) > 0
