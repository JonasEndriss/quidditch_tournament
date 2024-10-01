import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResultApp:
    def __init__(self, parent, tournament, main_buttons):
        self.heatmap_window = None
        self.pair_plot_window = None
        self.tournament = tournament
        self.main_buttons = main_buttons
        self.window = tk.Toplevel(parent)
        self.window.title("Tournament Results")
        self.window.geometry("1800x600")

        for button in self.main_buttons:
            button.config(state=tk.DISABLED)

        self.window.protocol("WM_DELETE_WINDOW", self.reset_tournament)

        self.console_text = tk.Text(self.window, height=15, font=("Courier", 10))
        self.console_text.pack(fill=tk.BOTH, expand=True)
        self.console_text.insert(tk.END, self.tournament.get_console_output())

        self.plot_frame = tk.Frame(self.window)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        self.save_tournament_button = tk.Button(self.window, text="Save Tournament", command=self.save_tournament)
        self.save_tournament_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_plots_button = tk.Button(self.window, text="Save Plots", command=self.save_plots)
        self.save_plots_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_tournament)
        self.reset_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.display_plots()

    def display_plots(self):
        data = []
        for team in self.tournament.teams:
            data.append({
                'Team': team.name,
                'Keeper Skill': team.keeper_skill,
                'Hunter Skill': team.hunter_skill,
                'Chaser Skill': team.chaser_skill,
                'Seeker Skill': team.seeker_skill,
                'Win Rate': team.wins / team.games_played if team.games_played > 0 else 0
            })

        df = pd.DataFrame(data)

        self.pair_plot_window = tk.Toplevel(self.window)
        self.pair_plot_window.title("Pair Plot")
        self.pair_plot_window.geometry("1100x860")
        pair_plot = sns.pairplot(df, vars=['Keeper Skill', 'Hunter Skill', 'Chaser Skill', 'Seeker Skill', 'Win Rate'],
                                 diag_kind='kde')
        pair_plot.fig.set_size_inches(12, 8)
        pair_plot.fig.set_dpi(60)
        pair_plot.fig.tight_layout()
        for ax in pair_plot.axes.flatten():
            ax.tick_params(labelsize=8)
        pair_plot_canvas = FigureCanvasTkAgg(pair_plot.fig, master=self.pair_plot_window)
        pair_plot_canvas.draw()
        pair_plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.pair_plot_window.update_idletasks()

        self.pair_plot_window.geometry("1101x861")
        self.pair_plot_window.update()
        self.pair_plot_window.geometry("1100x860")

        self.heatmap_window = tk.Toplevel(self.window)
        self.heatmap_window.title("Correlation Heatmap")
        heatmap_fig, ax = plt.subplots(figsize=(8, 6))
        corr = df[['Keeper Skill', 'Hunter Skill', 'Chaser Skill', 'Seeker Skill', 'Win Rate']].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
        heatmap_fig.suptitle('Correlation Heatmap of Skill Levels and Win Rate')
        heatmap_canvas = FigureCanvasTkAgg(heatmap_fig, master=self.heatmap_window)
        heatmap_canvas.draw()
        heatmap_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_tournament(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            self.tournament.save_results(file_path)
            messagebox.showinfo("Info", "Tournament results saved!")

    def save_plots(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            plt.savefig(file_path)
            messagebox.showinfo("Info", "Plots saved!")

    def reset_tournament(self):
        self.window.destroy()
        self.pair_plot_window.destroy()
        self.heatmap_window.destroy()

        for team in self.tournament.teams:
            team.reset_stats()
        self.tournament.results = []

        for button in self.main_buttons:
            button.config(state=tk.NORMAL)

        messagebox.showinfo("Info", "Tournament and team stats have been reset!")