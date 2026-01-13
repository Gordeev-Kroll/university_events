import sqlite3
from typing import List
from model.event import Lecture, Workshop, Conference

class DBDataSource:
    def __init__(self, db_name='events.db'):
        self.db_name = db_name

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT, date TEXT, place TEXT, participants INT, description TEXT)''')
        conn.commit()
        return conn, cursor

    def load_events(self) -> List:
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT * FROM events")
            rows = cursor.fetchall()
            events = []
            for row in rows:
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
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id FROM events 
                WHERE type=? AND date=? AND place=? AND description=?
            """, (event.type, event.date.strftime("%Y-%m-%d"), event.place, event.description))
            
            row = cursor.fetchone()
            if row:
                event_id = row[0]
                cursor.execute("""
                    UPDATE events SET participants = ? 
                    WHERE id = ?
                """, (event.participants, event_id))
            else:
                cursor.execute("""
                    INSERT INTO events (type, date, place, participants, description) 
                    VALUES (?, ?, ?, ?, ?)
                """, (event.type, event.date.strftime("%Y-%m-%d"), event.place, event.participants, event.description))
            conn.commit()
        finally:
            conn.close()

    def delete_event(self, event):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""
                DELETE FROM events 
                WHERE type = ? AND date = ? AND place = ? AND participants = ? AND description = ?
            """, (
                event.type,
                event.date.strftime("%Y-%m-%d"),
                event.place,
                event.participants,
                event.description
            ))
            conn.commit()
        finally:
            conn.close()