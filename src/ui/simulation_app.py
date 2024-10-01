import tkinter as tk
from tkinter import messagebox
import numpy as np
import ttkbootstrap as ttk
import threading

from src.logic.team import Team
from src.logic.tournament import Tournament
from src.ui.result_app import ResultApp


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quidditch Tournament")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.teams = []
        self.main_buttons = []

        style = ttk.Style()
        style.configure('TButton', padding=6, relief="flat", borderwidth=0)
        style.map('TButton',
                  background=[('active', '#0052cc'), ('!disabled', '#007bff')],
                  foreground=[('active', 'white'), ('!disabled', 'white')])

        self.header_label = ttk.Label(root, text="Quidditch Tournament", font=("Helvetica", 18, "bold"))
        self.header_label.pack(pady=10)

        self.team_name_frame = ttk.Frame(root)
        self.team_name_frame.pack(pady=5)
        self.team_name_label = ttk.Label(self.team_name_frame, text="Team Name:")
        self.team_name_label.grid(row=0, column=0, padx=5)
        self.team_name_entry = ttk.Entry(self.team_name_frame)
        self.team_name_entry.grid(row=0, column=1, padx=5)

        self.add_team_button = ttk.Button(root, text="Add Team Manually", command=self.add_team, style='TButton')
        self.add_team_button.pack(pady=5)
        self.main_buttons.append(self.add_team_button)

        self.num_teams_frame = ttk.Frame(root)
        self.num_teams_frame.pack(pady=5)
        self.num_teams_label = ttk.Label(self.num_teams_frame, text="Number of Teams:")
        self.num_teams_label.grid(row=0, column=0, padx=5)
        vcmd = (root.register(self.validate_numeric_input), '%P')
        self.num_teams_entry = ttk.Entry(self.num_teams_frame, validate='key', validatecommand=vcmd)
        self.num_teams_entry.grid(row=0, column=1, padx=5)

        self.generate_buttons_frame = ttk.Frame(root)
        self.generate_buttons_frame.pack(pady=5)
        self.generate_teams_one_button = ttk.Button(self.generate_buttons_frame, text="Generate Teams (Method 1)",
                                                    command=self.generate_teams_one, style='TButton')
        self.generate_teams_one_button.grid(row=0, column=0, padx=5)
        self.main_buttons.append(self.generate_teams_one_button)

        self.generate_teams_two_button = ttk.Button(self.generate_buttons_frame, text="Generate Teams (Method 2)",
                                                    command=self.generate_teams_two, style='TButton')
        self.generate_teams_two_button.grid(row=0, column=1, padx=5)
        self.main_buttons.append(self.generate_teams_two_button)

        self.num_matches_frame = ttk.Frame(root)
        self.num_matches_frame.pack(pady=5)
        self.num_matches_label = ttk.Label(self.num_matches_frame, text="Number of Matches:")
        self.num_matches_label.grid(row=0, column=0, padx=5)
        self.num_matches_entry = ttk.Entry(self.num_matches_frame, validate='key', validatecommand=vcmd)
        self.num_matches_entry.insert(0, "1")
        self.num_matches_entry.grid(row=0, column=1, padx=5)

        self.start_tournament_button = ttk.Button(root, text="Start Tournament", command=self.start_tournament,
                                                  style='TButton success')
        self.start_tournament_button.pack(pady=20)
        self.start_tournament_button.config(width=20)
        self.main_buttons.append(self.start_tournament_button)

        self.avg_skill_label = ttk.Label(root, text="Overall Average Skill Level: 0.00")
        self.avg_skill_label.pack(pady=5)

        self.teams_frame = ttk.Frame(root)
        self.teams_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.header_frame = ttk.Frame(self.teams_frame)
        self.header_frame.pack(fill=tk.X)

        headers = ["Team", "Keeper Skill", "Hunter Skill", "Chaser Skill", "Seeker Skill", "Avg Skill", ""]
        column_widths = [20, 14, 14, 14, 14, 12.5, 10]
        for col, (header, width) in enumerate(zip(headers, column_widths)):
            header_label = ttk.Label(self.header_frame, text=header, font=("Helvetica", 10, "bold"))
            header_label.grid(row=0, column=col, sticky="w")
            self.header_frame.grid_columnconfigure(col, minsize=width * 10)

        style = ttk.Style()
        style.configure('Red.TButton', background='red', foreground='white', borderwidth=0, relief='flat')
        style.map('Red.TButton', background=[('active', 'darkred')])

        self.canvas = tk.Canvas(self.teams_frame)
        self.scrollbar = ttk.Scrollbar(self.teams_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.update_teams_listbox()

    def show_progress_bar_window(self):
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Tournament Progress")
        self.progress_window.geometry("400x100")
        self.progress_bar = ttk.Progressbar(self.progress_window, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack(pady=20)
        self.progress_window.protocol("WM_DELETE_WINDOW", self.reset_tournament)

    def start_tournament(self):
        if not self.teams:
            messagebox.showwarning("Warning", "No teams generated!")
            return
        num_matches = int(self.num_matches_entry.get())

        self.disable_buttons()
        self.show_progress_bar_window()

        self.progress_bar['maximum'] = num_matches * len(self.teams) * (len(self.teams) - 1) // 2

        def run_tournament():
            tournament = Tournament(self.teams, num_matches, progress_bar=self.progress_bar)
            tournament.start()
            tournament.display_detailed_results()
            self.show_results(tournament)
            self.enable_buttons()
            self.progress_window.destroy()

        tournament_thread = threading.Thread(target=run_tournament)
        tournament_thread.start()

    def reset_tournament(self):
        for team in self.teams:
            team.reset_stats()
        self.update_teams_listbox()
        self.enable_buttons()
        self.progress_window.destroy()

    def disable_buttons(self):
        for button in self.main_buttons:
            button.config(state='disabled')

    def enable_buttons(self):
        for button in self.main_buttons:
            if button.winfo_exists():
                button.config(state='normal')

    def show_results(self, tournament):
        ResultApp(self.root, tournament, self.main_buttons)

    def validate_numeric_input(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def add_team(self):
        name = self.team_name_entry.get()
        if not name:
            messagebox.showwarning("Warning", "Team name cannot be empty!")
            return
        if any(team.name == name for team in self.teams):
            messagebox.showwarning("Warning", "Team name already exists!")
            return
        keeper_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
        hunter_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
        chaser_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
        seeker_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
        team = Team(name, keeper_skill, hunter_skill, chaser_skill, seeker_skill)
        self.teams.append(team)
        self.update_teams_listbox()

    def generate_teams_one(self):
        num_teams = int(self.num_teams_entry.get())
        new_teams = self._generate_teams(num_teams, method=1)
        self.teams.extend(new_teams)
        self.update_teams_listbox()
        messagebox.showinfo("Info", f"Generated {num_teams} teams using Method 1")

    def generate_teams_two(self):
        num_teams = int(self.num_teams_entry.get())
        new_teams = self._generate_teams(num_teams, method=2)
        self.teams.extend(new_teams)
        self.update_teams_listbox()
        messagebox.showinfo("Info", f"Generated {num_teams} teams using Method 2")

    def _generate_teams(self, num_teams, method):
        teams = []
        overall_skill_average = 0
        start_index = len(self.teams) + 1
        for i in range(num_teams):
            base_name = f"Team_{start_index + i}"
            name = base_name
            count = 1
            while any(team.name == name for team in self.teams):
                name = f"{base_name}_{count}"
                count += 1
            if method == 1:
                keeper_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
                hunter_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
                chaser_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
                seeker_skill = round(np.random.beta(0.5, 0.5) * 10 + 2, 2)
            else:
                keeper_skill = round(np.clip(np.random.normal(10, 2), 0, 20), 2)
                hunter_skill = round(np.clip(np.random.normal(10, 2), 0, 20), 2)
                chaser_skill = round(np.clip(np.random.normal(10, 2), 0, 20), 2)
                seeker_skill = round(np.clip(np.random.normal(10, 2), 0, 20), 2)
            team = Team(name, keeper_skill, hunter_skill, chaser_skill, seeker_skill)
            teams.append(team)
            overall_skill_average += keeper_skill + hunter_skill + chaser_skill + seeker_skill
        print(f"Average skill level of all teams: {round(overall_skill_average / (4 * num_teams), 2)}")
        return teams

    def update_teams_listbox(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        total_skill_sum = 0
        for index, team in enumerate(self.teams):
            team_skill_sum = team.keeper_skill + team.hunter_skill + team.chaser_skill + team.seeker_skill
            team_skill_avg = team_skill_sum / 4
            total_skill_sum += team_skill_sum
            team_info = f"{team.name}"
            team_label = ttk.Label(self.scrollable_frame, text=team_info, padding=(10, 0))
            team_label.grid(row=index * 2, column=0, sticky="w")
            self.scrollable_frame.grid_columnconfigure(0, minsize=20 * 10)

            keeper_label = ttk.Label(self.scrollable_frame, text=f"{team.keeper_skill:.2f}", padding=(10, 0))
            keeper_label.grid(row=index * 2, column=1, sticky="w")
            self.scrollable_frame.grid_columnconfigure(1, minsize=14 * 10)

            hunter_label = ttk.Label(self.scrollable_frame, text=f"{team.hunter_skill:.2f}", padding=(10, 0))
            hunter_label.grid(row=index * 2, column=2, sticky="w")
            self.scrollable_frame.grid_columnconfigure(2, minsize=14 * 10)

            chaser_label = ttk.Label(self.scrollable_frame, text=f"{team.chaser_skill:.2f}", padding=(10, 0))
            chaser_label.grid(row=index * 2, column=3, sticky="w")
            self.scrollable_frame.grid_columnconfigure(3, minsize=14 * 10)

            seeker_label = ttk.Label(self.scrollable_frame, text=f"{team.seeker_skill:.2f}", padding=(10, 0))
            seeker_label.grid(row=index * 2, column=4, sticky="w")
            self.scrollable_frame.grid_columnconfigure(4, minsize=14 * 10)

            avg_label = ttk.Label(self.scrollable_frame, text=f"{team_skill_avg:.2f}", padding=(10, 0))
            avg_label.grid(row=index * 2, column=5, sticky="w")
            self.scrollable_frame.grid_columnconfigure(5, minsize=12.5 * 10)

            remove_button = ttk.Button(self.scrollable_frame, text="X", command=lambda idx=index: self.remove_team(idx),
                                       style='Red.TButton')
            remove_button.grid(row=index * 2, column=6, sticky="e", padx=5)
            self.scrollable_frame.grid_columnconfigure(6, minsize=10 * 10)
            self.main_buttons.append(remove_button)

            if index < len(self.teams) - 1:
                separator = ttk.Separator(self.scrollable_frame, orient='horizontal')
                separator.grid(row=index * 2 + 1, column=0, columnspan=7, sticky='ew', pady=5)

        overall_avg_skill = total_skill_sum / (4 * len(self.teams)) if self.teams else 0
        self.avg_skill_label.config(text=f"Overall Average Skill Level: {overall_avg_skill:.2f}")

    def remove_team(self, index):
        self.teams.pop(index)
        self.update_teams_listbox()