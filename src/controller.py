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

    # Function for starting game.
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

                # Ask the user for number of players.
                num_players = int(get_input("\nEnter number of players: "))

                # If number is greater than 0.
                if num_players > 0:

                    # We exit the while loop.
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

    # Play game function.
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
                    if rolls > 0:
                        #flag to break the outer while-loop
                        flag = False

                        # Print the result.
                        clear_screen()
                        display_message((f"Round {player_round+1} Rerolls left: {rolls} {player.name}'s turn\n"))
                        display_message(f"Roll {count_rolls}: {player.values()}\n")

                        #lock all the dices
                        player.lock_all()

                        # We initialize a while
                        # loop for iteration.
                        while True:
                            try:

                                # We ask the user what input
                                # to re roll
                                lock_input = get_input(
                                "Enter dice numbers to re-roll sepereted by space (e.g., 1 3 5), "\
                                "or press Enter to keep all: "
                                )

                                #if player has pushed the enter button, the flag breaks the outmost
                                #loop to go to category selection
                                if lock_input.strip() == '':
                                    flag = True

                                    #save the remaining rerolls if the game is maxiyatzy
                                    if self.game_type == 2:
                                        player.save_roll(player.get_roll()+rolls)
                                    break

                                # For each element in only_nums when
                                # parsing the lock_input as an argument:
                                #
                                # We add the value - 1 to represent the
                                # index.
                                #
                                # Meaning we add each index to the indices
                                # variable as a list type.
                                indices = [num - 1 for num in list(set(only_nums(lock_input)))]

                                # We first check if the length is greater than 0
                                # if the game is yatzy and the reroll input is
                                # in the correct range (5 dices) or in maxi yatzy
                                # (6 dices)
                                if (len(indices) > 0 and
                                    ((self.game_type == 1 and all(0 <= x < 5 for x in indices)) or
                                    (self.game_type == 2 and all(0 <= x < 6 for x in indices)))):
                                    for index in indices:

                                        # We unlock all dice that corresponds
                                        # to an index.
                                        player.unlock_dice([index + 1])
                                    break

                                #if incorrect range has been entered
                                print_error()
                            except ValueError:
                                print_error()
                        player.roll_unlocked()

                        # If flag is true,
                        # meaning that we've
                        # checked the user input
                        # and rolled each die that should
                        # be rolled.
                        if flag is True:

                            # We exit the loop.
                            break
                    display_message(player.values())
                    
                    # If its maxi yatzy and the player has used their 2 rerolls, we
                    # ask if they want to use their saved rerolls, if yes, the rerolls
                    # are added to the total rerolls and the loop continues otherwise
                    # the loop breaks and the player gets to choose the categories
                    if rolls == 0 and self.game_type == 2 and player.get_roll() > 0:
                        while True:
                            try:
                                ans = get_input((f"Do you want to use your saved rerolls? "
                                            f"{player.get_roll()} left (y/n):")).lower()
                                if ans == 'y':
                                    rolls += player.get_roll() + 1
                                    # reset the player reroll to 0 since we add all of the
                                    # saved rerolls to the current rolls
                                    player.save_roll(0)
                                    break
                                if ans == 'n':
                                    break
                                print_error()
                            except ValueError:
                                print_error()
                clear_screen()
                dice_values = player.values()

                # We run the function for deciding eligible
                # categories when parsing the dice_values and
                # used categories depending on the gametype
                eligible_categories = decide_eligible_categories(self.game_type, dice_values, player.scorecard.used, self.categories)
                display_message(f"{player.name}'s Scorecard:")
                
                # Display the scorecard
                player.scorecard.print_card()

                display_message(
                    "\nEligible categories based on your dice:\n"
                )
                display_message(f"Your dice: {player.values()}\n")

                #Call the function to print out the eligible
                #categories
                print_cat(eligible_categories)

                # Start a loop to get user input for selecting a category to score in.
                while True:

                    # Prompt the player to choose a category or dispose of one.
                    select = get_input("\nSelect a category to score in "\
                                         "or type 'x' to dispose category: ")

                    # Check if input is a digit or string
                    if select.isdigit():

                        #if the correct range is entered
                        if 0 < int(select) <= len(eligible_categories):
                            clear_screen()
                            # Get the category name from the list
                            category = eligible_categories[int(select) - 1]
                            # Calculate the score for the chosen category based on dice values.
                            score = calculate_score(dice_values, category)
                            # Record the score in the player's scorecard.
                            player.scorecard.record_scores(category, score)
                            # Display the score recorded for the selected category.
                            display_message(f"Scored {score} points in category {category}\n")
                            break
                        print_error()
                    if select in ("x", "X"):
                        clear_screen()
                        display_message(f"Your dice: {player.values()}")
                        display_message("Categories eligible for removal:\n")

                        # Create a list of categories not eligible or already used.
                        not_eligible = [cat for cat in self.categories if cat not
                                        in (eligible_categories + player.scorecard.used)]
                        # Display the list of not eligible categories
                        print_cat(not_eligible)
                        try:
                            # Prompt the player to select a category to remove.
                            select = int(get_input("\nWhich category would you like "\
                                                        "to remove: (ex. 3)"))

                            # Check if the range is right
                            if select <= len(not_eligible):
                                # Get the category name from the list
                                category = eligible_categories[int(select) - 1]
                                # Record a score of zero for the removed category.
                                player.scorecard.record_scores(category, 0)
                                # Check if a category was removed, and display appropriate message.
                                display_message(f"Category '{not_eligible[category - 1]}' removed. ")
                                break
                            print_error()
                        except ValueError:
                            print_error()
                    else:
                        print_error()
                # Print the scorecard
                player.scorecard.print_card()
                display_message(f"Saved rerolls: {player.get_roll()}")
                # Wait for the player to press enter before continuing.
                get_input("\nPress enter to continue...")
        clear_screen()

        # Display the end-of-game message showing the final scores.
        display_message("Game over! Final scores:")
        max_score = max(player.scorecard.total_score() for player in self.players)

        # Initialize a list to hold the names of the winners.
        winners = []

        # Iterate over each player to identify the winners.
        for player in self.players:

            # Display each player's name and their final score.
            display_message(f"{player.name}: {player.scorecard.total_score()} points")

            # Check if the player's score matches the max score.
            if player.scorecard.total_score() == max_score:

                # Add the player's name to the list of winners.
                winners.append(player.name)
                save_score(player.name, max_score)

        # Announce the winner(s) and display their score.
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")
