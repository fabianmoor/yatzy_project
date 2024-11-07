'''Class to collect all the static methods'''
from typing import List
from collections import Counter
import os
import csv

# Function to clear the screen and printout
# the yatzy art. it checks for cls if its windows
# or clear if its unix
def clear_screen() -> None:
    """Clear the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')
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

# Function to print a message
def display_message(message: str) -> None:
    """Display a message to the user."""
    print(message)

# Get input from a user and display the prompt
def get_input(prompt: str) -> str:
    """Get input from the user."""
    return input(prompt)

# Return a list of digits from a string input
# used in dice reroll selection
def only_nums(ans: str) -> list[int]:
    """Extract numbers from a string."""
    # Strip and split the string and only append the digits
    # to the list before returning the list
    return [int(num) for num in ans.strip().split() if num.isdigit()]

# Counts the occurences of the associated values
# for the selected category and return the result
# of the points (sum of the value)
def upper_score(values: List[int], category: str) -> int:
    """Function to return the results of the upper scorecard
    unused"""
    count = 0
    if category == "ones":
        count = values.count(1) * 1
    elif category == "twos":
        count = values.count(2) * 2
    elif category == "threes":
        count = values.count(3) * 3
    elif category == "fours":
        count = values.count(4) * 4
    elif category == "fives":
        count = values.count(5) * 5
    elif category == "sixes":
        count = values.count(6) * 6
    return count

# check for pair combination in the dice list and
# return the result of the points
def check_pairs(values: List[int], category: str) -> int:
    """Function to check for pairs in the dice values"""
    # Get the unique values from the diceset and count each
    # occurances of the value. if it is 2, then it is a pair
    pairs = [i for i in set(values) if values.count(i) == 2]
    if category == "one pair":
        # Use the top pair if several pairs are present
        return max(pairs) * 2
    if category == "two pairs" and len(pairs) >= 2:
        # Use the top two pairs if several pairs are present
        return sum(sorted(pairs)[-2:]) * 2
    if category == "three pairs" and len(pairs) == 3:
        # since we use maximum of 6 dices, 3 pairs means
        # all 6 dices are used so we return the sum of all
        # the dices
        return sum(values)
    return 0

# Check for duplicated values, like two-, three-, four- or
# five-of a kind
def check_dupes(values: List[int], category: str) -> int:
    """function to check for __ of a kind"""
    # Count the occurences depending on the category
    for i in set(values):
        if values.count(i) >= 3 and category == "three of a kind":
            return i * 3
        if values.count(i) >= 4 and category == "four of a kind":
            return i * 4
        if values.count(i) >= 5 and category == "five of a kind":
            return i * 5
    return 0

# Check for the combination of dicepair or values such as
# full house (2+3), villa (3+3) or tower (2+4)
def check_combo(values: List[int], category: str) -> int:
    """Function to check for combinations of pairs or dupes"""
    #use Counter(list) to count the
    #occurences of each item in the list
    counts = Counter(values)
    
    # count the occurances of each value and save it in a list
    # val = value, count = how many duplicates there are
    twos = [val for val, count in counts.items() if count == 2]
    threes = [val for val, count in counts.items() if count == 3]
    fours = [val for val, count in counts.items() if count == 4]
    
    # Calculate the result depending on the category
    if category == "full house" and len(twos) == 1 and len(threes) == 1:
        return threes[0] * 3 + twos[0] * 2
    if category == "villa" and len(threes) == 2:
        return threes[0] * 3 + threes[1] * 3
    if category == "tower" and len(twos) == 1 and len(fours) == 1:
        return twos[0] * 2 + fours[0] * 4
    return 0

# Check for different straight combinations. small and large
# straight are for yatzy and full straight for maxiyatzy
def check_straight(values: List[int], category: str) -> int:
    """Check for sequence of following integers"""
    # Define the target sequences and scores in a dictionary
    straight_scores = {
        "small straight": ([1, 2, 3, 4, 5], 15),
        "large straight": ([2, 3, 4, 5, 6], 20),
        "full straight":  ([1, 2, 3, 4, 5, 6], 21),
    }

    # Check if the category is a straight, and if so,
    # match the sorted dice values to the expected sequence
    if category in straight_scores:
        target_sequence, score = straight_scores[category]
        # Check if the dice set is matching the sequence of the straight
        # categories and return the appropriate result
        if all(element in values for element in target_sequence):
            return score
        return 0

# Calculate the right score from the diceset and selected category.
# Most if not all the calculations are done through the functions
# above
def calculate_score(dice_values: List[int], category: str) -> int:
    """Calculate the result of the round and return the value."""
    result = 0
    if category in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
        result = upper_score(dice_values, category)
    elif category in ["one pair", "two pairs", "three pairs"]:
        result = check_pairs(dice_values, category)
    elif category in ["three of a kind", "four of a kind", "five of a kind"]:
        result = check_dupes(dice_values, category)
    elif category in ["full house", "villa", "tower"]:
        result = check_combo(dice_values, category)
    elif category in ["small straight", "large straight", "full straight"]:
        result = check_straight(dice_values, category)
    elif category == "yatzy":
        result = 50 if len(set(dice_values)) == 1 else 0
    elif category == "chance":
        result = sum(dice_values)
    return result

# Save the name and score in a csv file
def save_score(name, score):
    """Function for saving scores"""
    path = "score.csv"

    # Check if the path is valid
    if os.path.isfile(path):
        #Opening the file as appending
        with open(path, "a", encoding = 'utf8', newline="") as f:
            # Using a csv writer to right the name and score
            writer = csv.writer(f)
            writer.writerow([name, score])
    else:
        # If its the first time playing and there is no such file,
        # create file and write the score
        with open(path, "x", encoding = 'utf8', newline= "") as f:
            writer = csv.writer(f)
            writer.writerow([name, score])
    # Confirmation message of successful saving
    display_message(f"Highscore of {name} with {score} score saved to {path}")

def read_score(times: int):
    """Function for reading score"""
    path = "score.csv"
    dic = {}

    # If the file exists, read the data.
    if os.path.exists(path):
        with open(path, "r", encoding='utf8') as f:
            print("Previous players with their highscores\n")

            # Reading file using a csv reader and splitting the data.
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:
                # If the row is not empty line
                if row != "":
                    player = row[0]
                    score = int(row[1])

                    # Check if player is already in the dictionary
                    if player not in dic:
                        dic[player] = []  # Initialize an empty list for the player

                    # Append the score to the player's list of scores
                    dic[player].append(score)

            # Sort each player's scores in descending order
            for player, scores in dic.items():
                scores.sort(reverse=True)

            # sort the players depending on the scores and add as tuple in the list
            sorted_scores = sorted(
                [(player, score) for player, scores in dic.items() for score in scores],
                key=lambda item: item[1],
                reverse=True
            )

            # Print out the name and corresponding score 
            for count, (player, score) in enumerate(sorted_scores):
                # times = how many players we want the score for
                if count == times:
                    break
                print(f"{player}: {score}")
    # If its the first time playing and there are no records
    else:
        print("Highscore not available yet")

# Print out an error message for invalid input
def print_error() -> None:
    """Print error message"""
    print("Invalid input! Please try again!")

# Function for generating eligible categories to put your score within.
def decide_eligible_categories(game_type, dice_values, used, unused):
    """Decide which categories are eligible based on the dice roll."""
    # Init list for eligible categories
    eligible_categories = []
    # Use Counter to get frequency of each value
    counts = Counter(dice_values)

    # We keep track of the different
    # values within the dice_values
    # by converting it to a set, hence
    # removing all the duplicates.
    unique_values = set(dice_values)

    # We make a dict with
    # numbers as values.
    category_numbers = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5, 'sixes': 6}

    #we iteratte over the dictionary with category name and values pairs
    for category, number in category_numbers.items():

        # If the number is in counts
        # and if the category iteration
        # element not in used_categories.
        if number in counts and category not in used:
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
        and "one_pair" not in used):

        # If so we append "one_pair" to the
        # eligible_categories.
        eligible_categories.append("one_pair")

    # Here we check the other types of potential categories.
    # Here specifically two pairs.
    pairs = [num for num, count in counts.items() if count >= 2]
    if len(pairs) >= 2 and "two pairs" not in used:
        eligible_categories.append("two pairs")

    # similar code as above, we just check for 3 pairs
    # only in maxi yatzy
    pairs = [num for num, count in counts.items() if count >= 2]
    if len(pairs) == 3 and "three pairs" not in used and game_type == 2:
        eligible_categories.append("three pairs")

    # Here we check if there is three of the same
    # value.
    if any(count >= 3 for count in counts.values()) and "three of a kind" not in used:
        eligible_categories.append("three of a kind")

    # Here we check if there is four of the same
    # value.
    if any(count >= 4 for count in counts.values()) and "four of a kind" not in used:
        eligible_categories.append("four of a kind")

    # Five of a kind (only in maxiYatzy)
    if any(count >= 5 for count in counts.values()) and "five of a kind" not in used:
        if game_type == 2:
            eligible_categories.append("five of a kind")

    # Using this condition we can see if
    # there is a full house.
    # Since we need to have 2 of one num
    # and 3 of another num.
    # (and special case for maxi yatzy)
    # If that condition is met, we know that there
    # is a full house of some kind.
    if sorted(counts.values()) in ([2, 3], [1, 2, 3]) and "full house" not in used:
        if (game_type == 1 and sorted(counts.values()) == [2, 3]) or (game_type == 2 and sorted(counts.values()) == [1, 2, 3]):
            eligible_categories.append("full house")


    # Similar code as above but checking for Villa (two triplets)
    if sorted(counts.values()) == [3, 3] and "villa" not in used:
        if game_type == 2:
            eligible_categories.append("villa")

    # Tower (exactly one pair and one four of a kind)
    if sorted(counts.values()) == [2, 4] and "tower" not in used:
        if game_type == 2:
            eligible_categories.append("tower")

    # Here we check if we have a small straight.
    # We do this by checking if all unique_values
    # are in the list [1, 2, 3, 4, 5]
    if all(num in unique_values for num in [1, 2, 3, 4, 5]) and "small straight" not in used:
        eligible_categories.append("small straight")

    # similar code but for Large Straight (2-6 sequence)
    if all(num in unique_values for num in [2, 3, 4, 5, 6]) and "large straight" not in used:
        eligible_categories.append("large straight")

    # and for Full Straight (1-6 sequence)
    if all(num in unique_values for num in [1, 2, 3, 4, 5, 6]) and "full straight" not in used:
        if game_type == 2:
            eligible_categories.append("full straight")

    # Here if uniquie values == 1, it means that
    # all dices where the same.
    #
    # Hence we are eligible for a yatzy.
    if len(unique_values) == 1 and "yatzy" not in used:
        eligible_categories.append("yatzy")

    # Chance should always be available
    # if it hasn't been used yet.
    #
    # Hence we only check if it's been used.
    if "chance" not in used:
        eligible_categories.append("chance")

    # Finally we iterate over the eligible categories
    # We check if the current element is in self.categories
    #
    # If the condition is met, the category is kept in the
    # new list. If not, it is removed.
    eligible_categories = [cat for cat in eligible_categories if cat in unused]

    # We finally return the eligible
    # categories as a list.
    return eligible_categories

# Function to print out a list of categories in pairs of two
# side by side for asthetic purposes
def print_cat(categories: list) -> None:
    """Print the list of categories for eligible and removal"""
    # We iterate over the eligible_categories list two elements at a time.
    for i in range(0, len(categories), 2):

        # Check if there's a pair of categories to display.
        if i + 1 < len(categories):

            # Display two categories side by side.
            display_message(
                f"[{i+1}] - {categories[i]:<15}\t"\
                f"[{i+2}] - {categories[i + 1]:<15}")
        else:
            # If only one category remains, display it alone.
            display_message(f"[{i+1}] - {categories[i]:<15}")
