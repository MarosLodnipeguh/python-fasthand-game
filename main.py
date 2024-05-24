import gui
from logic import GameLogic

def main():
    app = gui.GameGUI()
    logic = GameLogic(app)
    app.set_logic(logic)
    app.run()

if __name__ == "__main__":
    main()
