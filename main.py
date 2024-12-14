import tkinter as tk
from tkinter import ttk, messagebox
import csv
from collections import Counter
from typing import Tuple, List

CSV_FILE = 'street_fighter_results.csv'

def save_result(win_or_loss: str, fighter: str) -> None:
    """Save the result of a match to the CSV file."""
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([win_or_loss, fighter])

def get_results() -> List[List[str]]:
    """Retrieve all results from the CSV file."""
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []

def clear_results() -> None:
    """Clear all results from the CSV file."""
    open(CSV_FILE, 'w').close()

def analyze_results() -> Tuple[str, str]:
    """Analyze the results and return the fighters with the most losses and wins."""
    results = get_results()
    if not results:
        return "No Current Data", "No Current Data"

    wins = [row[1] for row in results if row[0] == 'Win']
    losses = [row[1] for row in results if row[0] == 'Loss']

    if not wins:
        most_wins = "No Current Data"
    else:
        win_count = Counter(wins)
        max_wins = max(win_count.values())
        most_wins = ", ".join([fighter for fighter, count in win_count.items() if count == max_wins])

    if not losses:
        most_losses = "No Current Data"
    else:
        loss_count = Counter(losses)
        max_losses = max(loss_count.values())
        most_losses = ", ".join([fighter for fighter, count in loss_count.items() if count == max_losses])

    return most_losses, most_wins

class TrackerApp:
    """A GUI application for tracking Street Fighter match results."""
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Street Fighter Tracker")

        # Main Screen
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text="Did You Win or Lose?", font=("Arial", 14)).pack(pady=5)
        self.win_loss_var = tk.StringVar()
        tk.Radiobutton(self.main_frame, text="Win", variable=self.win_loss_var, value="Win").pack()
        tk.Radiobutton(self.main_frame, text="Loss", variable=self.win_loss_var, value="Loss").pack()

        tk.Label(self.main_frame, text="Which Fighter Did You Fight Against?", font=("Arial", 14)).pack(pady=5)
        self.fighter_var = tk.StringVar()
        self.fighter_dropdown = ttk.Combobox(self.main_frame, textvariable=self.fighter_var)
        self.fighter_dropdown['values'] = ["Ryu", "Ken", "Chun-Li", "Guile", "Blanka"]
        self.fighter_dropdown.set("Select a Fighter")
        self.fighter_dropdown.pack()

        tk.Button(self.main_frame, text="Submit", command=self.submit_result).pack(pady=5)
        tk.Button(self.main_frame, text="View Results", command=self.show_results_screen).pack(pady=5)

        # Results Screen
        self.results_frame = tk.Frame(self.root)

        self.most_losses_label = tk.Label(self.results_frame, text="Most Losses Against: ", font=("Arial", 14))
        self.most_losses_label.pack(pady=5)

        self.most_wins_label = tk.Label(self.results_frame, text="Most Wins Against: ", font=("Arial", 14))
        self.most_wins_label.pack(pady=5)

        tk.Button(self.results_frame, text="Clear Results", command=self.clear_results).pack(pady=5)
        tk.Button(self.results_frame, text="Return", command=self.show_main_screen).pack(pady=5)

    def submit_result(self) -> None:
        """Handle the submission of match results."""
        win_or_loss = self.win_loss_var.get()
        fighter = self.fighter_var.get()

        if not win_or_loss or fighter == "Select a Fighter":
            messagebox.showerror("Error", "Please select win/loss and a fighter.")
            return

        save_result(win_or_loss, fighter)
        messagebox.showinfo("Success", "Result saved successfully!")
        self.win_loss_var.set("")
        self.fighter_var.set("Select a Fighter")

    def show_results_screen(self) -> None:
        """Display the results screen."""
        most_losses, most_wins = analyze_results()
        self.most_losses_label.config(text=f"Most Losses Against: {most_losses}")
        self.most_wins_label.config(text=f"Most Wins Against: {most_wins}")

        self.main_frame.pack_forget()
        self.results_frame.pack(fill="both", expand=True)

    def clear_results(self) -> None:
        """Clear all stored match results."""
        clear_results()
        self.most_losses_label.config(text="Most Losses Against: No Current Data")
        self.most_wins_label.config(text="Most Wins Against: No Current Data")
        messagebox.showinfo("Success", "Results cleared successfully!")

    def show_main_screen(self) -> None:
        """Return to the main screen."""
        self.results_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackerApp(root)
    root.mainloop()