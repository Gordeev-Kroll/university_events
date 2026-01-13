from typing import List
from .event import IEvent
from .strategies import AggregateStrategy, SumStrategy, AvgStrategy, MaxStrategy

class EventList:
    def __init__(self):
        self.events: List[IEvent] = []
        self.observers = []  # Observer pattern

    def add_event(self, event: IEvent):
        self.events.append(event)
        self.notify_observers()

    def delete_event(self, index: int):
        if 0 <= index < len(self.events):
            del self.events[index]
            self.notify_observers()
        else:
            raise IndexError("Invalid event index")

    def get_total_participants(self, strategy: AggregateStrategy = SumStrategy()):
        return strategy.calculate([e.get_participants() for e in self.events])

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def attach_observer(self, observer):
        self.observers.append(observer)
        
    def analyze(self):
        return {
            'sum': self.get_total_participants(SumStrategy()),
            'avg': self.get_total_participants(AvgStrategy()),
            'max': self.get_total_participants(MaxStrategy())
        }