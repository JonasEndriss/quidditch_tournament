import pickle
import time
from tqdm import tqdm
from src.logic.game import Game
from src.ui.elements.tqdm_tk import TqdmTk


class Tournament:
    def __init__(self, teams, games_per_match_up, progress_bar=None):
        self.teams = teams
        self.results = []
        self.games_per_match_up = games_per_match_up
        self.progress_bar = progress_bar

    def _play_game(self, team_one, team_two, pbar):
        game = Game(team_one, team_two, False)
        game.play()
        self.results.append((team_one.name, team_two.name, game.winner.name if game.winner else "Draw"))
        pbar.update(1)

    def start(self):
        start_time = time.time()
        total_games = self.games_per_match_up * len(self.teams) * (len(self.teams) - 1) // 2
        with TqdmTk(total=total_games, desc="Playing Games", tk_progress_bar=self.progress_bar) as pbar:
            for _ in range(self.games_per_match_up):
                for i in range(len(self.teams)):
                    for j in range(i + 1, len(self.teams)):
                        self._play_game(self.teams[i], self.teams[j], pbar)
        print(f"Time taken: {time.time() - start_time:.2f} seconds")

    @staticmethod
    def _display_team_stats(team):
        average_score = team.overall_stats.score / len(team.games_played_stats) if team.games_played_stats else 0
        team.overall_stats.display(title=f'{team.name} - Wins: {team.wins}', width=50)
        print(f"Snitch Caught Wins: {team.wins_with_snitch:<3} Snitch Caught Losses: {team.loses_with_snitch:<3}")
        print(f"Average Score: {average_score:<8.2f} Games Played: {team.games_played:<3}")
        team.display_player_skill()
        print("-" * 50 + "\n")

    def display_detailed_results(self):
       print(self.get_console_output())

    def get_console_output(self):
        output = []
        sorted_teams = sorted(self.teams, key=lambda team: team.wins, reverse=True)

        output.append("\n" + "=" * 167)
        output.append(f"{'Detailed Team Statistics':^167}")
        output.append("=" * 167)
        output.append(
            f"{'Team':<15}|{'Avg Score':<10}|{'Wins':<10}|{'Wins w/ Snitch':<15}|{'Wins w/o Snitch':<15}|{'Losses w/ Snitch':<16}|{'Games Played':<15}|{'Keeper Skill':<15}|{'Hunter Skill':<15}|{'Chaser Skill':<15}|{'Seeker Skill':<15}|")
        output.append("=" * 167)
        for team in sorted_teams:
            average_score = round(team.overall_stats.score / len(team.games_played_stats), 2) if team.games_played_stats else 0
            output.append(
                f"{team.name:<15}|{average_score:<10}|{team.wins:<10}|{team.wins_with_snitch:<15}|{team.wins_without_snitch:<15}|{team.loses_with_snitch:<16}|{team.games_played:<15}|{team.keeper_skill:<15}|{team.hunter_skill:<15}|{team.chaser_skill:<15}|{team.seeker_skill:<15}|")
        output.append("=" * 167)

        return "\n".join(output)

    def save_results(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.results, file)

    def load_results(self, filename):
        with open(filename, "rb") as file:
            self.results = pickle.load(file)