import json
from habit import Habit

class DataManager:
    FILE = 'data.json'

    @staticmethod
    def save_data(habits):
        with open(DataManager.FILE, 'w') as f:
            json.dump(
                [habit.__dict__ for habit in habits],
                f,
                indent=4
            )

    @staticmethod
    def load_data():
        try:
            with open(DataManager.FILE, 'r') as f:
                data = json.load(f)
                return [Habit(
                    name=d['name'],
                    periodicity=d['periodicity'],
                    creation_dt=d['creation_dt'],
                    completion_dt=d['completion_dt']
                ) for d in data]
        except FileNotFoundError:
            return []
