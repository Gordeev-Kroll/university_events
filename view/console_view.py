class ConsoleView:
    def show_message(self, msg):
        print(msg)

    def get_input(self, prompt):
        return input(prompt)

    def update(self, model):  # Observer
        self.show_message("List updated. Total events: " + str(len(model.events)))