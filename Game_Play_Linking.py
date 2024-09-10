#import everything
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()
import pygame.mixer_music
import pygame.mixer
#import the run variable
from Menu_Finished import run 
pygame.mixer.init


#Set info
WIDTH, HEIGHT = 1000, 650

#FPS. Change this if you want it to look smoother (it may run slower due to computer specs)
FPS = 60

#player vel is how fast the player moves. you could change this to make the player faster or slower which could be used to change the difficulty of the game
PLAYER_VEL = 9

#set caption
pygame.display.set_caption("Game_play")





#define window (this is what we draw to)
window = pygame.display.set_mode((WIDTH, HEIGHT))





# flip sprites
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]






#function that loads sprites and sorts directional sprites
def load_sprite_sheets(dir1, dir2, width, height,direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):  # get all out images and find the width of the actul image part, then devide it by the whole size of the image so that we can get the width of just one part at a time
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites  #this swaps .png and assigns the image name a direction
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites) #this flips the image if it should be looking left
        else:
            all_sprites[image.replace(".png", "")] = sprites #this gets rid of the png
    return all_sprites
    



#load_block function
def load_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)  #96, 0 is the position of my image in the terrain file
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)










#Create Player class
class Player(pygame.sprite.Sprite):
    COLOR = (255, 255, 255)
    #set gravity 
    GRAVITY = 9.8
    #sprites
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    #create an animation delay
    ANIMATION_DELAY = 20
    
    fall_sound = pygame.mixer.Sound("assets/Sounds/Fall.mp3")
    jump_sound = pygame.mixer.Sound("assets/Sounds/Jump.mp3")
    move_sound = pygame.mixer.Sound("assets/Sounds/Run.mp3")
    double_jump = pygame.mixer.Sound("assets/Sounds/Double_jump.mp3")
        
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # Create a rectangle to make things like movement, collisions, etc, easier
        self.x_vel = 0 #velocities so we can see when its moving
        self.y_vel = 0
        self.mask = None
        #direction for sprite flipping
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0  # so that we can see how long we've been falling
        #for double jumps
        self.jump_count = 0
        #hit attributes
        self.hit = False
        self.hit_count = 0
        #lives (you can increase or decrease them here)
        self.lives = 3
        self.sprite = None
        #load in sounds
        self.fall_sound = pygame.mixer.Sound("assets/Sounds/Fall.mp3")
        self.jump_sound = pygame.mixer.Sound("assets/Sounds/Jump.mp3")
        self.move_sound = pygame.mixer.Sound("assets/Sounds/Run.mp3")
        self.double_jump = pygame.mixer.Sound("assets/Sounds/Double_jump.mp3")
        #mute toggle
        self.mute = [False]
        #finished variable
        self.Finished = False
        
    #jump function
    def jump(self):
        self.y_vel  = -self.GRAVITY * 1.4 # this multiplier will change how high you jump
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    #just moves the player
    def move(self, dx, dy):  # Displacement on each axis 
        self.rect.x += dx
        self.rect.y += dy


    #move left
    def move_left(self, vel):
        self.x_vel = -vel #notice that it's - so that its opposite to the right movement
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
        
    #move right
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    #function that makes hit
    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    #function that sets finished to true
    def make_Finished(self):
        self.Finished = True
            
    
    #loop function that updates everything
    def loop(self, FPS, game_state, clock):
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        #check if we finished
        if self.Finished:
            print (clock.rounded_time)
            game_state[0] = False
        #check if we're hit
        if self.hit:
            self.hit_count += 1
            if self.hit_count > 1 * FPS:
                self.hit = False
                self.hit_count = 0
                self.lives -= 1
                if self.lives <= 0:  # Check if the player has run out of lives
                    self.lives = 0  # Ensure lives don't go negative
                    
                    no_time() #this ends the game and gives you a score that wont be on the score board
                    game_state[0] = False
                    

    
        self.fall_count += 1 #this makes the player fall. (you can increase this to make the player fall faster although the gravity variable at the top is a better way to do that)
        self.update_sprite_and_sounds() #run the update function to update everything


