
import pygame
import sys
from menu import start_menu


print(sys.argv)
if len(sys.argv) == 2:
    if sys.argv[1] == "affichage2D":
        from menu_2D import start_menu_2D
        start_menu_2D()
else:
    start_menu()


