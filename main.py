from hand_tracking_module import HandMusicController

def main():
    """
    Initializes and runs the hand tracking music controller.
    """
    # Create an instance of the controller
    controller = HandMusicController()

    # Start the controller with a window display.
    # For Jupyter, you would call controller.start_notebook_display()
    controller.start_window_display()

if __name__ == "__main__":
    main()