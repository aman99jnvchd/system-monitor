import tkinter
from modules.gui import App
from modules.cli import run_cli

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except tkinter.TclError:
        run_cli()
