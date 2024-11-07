'''Class to collect all the static methods'''
from typing import List
from collections import Counter
import os
import csv

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

def display_message(message: str) -> None:
    """Display a message to the user."""
    print(message)

def get_input(prompt: str) -> str:
    """Get input from the user."""
    return input(prompt)

def only_nums(ans: str) -> list[int]:
    """Extract numbers from a string."""
    return [int(num) for num in ans.strip().split() if num.isdigit()]

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

def check_pairs(values: List[int], category: str) -> int:
    """Function to check for pairs in the dice values"""
    pairs = [i for i in set(values) if values.count(i) == 2]
    if category == "one_pair":
        return max(pairs) * 2
    if category == "two_pairs" and len(pairs) >= 2:
        return sum(sorted(pairs)[-2:]) * 2
    if category == "three_pairs" and len(pairs) == 3:
        return sum(values)
    return 0

def check_dupes(values: List[int], category: str) -> int:
    """function to check for ___of_a_kind"""
    for i in set(values):
        if values.count(i) >= 3 and category == "three_of_a_kind":
            return i * 3
        if values.count(i) >= 4 and category == "four_of_a_kind":
            return i * 4
        if values.count(i) >= 5 and category == "five_of_a_kind":
            return i * 5
    return 0

def check_combo(values: List[int], category: str) -> int:
    """Function to check for combinations of pairs or dupes"""
    #use Counter(list) to count the
    #occurences of each item in the list
    counts = Counter(values)
    twos = [val for val, count in counts.items() if count == 2]
    threes = [val for val, count in counts.items() if count == 3]
    fours = [val for val, count in counts.items() if count == 4]
    if category == "full_house" and len(twos) == 1 and len(threes) == 1:
        return threes[0] * 3 + twos[0] * 2
    if category == "villa" and len(threes) == 2:
        return threes[0] * 3 + threes[1] * 3
    if category == "tower" and len(twos) == 1 and len(fours) == 1:
        return twos[0] * 2 + fours[0] * 4
    return 0

def check_straight(values: List[int], category: str) -> int:
    """Check for sequence of following integers"""
    # Define the target sequences and scores in a dictionary
    straight_scores = {
        "small_straight": ([1, 2, 3, 4, 5], 15),
        "large_straight": ([2, 3, 4, 5, 6], 20),
        "full_straight":  ([1, 2, 3, 4, 5, 6], 21),
    }

    # Check if the category is a straight, and if so,
    # match the sorted dice values to the expected sequence
    if category in straight_scores:
        target_sequence, score = straight_scores[category]
        if all(element in values for element in target_sequence):
            return score
        return 0

def calculate_score(dice_values: List[int], category: str) -> int:
    """Calculate the result of the round and return the value."""
    result = 0
    if category in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
        result = upper_score(dice_values, category)
    elif category in ["one_pair", "two_pairs", "three_pairs"]:
        result = check_pairs(dice_values, category)
    elif category in ["three_of_a_kind", "four_of_a_kind", "five_of_a_kind"]:
        result = check_dupes(dice_values, category)
    elif category in ["full_house", "villa", "tower"]:
        result = check_combo(dice_values, category)
    elif category in ["small_straight", "large_straight", "full_straight"]:
        result = check_straight(dice_values, category)
    elif category == "yatzy":
        result = 50 if len(set(dice_values)) == 1 else 0
    elif category == "chance":
        result = sum(dice_values)
    return result

def save_score(name, score):
    """Function for saving scores"""
    path = "score.csv"

    # Check if the path is valid
    if os.path.isfile(path):
        #Opening the file as appending
        with open(path, "a", encoding = 'utf8', newline="") as f:
            print(f"File {path} already exists,"\
                f"appending highscore of {name} with {score}")
            writer = csv.writer(f)
            writer.writerow([name, score])
    else:
        # If its the first time calculating,
        # create file and write the data.
        with open(path, "x", encoding = 'utf8', newline= "") as f:
            writer = csv.writer(f)
            writer.writerow([name, score])
            print(f"Highscore of {name} with {score} score saved to {path}")

