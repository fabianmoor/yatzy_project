"""Controller file"""
from src.model import Player, ScoreCard
from src.view import clear_screen, display_message, get_input, only_nums



class YatzyController:
    """Controller class to manage the game flow."""
    def __init__(self):

        clear_screen()

        # Init player_list
        self.players = []

        # Define different score categories
        self.categories = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one_pair", "two_pairs", "three_of_a_kind", "four_of_a_kind",
            "small_straight", "large_straight", "full_house", "chance", "yatzy"
        ]

    # Function for calling High Scores.
    def show_highscores(self):
        """Function for showing previous HighScores"""
        clear_screen()
        ScoreCard.read_score()

    # Function for starting game.
    def start_game(self):
        """Start Game (Init Game)"""
        clear_screen()
        display_message("Welcome to Yatzy!\n")

        # Fetch the Read Score
        ScoreCard.read_score()

        # Get number of players.
        while True:
            try:

                # Ask the user for number of players.
                num_players = int(get_input("\nEnter number of players: "))

                # If number is greater than 0.
                if num_players > 0:

                    # We exit the while loop.
                    break

                # Else we print invalid input.
                print("Invalid input! Please try again!")

            # In the case of a value error
            # such as a letter.
            except ValueError:

                # We give the same error.
                print("Invalid input! Please try again!")

        # Create players
        for i in range(num_players):

            # Get name for each player
            name = get_input(f"Enter name for player {i+1}: ")

            # Add player to player list.
            self.players.append(Player(name))

    # Function for generating eligible categories to put your score within.
    def decide_eligible_categories(self, dice_values, used_categories):
        """Decide which categories are eligible based on the dice roll."""

        # Init list for eligible categories
        eligible_categories = []

        # Dict for counting each num
        # occurance.
        counts = {}

        # We iterate through all values
        # of our dice_values.
        for value in dice_values:

            # For each value we iterate we count it.
            # and add it to the counts dict.
            # Ex. ["2", "3", "4", "2"]
            # Like: { 2: 2, 3: 1, 4: 1 }
            counts[value] = counts.get(value, 0) + 1

        # We keep track of the different
        # values within the dice_values
        # by converting it to a set, hence
        # removing all the duplicates.
        unique_values = set(dice_values)

        # We then iterate over the simpler
        # categories. If any of them are
        # used we do not append them to
        # the eligible list.
        category_name = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']

        # We make a similair dict with 
        # numbers as values.
        category_numbers = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5, 'sixes': 6}

        # We iterate over the category_name.
        for category in category_name:

            # We assign the current element 
            # into number.
            number = category_numbers[category]

            # If the number is in counts
            # and if the category iteration
            # element not in used_categories.
            if number in counts and category not in used_categories:

                # We include it into the 
                # eligible_categories.
                eligible_categories.append(category)

        # We check if there are any pairs.
        #
        # We do this by using any() which returns
        # True if ANY value is True.
        # Hence we check if any element in the iteration
        # meets the condition.
        #
        # Meaning if any counts.value is greater than
        # or equal to 2 the first half of the condition
        # is met.
        #
        # Finally we just check if "one_pair" also not in
        # used_categories.
        #
        # If both conditions are met, we append it to the
        # eligible list.
        if (any(count >= 2 for count in counts.values())
            and "one_pair" not in used_categories):

            # If so we append "one_pair" to the 
            # eligible_categories.
            eligible_categories.append("one_pair")

        # We iterate over counts.item() and keep track of both
        # the key and the value.
        #
        # If the count >= 2 we add it to pairs.
        pairs = [num for num, count in counts.items() if count >= 2]

        # Here we check the other types of potential categories.
        # Here specifically two pairs.
        if len(pairs) >= 2 and "two_pairs" not in used_categories:
            eligible_categories.append("two_pairs")

        # Here we check if there is three of the same
        # value.
        if (any(count >= 3 for count in counts.values())
            and "three_of_a_kind" not in used_categories):
            eligible_categories.append("three_of_a_kind")

        # Here we check if there is four of the same
        # value.
        if (any(count >= 4 for count in counts.values())
            and "four_of_a_kind" not in used_categories):
            eligible_categories.append("four_of_a_kind")

        # Using this condition we can see if
        # there is a full house.
        # Since we need to have 2 of one num
        # and 3 of another num.
        #
        # If that condition is met, we know that there
        # is a full house of some kind.
        if (sorted(counts.values()) == [2, 3]
            and "full_house" not in used_categories):
            eligible_categories.append("full_house")

        # Here we check if we have a small straight.
        # We do this by checking if all unique_values
        # are in the list [1, 2, 3, 4, 5]
        if (all(num in unique_values for num in [1, 2, 3, 4, 5])
            and "small_straight" not in used_categories):
            eligible_categories.append("small_straight")

        # Here we check if we have a large straight.
        # The same logic as above, but instead of
        # comparing 1 to 5, we compare 2 to 6.
        if (all(num in unique_values for num in [2, 3, 4, 5, 6])
            and "large_straight" not in used_categories):
            eligible_categories.append("large_straight")

        # Here if uniquie values == 1, it means that
        # all dices where the same.
        #
        # Hence we are eligible for a yatzy.
        if len(unique_values) == 1 and "yatzy" not in used_categories:
            eligible_categories.append("yatzy")

        # Chance should always be available
        # if it hasn't been used yet.
        #
        # Hence we only check if it's been used.
        if "chance" not in used_categories:
            eligible_categories.append("chance")

        # Finally we iterate over the eligible categories
        # We check if the current element is in self.categories
        #
        # If the condition is met, the category is kept in the
        # new list. If not, it is removed.
        eligible_categories = [cat for cat in eligible_categories if cat in self.categories]

        # We finally return the eligible
        # categories as a list.
        return eligible_categories

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

                # Print who's turn it is.
                clear_screen()
                display_message(f"Round {player_round+1}: {player.name}'s turn\n")
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

                        # We init a flag var to
                        # False.
                        flag = False

                        clear_screen()

                        # Print the result.
                        display_message(f"Roll {rolls+1}: {player.values()}\n")

                        # We lock all dice of 
                        # the current player.
                        player.lock_all()

                        # We initialize a while
                        # loop for iteration.
                        while True:

                            # We ask the user what input
                            # to re roll.
                            lock_input = get_input(
                            "Enter dice numbers to re-roll (e.g., 1 3 5), "\
                            "or press Enter to keep all: "
                            )

                            # We strip all the nums
                            # in order to fetch the values
                            # specified by the user.
                            if lock_input.strip() == '':

                                # If so we set flag to
                                # True.
                                flag = True

                                # And exit the while loop.
                                print("Exited while loop")
                                break

                            # Init a try error handling.
                            try:

                                # For each element in only_nums when
                                # parsing the lock_input as an argument:
                                #
                                # We add the value - 1 to represent the
                                # index.
                                #
                                # Meaning we add each index to the indices
                                # variable as a list type.
                                indices = [num - 1 for num in list(set(only_nums(lock_input)))]

                                # We first check if the length
                                # is greater than 0.
                                #
                                # To check if the user wants to
                                # re roll any dice.
                                if len(indices) > 0:

                                    # If 0 <= x < 5 for all elements
                                    # in the list.
                                    if all(0 <= x < 5 for x in indices):

                                        # If above holds true,
                                        # we initiate a for loop.
                                        for index in indices:

                                            # We unlock all dice that corresponds
                                            # to an index.
                                            player.unlock_dice([index+1])

                                        break

                                # If above failes,
                                # we print the following.
                                print("Invalid input! Please try again!")

                            # If we get a ValueError such as 
                            # a character instead of an int.
                            except ValueError:

                                # We print the following.
                                print("Invalid input")

                        # We roll all the dice
                        # that are unlocked.
                        player.roll_unlocked()

                        # If flag is true,
                        # meaning that we've
                        # checked the user input
                        # and rolled each die that should
                        # be rolled.
                        if flag is True:

                            # We exit the loop.
                            break

                    # Also we incriment the
                    # rolls.
                    rolls += 1

                # We save the dices
                dice_values = player.values()

                clear_screen()

                # Showcase the dices.
                display_message(f"Your dice: {dice_values}")

                # We check what categories the player has
                # used and save it to a var for later use.
                used_categories = list(player.scorecard.scores.keys())

                # We run the function for deciding eligible
                # categories when parsing the dice_values and
                # used_categories.
                eligible_categories = self.decide_eligible_categories(dice_values, used_categories)

                display_message(
                    "\nEligible categories based on your dice:\n"
                )

                # We iterate over the eligible_categories list two elements at a time.
                for i in range(0, len(eligible_categories), 2):

                    # Check if there's a pair of categories to display.
                    if i + 1 < len(eligible_categories):

                        # Display two categories side by side.
                        display_message(
                            f"{eligible_categories[i]:<15}\t"\
                            f"{eligible_categories[i + 1]:<15}")

                    # If only one category remains, display it alone.
                    else:
                        display_message(f"{eligible_categories[i]:<15}")

                # Start a loop to get user input for selecting a category to score in.
                while True:

                    # Prompt the player to choose a category or dispose of one.
                    category = get_input("\nSelect a category to score in "\
                                         "or type 'x' to dispose category: ").lower()

                    # Check if the selected category is in the list of eligible categories.
                    if category in eligible_categories:

                        # Clear the screen before displaying the score.
                        clear_screen()

                        # Calculate the score for the chosen category based on dice values.
                        score = ScoreCard.calculate_score(dice_values, category)

                        # Record the score in the player's scorecard.
                        player.scorecard.record_scores(category, score)

                        # Exit the loop as a valid category was selected.
                        break

                    # Check if the player chose to dispose of a category.
                    elif category == "x":

                        # Set the removed flag to True, as a category might be removed.
                        removed = True

                        # Clear the screen to display removal options.
                        clear_screen()

                        # Display message indicating available categories for removal.
                        display_message("Categories eligible for removal:\n")

                        # Create a list of categories not eligible or already used.
                        not_eligible = [cat for cat in self.categories if cat not
                                        in (eligible_categories + used_categories)]

                        # Format the list of not eligible categories for display.
                        formatted_output = "\n".join(
                            [f"{not_eligible[i]:<15}\t\t{not_eligible[i + 1]:<15}"
                            if i + 1 < len(not_eligible) else f"{not_eligible[i]:<15}"
                            for i in range(0, len(not_eligible), 2)]
                        )

                        # Display the formatted list of not eligible categories.
                        display_message(formatted_output)

                        # Prompt the player to select a category to remove.
                        category = get_input("\nWhich category would you like "\
                                             "to remove: ").lower()

                        # Check if the selected category is valid for removal.
                        if category in self.categories:

                            # Record a score of zero for the removed category.
                            player.scorecard.record_scores(category, 0)

                            # Exit the loop as a category has been removed.
                            break

                    # If input is invalid, display an error message and continue the loop.
                    else:
                        print("Invalid input! Please try again!")

                # Check if a category was removed, and display appropriate message.
                if removed:
                    display_message(f"Category '{category}' removed. " \
                                    f"Total score: {player.scorecard.total_score()}")

                # Otherwise, display the score recorded for the selected category.
                else:
                    display_message(f"Scored {score} points in category '{category}'. " \
                                    f"Total score: {player.scorecard.total_score()}")

                # Wait for the player to press enter before continuing.
                get_input("Press enter to continue...")

                # Reset the removed flag for the next round.
                removed = False

        clear_screen()

        # Display the end-of-game message showing the final scores.
        display_message("\nGame over! Final scores:")

        # Calculate the highest score achieved among all players.
        max_score = max(player.scorecard.total_score() for player in self.players)

        # Initialize a list to hold the names of the winners.
        winners = []

        # Iterate over each player to identify the winners.
        for player in self.players:

            # Check if the player's score matches the max score.
            if player.scorecard.total_score() == max_score:

                # Add the player's name to the list of winners.
                winners.append(player.name)

                # Save the high score with the player's name.
                ScoreCard.save_score(player.name, max_score)

        # Display each player's name and their final score.
        for player in self.players:
            display_message(f"{player.name}: {player.scorecard.total_score()} points")

        # Announce the winner(s) and display their score.
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")