#this draws the hearts on the screen
    def draw_lives(self):
            
        if self.lives == 3: #just keep adding if statements if you want to add more lives
            window.blit(Heart_1, (400, 25))
            window.blit(Heart_1, (480, 25))
            window.blit(Heart_1, (560, 25))

        if self.lives == 2:
            window.blit(Heart_1, (400, 25))
            window.blit(Heart_1, (480, 25))
            
        if self.lives == 1:
            window.blit(Heart_1, (400, 25))
        

    #landed function
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0 
        self.jump_count = 0   #this is for double jump later
        
    #if player colides with block above
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    #mute button toggle
    def mute_sound(self):
        if self.mute[0]:
            self.mute[0] = False
        else:
            self.mute[0] = True
        
    #update sprites and sound  (if you want more sounds, this is where you impliment them)
    def update_sprite_and_sounds(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit" #add hit sound here
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
                if self.mute[0] == False:
                    self.jump_sound.play()

            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
                if self.mute[0] == False:
                    self.jump_sound.play()
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
            if self.mute[0] == False:
                self.fall_sound.play()
        elif self.x_vel != 0:
            sprite_sheet = "run"
            if self.mute[0] == False:
                self.move_sound.play()
            
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction # direction makes sure we're looking the right was while playing these animations
        sprites = self.SPRITES[sprite_sheet_name]
        sprites_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # this insures we can play the frames (our choice of) frames apart and no matter how many frames are in a given animation it will still work 
        self.sprite = sprites[sprites_index]
        self.animation_count += 1  # this incriments the frame to keep playing the next one
        
        
    #keep sprite animations and sounds up to date
    def update(self):
        self.update_sprite_and_sounds()
        if self.sprite is not None:
            self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.sprite)

    
    def draw(self, win, offset_x):  # this is so we can draw the character
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y)) 


        
        

            





#class for objects (any objects that are added should inherit from this class)
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    #draw function for objects
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

#block class that inherits from the object class
class Block(Object):
    def __init__(self, x, y,size):
        super().__init__(x, y, size, size)
        block = load_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image) # gets rect for collisions

#flag class that inherits from object class
class Flag(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "Flag")
        self.spike = load_sprite_sheets("Traps", "Spikes", width, height)
        self.image = self.spike["Flag"][0]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y)) # I just used rect for this one instead of mask, can always be updated if needed

#class for spikes that also inherits from the object class
class Spike(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "Big_Spike")
        self.spike = load_sprite_sheets("Traps", "Spikes", width, height)
        self.image = self.spike["Big_Spike"][0]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))






# Load button images
exit_image = pygame.image.load('assets/Buttons/Exit.png').convert_alpha()
mute_image = pygame.image.load('assets/Buttons/Mute.png').convert_alpha()
options_image = pygame.image.load('assets/Buttons/Options.png').convert_alpha()
menu_image = pygame.image.load('assets/Buttons/Menu.png').convert_alpha()
Heart_1 = pygame.image.load('assets/Buttons/Heart.png').convert_alpha()
  
  
  
  
  


# Create button class
class Button:
    def __init__(self, x, y, image, action=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action
        self.clicked = False 

    #function that fraws our button
    def draw(self, screen):
        action = False
        # get mouse position 
        pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked conditions 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True #this means our button has been clicked
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked  = False
                
            
        # draw button on screen
        screen.blit(self.image, self.rect.topleft)

        return action #we return action so that we can use this function in an if statement later







#create a class for our game clock
class Clock:
    def __init__(self, x, y):
        self.time_count = 0 #clock starts at 0
        self.font = pygame.font.SysFont("Arial", 40)
        self.x = 160 #positioning on the screen
        self.y = 25

    #this incriments the clock
    def tick_clock(self):
        self.time_count += 1
        self.rounded_time = round(self.time_count / 49) #this just rounds the time and makes in incriment at a slower rate

    #this just draws our clock 
    def draw_time(self, window):
        time_text = self.font.render("Time: " + str(self.rounded_time), True, (100, 100, 100))
        window.blit(time_text, (self.x, self.y))
        

            
        




#create button instances 
exit_button = Button(10, 10, exit_image, action=None)
mute_button = Button(10 + exit_image.get_width() + 10, 10, mute_image, action=None)
menu_button = Button(WIDTH - menu_image.get_width() - 10, 10, menu_image, action=None)

buttons = exit_button, mute_button, 






#get background 
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    
    #cover the whole screen 
    for i in range(WIDTH // width + 1):  #(using for i means that we can draw one block after the other by just adding the width of a block to the x ordinate)
        for j in range(HEIGHT // height +1):
            pos = [i * width, j * height]
            tiles.append(pos)
            
    return tiles, image

#draw background, (and just about everything else)
def draw_things(window, background, bg_image, player, objects, offset_x, clock):
    #draw background
    for tile in background:
        window.blit(bg_image, tile)

    #draw objects
    for obj in objects:
        obj.draw(window, offset_x)    
        
    # Draw player
    player.draw(window, offset_x)
    
    # Draw buttons
    exit_button.draw(window)
    mute_button.draw(window)
    menu_button.draw(window) 

    # Draw time
    clock.draw_time(window)

    #draw lives
    player.draw_lives()
    

    pygame.display.update() #keep things updated
    
    
    
    
#looking for vertical collisions
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            #landing
            if dy > 0:
                player.rect.bottom = obj.rect.top 
                player.landed()
            #hitting head
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj) #add to list of collided objects

    
    
    
    return [collided_objects] if collided_objects else []







#make a function that handles horizontal collision
def collide(player, objects, dx):
    player.move(dx, 0)  # Move the player
    player.update()

    collided_objects = []  # Use a list to store all collided objects
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            collided_objects.append(obj)

    player.move(-dx, 0)  # Move the player back
    player.update()

    return collided_objects


    
    
    
    
#make a function for movement
def handle_move(player, objects):
    #look for key presses
    keys = pygame.key.get_pressed()
    
    #call our function and name it
    collide_left = collide(player, objects, -PLAYER_VEL) #-vel so that it moves right 
    collide_right = collide (player, objects, PLAYER_VEL)
    
    #start with no velocity
    player.x_vel = 0
    
    #is the user pushing buttons that matter
    if (keys[pygame.K_LEFT] and not collide_left) or (keys[pygame.K_a] and not collide_left):  #LITRALLY JUST LOOKING FOR BUTTON PRESSES
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] and not collide_right) or (keys[pygame.K_d] and not collide_right):  
        player.move_right(PLAYER_VEL)
        
    #call and name vertical collisions
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    #name everything one things
    to_check = [collide_left, collide_right, *vertical_collide]
    
    for sublist in vertical_collide:  #check for vertical collisions with spikes
        for obj in sublist:
            if obj and obj.name == "Big_Spike":
                player.make_hit()
                
    for sublist in to_check:  #check for collisisons with flag
        for obj in sublist:
            if obj and obj.name == "Flag":
                player.make_Finished()
  
                
    #add another for loop here to add more object collisions
  
  
  
  
  
  
