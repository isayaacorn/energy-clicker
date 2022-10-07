from wx import App

from src import MainFrame, State


def main():
    app = App()
    MainFrame(None, title="Energy Clicker", state=State()).Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
