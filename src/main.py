# Standard library imports
import os
import sys
from datetime import datetime
from tkinter import messagebox

# UI framework
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


# === Habit Class ===
class Habit:
    def __init__(self, name, periodicity):
        self.name = name
        self.periodicity = periodicity  # 'daily' or 'weekly'
        self.completion_dates = []      # List of dates when habit was marked as completed
        self.streak = 0                 # Current streak count

    def mark_completed(self):
        """Mark habit as completed for today if not already marked."""
        today = datetime.now().date()
        if today not in self.completion_dates:
            self.completion_dates.append(today)
            self.update_streak()
            return True
        return False

    def update_streak(self):
        """Calculate and update the current streak based on completion history."""
        if not self.completion_dates:
            self.streak = 0
            return

        sorted_dates = sorted(self.completion_dates, reverse=True)
        current_streak = 1

        for i in range(1, len(sorted_dates)):
            delta = (sorted_dates[i - 1] - sorted_dates[i]).days
            expected = 1 if self.periodicity == "daily" else 7
            if delta == expected:
                current_streak += 1
            else:
                break

        self.streak = current_streak

    def get_completion_rate(self):
        """Calculate percentage of expected completions that were completed."""
        if not self.completion_dates:
            return 0
        first = min(self.completion_dates)
        today = datetime.now().date()
        days = (today - first).days + 1
        expected = days if self.periodicity == "daily" else (days // 7) + 1
        return round((len(self.completion_dates) / expected) * 100)


# === HabitTracker Class ===
class HabitTracker:
    def __init__(self):
        self.habits = []

    def add_habit(self, name, periodicity):
        """Add a new habit if not duplicate and valid periodicity."""
        if periodicity not in ["daily", "weekly"]:
            return False
        if not any(h.name.lower() == name.lower() for h in self.habits):
            self.habits.append(Habit(name, periodicity))
            return True
        return False

    def find_habit(self, name):
        """Find a habit by name (case insensitive)."""
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                return habit
        return None

    def delete_habit(self, name):
        """Remove a habit by name."""
        habit = self.find_habit(name)
        if habit:
            self.habits.remove(habit)
            return True
        return False

    def reset_all_streaks(self):
        """Clear all habits' completion data and streaks."""
        for habit in self.habits:
            habit.streak = 0
            habit.completion_dates = []


# === Analytics Class ===
class Analytics:
    @staticmethod
    def get_longest_streak(tracker):
        """Return the habit with the longest streak."""
        if not tracker.habits:
            return None
        return max(tracker.habits, key=lambda x: x.streak)


# === Utility to Get Icon Path (Compatible with PyInstaller) ===
def get_icon_path(filename="icon.ico"):
    if getattr(sys, "frozen", False):  # Running as a bundled exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


# === GUI Creation Function ===
def create_habit_tracker_gui():
    app = ttkb.Window(title="Habit Tracker", themename="cosmo")

    # Set icon for both title bar and taskbar (if possible)
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        try:
            app.iconbitmap(icon_path)
        except Exception as e:
            print("Icon load failed:", e)

    app.geometry("600x650")
    app.minsize(400, 500)
    app.resizable(True, True)

    tracker = HabitTracker()
    analytics = Analytics()

    # === Scrollable Main Frame ===
    main_frame = ttkb.Frame(app, padding=10)
    main_frame.pack(fill=BOTH, expand=YES)

    canvas = ttkb.Canvas(main_frame, highlightthickness=0)
    scrollbar = ttkb.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=YES)

    content_frame = ttkb.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Scroll & resize logic
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    content_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # === Header ===
    ttkb.Label(content_frame, text="📋 Habit Tracker", font=("Helvetica", 20, "bold")).pack(pady=20)

    # === Habit Input Section ===
    input_frame = ttkb.Frame(content_frame)
    input_frame.pack(pady=10)

    ttkb.Label(input_frame, text="Habit Name:").pack()
    name_entry = ttkb.Entry(input_frame, width=40, justify="center")
    name_entry.pack(pady=5)

    ttkb.Label(input_frame, text="Periodicity:").pack()
    periodicity_choice = ttkb.Combobox(
        input_frame, values=["daily", "weekly"], state="readonly", width=38, justify="center"
    )
    periodicity_choice.set("daily")
    periodicity_choice.pack(pady=10)

    # === Button Functions ===
    def add_habit():
        name = name_entry.get().strip()
        periodicity = periodicity_choice.get()
        if not name:
            messagebox.showerror("Error", "Habit name required.")
            return
        if tracker.add_habit(name, periodicity):
            messagebox.showinfo("Success", f"Habit '{name}' added.")
        else:
            messagebox.showerror("Error", "Invalid input or habit already exists.")

    def complete_habit():
        name = name_entry.get().strip()
        habit = tracker.find_habit(name)
        if habit and habit.mark_completed():
            messagebox.showinfo("Success", f"Habit '{name}' marked as completed.")
        else:
            messagebox.showerror("Error", "Habit not found or already completed today.")

    def delete_habit():
        name = name_entry.get().strip()
        if tracker.delete_habit(name):
            messagebox.showinfo("Deleted", f"Habit '{name}' deleted.")
        else:
            messagebox.showerror("Error", "Habit not found.")

    def list_habits():
        list_win = ttkb.Toplevel(app)
        list_win.title("Your Habits")
        list_win.geometry("320x400")
        frame = ttkb.Frame(list_win, padding=10)
        frame.pack(fill=BOTH, expand=True)

        if not tracker.habits:
            ttkb.Label(frame, text="No habits yet.").pack()
        else:
            for habit in tracker.habits:
                rate = habit.get_completion_rate()
                ttkb.Label(
                    frame,
                    text=f"{habit.name} ({habit.periodicity})\nStreak: {habit.streak} | Completion: {rate}%",
                    justify=LEFT
                ).pack(pady=5, anchor=W)

    def show_longest_streak():
        habit = analytics.get_longest_streak(tracker)
        if habit:
            messagebox.showinfo("Longest Streak", f"{habit.name}: {habit.streak} {'day' if habit.periodicity == 'daily' else 'week'} streak")
        else:
            messagebox.showinfo("Info", "No habits available.")

    def reset_streaks():
        tracker.reset_all_streaks()
        messagebox.showinfo("Reset", "All streaks and completions reset.")

    def analyze_habits():
        analysis_win = ttkb.Toplevel(app)
        analysis_win.title("📊 Habit Analysis")
        analysis_win.geometry("350x300")
        frame = ttkb.Frame(analysis_win, padding=15)
        frame.pack(fill=BOTH, expand=True)

        if not tracker.habits:
            ttkb.Label(frame, text="No habits to analyze.").pack(pady=20)
            return

        top = analytics.get_longest_streak(tracker)
        if top:
            ttkb.Label(frame, text=f"🏆 Top Habit:\n{top.name}", font=("Helvetica", 14, "bold")).pack(pady=10)
            ttkb.Label(frame, text=f"🔥 Streak: {top.streak}").pack()

        ttkb.Label(frame, text="📈 Completion Rates", font=("Helvetica", 12, "underline")).pack(pady=(15, 5))
        for habit in tracker.habits:
            rate = habit.get_completion_rate()
            ttkb.Label(frame, text=f"{habit.name} ({habit.periodicity}) → {rate}%", justify=LEFT).pack(anchor=W)

    # === Action Buttons ===
    actions = [
        ("➕ Add Habit", add_habit),
        ("✅ Complete Habit", complete_habit),
        ("🗑️ Delete Habit", delete_habit),
        ("📋 List Habits", list_habits),
        ("📈 Longest Streak", show_longest_streak),
        ("📊 Analyze Habits", analyze_habits),
        ("🔄 Reset All", reset_streaks),
    ]

    for text, cmd in actions:
        ttkb.Button(content_frame, text=text, command=cmd, bootstyle="primary", width=25).pack(pady=6, ipadx=6, ipady=6)

    # Start main event loop
    app.mainloop()


# === Main Entry Point ===
if __name__ == "__main__":
    create_habit_tracker_gui()
