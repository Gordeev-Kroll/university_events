import importlib
import sys

from view.console_view import ConsoleView
from presenter.presenter import Presenter

for module_name in list(sys.modules.keys()):
    if module_name.startswith('server.') or module_name.startswith('presenter.') or module_name == 'server.database':
        importlib.reload(sys.modules[module_name])

from view.console_view import ConsoleView
from presenter.presenter import Presenter

view = ConsoleView()
presenter = Presenter(view, 'db')
presenter.load_events()

while True:
    cmd = view.get_input("Command (add/list/analyze/register/delete/exit): ")
    if cmd == 'exit': break
    elif cmd == 'add':
        type = view.get_input("Type: ")
        date = view.get_input("Date (YYYY-MM-DD): ")
        place = view.get_input("Place: ")
        parts = view.get_input("Participants: ")
        desc = view.get_input("Desc: ")
        presenter.add_event(type, date, place, parts, desc)
    elif cmd == 'list':
        presenter.show_list()
    elif cmd == 'analyze':
        presenter.analyze()
    elif cmd == 'register':
        idx = int(view.get_input("Event index: "))
        presenter.register_participant(idx)
    elif cmd == 'delete':
        idx = int(view.get_input("Event index to delete: "))
        presenter.delete_event(idx)