from abc import ABC, abstractmethod
from datetime import datetime

class IEvent(ABC):
    @abstractmethod
    def get_participants(self):
        pass

    @abstractmethod
    def to_string(self):
        pass

class BaseEvent(IEvent):
    def __init__(self, type, date, place, participants=0, description=""):
        self.type = type
        try:
            self.date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        self.place = place
        self.participants = participants
        self.description = description

    def get_participants(self):
        return self.participants

    def to_string(self):
        return f"{self.type}: {self.date.date()} at {self.place}, Participants: {self.participants}, Desc: {self.description}"

# Полиморфные наследники (Strategy в полиморфизме)
class Lecture(BaseEvent):
    pass

class Workshop(BaseEvent):
    def get_participants(self):
        return super().get_participants() + 5

class Conference(BaseEvent):
    pass