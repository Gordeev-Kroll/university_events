import json
import sqlite3
from typing import List
from .event import Lecture, Workshop, Conference

class DataSourceAdapter:
    def load_events(self) -> List:
        raise NotImplementedError

class MockDataSource(DataSourceAdapter):
    def load_events(self) -> List:
        return [Lecture("Lecture", "2026-01-10", "Aud1", 50, "Test")]

class FileDataSource(DataSourceAdapter):
    def __init__(self, filename):
        self.filename = filename

    def load_events(self) -> List:
        with open(self.filename, 'r') as f:
            data = json.load(f)
        events = []
        for d in data:
            cls = {'Lecture': Lecture, 'Workshop': Workshop, 'Conference': Conference}.get(d['type'], Lecture)
            events.append(cls(d['type'], d['date'], d['place'], d['participants'], d['description']))
        return events

class DBDataSource(DataSourceAdapter):
    def __init__(self, db_name='events.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT, date TEXT, place TEXT, participants INT, description TEXT)''')
        self.conn.commit()

    def load_events(self) -> List:
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT * FROM events")
            rows = cursor.fetchall()
            events = []
            for row in rows:
                # row[0] — id
                # row[1] — type
                # row[2] — date
                # row[3] — place
                # row[4] — participants
                # row[5] — description
                event_type = row[1]
                cls = {'Lecture': Lecture, 'Workshop': Workshop, 'Conference': Conference}.get(event_type, Lecture)
                
                event = cls(
                    type=event_type,
                    date=row[2],
                    place=row[3],
                    participants=row[4],
                    description=row[5]
                )
                events.append(event)
            return events
        finally:
            conn.close()

    def save_event(self, event):
        self.cursor.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?)",
                            (event.type, event.date.strftime("%Y-%m-%d"), event.place, event.participants, event.description))
        self.conn.commit()

    def delete_event(self, type, date, place, participants, description):
        self.cursor.execute("""
            DELETE FROM events 
            WHERE type = ? AND date = ? AND place = ? AND participants = ? AND description = ?
        """, (type, date, place, participants, description))
        self.conn.commit()