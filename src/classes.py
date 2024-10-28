import random
import os

class Player:
    """Player class to initialise each player with their own set of 5 dices. Functions to
    roll the dices, lock and unlock specific dices, get the values from the dicerolls and
    reset the dices for next player round."""
    def __init__(self, name: str):
        self.name = name
        self.scorecard = ScoreCard()
        self.dice = [Dice() for _ in range(5)]

    def roll_unlocked(self):
        """Roll all the dices that are unlocked. In the beginning of the round, all dices
        are unlocked"""
        return [dice.roll() for dice in self.dice]

    def lock_dice(self, indices: list):
        """Lock the specific dice/dices to save the value"""
        for index in indices:
            self.dice[index-1].lock()
    
    def unlock_all(self):
        for i in self.dice:
            i.unlock()
            
    def unlock_dice(self, indices: list):
        """Unlock the specific dice/dices to enable reroll"""
        for index in indices:
            self.dice[index].unlock()

    def values(self):
        """Return the values from the diceroll"""
        return [dice.get_value() for dice in self.dice]

    def reset(self):
        """Reset the diceset for the new player round"""
        for dice in self.dice:
            dice.unlock()
            dice.value = None

class Dice:
    """Class of dice, defines the functions of the dice such as roll, lock,
    unlock and get value"""
    def __init__(self):
        self.sides = 6
        self.value = 1
        self.locked = False

    def roll(self):
        """Roll the dice"""
        if self.locked == False:
            self.value = random.randint(1, self.sides)
        return int(self.value)

    def lock(self):
        """Lock the dice"""
        self.locked = True

    def unlock(self):
        """Unlock the dice"""
        self.locked = False

    def get_value(self):
        """Return the value"""
        return int(self.value)

class ScoreCard:
    """Class for scorecard. Enables score counting, recording and getting the total score"""
    def __init__(self):
        self.scores = {}

    def record_scores(self, category: str, score: int):
        """Record the scores for each category"""
        self.scores[category] = score

    def total_score(self):
        """Return the sum of the scorecard for the player"""
        return sum(self.scores.values())

    @staticmethod
    def calculate_score(dice_values: list[int], category: str) -> int:
        """Calculate the result of the round and return the value"""
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
            top = 0
            for i in range(1, 7):
                if dice_values.count(i) >= 2:
                    top = max(top, i)
            return top*2
        elif category == "two_pairs":
            total = 0
            for i in range(1, 7):
                if dice_values.count(i) >= 2:
                    total += i*2
                    return total
        elif category == "three_of_a_kind":
            for i in range(1, 7):
                if dice_values.count(i) >= 3:
                    return i*3
        elif category == "four_of_a_kind":
            for i in range(1, 7):
                if dice_values.count(i) >= 4:
                    return i*4
        elif category == "full_house":
            unique_values = set(dice_values)
            if len(unique_values) == 2 and (dice_values.count(list(unique_values)[0]) in [2, 3]):
                return sum(dice_values)
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

def clear_screen():
    """Clear the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def only_nums(ans: str):
    """Get int from input"""
    choices = []
    for char in ans:
        if char.isdigit():
            choices.append(int(char))
    return choices

david = Player("David")
david.roll_unlocked()
print("First roll:", david.values())
count = 0
while True:
    x = input("Do you want to re-roll: ")
    if x.lower() == "n" or count == 3:
        break
    david.unlock_all()
    count += 1
    y = input("Which ones do you want to lock: (1,2,3,4,5): ")
    david.lock_dice(only_nums(y))
    david.roll_unlocked()
    print(david.values())