"""Controller file"""
from src.model import Player
from src.view import clear_screen, display_message, get_input, only_nums
from src.methods import Methods


class Controller:
    """Controller class to manage the game flow."""
    def __init__(self, game_type: int):

        clear_screen()
        self.game_type = game_type
        # Init player_list
        self.players = []
        yatzy = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one_pair", "two_pairs", "three_of_a_kind", "four_of_a_kind",
            "small_straight", "large_straight", "full_house", "chance", "yatzy"
        ]
        # Define different score categories
        maxi_yatzy = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one_pair", "two_pairs", "three_pairs", "three_of_a_kind",
            "four_of_a_kind", "five_of_a_kind", "small_straight",
            "large_straight", "full_straight", "full_house", "villa",
            "tower", "chance", "yatzy"
        ]
        self.categories = yatzy if game_type == 0 else maxi_yatzy

    def start_game(self):
        """Start Game (Init Game)"""
        clear_screen()
        display_message("Welcome to Yatzy!\n")
        Methods.read_score()
        # Get number of players.
        while True:
            try:
                num_players = int(get_input("\nEnter number of players: "))
                if num_players > 0:
                    break
                Methods.print_error()
            except ValueError:
                Methods.print_error()

        # Create players
        for i in range(num_players):

            # Get name for each player
            name = get_input(f"Enter name for player {i+1}: ")

            # Add player to player list.
            self.players.append(Player(name, self.game_type))

    def play_game(self) -> None:
        """Main game loop for playing Yatzy."""

        # Define how many rounds
        # depending on the amount of
        # categories.
        num_rounds = len(self.categories)

        # Iterating through all rounds
        # for each player.
        for player_round in range(num_rounds):

            # Loop through each player
            # so each round.
            for player in self.players:

                # Reset player class
                player.reset()

                # Print who's turn it is.
                clear_screen()
                
                removed = False

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
                        clear_screen()
                        display_message(f"Round {player_round+1} Saved rolls: {player.get_roll()}: {player.name}'s turn\n")
                        display_message(f"Roll {rolls+1}: {player.values()}\n")
                        player.lock_all()
                        while True:
                            lock_input = get_input(
                            "Enter dice numbers to re-roll (e.g., 1 3 5), "\
                            "or press Enter to keep all: "
                            )
                            if lock_input.strip() == '':
                                flag = True
                                #player.save_roll(player.rolls)
                                break
                            try:
                                indices = [num - 1 for num in list(set(only_nums(lock_input)))]
                                if len(indices) > 0:
                                    if all(0 <= x < 5 for x in indices):
                                        for index in indices:
                                            player.unlock_dice([index+1])
                                        break
                                Methods.print_error()
                            except ValueError:
                                Methods.print_error()

                        player.roll_unlocked()
                        if flag is True:
                            break

                    rolls += 1
                    
                dice_values = player.values()
                clear_screen()
                display_message(f"Your dice: {dice_values}")

                used_categories = list(player.scorecard.scores.keys())
                eligible_categories = Methods.decide_eligible_categories(self.game_type, dice_values, used_categories, self.categories)

                display_message(
                    "\nEligible categories based on your dice:\n"
                )
                for i in range(0, len(eligible_categories), 2):
                    if i + 1 < len(eligible_categories):
                        display_message(
                            f"{eligible_categories[i]:<15}\t"\
                            f"{eligible_categories[i + 1]:<15}")
                    else:
                        display_message(f"{eligible_categories[i]:<15}")


                while True:
                    category = get_input("\nSelect a category to score in "\
                                         "or type 'x' to dispose category: ").lower()
                    if category in eligible_categories:
                        clear_screen()
                        score = Methods.calculate_score(dice_values, category)
                        player.scorecard.record_scores(category, score)
                        break
                    elif category == "x":
                        removed = True
                        clear_screen()
                        display_message("Categories eligible for removal:\n")

                        not_eligible = [cat for cat in self.categories if cat not
                                        in (eligible_categories + used_categories)]
                        formatted_output = "\n".join(
                            [f"{not_eligible[i]:<15}\t\t{not_eligible[i + 1]:<15}"
                            if i + 1 < len(not_eligible) else f"{not_eligible[i]:<15}"
                            for i in range(0, len(not_eligible), 2)]
                        )
                        display_message(formatted_output)

                        category = get_input("\nWhich category would you like "\
                                                      "to remove: ").lower()
                        if category in self.categories:
                            player.scorecard.record_scores(category, 0)
                            break
                        Methods.print_error()
                    else:
                        Methods.print_error()
                if removed:
                    display_message(f"Category '{category}' removed. " \
                                    f"Total score: {player.scorecard.total_score()}")
                else:
                    display_message(f"Scored {score} points in category '{category}'. " \
                                    f"Total score: {player.scorecard.total_score()}")
                get_input("Press enter to continue...")
                removed = False

        display_message("\nGame over! Final scores:")
        max_score = max(player.scorecard.total_score() for player in self.players)
        winners = []
        for player in self.players:
            if player.scorecard.total_score() == max_score:
                winners.append(player.name)
                Methods.save_score(player.name, max_score)
        for player in self.players:
            display_message(f"{player.name}: {player.scorecard.total_score()} points")
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")
