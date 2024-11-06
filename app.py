"""Main Program File"""
from src.controller import Controller
from src.view import clear_screen

def main() -> int:
    """Main function to start the Yatzy game."""

    while True:
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
                    game_choice = int(input("\n" \
                                    "[1] Yatzy,\n"\
                                    "[2] Maxi Yatzy\n" \
                                    "\n" \
                                    "Choice: "))
                    match game_choice:
                        case 1:
                            controller = Controller(0)
                        case 2:
                            controller = Controller(1)
                    controller.start_game()
                    controller.play_game()
                case 2:
                    controller.show_highscores()


if __name__ == "__main__":
    main()
