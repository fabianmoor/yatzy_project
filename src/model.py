"""Model File"""
import random
from typing import List
from src.methods import display_message

class Player:
    """Player class to initialize each player with their own set of 5 dice. Functions to
    roll the dice, lock and unlock specific dice, get the values from the dice rolls, and
    reset the dice for the next player round."""
    def __init__(self, name: str, game_type: int, categories: list):
        self.name = name
        self.scorecard = ScoreCard(game_type, categories)
        dice_count = 5 if game_type == 1 else 6
        self.dice = [Dice() for _ in range(dice_count)]
        self.roll = 0

    def save_roll(self, roll_count: int) -> None:
        """save the leftover rolls"""
        self.roll = roll_count

    def get_roll(self) -> int:
        """return the saved rolls"""
        return self.roll

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
    def __init__(self, game_type: int, categories: list):
        self.scores, self.used = {}, []
        for item in categories:
            self.scores[item] = 0
        self.upper_cat = 0
        self.game_type = game_type

    def record_scores(self, category: str, score: int) -> None:
        """Record the scores for each category."""
        self.scores[category] = score
        self.used.append(category)
        upper_category = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        if category in upper_category:
            self.upper_cat += score

    def total_score(self) -> int:
        """Return the sum of the scorecard for the player."""
        total = sum(self.scores.values())
        if self.game_type == 1:
            if self.upper_cat >= 63:
                total += 50
        else:
            if self.upper_cat >= 75:
                total += 50
        return total

    def print_card(self) -> None:
        """Print the scorecard"""
        items = list(self.scores.items())
        for i in range(0, len(items), 2):
            if i + 1 < len(items):
                display_message(
                    f"{items[i][0]:<20}: {items[i][1]:<10}\t"
                    f"{items[i + 1][0]:<20}: {items[i + 1][1]:<10}"
                )
            else:
                display_message(f"{items[i][0]:<20}: {items[i][1]:<10}")
        display_message(f"\nTotal: {self.total_score()}")
