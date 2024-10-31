from model import Player, ScoreCard
from view import clear_screen, display_message, get_input, only_nums

class YatzyController:
    """Controller class to manage the game flow."""
    def __init__(self):
        clear_screen()
        display_message("Welcome to Yatzy!")
        num_players = int(get_input("Enter number of players: "))
        self.players = []
        for i in range(num_players):
            name = get_input(f"Enter name for player {i+1}: ")
            self.players.append(Player(name))
        self.categories = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one_pair", "two_pairs", "three_of_a_kind", "four_of_a_kind",
            "small_straight", "large_straight", "full_house", "chance", "yatzy"
        ]

    def play_game(self) -> None:
        """Main game loop for playing Yatzy."""
        num_rounds = len(self.categories)
        for _ in range(num_rounds):
            for player in self.players:
                player.reset()
                display_message(f"\n{player.name}'s turn")
                rolls = 0
                while rolls < 3:
                    if rolls == 0:
                        player.roll_unlocked()
                    if rolls < 2:
                        display_message(f"Roll {rolls+1}: {player.values()}")
                        lock_input = get_input("Enter dice numbers to re-roll (e.g., 1 3 5), or press Enter to keep all: ")
                        if lock_input.strip() == '':
                            break
                        indices = [num - 1 for num in only_nums(lock_input)]
                        player.unlock_all()
                        player.lock_all()
                        for index in indices:
                            if 0 <= index < 5:
                                player.unlock_dice([index+1])
                        player.roll_unlocked()
                    rolls +=1
                dice_values = player.values()
                display_message(f"Your dice: {dice_values}")
                available_categories = [cat for cat in self.categories if cat not in player.scorecard.scores]
                display_message(f"Available categories:\n\n{'\n'.join(available_categories)}\n")
                while True:
                    category = get_input("Select a category to score in: ").lower()
                    if category in available_categories:
                        break
                    else:
                        display_message("Invalid category or already used. Please choose another.")
                score = ScoreCard.calculate_score(dice_values, category)
                player.scorecard.record_scores(category, score)
                display_message(f"Scored {score} points in category '{category}'. Total score: {player.scorecard.total_score()}")
        display_message("\nGame over! Final scores:")
        max_score = max(player.scorecard.total_score() for player in self.players)
        winners = [player.name for player in self.players if player.scorecard.total_score() == max_score]
        for player in self.players:
            display_message(f"{player.name}: {player.scorecard.total_score()} points")
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")
