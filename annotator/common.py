from enum import Enum
class IntegerEnum(Enum):
    @classmethod
    def choices(cls):
        choices = list()
        # Loop thru defined enums
        for item in cls:
            choices.append((item.value, item.name))
        # return as tuple
        return tuple(choices)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value