from models.library import Library
from ui.console_ui import ConsoleUI
from utils.data_loader import load_sample_data

def main():
    library = Library()
    load_sample_data(library)

    ui = ConsoleUI(library)
    ui.run()

if __name__ == "__main__":
    main()