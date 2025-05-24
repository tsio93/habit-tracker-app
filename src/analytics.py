# Return all habit objects from the tracker
def get_all_habits(tracker):
    return tracker.get_habits()

# Filter habits by their periodicity (daily or weekly)
def get_habits_by_periodicity(tracker, periodicity):
    return [h for h in tracker.get_habits() if h.periodicity == periodicity]

# Find and return the habit with the longest streak
def get_longest_streak(tracker):
    habits = tracker.get_habits()
    if not habits:
        return None
    # Use max with a key function to find the habit with the longest streak
    return max(habits, key=lambda h: h.get_streak(), default=None)

# Get the longest streak for a specific habit by name
def get_longest_streak_for_habit(tracker, name):
    habit = tracker.find_habit(name)
    if habit:
        return habit.get_streak()
    return None
