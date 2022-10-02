from wx import App, Frame

from src import MainFrame, State

def main():
    app = App()
    frame = MainFrame(None, title = "Energy Clicker", state = State())
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()