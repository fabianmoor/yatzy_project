"""View file"""
import os

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
