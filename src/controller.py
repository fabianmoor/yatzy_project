from .model import Player
from .view import clear_screen, display_message, get_input, only_nums

class YatzyController:
    """Controller class to manage the game flow."""
    def __init__(self):
        self.player = Player("David")

    def play_game(self) -> None:
        """Main game loop for playing Yatzy."""
        self.player.reset()
        clear_screen()
        display_message("Welcome to Yatzy!")
        
        # First roll
        self.player.roll_unlocked()
        display_message(f"First roll: {self.player.values()}")
        
        count = 0
        while count < 3:
            self.player.lock_all()
            count += 1
            print("Which ones do you want to re-roll? (1,2,3,4,5)")
            lock_input = get_input("or type 'save':  ")

            if lock_input.lower() == 'save':
                break
            
            self.player.unlock_dice(only_nums(lock_input))
            self.player.roll_unlocked()
            display_message(f"New roll: {self.player.values()}")
        
        # Here you would implement score selection and recording
        display_message("Round over. Implement score recording here.") 