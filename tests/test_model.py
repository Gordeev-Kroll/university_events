import unittest
from model.event import Lecture
from model.event_list import EventList
from model.strategies import SumStrategy

class TestModel(unittest.TestCase):
    def test_add_event(self):
        el = EventList()
        el.add_event(Lecture("Lecture", "2026-01-10", "Aud1", 50))
        self.assertEqual(len(el.events), 1)

    def test_aggregate(self):
        el = EventList()
        el.add_event(Lecture("Lecture", "2026-01-10", "Aud1", 50))
        el.add_event(Lecture("Lecture", "2026-01-11", "Aud2", 30))
        self.assertEqual(el.get_total_participants(SumStrategy()), 80)

if __name__ == '__main__':
    unittest.main()