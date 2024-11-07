"""Controller file"""
from src.model import Player
from src.methods import print_error, clear_screen, display_message, read_score, get_input, only_nums
from src.methods import decide_eligible_categories, calculate_score, save_score, print_cat


class Controller:
    """Controller class to manage the game flow."""
    def __init__(self, game_type: int):

        self.game_type = game_type
        # Init player_list
        self.players = []
        yatzy = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one pair", "two pairs", "three of a kind", "four of a kind",
            "small straight", "large straight", "full house", "chance", "yatzy"
        ]
        # Define different score categories
        maxi_yatzy = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one pair", "two pairs", "three pairs", "three of a kind",
            "four of a kind", "five of a kind", "small straight",
            "large straight", "full straight", "full house", "villa",
            "tower", "chance", "yatzy"
        ]
        self.categories = yatzy if game_type == 1 else maxi_yatzy

    def start_game(self):
        """Start Game (Init Game)"""
        clear_screen()
        if self.game_type == 1:
            display_message("Welcome to Yatzy!\n")
        elif self.game_type == 2:
            display_message("Welcome to MaxiYatzy!\n")
        read_score(3)
        # Get number of players.
        while True:
            try:
                num_players = int(get_input("\nEnter number of players: "))
                if num_players > 0:
                    break
                print_error()
            except ValueError:
                print_error()

        # Create players
        for i in range(num_players):

            # Get name for each player
            name = get_input(f"Enter name for player {i+1}: ").capitalize()

            # Add player to player list.
            self.players.append(Player(name, self.game_type, self.categories))

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

                # Count players rolls
                # since all should have
                # 3 total throws.
                rolls = 3
                count_rolls = 0
                

                # Check that player
                # hasn't rolled more
                # than 3 times including
                # first roll.
                while rolls > 0:
                    rolls -= 1
                    count_rolls += 1
                    # If we haven't rolled
                    # prior.
                    if count_rolls == 1:

                        # We unlock all dices
                        player.roll_unlocked()

                    # We still check if
                    # we've reached max rolls.
                    if rolls >= 1:
                        flag = False
                        # Print the result.
                        clear_screen()
                        display_message((f"Round {player_round+1} Rerolls left: {rolls} {player.name}'s turn\n"))
                        display_message(f"Roll {count_rolls}: {player.values()}\n")
                        player.lock_all()
                        while True:
                            lock_input = get_input(
                            "Enter dice numbers to re-roll (e.g., 1 3 5), "\
                            "or press Enter to keep all: "
                            )
                            if lock_input.strip() == '':
                                flag = True
                                if self.game_type == 2:
                                    player.save_roll(player.get_roll()+rolls)
                                break
                            try:
                                indices = [num - 1 for num in list(set(only_nums(lock_input)))]
                                if len(indices) > 0:
                                    if all(0 <= x < 5 for x in indices) and self.game_type == 1:
                                        for index in indices:
                                            player.unlock_dice([index+1])
                                        break
                                    if all(0 <= x < 6 for x in indices) and self.game_type == 2:
                                        for index in indices:
                                            player.unlock_dice([index+1])
                                        break
                                print_error()
                            except ValueError:
                                print_error()

                        player.roll_unlocked()
                        if flag is True:
                            break

                    display_message(f"Your dice: {player.values()}")

                    if rolls == 0 and self.game_type == 2 and player.get_roll() > 0:
                        while True:
                            ans = input((f"Do you want to use your saved rerolls? "
                                         f"{player.get_roll()} left (y/n):")).lower()
                            if ans == 'y':
                                rolls += player.get_roll()
                                player.save_roll(0)
                                break
                            if ans == 'n':
                                break
                            print_error()
                clear_screen()
                dice_values = player.values()
                eligible_categories = decide_eligible_categories(self.game_type, dice_values, player.scorecard.used, self.categories)
                display_message(f"{player.name}'s Scorecard:")
                player.scorecard.print_card()

                display_message(
                    "\nEligible categories based on your dice:\n"
                )
                display_message(f"Your dice: {player.values()}\n")
                print_cat(eligible_categories)

                while True:
                    select = int(get_input("\nSelect a category to score in "\
                                         "or type '0' to dispose category: ").lower())
                    if select <= len(eligible_categories) and select > 0:
                        clear_screen()
                        category = eligible_categories[select - 1]
                        score = calculate_score(dice_values, category)
                        player.scorecard.record_scores(category, score)
                        display_message(f"Scored {score} points in category {category}\n")
                        break
                    if category == 0:
                        clear_screen()
                        display_message(f"Your dice: {player.values()}")
                        display_message("Categories eligible for removal:\n")

                        not_eligible = [cat for cat in self.categories if cat not
                                        in (eligible_categories + player.scorecard.used)]
                        print_cat(not_eligible)
                        category = int(get_input("\nWhich category would you like "\
                                                      "to remove: (ex. 3)"))
                        if category <= len(not_eligible):
                            player.scorecard.record_scores(category, 0)
                            display_message(f"Category '{not_eligible[category - 1]}' removed. ")
                            break
                        print_error()
                    else:
                        print_error()
                player.scorecard.print_card()
                get_input("\nPress enter to continue...")
        clear_screen()
        display_message("Game over! Final scores:")
        max_score = max(player.scorecard.total_score() for player in self.players)
        winners = []
        for player in self.players:
            if player.scorecard.total_score() == max_score:
                winners.append(player.name)
                save_score(player.name, max_score)
        for player in self.players:
            display_message(f"{player.name}: {player.scorecard.total_score()} points")
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")
