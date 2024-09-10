import os
import pygame
import sys
from os.path import *



#run needs to be a list so that it can be changes in our if statements below
run = [True]

pygame.init()
pygame.display.set_caption("Main Menu")

# Font  Add more fonts here in future if desired
text_font = pygame.font.SysFont('Arial', 60)

# Draw text function 
def draw_text(text, font, text_col, outline_col, x, y):
    #create a text image
    img = font.render(text, True, text_col)
    #define the outline
    outline = font.render(text, True, outline_col)
    img_rect = img.get_rect(center=(x, y))
    outline_rect = outline.get_rect(center=(x, y))
    screen.blit(outline, outline_rect.move(3, 3))  # Black outline
    screen.blit(img, img_rect) # draw to screen


#add more text to screen in the future using function above 



# Global variables
WIDTH, HEIGHT = 1000, 650  # Updated window size

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Load button images
start_image = pygame.image.load('assets/Buttons/Game_Play.png').convert_alpha()
exit_image = pygame.image.load('assets/Buttons/Exit.png').convert_alpha()








# Create button class
#this is for all buttons. If more buttons need adding in future versions, add them using this class
class Button:
    def __init__(self, x, y, image, action=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y)) #get the rectangle from out image
        self.action = action   #this can all stay the same if you need to add more buttons
        self.clicked = False 

#draw function for buttons
    def draw(self):
        action = False
        # get mouse position 
        pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked conditions 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True   #action is what we use to check if something has been clicked
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked  = False
                
            
        # draw button on screen
        screen.blit(self.image, self.rect.topleft)

        return action #return action so that we can use our function in an if statement later
        
        






#clock class
class Clock_menu:
    def __init__(self, x, y):
        self.time_count = 0
        self.font = pygame.font.SysFont("Arial", 40)
        self.x = 160
        self.y = 25

#incriment the clock using tick_clock function
    def tick_clock(self):
        self.time_count += 1
        self.rounded_time = round(self.time_count / 49)

#draw the clock to the screen
    def draw_time(self, window):
        time_text = self.font.render("Time: " + str(self.rounded_time), True, (100, 100, 100))
        window.blit(time_text, (self.x, self.y))
        
        




 
# Create button instances
start_button = Button(WIDTH // 2 - start_image.get_width() // 2, HEIGHT // 2 - start_image.get_height() // 2, start_image, action=None)
exit_button = Button(10, 10, exit_image, action=None)






# Draw Things function
def draw_things(window, background, bg_image, clock_menu):
    for tile in background:
        window.blit(bg_image, tile) #draw background
        
    clock_menu.draw_time(window) #draw clock






# Draw background
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):  # use "for i" to incriment the x coordinate that the blocks are drawn at
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image








# Global variable to store the entered name
entered_name = ""  #empty to start 


#save username
def save_username():
 
    with open("scoreboard.txt", "a") as file:
        file.write(f"{entered_name}: 0")  
        







# Draw text input box with flashing cursor
def draw_text_input_box(x, y, width, height, text, cursor_visible, frame_count):
    #draw the rectangle
    pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)
    input_text_font = pygame.font.SysFont('Arial', 30)  #define font

    # Draw default text if input is empty
    if text == "":  #check for empty
        text_surface = input_text_font.render("Enter Username", True, (100, 100, 100))
    else:
        text_surface = input_text_font.render(text, True, (100, 100, 100))

    text_rect = text_surface.get_rect(topleft=(x + 5, y + 5))
    screen.blit(text_surface, text_rect)

    # Draw flashing cursor
    if cursor_visible and (frame_count // 30) % 2 == 0:  # Toggle cursor every half second
        cursor_x = text_rect.right + 2
        cursor_height = text_font.get_height()
        cursor_y = text_rect.y
        pygame.draw.line(screen, (100, 100, 100), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height/2.3), 2)









def print_scoreboard():
    scores = []
    
    # Open the scoreboard file and read the scores
    with open("scoreboard.txt", "r") as file:
        for line in file:
            name, time_str = line.strip().split(": ")
            if time_str:  # Check if time_str is not empty
                time = int(time_str)
                scores.append((name, time))
    
    # Sort scores based on the time component
    sorted_scores = sorted(scores, key=lambda x: x[1]) # define sorted_scores as a sorted version of the scores
    
    # Draw the scoreboard inside the box
    box_x, box_y, box_width, box_height = 50, 120, 250, 400
    line_spacing = 60
    
    # Render and display the top 7 scores
    for i, (name, time) in enumerate(sorted_scores[:6]):
        text_surface = text_font.render(f"{name}: {time}", True, (100, 100, 100))
        text_rect = text_surface.get_rect(topleft=(box_x + 10, box_y + 10 + i * line_spacing))
        screen.blit(text_surface, text_rect)

    # Draw the box outline
    pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, box_width, box_height), 2)










# Main game loop
def run_menu(window):
    
    #define clock_menu    
    clock_menu = Clock_menu(10, HEIGHT - 40)

    #menu states
    menu_state = [True]
    game_state = [False]
    
    #variables for cursor 
    global entered_name
    cursor_visible = True  
    frame_count = 0
    
    while menu_state[0]: #main while loop
        
        
        clock_menu.tick_clock() # run clock to begin incrimenting
        
        background, bg_image = get_background("green.png")  # Draw Background  # change colour here

        frame_count += 1 # incriment the frame count

        print_scoreboard() # print the score board with each itteration to keep it up to date
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #look for the x in the top corner being pressed
                run[0] = False
                return run
            
            # Handle text input events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    entered_name = entered_name[:-1]  # Remove the last character
                elif event.key == pygame.K_RETURN:
                    # Save the entered name to the scoreboard file
                    save_username()
                    # Clear the entered_name variable for the next user
                    entered_name = ""
                else:
                    entered_name += event.unicode  #key presses


        draw_things(window, background, bg_image, clock_menu) #draw all the main stuff
        
        # Draw title on top of background
        draw_text("Inferno Runner", text_font, (255, 255, 255), (0, 0, 0), WIDTH // 2, HEIGHT // 2 - 150)  
        
        # Draw text input box on top of background
        draw_text_input_box(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 40, entered_name, cursor_visible, frame_count)
        
        # Draw all buttons
        if exit_button.draw():
            menu_state[0] = False
            game_state[0] = False
            run[0] = False
            return run

        if start_button.draw():   #edit these if you want to add more functionality to a button
            menu_state[0] = False
            game_state[0] = True
        
        #display the score board on top of background
        print_scoreboard() 
        
        
        pygame.display.flip()  # Update the entire screen


