# main.py
import time
from terminal import Terminal
from functions import Functions, log

"""
Toggle error prints
"""
ERR_PRINT_ENABLED = False

if __name__ == "__main__":
    print("Starting..")
    Terminal()
    while True:
        try:
            post_id = int(input("Enter the Definition ID: "))
            break
        except ValueError:
            log("ERR", "Invalid input. Please enter a valid number.")

    while True:
        choice = input("Upvote? (true/false): ").strip().lower()
        if choice in {"true", "false"}:
            direction = "up" if choice == "true" else "down"
            break
        log("ERR", "Invalid input. Please enter 'true' or 'false'.")

    while True:
        from pystyle import System, Center
        Functions.begin(post_id=post_id, direction=direction)
        System.Clear()
        print("\n\n")
        print(Center.XCenter("Cycle finished, beginning new cycle.."))
        print("\n")
        time.sleep(3)
