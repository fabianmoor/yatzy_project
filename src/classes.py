import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def only_nums(ans: str):
    choices = []
    for char in ans:
        if char.isalnum():
            choices.append(int(char))
    return choices

class Dice:
    def __init__(self):
        self.sides = 6
        self.value = None
        self.locked = False

    def roll(self):
        self.value = random.randint(1, self.sides)
        return self.value

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def get_value(self):
        return self.value

class DiceSet:
    def __init__(self, num_dice):
        self.dice = [Dice() for _ in range(num_dice)]

    def roll_all(self):
        return [dice.roll() for dice in self.dice]

    def roll_unlocked(self):
        return [dice.roll() if not dice.locked else dice.value for dice in self.dice]

    def lock_dice(self, indices: list):
        for index in indices:
            self.dice[index-1].lock()

    def unlock_dice(self, indices: list):
        for index in indices:
            self.dice[index].unlock()

    def values(self):
        return [dice.get_value for dice in self.dice]

    def reset(self):
        for dice in self.dice:
            dice.unlock()
            dice.value = None



while True:
    clear_screen()
    dice_set = DiceSet(5)
    print("First roll:", dice_set.roll_all())
    x = input("Do you want to re-roll: ")
    result = []
    if x.lower() == "y":
        y = input("Which ones do you want to lock: (1,2,3,4,5): ")
        clear_screen()
        result = only_nums(y)

    for i in result:
        dice_set.lock_dice([i])
        #print(i)
    print("Roll Unlocked Dice:", dice_set.roll_unlocked())
    time.sleep(10)




#print("Current Values:", dice_set.values())


#dice_set.unlock_dice([0, 2])


#print("Final Roll:", dice_set.roll_all())
