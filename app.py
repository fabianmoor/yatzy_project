from src.controller import YatzyController

def main() -> int:
    """Main function to start the Yatzy game."""
    controller = YatzyController()
    controller.play_game()
    return 0

if __name__ == "__main__":
    main()
