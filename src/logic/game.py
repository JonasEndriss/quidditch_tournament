import random
from src.logic.stats import Stats

class Game:
    def __init__(self, team_one, team_two, verbose=False, snitch_probability = 0.02):
        self.team_one = team_one
        self.team_two = team_two
        self.snitch_probability = snitch_probability
        self.round_counter = 0
        self.snitch_appeared = 0
        self.game_over = False
        self.team_one_stats = Stats()
        self.team_two_stats = Stats()
        self.winner = None
        self.team_caught_snitch = None
        self.verbose = verbose

    def play(self):
        if not self.game_over:
            while not self.game_over:
                while random.randint(1, 100) < 100 - self.snitch_probability * 100:
                    self._play_round()
                    self.round_counter += 1
                self._snitch_appears()

    @staticmethod
    def _duel(player_one_skill, player_two_skill):
        challenge_level_for_one = 100 * (0.5 - 0.1 * (player_one_skill - player_two_skill))
        return random.randint(1, 100) >= challenge_level_for_one

    def _shoot_at_goal(self, attacking_team, attacking_team_stats, defending_team, defending_team_stats):
        if self._duel(attacking_team.hunter_skill, defending_team.keeper_skill):
            print(f"Tooor für {attacking_team.name}") if self.verbose else None
            attacking_team_stats.score += 10
            attacking_team_stats.hunter_goals += 1
        else:
            print(f"Hüter {defending_team.name} hält") if self.verbose else None
            defending_team_stats.keeper_block += 1

    def _handle_attack(self, attacking_team, attacking_team_stats, defending_team, defending_team_stats, verbose=False):
        if self._duel(attacking_team.chaser_skill, defending_team.chaser_skill):
            print(f"Treiber {attacking_team.name} schlagen Klatscher") if self.verbose else None
            attacking_team_stats.chaser_hit_ball += 1
            if self._duel(attacking_team.chaser_skill, defending_team.keeper_skill):
                print(
                    f"Hüter {defending_team.name} wird ausgeschaltet!, Toor für {attacking_team.name}") if self.verbose else None
                attacking_team_stats.score += 10
                attacking_team_stats.hunter_goals += 1
                attacking_team_stats.chaser_hits_person += 1
            else:
                print(f"Hüter {defending_team.name} weicht Klatscher aus, und ... ") if self.verbose else None
                defending_team_stats.keeper_evade += 1
                self._shoot_at_goal(attacking_team, attacking_team_stats, defending_team, defending_team_stats)
        else:
            print(f"Treiber {defending_team.name} schlagen Klatscher") if self.verbose else None
            defending_team_stats.chaser_hit_ball += 1
            if self._duel(attacking_team.hunter_skill, defending_team.chaser_skill):
                print(f"aaaber, Jäger {attacking_team.name} wird vom Besen gehaun") if self.verbose else None
                defending_team_stats.chaser_hits_person += 1
                defending_team_stats.chaser_blocks_goal += 1
            else:
                print(f"Jäger {attacking_team.name} weicht aus, holen zum Wurf aus und ... ") if self.verbose else None
                attacking_team_stats.hunter_evade += 1
                self._shoot_at_goal(attacking_team, attacking_team_stats, defending_team, defending_team_stats)

    def _finish_game(self):
        if self.team_one_stats.score > self.team_two_stats.score:
            self.winner = self.team_one
        elif self.team_one_stats.score < self.team_two_stats.score:
            self.winner = self.team_two
        else:
            self.winner = None

        self.game_over = True
        if self.winner:
            self.winner.wins += 1
            if self.team_caught_snitch == self.winner:
                self.winner.wins_with_snitch += 1
            else:
                self.winner.wins_without_snitch += 1
                self.team_caught_snitch.loses_with_snitch += 1
        self.team_one.games_played += 1
        self.team_two.games_played += 1
        self.team_one.overall_stats.__add__(self.team_one_stats)
        self.team_two.overall_stats.__add__(self.team_two_stats)
        self.team_one.games_played_stats.append(self.team_one_stats)
        self.team_two.games_played_stats.append(self.team_two_stats)

    def _catch_snitch(self, attacking_team, attacking_team_stats, defending_team, defending_team_stats):
        if self._duel(attacking_team.chaser_skill, defending_team.chaser_skill):
            print(f"{attacking_team.name} findet den Schnatz!") if self.verbose else None
            attacking_team_stats.score += 150
            self.team_caught_snitch = attacking_team
            self._finish_game()
        elif self._duel(attacking_team.seeker_skill, defending_team.chaser_skill):
            print(f"{attacking_team.name} taucht unter Klatscher durch und fängt den Schnatz!") if self.verbose else None
            attacking_team_stats.score += 150
            self.team_caught_snitch = attacking_team
            self._finish_game()
        else:
            print(f"whämm, {attacking_team.name} greift nach Schnatz, doch wird im letzen Moment vom Klatscher daran gehindert") if self.verbose else None
            attacking_team_stats.snitch_missed += 1
            defending_team_stats.snitch_prevented += 1

    def _snitch_appears(self):
        self.snitch_appeared += 1
        if self._duel(self.team_one.seeker_skill, self.team_two.seeker_skill):
            self._catch_snitch(self.team_one, self.team_one_stats, self.team_two, self.team_two_stats)
        else:
            self._catch_snitch(self.team_two, self.team_two_stats, self.team_one, self.team_one_stats)

    def _play_round(self):
        if self._duel(self.team_one.hunter_skill, self.team_two.hunter_skill):
            print(f"Jäger {self.team_one.name} hat den Quaffel") if self.verbose else None
            self.team_one_stats.hunter_wins += 1
            self._handle_attack(self.team_one, self.team_one_stats, self.team_two, self.team_two_stats)
        else:
            if self.verbose:
                print(f"Jäger {self.team_two.name} hat den Quaffel") if self.verbose else None
            self.team_two_stats.hunter_wins += 1
            self._handle_attack(self.team_two, self.team_two_stats, self.team_one, self.team_one_stats)

        # End round
        print(self.team_one_stats.score, " : ", self.team_two_stats.score) if self.verbose else None
        self.round_counter += 1

    def print_end_screen(self):
        if self.game_over:
            print("\n" + "=" * 63)
            print(f"{'Endergebnis':^63}")
            print("=" * 63 + "\n")
            if self.team_one_stats.score > self.team_two_stats.score:
                print(
                    f"{self.team_one.name} gewinnt mit {self.team_one_stats.score} : {self.team_two_stats.score} Punkten!!")
            elif self.team_one_stats.score < self.team_two_stats.score:
                print(
                    f"{self.team_two.name} gewinnt mit {self.team_one_stats.score} : {self.team_two_stats.score} Punkten!!")
            else:
                print(f"Mit {self.team_one_stats.score} : {self.team_two_stats.score} geht es unentschieden aus!")
            print("")
            self.team_one_stats.display_comparison(self.team_two_stats, titles=(self.team_one.name, self.team_two.name))
            print(f"\nBallwechsel: {self.round_counter}")
            print(f"Schnatz erschienen: {self.snitch_appeared}")
            print("\n" + "=" * 63 + "\n")
        else:
            print("Das Spiel ist noch nicht beendet")