#to save time to external file
def save_time(run_time):
    # Read all lines from the file
    with open("scoreboard.txt", "r") as file:
        lines = file.readlines()
    
    # Find the line ending with "0" and replace the "0" with the new run_time
    for i, line in enumerate(lines):
        if line.strip().endswith("0"):
            lines[i] = line.replace("0", str(run_time) + "\n")  # Replace "0" with run_time and add newline
            break
    
    # Rewrite the file with the updated content
    with open("scoreboard.txt", "w") as file:
        file.writelines(lines)





        
#add new line if no time is recorded 
def no_time():
        # Read all lines from the file
    with open("scoreboard.txt", "r") as file:
        lines = file.readlines()
    
    # Find the line ending with "0" and replace the "0" with the new run_time
    for i, line in enumerate(lines):
        if line.strip().endswith("0"):
            lines[i] = line.replace("0", "999") + "\n"  # Replace "0" with "999" and add newline
            break
    
    # Rewrite the file with the updated content
    with open("scoreboard.txt", "w") as file:
        file.writelines(lines)
    
    
    
    
    

    
    
    
#main function for running things 
def game_main(window, Player):
    
    #define block size
    block_size = 96

    
    #call background
    background, bg_image = get_background("Purple.png")
    
    #name things here
    player = Player(100, 100, 50, 50)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 4 // block_size) if i not in [7, 6, 11, 12, 14, 24, 28, 18, 22, 25, 26, 27]]
    
    #objects is a list that can be drawn. (if you wanted to add levels you could call this "level_1" instead and create another list called"level_2" that has a different layout, then just call them when the level is selected)
    objects = [
        *floor,
        Spike(block_size * 12, HEIGHT - block_size * 1, 46, 45), 
        Spike(block_size * 11, HEIGHT - block_size * 1, 46, 45),
        Spike(block_size * 24, HEIGHT - block_size * 1, 46, 45),
        Spike(block_size * 25, HEIGHT - block_size * 1, 46, 45),
        Spike(block_size * 26, HEIGHT - block_size * 1, 46, 45),
        Spike(block_size * 27, HEIGHT - block_size * 1, 46, 45),
        Spike(block_size * 28, HEIGHT - block_size * 1, 46, 45),
        Block(0, HEIGHT - block_size * 2, block_size), 
        Block(0, HEIGHT - block_size * 3, block_size),
        Block(0, HEIGHT - block_size * 4, block_size),
        Block(0, HEIGHT - block_size * 5, block_size),
        Block(0, HEIGHT - block_size * 6, block_size),
        Block(0, HEIGHT - block_size * 7, block_size),
        Block(0, HEIGHT - block_size * 8, block_size),
        Block(0, HEIGHT - block_size * 9, block_size),
        Block(block_size * 4, HEIGHT - block_size * 2, block_size),
        Block(block_size * 4, HEIGHT - block_size * 3, block_size),
        Block(block_size * 5, HEIGHT - block_size * 4, block_size),
        Block(block_size * 5, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 5, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 9, HEIGHT - block_size * 2, block_size),
        Block(block_size * 9, HEIGHT - block_size * 4, block_size), 
        Block(block_size * 9, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 8, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 8, HEIGHT - block_size * 2, block_size),
        Block(block_size * 8, HEIGHT - block_size * 4, block_size), 
        Block(block_size * 9, HEIGHT - block_size * 6, block_size), 
        Block(block_size * 10, HEIGHT - block_size * 2, block_size),
        Block(block_size * 10, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 12, HEIGHT - block_size * 5, block_size), 
        Block(block_size * 13, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 13, HEIGHT - block_size * 3, block_size),
        Block(block_size * 13, HEIGHT - block_size * 4, block_size), 
        Block(block_size * 13, HEIGHT - block_size * 5, block_size), 
        Block(block_size * 14, HEIGHT - block_size * 5, block_size), 
        Block(block_size * 15, HEIGHT - block_size * 3, block_size),
        Block(block_size * 16, HEIGHT - block_size * 3, block_size),
        Block(block_size * 16, HEIGHT - block_size * 4, block_size),
        Block(block_size * 16, HEIGHT - block_size * 5, block_size),
        Block(block_size * 16, HEIGHT - block_size * 6, block_size),
        Block(block_size * 16, HEIGHT - block_size * 7, block_size),
        Block(block_size * 17, HEIGHT - block_size * 3, block_size),
        Block(block_size * 19, HEIGHT - block_size * 4, block_size),
        Block(block_size * 20, HEIGHT - block_size * 5, block_size),
        Spike(block_size * 20, HEIGHT - block_size * 6, 46, 45),
        Block(block_size * 20, HEIGHT - block_size * 2, block_size),
        Block(block_size * 20, HEIGHT - block_size * 3, block_size),
        Block(block_size * 20, HEIGHT - block_size * 4, block_size),
        Block(block_size * 17, HEIGHT - block_size * 6, block_size),
        Block(block_size * 21, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 21, HEIGHT - block_size * 3, block_size), 
        Spike(block_size * 21, HEIGHT - block_size * 4, 46, 45), 
        Block(block_size * 23, HEIGHT - block_size * 4, block_size), 
        Block(block_size * 23, HEIGHT - block_size * 5, block_size), 
        Block(block_size * 23, HEIGHT - block_size * 6, block_size), 
        Block(block_size * 23, HEIGHT - block_size * 7, block_size), 
        Block(block_size * 29, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 30, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 30, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 31, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 31, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 32, HEIGHT - block_size * 2, block_size), 
        Block(block_size * 32, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 33, HEIGHT - block_size * 2, block_size),
        Block(block_size * 33, HEIGHT - block_size * 3, block_size), 
        Flag(block_size * 33, HEIGHT - block_size * 4, 23, 46), 
        Block(block_size * 34, HEIGHT - block_size * 2, block_size),
        Block(block_size * 34, HEIGHT - block_size * 3, block_size), 
        Block(block_size * 34, HEIGHT - block_size * 4, block_size), 
        Block(block_size * 34, HEIGHT - block_size * 5, block_size), 
        Block(block_size * 34, HEIGHT - block_size * 6, block_size), 
        Block(block_size * 34, HEIGHT - block_size * 7, block_size),       
        ]   # by using *floor we break down floor into all its elements and pass them all at once 
    

    #screen scroll things
    offset_x = 0 
    scroll_area_width = 350
    
    #game states
    menu_state = [False]
    game_state = [True]
    
    #clock
    clock = Clock(10, HEIGHT - 40)
    
    
    #main while loop
    while game_state[0]:
        #set clock running
        clock.tick_clock()
    
        
        
        #look for x being pressed in top right corner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run[0] = False
                return run
                
            #jump things
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_UP and player.jump_count < 2 or event.key == pygame.K_w and player.jump_count < 2:
                     player.jump()
            
            #check if exit button has been pressed
            if exit_button.draw(window):
                menu_state[0] = False
                game_state[0] = False
                run[0] = False
                return run
            
            #check if mute button has been pressed
            if mute_button.draw(window):
                player.mute_sound()#toggle on mute
                
            #check if menu button has been pressed
            if menu_button.draw(window):
                game_state[0] = False
                menu_state[0] = True #change game states
                
                
 
 

        player.loop(FPS, game_state, clock) #the function that keeps everything looping
        handle_move(player, objects) #the function that takes the key inputs
        draw_things(window, background, bg_image, player, objects, offset_x, clock) #the function that draws things
        
        if player.Finished:
            game_state[0] = False
            save_time(clock.rounded_time)
 


        if player.rect.top > HEIGHT:
            game_state[0] = False
            no_time()
            
        if (player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
              offset_x += player.x_vel
        pygame.display.update()
