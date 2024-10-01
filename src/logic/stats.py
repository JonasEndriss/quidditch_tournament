class Stats:
    def __init__(self):
        self.score = 0
        self.chaser_blocks_goal = 0
        self.keeper_block = 0
        self.chaser_hit_ball = 0
        self.snitch_prevented = 0
        self.snitch_missed = 0
        self.keeper_evade = 0
        self.hunter_evade = 0
        self.hunter_goals = 0
        self.chaser_hits_person = 0
        self.hunter_wins = 0 #Hunter vs Hunter

    def __add__(self, other):
        self.score += other.score
        self.chaser_blocks_goal += other.chaser_blocks_goal
        self.keeper_block += other.keeper_block
        self.chaser_hit_ball += other.chaser_hit_ball
        self.snitch_prevented += other.snitch_prevented
        self.snitch_missed += other.snitch_missed
        self.keeper_evade += other.keeper_evade
        self.hunter_evade += other.hunter_evade
        self.hunter_goals += other.hunter_goals
        self.chaser_hits_person += other.chaser_hits_person
        self.hunter_wins += other.hunter_wins

    def reset_stats(self):
        self.__init__()

    def display(self, title="", width=30):
        print("=" * width)
        if title:
            print(f"{title:^{width}}")
        else:
            print(f"{'Statistik':^{width}}")
        print("=" * width)
        print(f"Punkte: {self.score:<{width - 8}}")
        print(f"Treiber blockiert Tor: {self.chaser_blocks_goal:<{width - 20}}")
        print(f"Hüter blockiert: {self.keeper_block:<{width - 14}}")
        print(f"Treiber trifft Klatscher: {self.chaser_hit_ball:<{width - 21}}")
        print(f"Schnatzfang verhindert: {self.snitch_prevented:<{width - 20}}")
        print(f"Schnatz verpasst: {self.snitch_missed:<{width - 15}}")
        print(f"Hüter weicht aus: {self.keeper_evade:<{width - 15}}")
        print(f"Jäger weicht aus: {self.hunter_evade:<{width - 15}}")
        print(f"Jäger Tore: {self.hunter_goals:<{width - 11}}")
        print(f"Treiber trifft Person: {self.chaser_hits_person:<{width - 20}}")
        print(f"Jäger bekommt Ball: {self.hunter_wins:<{width - 15}}")
        print("=" * width)

    def display_comparison(self, other, titles=None, width=63):
        print("=" * width)
        if titles and titles[0] and titles[1]:
            print(f"{titles[0]:^{width // 2}} | {titles[1]:^{width // 2}}")
        else:
            print(f"{'Statistik':^{width // 2}} | {'Statistik':^{width // 2}}")
        print("=" * width)
        print(f"Punkte: {self.score:<{(width // 2) - 8}} | Punkte: {other.score}")
        print(f"Treiber blockiert Tor: {self.chaser_blocks_goal:<{(width // 2) - 20}} | Treiber blockiert Tor: {other.chaser_blocks_goal}")
        print(f"Hüter blockiert: {self.keeper_block:<{(width // 2) - 14}} | Hüter blockiert: {other.keeper_block}")
        print(f"Treiber trifft Klatscher: {self.chaser_hit_ball:<{(width // 2) - 21}} | Treiber trifft Klatscher: {other.chaser_hit_ball}")
        print(f"Schnatzfang verhindert: {self.snitch_prevented:<{(width // 2) - 20}} | Schnatzfang verhindert: {other.snitch_prevented}")
        print(f"Schnatz verpasst: {self.snitch_missed:<{(width // 2) - 15}} | Schnatz verpasst: {other.snitch_missed}")
        print(f"Hüter weicht aus: {self.keeper_evade:<{(width // 2) - 15}} | Hüter weicht aus: {other.keeper_evade}")
        print(f"Jäger weicht aus: {self.hunter_evade:<{(width // 2) - 15}} | Jäger weicht aus: {other.hunter_evade}")
        print(f"Jäger Tore: {self.hunter_goals:<{(width // 2) - 11}} | Jäger Tore: {other.hunter_goals}")
        print(f"Treiber trifft Person: {self.chaser_hits_person:<{(width // 2) - 20}} | Treiber trifft Person: {other.chaser_hits_person}")
        print(f"Jäger bekommt Ball: {self.hunter_wins:<{(width // 2) - 15}} | Jäger bekommt Ball: {other.hunter_wins}")
        print("=" * width)