import json
import datetime

class Reminder:
    def __init__(self):
        self.events = {}

    def load_reminders(self):
        with open('reminders.json', 'r') as file:
            self.events = json.load(file)

    def save_reminders(self):
        with open('reminders.json', 'w') as file:
            json.dump(self.events, file)

    def add_event(self, event_name, event_date):
        self.events[event_name] = event_date
        self.save_reminders()

    def remove_event(self, event_name):
        if event_name in self.events:
            del self.events[event_name]
            self.save_reminders()

    def get_event_date(self, event_name):
        if event_name in self.events:
            return self.events[event_name]
        else:
            return None

    def get_events(self):
        return self.events

    def speak_events(self):
        events = self.get_events()
        if len(events) == 0:
            print("You have no reminders.")
        else:
            print("Your reminders are:")
            for event in events:
                event_date = datetime.datetime.strptime(events[event], '%Y-%m-%d')
                print(f"{event} on {event_date.strftime('%B %d, %Y')}")
