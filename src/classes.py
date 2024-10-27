import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def only_nums(s: str):
    choices = []
    for i in s:
        if i.isalnum():
            choices.append(int(i))
    return choices

class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.value = None
        self.locked = False

    def roll(self):
        if not self.locked:
            self.value = random.randint(1, self.sides)
        return self.value

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

class DiceSet:
    def __init__(self, num_dice=5, sides=6):
        self.dice = [Dice(sides) for _ in range(num_dice)]

    def roll_all(self):
        return [die.roll() for die in self.dice]

    def roll_unlocked(self):
        return [die.roll() if not die.locked else die.value for die in self.dice]

    def lock_dice(self, indices):
        for index in indices:
            self.dice[index-1].lock()

    def unlock_dice(self, indices):
        for index in indices:
            self.dice[index].unlock()

    def values(self):
        return [die.value for die in self.dice]

    def reset(self):
        for die in self.dice:
            die.unlock()
            die.value = None



while True:
    clear_screen()
    dice_set = DiceSet(num_dice=5)
    print("First roll:", dice_set.roll_all())
    x = input("Do you want to re-roll: ")

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
