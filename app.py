"""Main Program File"""
from src.controller import YatzyController
from src.view import clear_screen

import sys

def main() -> int:
    """Main function to start the Yatzy game."""

    controller = YatzyController()
    while True:
        # controller.show_menu()
        clear_screen()
        while True:
            menu_choice = int(input("\n" \
                                    "[1] Play Game,\n"\
                                    "[2] Show High Score,\n" \
                                    "[3] Quit:\n" \
                                    "\n" \
                                    "Choice: "))
            match menu_choice:
                case 1:
                    controller.start_game()
                    controller.play_game()
                case 2:
                    controller.show_highscores()
                case 3:
                    print("Quiting program...")
                    sys.exit(0)

if __name__ == "__main__":
    main()
