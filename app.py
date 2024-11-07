"""Main Program File"""
import sys
from src.controller import Controller
from src.methods import read_score, clear_screen, print_error


def main() -> int:
    """Main function to start the Yatzy game."""
    clear_screen()
    while True:
        try:
            menu_choice = int(input("\n"
                                    "[1] Play Game\n"
                                    "[2] Show High Score\n"
                                    "[3] Quit:\n"
                                    "\n"
                                    "Choice: "))

            match menu_choice:
                case 1:
                    game_choice = int(input("\n"
                                            "[1] Yatzy\n"
                                            "[2] Maxi Yatzy\n"
                                            "\n"
                                            "Choice: "))

                    if game_choice == 1:
                        controller = Controller(1)
                    else:
                        controller = Controller(2)
                    controller.start_game()
                    controller.play_game()
                case 2:
                    clear_screen()
                    read_score(10)
                case 3:
                    print("Quiting program...")
                    sys.exit(0)
        except ValueError:
            print_error()

if __name__ == "__main__":
    main()
