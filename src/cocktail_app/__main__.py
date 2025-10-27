"""Entry point for the packaged cocktail app

Run with: python -m cocktail_app
"""
import tkinter as tk
from .gui import ModernCocktailExpertSystem

def main():
    root = tk.Tk()
    app = ModernCocktailExpertSystem(root)
    root.mainloop()

if __name__ == '__main__':
    main()
