import os
from random import randint as r


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def only_nums(s: str):
    choices = []
    for i in s:
        if i.isalnum():
            choices.append(int(i))
    return choices


def throw_dice():
    dice_results = []
    done = False
    throws = 0
    for i in range(5):
        dice_results.append(r(1, 6))

    while not done:
        if throws == 2:
            break
        clear()

        print(f"Results: {dice_results}")
        print("Do you want to re-throw?")
        x = input("[Y/n]: ")

        clear()

        if x.lower() == "n":
            done = True
        elif x.lower() == "y":
            print(f"Results: {dice_results}")
            print("Which dice do you want to re-throw?")
            print("(If multiple, write all): ")
            y = input("Options: 1, 2, 3, 4, 5: ")
            y = only_nums(y)
            clear()

        for i in y:
            dice_results[i - 1] = r(1, 6)
            print(dice_results)

        throws += 1
    return dice_results


if __name__ == "__main__":
    throw_dice()
