from datetime import datetime

class Habit:
    def __init__(self, name, periodicity, creation_dt=None, completion_dt=None):
        self.name = name
        self.periodicity = periodicity  # 'daily' or 'weekly'
        self.creation_dt = creation_dt or datetime.now().isoformat()
        self.completion_dt = completion_dt or []

    def mark_completed(self):
        self.completion_dt.append(datetime.now().isoformat())

    def get_streak(self):
        if not self.completion_dt:
            return 0

        dates = sorted(datetime.fromisoformat(dt).date() for dt in self.completion_dt)
        streak = 1
        for i in range(len(dates) - 1, 0, -1):
            if (dates[i] - dates[i - 1]).days == 1:
                streak += 1
            else:
                break
        return streak

def reset_streak(self):
    self.completion_dt = []

def get_completion_rate(self):
    if not self.completion_dt:
        return 0
    from datetime import datetime
    first = datetime.fromisoformat(self.creation_dt).date()
    last = datetime.now().date()
    total_days = (last - first).days + 1
    return round(len(set(self.completion_dt)) / total_days * 100, 2) if total_days > 0 else 0

