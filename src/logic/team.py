from src.logic.stats import Stats

class Team:
    def __init__(self, name, keeper_skill, hunter_skill, chaser_skill, seeker_skill):
        self.name = name
        self.keeper_skill = keeper_skill
        self.hunter_skill = hunter_skill
        self.chaser_skill = chaser_skill
        self.seeker_skill = seeker_skill
        self.games_played_stats = []
        self.overall_stats = Stats()
        self.wins = 0
        self.wins_with_snitch = 0
        self.wins_without_snitch = 0
        self.loses_with_snitch = 0
        self.games_played = 0

    def display_player_skill(self):
        print(f"Average Skill: {(self.keeper_skill + self.hunter_skill + self.chaser_skill + self.seeker_skill) / 4}")
        print(f"Keeper Skill: {self.keeper_skill}")
        print(f"Hunter Skill: {self.hunter_skill}")
        print(f"Chaser Skill: {self.chaser_skill}")
        print(f"Seeker Skill: {self.seeker_skill}")

    def reset_stats(self):
        self.games_played_stats = []
        self.overall_stats = Stats()
        self.wins = 0
        self.wins_with_snitch = 0
        self.wins_without_snitch = 0
        self.loses_with_snitch = 0
        self.games_played = 0