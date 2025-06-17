import random

class SnakeAndLadder:
    def __init__(self):
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        self.players = {}
        self.turn_order = []

    def add_player(self, name):
        if name not in self.players:
            self.players[name] = 0
            self.turn_order.append(name)

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self, player):
        input(f"{player}'s turn. Press Enter to roll the dice...")
        roll = self.roll_dice()
        print(f"{player} rolled a {roll}")
        new_position = self.players[player] + roll

        if new_position > 100:
            print(f"{player} cannot move. Needs exact roll to reach 100.")
            return

        if new_position in self.snakes:
            print(f"Oh no! {player} got bitten by a snake and slides from {new_position} to {self.snakes[new_position]}")
            new_position = self.snakes[new_position]
        elif new_position in self.ladders:
            print(f"Yay! {player} climbed a ladder from {new_position} to {self.ladders[new_position]}")
            new_position = self.ladders[new_position]

        self.players[player] = new_position
        print(f"{player} is now at position {new_position}")

    def play(self):
        while True:
            for player in self.turn_order:
                self.move_player(player)
                if self.players[player] == 100:
                    print(f"🎉 {player} wins the game! 🎉")
                    return

if __name__ == '__main__':
    game = SnakeAndLadder()
    num_players = int(input("Enter number of players: "))
    for _ in range(num_players):
        name = input("Enter player name: ")
        game.add_player(name)
    game.play()
