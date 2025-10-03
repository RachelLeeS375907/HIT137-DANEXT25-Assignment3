import tkinter as tk
from gui_application import AIModelGUI


def main():
    # Create root window
    root = tk.Tk()
    
    # Initialize the GUI application
    app = AIModelGUI(root)
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    print("  AI Models Integration - Hugging Face")
    print("  Demonstrating Object-Oriented Programming Concepts")
    print("\nStarting application...")
    print("\nNote: First-time model loading may take a few moments")
    print("as models are downloaded from Hugging Face.\n")
    
    main()