def read_score(times: int):
    """Function for reading score"""
    path = "score.csv"
    dic = {}

    # If the file already exists, read the data.
    if os.path.exists(path):
        with open(path, "r", encoding='utf8') as f:
            print("Previous players with their highscores\n")

            # Reading file using a csv reader and splitting the data.
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:
                if row != "":
                    player = row[0]
                    score = int(row[1])

                    # Check if player is already in the dictionary
                    if player not in dic:
                        dic[player] = []  # Initialize an empty list for the player

                    # Append the score to the player's list of scores
                    dic[player].append(score)

            # Sort each player's scores in descending order (optional)
            for player, scores in dic.items():
                scores.sort(reverse=True)

            # Display the top 5 scores across all players
            sorted_scores = sorted(
                [(player, score) for player, scores in dic.items() for score in scores],
                key=lambda item: item[1],
                reverse=True
            )

            for count, (player, score) in enumerate(sorted_scores):
                if count == times:  # Only print the top 5 scores
                    break
                print(f"{player}: {score}")
    else:
        print("Highscore not available yet")

def print_error() -> None:
    """Print error message"""
    print("Invalid input! Please try again!")

def decide_eligible_categories(game_type, dice_values, used, unused):
    """Decide which categories are eligible based on the dice roll."""
    eligible_categories = []
    counts = Counter(dice_values)  # Use Counter to get frequency of each value
    unique_values = set(dice_values)

    # Single numbers
    category_numbers = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5, 'sixes': 6}
    for category, number in category_numbers.items():
        if number in counts and category not in used:
            eligible_categories.append(category)

    # One Pair
    if any(count >= 2 for count in counts.values()) and "one_pair" not in used:
        eligible_categories.append("one_pair")

    # Two Pairs
    pairs = [num for num, count in counts.items() if count >= 2]
    if len(pairs) >= 2 and "two_pairs" not in used:
        eligible_categories.append("two_pairs")

    # Three Pairs
    pairs = [num for num, count in counts.items() if count >= 2]
    if len(pairs) == 3 and "three_pairs" not in used and game_type == 2:
        eligible_categories.append("three_pairs")

    # Three of a Kind
    if any(count >= 3 for count in counts.values()) and "three_of_a_kind" not in used:
        eligible_categories.append("three_of_a_kind")

    # Four of a Kind
    if any(count >= 4 for count in counts.values()) and "four_of_a_kind" not in used:
        eligible_categories.append("four_of_a_kind")

    # Five of a Kind
    if any(count >= 5 for count in counts.values()) and "five_of_a_kind" not in used:
        if game_type == 2:
            eligible_categories.append("five_of_a_kind")

    # Full House (exactly one pair and one triplet)
    if sorted(counts.values()) in ([2, 3], [1, 2, 3]) and "full_house" not in used:
        if (game_type == 1 and sorted(counts.values()) == [2, 3]) or (game_type == 2 and sorted(counts.values()) == [1, 2, 3]):
            eligible_categories.append("full_house")


    # Villa (two triplets)
    if sorted(counts.values()) == [3, 3] and "villa" not in used:
        if game_type == 2:
            eligible_categories.append("villa")

    # Tower (exactly one pair and one four of a kind)
    if sorted(counts.values()) == [2, 4] and "tower" not in used:
        if game_type == 2:
            eligible_categories.append("tower")

    # Small Straight (1-5 sequence)
    if all(num in unique_values for num in [1, 2, 3, 4, 5]) and "small_straight" not in used:
        eligible_categories.append("small_straight")

    # Large Straight (2-6 sequence)
    if all(num in unique_values for num in [2, 3, 4, 5, 6]) and "large_straight" not in used:
        eligible_categories.append("large_straight")

    # Full Straight (1-6 sequence)
    if all(num in unique_values for num in [1, 2, 3, 4, 5, 6]) and "full_straight" not in used:
        if game_type == 2:
            eligible_categories.append("full_straight")

    # Yatzy (all dice the same)
    if len(unique_values) == 1 and "yatzy" not in used:
        eligible_categories.append("yatzy")

    # Chance (always eligible if not used)
    if "chance" not in used:
        eligible_categories.append("chance")

    # Filter based on unused
    eligible_categories = [cat for cat in eligible_categories if cat in unused]
    return eligible_categories
