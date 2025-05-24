from habit import Habit

class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, name, periodicity):
        habit = Habit(name, periodicity)
        self.habits.append(habit)

    def delete_habit(self, name):
        self.habits = [h for h in self.habits if h.name != name]

    def get_habits(self):
        return self.habits

    def find_habit(self, name):
        return next((h for h in self.habits if h.name == name), None)
