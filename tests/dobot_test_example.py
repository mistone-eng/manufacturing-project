# Import from external/pydobotplus
from pydobotplus import Dobot, auto_connect_dobot

def main():
    dobot = auto_connect_dobot()
    dobot.speed(velocity=100, acceleration=100)
    dobot.move_to(200, 0, 0)
    dobot.home()
    print("Move complete")

if __name__ == "__main__":
    main()
