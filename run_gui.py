from view.gui_view import GuiView
from presenter.presenter import Presenter

view = GuiView()
presenter = Presenter(view, 'db')

def add_callback():
    event_type = view.get_input("Type (Lecture/Workshop/Conference):")
    if not event_type: return
    date = view.get_input("Date (YYYY-MM-DD):")
    if not date: return
    place = view.get_input("Place:")
    if not place: return
    participants_str = view.get_input("Participants:")
    if not participants_str: return
    desc = view.get_input("Description:")
    
    try:
        participants = int(participants_str)
        presenter.add_event(event_type, date, place, participants, desc or "")
    except ValueError:
        view.show_message("Ошибка: количество участников должно быть числом")
    except ValueError as e:
        view.show_message(f"Ошибка: {str(e)}")

def load_callback():
    presenter.load_events()

def analyze_callback():
    presenter.analyze()

def register_callback():
    idx_str = view.get_input("Event index (число):")
    if idx_str:
        try:
            idx = int(idx_str)
            presenter.register_participant(idx)
        except ValueError:
            view.show_message("Ошибка: индекс должен быть числом")

def show_list_callback():
    presenter.show_list()

def delete_callback():
    idx_str = view.get_input("Event index to delete (число):")
    if idx_str:
        try:
            idx = int(idx_str)
            presenter.delete_event(idx)
        except ValueError:
            view.show_message("Ошибка: индекс должен быть числом")

if len(view.buttons) >= 6:
    view.buttons[0].config(command=add_callback)        # Add Event
    view.buttons[1].config(command=load_callback)       # Load Events
    view.buttons[2].config(command=analyze_callback)    # Analyze
    view.buttons[3].config(command=register_callback)   # Register
    view.buttons[4].config(command=show_list_callback)  # Show List
    view.buttons[5].config(command=delete_callback)     # Delete Event

view.mainloop()