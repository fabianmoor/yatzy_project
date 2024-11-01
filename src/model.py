"""Model File"""
import random, os, csv
from typing import List

class Player:
    """Player class to initialize each player with their own set of 5 dice. Functions to
    roll the dice, lock and unlock specific dice, get the values from the dice rolls, and
    reset the dice for the next player round."""
    def __init__(self, name: str):
        self.name = name
        self.scorecard = ScoreCard()
        self.dice = [Dice() for _ in range(5)]

    def roll_unlocked(self) -> List[int]:
        """Roll all the dice that are unlocked. In the beginning of the round, all dice
        are unlocked."""
        return [dice.roll() for dice in self.dice]

    def lock_dice(self, indices: List[int]) -> None:
        """Lock the specific dice to save the value."""
        for index in indices:
            self.dice[index - 1].lock()

    def unlock_dice(self, indices: List[int]) -> None:
        """Unlock the specific dice to enable reroll."""
        for index in indices:
            self.dice[index - 1].unlock()

    def unlock_all(self) -> None:
        """Unlock all dice."""
        for dice in self.dice:
            dice.unlock()

    def lock_all(self) -> None:
        """Lock all dice."""
        for dice in self.dice:
            dice.lock()

    def values(self) -> List[int]:
        """Return the values from the dice roll."""
        return [dice.get_value() for dice in self.dice]

    def reset(self) -> None:
        """Reset the dice set for the new player round."""
        for dice in self.dice:
            dice.unlock()

class Dice:
    """Class of dice, defines the functions of the dice such as roll, lock,
    unlock, and get value."""
    def __init__(self):
        self.sides = 6
        self.value = 1
        self.locked = False

    def roll(self) -> int:
        """Roll the dice."""
        if not self.locked:
            self.value = random.randint(1, self.sides)
        return self.value

    def lock(self) -> None:
        """Lock the dice."""
        self.locked = True

    def unlock(self) -> None:
        """Unlock the dice."""
        self.locked = False

    def get_value(self) -> int:
        """Return the value."""
        return self.value

class ScoreCard:
    """Class for scorecard. Enables score counting, recording, and getting the total score."""
    def __init__(self):
        self.scores = {}
        self.upper_cat = 0

    def record_scores(self, category: str, score: int) -> None:
        """Record the scores for each category."""
        self.scores[category] = score
        upper_category = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        if category in upper_category:
            self.upper_cat += score

    def total_score(self) -> int:
        """Return the sum of the scorecard for the player."""
        total = sum(self.scores.values())
        if self.upper_cat >= 63:
            total += 50
        return total

    @staticmethod
    def calculate_score(dice_values: List[int], category: str) -> int:
        """Calculate the result of the round and return the value."""
        if category == "ones":
            return dice_values.count(1) * 1
        elif category == "twos":
            return dice_values.count(2) * 2
        elif category == "threes":
            return dice_values.count(3) * 3
        elif category == "fours":
            return dice_values.count(4) * 4
        elif category == "fives":
            return dice_values.count(5) * 5
        elif category == "sixes":
            return dice_values.count(6) * 6
        elif category == "one_pair":
            pairs = [i for i in set(dice_values) if dice_values.count(i) >= 2]
            return max(pairs) * 2 if pairs else 0
        elif category == "two_pairs":
            pairs = [i for i in set(dice_values) if dice_values.count(i) >= 2]
            if len(pairs) >= 2:
                return sum(sorted(pairs)[-2:]) * 2
            return 0
        elif category == "three_of_a_kind":
            for i in set(dice_values):
                if dice_values.count(i) >= 3:
                    return i * 3
            return 0
        elif category == "four_of_a_kind":
            for i in set(dice_values):
                if dice_values.count(i) >= 4:
                    return i * 4
            return 0
        elif category == "full_house":
            unique_values = set(dice_values)
            if len(unique_values) == 2 and (dice_values.count(list(unique_values)[0]) in [2, 3]):
                return sum(dice_values)
            return 0
        elif category == "small_straight":
            return 15 if sorted(dice_values) == [1, 2, 3, 4, 5] else 0
        elif category == "large_straight":
            return 20 if sorted(dice_values) == [2, 3, 4, 5, 6] else 0
        elif category == "yatzy":
            return 50 if len(set(dice_values)) == 1 else 0
        elif category == "chance":
            return sum(dice_values)
        else:
            return 0
    @staticmethod
    def save_score(name, score):
        path = "score.csv"
        if os.path.isfile(path):          #Check if the path is valid
            with open(path, "a", encoding = 'utf8', newline="") as f:
                print(f"File {path} already exists, appending highscore of {name} with {score}")     #Opening the file as read only
                writer = csv.writer(f)
                writer.writerow([name, score])
        else:
            with open(path, "x", encoding = 'utf8', newline= "") as f:     #If its the first time calculating, create file and write the data
                writer = csv.writer(f)
                writer.writerow([name, score])
                print(f"Highscore of {name} with {score} score saved to {path}")
    @staticmethod
    def read_score():
        path = "score.csv"
        dic = {}
        if os.path.exists(path):                              #If the file already exists, update the data in the file
            with open(path, "r", encoding = 'utf8') as f:
                print("Previous players with their highscores")
                csv_reader = csv.reader(f, delimiter=",")        #Reading file using a csv reader and spliting the data
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
