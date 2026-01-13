from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from server.database import DBDataSource as ServerDB
from model.event_list import EventList
from model.event import Lecture, Workshop, Conference

app = FastAPI(title="University Events API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = ServerDB()
el = EventList()
el.events = db.load_events()

class EventData(BaseModel):
    type: str
    date: str
    place: str
    participants: int
    description: str = ""

@app.get("/events")
def get_events():
    """Возвращает список всех событий в строковом формате"""
    return [e.to_string() for e in el.events]

@app.post("/events")
def add_event(event: EventData):
    """Добавляет новое мероприятие"""
    try:
        cls = {'Lecture': Lecture, 'Workshop': Workshop, 'Conference': Conference}.get(event.type, Lecture)
        new_event = cls(
            type=event.type,
            date=event.date,
            place=event.place,
            participants=event.participants,
            description=event.description
        )
        el.add_event(new_event)
        db.save_event(new_event)
        return {"status": "added", "event": new_event.to_string()}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/analyze")
def analyze():
    """Возвращает агрегированную статистику по участникам"""
    stats = el.analyze()
    return {
        "total_participants": stats['sum'],
        "average_participants": stats['avg'],
        "max_participants": stats['max'],
        "total_events": len(el.events)
    }

@app.post("/register/{event_id}")
def register(event_id: int):
    """Регистрирует одного участника на мероприятие по индексу"""
    if 0 <= event_id < len(el.events):
        el.events[event_id].participants += 1
        db.save_event(el.events[event_id])
        return {
            "status": "registered",
            "new_participants": el.events[event_id].participants,
            "event": el.events[event_id].to_string()
        }
    return {"error": "Invalid event ID"}

@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    """Удаляет мероприятие по индексу"""
    if 0 <= event_id < len(el.events):
        event_to_delete = el.events[event_id]
        del el.events[event_id]
        db.delete_event(event_to_delete)
        el.events = db.load_events()
        return {"status": "deleted"}
    return {"error": "Invalid event ID"}

@app.get("/")
def root():
    return {"message": "University Events API is running"}