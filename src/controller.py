"""Controller file"""
from src.model import Player, ScoreCard
from src.view import clear_screen, display_message, get_input, only_nums

class YatzyController:
    """Controller class to manage the game flow."""
    def __init__(self):
        clear_screen()
        yatzy_art = r"""
__   __    _             
\ \ / /   | |            
 \ V /__ _| |_ _____   _ 
  \ // _` | __|_  / | | |
  | | (_| | |_ / /| |_| |
  \_/\__,_|\__/___|\__, |
                    __/ |
                   |___/ 

        """
        display_message(yatzy_art)
        display_message("""
[1]: Play Game
[2]: Show High Scores
[3]: Exit
        """)
        while True:
            menu_input = get_input("Choice: ").lower()
            try:
                match menu_input:
                    case "1":
                        menu_choice = 1
                        break
                    case "2":
                        menu_choice = 2
                        break
                    case "3":
                        menu_choice = 3
                        break
            except ValueError:
                display_message("Invalid input...")

        display_message("Welcome to Yatzy!")
        ScoreCard.read_score()
        # Get number of players.
        while True:
            try:
                num_players = int(get_input("Enter number of players: "))
                if num_players > 0:
                    break
                print("Invalid input! Please try again!")
            except ValueError:
                print("Invalid input! Please try again!")

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

    # Show Main Menu

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
        category_numbers = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5, 'sixes': 6}
        for category in category_name:
            number = category_numbers[category]
            if number in counts and category not in used_categories:
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
                        flag = False
                        # Print the result.
                        display_message(f"Roll {rolls+1}: {player.values()}\n")
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
                clear_screen()
                display_message(f"Your dice: {dice_values}")

                used_categories = list(player.scorecard.scores.keys())
                eligible_categories = self.decide_eligible_categories(dice_values, used_categories)

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
                        score = ScoreCard.calculate_score(dice_values, category)
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
                    else:
                        print("Invalid input! Please try again!")
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
                ScoreCard.save_score(player.name, max_score)
        for player in self.players:
            display_message(f"{player.name}: {player.scorecard.total_score()} points")
        display_message(f"The winner(s): {', '.join(winners)} with {max_score} points!")