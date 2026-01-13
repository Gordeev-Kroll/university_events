from model.event_list import EventList
from model.event import Lecture, Workshop, Conference
from model.data_sources import MockDataSource, FileDataSource
from server.database import DBDataSource

class Presenter:
    def __init__(self, view, source_type='mock'):
        self.model = EventList()
        self.view = view
        self.model.attach_observer(view)  # Observer
        self.data_source = {
            'mock': MockDataSource(),
            'file': FileDataSource('data/events.json'),
            'db': DBDataSource()
        }[source_type]

    def load_events(self):
        self.model.events = self.data_source.load_events()
        self.view.show_message("Loaded events: " + str(len(self.model.events)))

    def add_event(self, type, date, place, participants, desc):
        cls = {'Lecture': Lecture, 'Workshop': Workshop, 'Conference': Conference}.get(type, Lecture)
        event = cls(type, date, place, int(participants), desc)
        self.model.add_event(event)
        if isinstance(self.data_source, DBDataSource):
            self.data_source.save_event(event)

    def analyze(self):
        stats = self.model.analyze()
        self.view.show_message(f"Stats: Sum={stats['sum']}, Avg={stats['avg']}, Max={stats['max']}")

    def register_participant(self, event_index):
        if 0 <= event_index < len(self.model.events):
            event = self.model.events[event_index]
            event.participants += 1
            self.model.notify_observers()
            
            if isinstance(self.data_source, DBDataSource):
                self.data_source.save_event(event)
            
            self.view.show_message(f"Зарегистрирован участник. Новое количество: {event.participants}")
            return True
        else:
            self.view.show_message("Ошибка: неверный индекс")
            return False

    def show_list(self):
        if not self.model.events:
            self.view.show_message("Список событий пуст")
            return
        self.view.show_message("=== Список всех событий ===")
        for i, event in enumerate(self.model.events):
            self.view.show_message(f"[{i}] {event.to_string()}")
        self.view.show_message("=========================")

    def delete_event(self, event_index):
        if 0 <= event_index < len(self.model.events):
            event_to_delete = self.model.events[event_index]
            del self.model.events[event_index]
            if isinstance(self.data_source, DBDataSource):
                self.data_source.delete_event(event_to_delete)
            self.model.notify_observers()
            self.view.show_message(f"Событие [{event_index}] удалено")
        else:
            self.view.show_message("Ошибка: неверный индекс события")