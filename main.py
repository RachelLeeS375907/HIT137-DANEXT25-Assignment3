"""
main.py - Main entry point for the application
This file brings together all modules and starts the application
"""
import tkinter as tk
from gui_application import AIModelGUI


def main():
    """
    Main function to start the application.
    Creates the root window and initializes the GUI.
    """
    # Create root window
    root = tk.Tk()
    
    # Initialize the GUI application
    app = AIModelGUI(root)
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    print("="*60)
    print("  AI Models Integration - Hugging Face")
    print("  Demonstrating Object-Oriented Programming Concepts")
    print("="*60)
    print("\nStarting application...")
    print("\nNote: First-time model loading may take a few moments")
    print("as models are downloaded from Hugging Face.\n")
    
    main()