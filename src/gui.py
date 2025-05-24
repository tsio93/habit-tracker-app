import tkinter as tk
from tkinter import messagebox
from tracker import HabitTracker
from data_manager import DataManager
import analytics
from datetime import datetime
from PIL import Image, ImageTk

def main():
    tracker = HabitTracker()
    tracker.habits = DataManager.load_data()

    # === Theme Colors & Fonts ===
    bg = "#EEF4FB"
    card_bg = "#FFFFFF"
    accent = "#4A90E2"
    text_dark = "#1C1C1E"

    font_heading = ("Helvetica", 18, "bold")
    font_subheading = ("Helvetica", 14)
    font_main = ("Helvetica", 11)

    button_style = {
        "font": font_main,
        "bg": "white",
        "fg": accent,
        "activebackground": "#DDEEFF",
        "relief": "groove",
        "borderwidth": 1,
        "padx": 10,
        "pady": 6,
        "width": 22
    }

    # === Root Window ===
    root = tk.Tk()
    root.title("Habit Tracker")
    root.geometry("520x600")
    root.configure(bg=bg)

    try:
        root.iconbitmap("logo.ico")
    except:
        pass

    # === Scrollable Canvas ===
    canvas = tk.Canvas(root, bg=bg, highlightthickness=0)
    canvas.pack(side="top", fill="both", expand=True)

    v_scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    v_scrollbar.pack(side="right", fill="y")

    h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    h_scrollbar.pack(side="bottom", fill="x")

    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    main_frame = tk.Frame(canvas, bg=bg)
    window_id = canvas.create_window((0, 0), window=main_frame, anchor="n")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    main_frame.bind("<Configure>", on_frame_configure)

    def resize_main_frame(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_main_frame)

    # === Title and Logo ===
    tk.Label(main_frame, text="Habit Tracker", font=font_heading, bg=bg, fg=text_dark).pack(pady=(20, 5))
    try:
        img = Image.open("logo.png")
        img = img.resize((120, 120))
        root.logo_img = ImageTk.PhotoImage(img)
        tk.Label(main_frame, image=root.logo_img, bg=bg).pack(pady=(0, 20))
    except:
        pass

    # === Add Habit Card ===
    card = tk.Frame(main_frame, bg=card_bg, padx=15, pady=15, relief="ridge", borderwidth=1)
    card.pack(pady=10)

    tk.Label(card, text="Add Habit", font=font_subheading, bg=card_bg, fg=text_dark).grid(row=0, column=0, columnspan=2, pady=(0, 10))
    tk.Label(card, text="Name:", font=font_main, bg=card_bg, fg=text_dark).grid(row=1, column=0, sticky="e")
    name_entry = tk.Entry(card, width=26)
    name_entry.grid(row=1, column=1, pady=5, sticky="w")

    tk.Label(card, text="Frequency:", font=font_main, bg=card_bg, fg=text_dark).grid(row=2, column=0, sticky="e", pady=(10, 0))
    freq_var = tk.StringVar(value="")
    freq_frame = tk.Frame(card, bg=card_bg)
    freq_frame.grid(row=2, column=1, pady=(10, 0), sticky="w")

    def select_freq(value):
        freq_var.set(value)
        daily_btn.config(bg=accent if value == "daily" else "white", fg="white" if value == "daily" else accent)
        weekly_btn.config(bg=accent if value == "weekly" else "white", fg="white" if value == "weekly" else accent)

    daily_btn = tk.Button(freq_frame, text="Daily", command=lambda: select_freq("daily"), font=font_main, width=10, relief="ridge", bg="white", fg=accent, borderwidth=1)
    daily_btn.pack(side="left", padx=5)

    weekly_btn = tk.Button(freq_frame, text="Weekly", command=lambda: select_freq("weekly"), font=font_main, width=10, relief="ridge", bg="white", fg=accent, borderwidth=1)
    weekly_btn.pack(side="left", padx=5)

    def add_habit():
        name = name_entry.get().strip()
        periodicity = freq_var.get()
        if not name or periodicity not in ["daily", "weekly"]:
            messagebox.showerror("Error", "Please enter name and frequency.")
            return
        tracker.add_habit(name, periodicity)
        DataManager.save_data(tracker.get_habits())
        messagebox.showinfo("Success", f"Added '{name}' as {periodicity}.")
        name_entry.delete(0, tk.END)
        freq_var.set("")
        select_freq("")

    tk.Button(card, text="Add ➕", command=add_habit, **button_style).grid(row=4, column=0, columnspan=2, pady=15)

    # === Functional Buttons ===
    def show_habits():
        habits = tracker.get_habits()
        if not habits:
            messagebox.showinfo("No habits", "You have no habits yet.")
            return
        win = tk.Toplevel(root, bg=bg)
        win.title("Your Habits")
        for h in habits:
            text = f"{h.name} ({h.periodicity}) — Streak: {h.get_streak()}"
            tk.Label(win, text=text, font=font_main, bg=bg, fg=text_dark).pack(anchor="w", padx=20, pady=4)

    def complete_habit():
        habits = tracker.get_habits()
        if not habits:
            messagebox.showinfo("No habits", "Nothing to complete.")
            return
        win = tk.Toplevel(root, bg=bg)
        win.title("Complete Habit")
        selected = tk.StringVar(value=habits[0].name)
        tk.Label(win, text="Select a habit", font=font_subheading, bg=bg, fg=text_dark).pack(pady=10)
        tk.OptionMenu(win, selected, *[h.name for h in habits]).pack(pady=5)
        def mark():
            tracker.find_habit(selected.get()).mark_completed()
            DataManager.save_data(tracker.get_habits())
            messagebox.showinfo("Done", f"Marked '{selected.get()}' as complete.")
            win.destroy()
        tk.Button(win, text="Mark Completed", command=mark, **button_style).pack(pady=10)

    def analyze_habits():
        longest = analytics.get_longest_streak(tracker)
        if longest:
            s = longest.get_streak()
            messagebox.showinfo("Longest Streak", f"🌟 '{longest.name}' — {s} days")
        else:
            messagebox.showinfo("No streaks", "No data to analyze.")

    def delete_habit():
        habits = tracker.get_habits()
        if not habits:
            messagebox.showinfo("No habits", "Nothing to delete.")
            return
        win = tk.Toplevel(root, bg=bg)
        win.title("Delete Habit")
        selected = tk.StringVar(value=habits[0].name)
        tk.Label(win, text="Select a habit", font=font_subheading, bg=bg, fg=text_dark).pack(pady=10)
        tk.OptionMenu(win, selected, *[h.name for h in habits]).pack(pady=5)
        def delete():
            tracker.delete_habit(selected.get())
            DataManager.save_data(tracker.get_habits())
            messagebox.showinfo("Deleted", f"Habit '{selected.get()}' removed.")
            win.destroy()
        tk.Button(win, text="Delete", command=delete, **button_style).pack(pady=10)

    def reset_streaks():
        if messagebox.askyesno("Reset All", "Reset all streaks?"):
            for h in tracker.get_habits():
                h.completion_dt = []
            DataManager.save_data(tracker.get_habits())
            messagebox.showinfo("Reset", "Streaks reset.")

    def view_history():
        habits = tracker.get_habits()
        if not habits:
            messagebox.showinfo("Empty", "No habits available.")
            return
        win = tk.Toplevel(root, bg=bg)
        win.title("History")
        for h in habits:
            tk.Label(win, text=h.name, font=font_subheading, bg=bg, fg=text_dark).pack(anchor="w", padx=20, pady=(10, 0))
            if h.completion_dt:
                for dt in h.completion_dt:
                    tk.Label(win, text=f"• {dt}", font=font_main, bg=bg, fg=text_dark).pack(anchor="w", padx=40)
            else:
                tk.Label(win, text="• No completions", font=font_main, bg=bg, fg="#888").pack(anchor="w", padx=40)

    def view_completion_rate():
        habits = tracker.get_habits()
        if not habits:
            messagebox.showinfo("No habits", "Nothing to analyze.")
            return
        win = tk.Toplevel(root, bg=bg)
        win.title("Completion Rates")
        for h in habits:
            created = datetime.fromisoformat(h.creation_dt).date()
            today = datetime.now().date()
            total = (today - created).days + 1
            completed = len(set(datetime.fromisoformat(d).date() for d in h.completion_dt))
            rate = round((completed / total) * 100, 2) if total > 0 else 0
            msg = f"{h.name}: {rate}% ({completed}/{total} days)"
            tk.Label(win, text=msg, font=font_main, bg=bg, fg=text_dark).pack(anchor="w", padx=20, pady=4)

    # === Features Buttons ===
    features = [
        ("📄 View Habits", show_habits),
        ("✅ Complete", complete_habit),
        ("📊 Analyze", analyze_habits),
        ("🗑 Delete", delete_habit),
        ("🔁 Reset", reset_streaks),
        ("📅 History", view_history),
        ("🧮 Completion Rate", view_completion_rate),
    ]

    for label, func in features:
        tk.Button(main_frame, text=label, command=func, **button_style).pack(pady=6)

    root.mainloop()

if __name__ == "__main__":
    main()
