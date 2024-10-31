"""Controller file"""
from src.model import Player, ScoreCard
from src.view import clear_screen, display_message, get_input, only_nums

class YatzyController:
    """Controller class to manage the game flow."""
    def __init__(self):

        clear_screen()
        display_message("Welcome to Yatzy!")

        # Get number of players.
        num_players = int(get_input("Enter number of players: "))

        # Init player_list
        self.players = []

        # Create players
        for i in range(num_players):

            # Get name for each player
            name = get_input(f"Enter name for player {i+1}: ")

            # Add player to player list.
            self.players.append(Player(name))

        
        # Define different score categories
        self.categories = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one_pair", "two_pairs", "three_of_a_kind", "four_of_a_kind",
            "small_straight", "large_straight", "full_house", "chance", "yatzy"
        ]

    # Main game loop
    def play_game(self) -> None:
        """Main game loop for playing Yatzy."""

        # Define how many rounds
        # depending on the amount of
        # categories.
        num_rounds = len(self.categories)

        # Iterating through all rounds
        # for each player.
        for _ in range(num_rounds):

            # Loop through each player
            # so each round.
            for player in self.players:

                # Reset player class
                player.reset()

                # Print who's turn it is.
                display_message(f"\n{player.name}'s turn")

                # Count players rolls
                # since all should have 
                # 3 total throws.
                rolls = 0

                # Check that player
                # hasn't rolled more
                # than 3 times including
                # first roll.
                while rolls < 3:

                    # If we haven't rolled
                    # prior.
                    if rolls == 0:

                        # We unlock all dices
                        player.roll_unlocked()

                    # We still check if 
                    # we've reached max rolls.
                    if rolls < 2:
                        flag = False
                        # Print the result.
                        display_message(f"Roll {rolls+1}: {player.values()}")
                        player.lock_all()
                        while True:
                            lock_input = get_input(
                            "Enter dice numbers to re-roll (e.g., 1 3 5), "\
                            "or press Enter to keep all: "
                            )
                            if lock_input.strip() == '':
                                flag = True
                            try:
                                indices = [num - 1 for num in only_nums(lock_input)]
                                if all(0 < x < 5 for x in indices):
                                    for index in indices:
                                        player.unlock_dice([index+1])
                                    break
                                else:
                                    print("Invalid input! Please try again!")

                            except ValueError:
                                print("Invalid input")
                        player.roll_unlocked()
                        if flag == True:
                            break
                    rolls +=1
                dice_values = player.values()
                display_message(f"Your dice: {dice_values}")
                available_categories = [
                    cat for cat in self.categories if cat not in player.scorecard.scores
                    ]
                display_message(f"Available categories:\n{'\n'.join(available_categories)}\n")
                while True:
                    category = get_input("Select a category to score in: ").lower()
                    if category in available_categories:
                        break
                    else:
                        display_message("Invalid category or already used. Please choose another.")
                score = ScoreCard.calculate_score(dice_values, category)
                player.scorecard.record_scores(category, score)
                display_message(f"Scored {score} points in category '{category}'. " \
                                f"Total score: {player.scorecard.total_score()}")
        display_message("\nGame over! Final scores:")
        max_score = max(player.scorecard.total_score() for player in self.players)
        winners = [
            player.name for player in self.players if player.scorecard.total_score() == max_score
            ]
        for player in self.players:
            display_message(f"{player.name}: {player.scorecard.total_score()} points")
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")
