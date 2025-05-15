class Player:

    def __init__(self, name, selected_five, score):
        self.name = name
        self.selected_five = selected_five
        self.score = score

    def update_score(self, leaderboard):
        self.score = 0
        for player_name in self.selected_five:
            self.score += self.get_int(leaderboard[player_name])

    @staticmethod
    def get_int(score):
        try:
            if int(score):
                return int(score)
        except ValueError:
            return 0

        return 0

