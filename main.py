import gui
from logic import GameLogic

def main():
    logic = GameLogic()
    app = gui.GameGUI(logic)
    logic.set_gui(app)
    app.run()

if __name__ == "__main__":
    main()
