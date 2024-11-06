'''Class to collect all the static methods'''
from typing import List
from collections import Counter
import os
import csv

class Methods:
    @staticmethod
    def upper_score(values: List[int], category: str) -> int:
        if category == "ones":
            return values.count(1) * 1
        elif category == "twos":
            return values.count(2) * 2
        elif category == "threes":
            return values.count(3) * 3
        elif category == "fours":
            return values.count(4) * 4
        elif category == "fives":
            return values.count(5) * 5
        else:
            return values.count(6) * 6
    @staticmethod
    def check_pairs(values: List[int], category: str) -> int:
        pairs = [i for i in set(values) if values.count(i) == 2]
        if category == "one_pair":
            return max(pairs) * 2
        elif category == "two_pairs" and len(pairs) >= 2:
            return sum(sorted(pairs)[-2:]) * 2
        elif category == "three_pairs" and len(pairs) == 3:
            return sum(values)
        else:
            return 0
    @staticmethod
    def check_dupes(values: List[int], category: str) -> int:
        for i in set(values):
            if values.count(i) >= 3 and category == "three_of_a_kind":
                return i * 3
            elif values.count(i) >= 4 and category == "four_of_a_kind":
                return i * 4
            elif values.count(i) >= 5 and category == "five_of_a_kind":
                return i * 5
            else:
                return 0
    @staticmethod
    def check_combo(values: List[int], category: str) -> int:
        counts = Counter(values)
        twos = [val for val, count in counts.items() if count == 2]
        threes = [val for val, count in counts.items() if count == 3]
        fours = [val for val, count in counts.items() if count == 4]
        if category == "full_house" and len(twos) == 1 and len(threes) == 1:
            return threes[0] * 3 + twos[0] * 2
        elif category == "villa" and len(threes) == 2:
            return threes[0] * 3 + threes[1] * 3
        elif category == "tower" and len(twos) == 1 and len(fours) == 1:
            return twos[0] * 2 + fours[0] * 4
        else:
            return 0
    @staticmethod
    def check_straight(values: List[int], category: str) -> int:
        # Define the target sequences and scores in a dictionary
        straight_scores = {
            "small_straight": ([1, 2, 3, 4, 5], 15),
            "large_straight": ([2, 3, 4, 5, 6], 20),
            "full_straight":  ([1, 2, 3, 4, 5, 6], 21),
        }

        # Check if the category is a straight, and if so, match the sorted dice values to the expected sequence
        if category in straight_scores:
            target_sequence, score = straight_scores[category]
            return score if sorted(values) == target_sequence else 0

    @staticmethod
    def calculate_score(dice_values: List[int], category: str) -> int:
        """Calculate the result of the round and return the value."""
        result = 0
        if category in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
            result = Methods.upper_score(dice_values, category)
        elif category in ["one_pair", "two_pairs", "three_pairs"]:
            result = Methods.check_pairs(dice_values, category)
        elif category in ["three_of_a_kind", "four_of_a_kind", "five_of_a_kind"]:
            result = Methods.check_dupes(dice_values, category)
        elif category in ["full_house", "villa", "tower"]:
            result = Methods.check_combo(dice_values, category)
        elif category in ["small_straight", "large_straight", "full_straight"]:
            result = Methods.check_straight(dice_values, category)
        elif category == "yatzy":
            result = 50 if len(set(dice_values)) == 1 else 0
        elif category == "chance":
            result = sum(dice_values)
        return result

    @staticmethod
    def save_score(name, score):
        """Function for saving scores"""
        path = "score.csv"

        # Check if the path is valid
        if os.path.isfile(path):
            with open(path, "a", encoding = 'utf8', newline="") as f:

                #Opening the file as read only
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
    @staticmethod
    def read_score():
        """Function for reading score"""
        path = "score.csv"
        dic = {}

        # If the file already exists,
        # update the data in the file.
        if os.path.exists(path):
            with open(path, "r", encoding = 'utf8') as f:
                print("Previous players with their highscores\n")

                # Reading file using a csv reader
                # and spliting the data.
                csv_reader = csv.reader(f, delimiter=",")
                for row in csv_reader:
                    if row != "":
                        dic[row[0]] = row[1]
                sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1], reverse= True))
                for count, key in enumerate(sorted_dict.keys()):
                    if count == 5:       #print the first 10 key-value
                        break
                    print(f"{key:<10} {dic[key]}")
        else:
            print("Highscore not available yet")
    @staticmethod
    def print_error() -> None:
        print("Invalid input! Please try again!")
    @staticmethod
    def decide_eligible_categories(game_type, dice_values, used_categories, categories):
        """Decide which categories are eligible based on the dice roll."""
        eligible_categories = []
        counts = Counter(dice_values)  # Use Counter to get frequency of each value
        unique_values = set(dice_values)

        # Single numbers
        category_numbers = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5, 'sixes': 6}
        for category, number in category_numbers.items():
            if number in counts and category not in used_categories:
                eligible_categories.append(category)

        # One Pair
        if any(count >= 2 for count in counts.values()) and "one_pair" not in used_categories:
            eligible_categories.append("one_pair")

        # Two Pairs
        pairs = [num for num, count in counts.items() if count >= 2]
        if len(pairs) >= 2 and "two_pairs" not in used_categories:
            eligible_categories.append("two_pairs")

        # Three Pairs
        pairs = [num for num, count in counts.items() if count >= 2]
        if len(pairs) == 2 and "three_pairs" not in used_categories:
            if game_type == 1:
                eligible_categories.append("three_pairs")

        # Three of a Kind
        if any(count >= 3 for count in counts.values()) and "three_of_a_kind" not in used_categories:
            eligible_categories.append("three_of_a_kind")

        # Four of a Kind
        if any(count >= 4 for count in counts.values()) and "four_of_a_kind" not in used_categories:
            eligible_categories.append("four_of_a_kind")

        # Five of a Kind
        if any(count >= 5 for count in counts.values()) and "five_of_a_kind" not in used_categories:
            if game_type == 1:
                eligible_categories.append("five_of_a_kind")

        # Full House (exactly one pair and one triplet)
        if sorted(counts.values()) == [2, 3] and "full_house" not in used_categories:
            eligible_categories.append("full_house")

        # Villa (two triplets)
        if sorted(counts.values()) == [3, 3] and "villa" not in used_categories:
            if game_type == 1:
                eligible_categories.append("villa")

        # Tower (exactly one pair and one four of a kind)
        if sorted(counts.values()) == [2, 4] and "tower" not in used_categories:
            eligible_categories.append("tower")

        # Small Straight (1-5 sequence)
        if all(num in unique_values for num in [1, 2, 3, 4, 5]) and "small_straight" not in used_categories:
            eligible_categories.append("small_straight")

        # Large Straight (2-6 sequence)
        if all(num in unique_values for num in [2, 3, 4, 5, 6]) and "large_straight" not in used_categories:
            eligible_categories.append("large_straight")

        # Full Straight (1-6 sequence)
        if all(num in unique_values for num in [1, 2, 3, 4, 5, 6]) and "full_straight" not in used_categories:
            if game_type == 1:
                eligible_categories.append("large_straight")

        # Yatzy (all dice the same)
        if len(unique_values) == 1 and "yatzy" not in used_categories:
            eligible_categories.append("yatzy")

        # Chance (always eligible if not used)
        if "chance" not in used_categories:
            eligible_categories.append("chance")

        # Filter based on categories
        eligible_categories = [cat for cat in eligible_categories if cat in categories]
        return eligible_categories
