import pygame
from Game_Play_Linking import *
from Menu_Finished import *

pygame.init()

def run_things():

    while run[0]:
        run_menu(window) 
        if run[0]:
            game_main(window, Player)

run_things()

