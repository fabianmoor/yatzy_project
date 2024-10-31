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

<<<<<<< HEAD
    # Main game loop
=======
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
        for category in category_name:
            if category not in used_categories:
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
        if (
            any(count >= 2 for count in counts.values())
            and "one_pair" not in used_categories):
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

>>>>>>> 3bb6327 (Function for checking eligible categories)
    def play_game(self) -> None:
        """Main game loop for playing Yatzy."""

        # Define how many rounds
        # depending on the amount of
        # categories.
        num_rounds = len(self.categories)

        # Iterating through all rounds
        # for each player.
        for round in range(num_rounds):

            # Loop through each player
            # so each round.
            for player in self.players:

                # Reset player class
                player.reset()

                # Print who's turn it is.
                display_message(f"\nRound {round+1}: {player.name}'s turn")

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
                                break
                            try:
                                indices = [num - 1 for num in list(set(only_nums(lock_input)))]
                                if len(indices) > 0:
                                    if all(0 <= x < 5 for x in indices):
                                        for index in indices:
                                            player.unlock_dice([index+1])
                                        break
                                print("Invalid input! Please try again!")

                            except ValueError:
                                print("Invalid input")
                        player.roll_unlocked()
                        if flag is True:
                            break
                    rolls +=1
                dice_values = player.values()
                display_message(f"Your dice: {dice_values}")
<<<<<<< HEAD
                available_categories = [
                    cat for cat in self.categories if cat not in player.scorecard.scores
                    ]
                display_message(f"Available categories:\n{'\n'.join(available_categories)}\n")
=======

                used_categories = player.scorecard.scores.keys()
                eligible_categories = self.decide_eligible_categories(dice_values, used_categories)

                display_message(
                    f"Eligible categories based on your dice:\n\n{', '.join(eligible_categories)}\n"
                    )
>>>>>>> 3bb6327 (Function for checking eligible categories)
                while True:
                    category = get_input("Select a category to score in: ").lower()
                    if category in eligible_categories:
                        break
<<<<<<< HEAD
                    display_message("Invalid category or already used. Please choose another.")
=======
                    else:
                        display_message("Invalid category or already used. Please choose another.")

>>>>>>> 3bb6327 (Function for checking eligible categories)
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
