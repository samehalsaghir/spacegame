import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game_over state set to false
game_over = False

# Set up the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game")

# Set up clock
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
MILITANT = (132, 140, 115)
RED_DARK = (132, 0, 0)

def show_developer_credit():
    # Set up the credit screen
    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.Font('Grand9KPixel.ttf', 36)
    credit_text = font.render("Developed by", True, (255, 255, 255))
    name_text = font.render("Sameh Al Saghir", True, (255, 255, 255))
    
    # Position the text in the center of the screen
    credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    name_rect = name_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    
    # Display the text
    screen.blit(credit_text, credit_rect)
    screen.blit(name_text, name_rect)
    pygame.display.flip()
    
    # Wait for 3 seconds or until a key is pressed
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.time.Clock().tick(60)

def main_menu_screen():
    # Call the credit screen before initializing the menu
    show_developer_credit()
    
    global cursor_change_delay, last_cursor_change_time, cursor_images, current_cursor_index

# Define classes
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        # Remove the object if it goes off the screen
        if self.rect.top > SCREEN_HEIGHT:
            if isinstance(self, BlackFallingObject):  # Check if it's a black box
                lives[0] -= 1  # Deduct 1 life if a black cube reaches the bottom
                collision_sound_wall.play()
                bubbles = Bubbles(self.rect.centerx, SCREEN_HEIGHT)
                all_sprites.add(bubbles)
            self.kill()

class RedFallingObject(FallingObject):
    def __init__(self, speed):
        super().__init__("RedPlanet.png", speed)

class BlackFallingObject(FallingObject):
    def __init__(self, speed):
        super().__init__("WhiteStars2.png", speed)

class PurpleObject(pygame.sprite.Sprite):  
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("Astronaut.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = speed * 2  # 2 times the speed of black box

    def update(self):
        self.rect.y += self.speed
        # Remove the object if it goes off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 7):
            img = pygame.image.load(f"img/expl{num}.png")
            img = pygame.transform.scale(img, (60, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset aniation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

#create Sparks class
class Sparks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 7):
            img = pygame.image.load(f"img/spark{num}.png")
            img = pygame.transform.scale(img, (60, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        sparks_speed = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= sparks_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset aniation index
        if self.index >= len(self.images) - 1 and self.counter >= sparks_speed:
            self.kill()

#create Green Sparks class
class GSparks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/green{num}.png")
            img = pygame.transform.scale(img, (60, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        gsparks_speed = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= gsparks_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset aniation index
        if self.index >= len(self.images) - 1 and self.counter >= gsparks_speed:
            self.kill()

#create Bubbles class
class Bubbles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"img/bubbles{num}.png")
            img = pygame.transform.scale(img, (60, 60))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        bubbles_speed = 4
        #update bubbles animation
        self.counter += 1

        if self.counter >= bubbles_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset aniation index
        if self.index >= len(self.images) - 1 and self.counter >= bubbles_speed:
            self.kill()

def update_red_object_positions():
    # Update the positions of existing red box objects
    red_object_positions.clear()
    for obj in falling_objects:
        if isinstance(obj, RedFallingObject):
            red_object_positions.add(obj.rect.topleft)

# Measure distance between black and red objects
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Keep track of red box objects
red_object_positions = set()

# Create instances of FallingObject with images for black and red boxes
black_object_image = "WhiteStars2.png"  
red_object_image = "RedPlanet.png"  



def initialize_game():
    global score, lives, purple_spawn_timer, show_life_plus, show_game_over

    # Reset the set of red box positions
    red_object_positions.clear()

    score = 0
    lives = [3]  # Life counter starts at 3
    purple_spawn_timer = pygame.time.get_ticks() + 15000  # Timer for purple box spawn (15 seconds)

    # Variable to control +1 LIFE text display
    show_life_plus = False

    # Variable to control game over text display
    show_game_over = False

    # Animated cursor image
    global cursor_change_delay, last_cursor_change_time, cursor_images, current_cursor_index
    cursor_images = [pygame.image.load(f"ship_new{i}.png").convert_alpha() for i in range(1, 3)]
    # cursor_images = [pygame.transform.scale(pygame.image.load(f"ship_new{i}.png").convert_alpha(), (50, 60)) for i in range(1, 3)]
    current_cursor_index = 0  # Start with the first image
    cursor_change_delay = 100  # Delay between cursor changes in milliseconds
    last_cursor_change_time = 0  # Time of the last cursor change

# Function to get the non-transparent bounding rect of the cursor image
    def get_non_transparent_rect(image, margin):
        image_rect = image.get_rect()
        non_transparent_mask = pygame.mask.from_surface(image)
        non_transparent_points = non_transparent_mask.outline()
        min_x = min(non_transparent_points, key=lambda p: p[0])[0]
        max_x = max(non_transparent_points, key=lambda p: p[0])[0]
        min_y = min(non_transparent_points, key=lambda p: p[1])[1]
        max_y = max(non_transparent_points, key=lambda p: p[1])[1]
        width = max_x - min_x
        height = max_y - min_y
         # Subtract the margin from the width and height
        width -= 0 * margin
        height -= 0 * margin
         # Ensure width and height are non-negative
        width = max(0, width)
        height = max(0, height)
        return pygame.Rect(image_rect.left + min_x + margin, image_rect.top + min_y + margin, width, height)
        

    # Get the initial cursor rect
    global cursor_rect
    cursor_rect = get_non_transparent_rect(cursor_images[current_cursor_index], 10)
    # cursor = pygame.image.load("ship_new1.png")
    # cursor_rect = cursor.get_rect()
    

    # Hides Pygame cursor
    pygame.mouse.set_visible(False)

    # Create sprite groups
    global all_sprites, falling_objects, purple_objects
    all_sprites = pygame.sprite.Group()
    falling_objects = pygame.sprite.Group()
    purple_objects = pygame.sprite.Group()

    # Load background image
    global background_image
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load sound files
    global background_music, collision_sound_black, collision_sound_red, collision_sound_purple, collision_sound_wall, game_over_sound
    background_music = pygame.mixer.music.load("HoliznaCC0_Level2.mp3")
    collision_sound_black = pygame.mixer.Sound("Pickup_Coin97.wav")
    collision_sound_red = pygame.mixer.Sound("Explosion60.wav")
    collision_sound_purple = pygame.mixer.Sound("powerup18.wav")
    collision_sound_wall = pygame.mixer.Sound("Explosion40.wav")
    game_over_sound = pygame.mixer.Sound("GameOver.mp3")

    # Start playing music
    pygame.mixer.music.play(-1)

    # Set volume
    collision_sound_black.set_volume(0.6)
    collision_sound_red.set_volume(0.6)
    game_over_sound.set_volume(1.2)

def main_menu_screen():

    global cursor_change_delay, last_cursor_change_time, cursor_images, current_cursor_index

    cursor_images = [pygame.image.load(f"ship{i}.png").convert_alpha() for i in range(1, 3)]
    cursor_images = [pygame.transform.scale(img, (50, 60)) for img in cursor_images]
    current_cursor_index = 0
    cursor_change_delay = 100
    last_cursor_change_time = pygame.time.get_ticks()  # Initialize last_cursor_change_time here

    # Load sound files
    global background_music
    background_music = pygame.mixer.music.load("HoliznaCC0_Game_BOI_1_menu.wav")

    # Start playing music
    pygame.mixer.music.play(-1)

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    falling_objects = pygame.sprite.Group()

    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_change_time >= cursor_change_delay:
            last_cursor_change_time = current_time
            current_cursor_index = (current_cursor_index + 1) % len(cursor_images)

        # Load background image
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Display buttons
        font = pygame.font.Font("font.ttf", 30)
        play_text = font.render("PLAY", True, WHITE)
        quit_text = font.render("QUIT", True, WHITE)
        play_button_rect = play_text.get_rect(topleft=((SCREEN_WIDTH - play_text.get_width()) // 2, (SCREEN_HEIGHT - play_text.get_height()) // 2 + 40))
        quit_button_rect = quit_text.get_rect(topleft=((SCREEN_WIDTH - quit_text.get_width()) // 2, (SCREEN_HEIGHT - quit_text.get_height()) // 2 + 80))

        # Trademark text
        text = "Lipshitz Production™, 2024"
        font = pygame.font.Font("Grand9KPixel.ttf", 10)  # Choose your font and size
        text_surface = font.render(text, True, MILITANT)
        text_width, text_height = text_surface.get_size()
        text_x = (SCREEN_WIDTH - text_width) // 2
        text_y = SCREEN_HEIGHT - text_height - 10  # Adjust 20 pixels up from the bottom for some margin

    
        # Create falling objects
        if random.random() < 0.01:
            # Determine speed based on score
            speed = 3
            new_object = RedFallingObject(speed)
            all_sprites.add(new_object)
            falling_objects.add(new_object)

        all_sprites.update()
        all_sprites.draw(screen)
        screen.blit(cursor_images[current_cursor_index], (172, 450))


        #Logo
        logo = pygame.image.load("space_game_logo_1.png")
        logo = pygame.transform.scale(logo, (350, 100))
        screen.blit(logo, (28, 150))

        screen.blit(text_surface, (text_x, text_y))
        font = pygame.font.Font("font.ttf", 30)

        # Check for button events
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        if play_button_rect.collidepoint(pos):
            play_text = font.render("PLAY", True, RED_DARK)
        else:
            play_text = font.render("PLAY", True, MILITANT)
        if quit_button_rect.collidepoint(pos):
            quit_text = font.render("QUIT", True, RED_DARK)
        else:
            quit_text = font.render("QUIT", True, MILITANT)

        screen.blit(play_text, play_button_rect.topleft)
        screen.blit(quit_text, quit_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(pos):
                    initialize_game()
                    return  # Return from the function to restart the game
                if quit_button_rect.collidepoint(pos):
                    pygame.quit()
                    quit()
        
        pygame.display.flip()

def game_over_screen():
    font = pygame.font.Font("Grand9KPixel.ttf", 18)
    game_over_text2 = font.render(f"Your score is: {score}", True, RED)
    screen.blit(game_over_text2, ((SCREEN_WIDTH - game_over_text2.get_width()) // 2, 275))


    #Logo
    gameoverlogo = pygame.image.load("gameoverlogo1.png")
    gameoverlogo = pygame.transform.scale(gameoverlogo, (220, 140))

    screen.blit(gameoverlogo, (85, 120))
    
    # screen.blit(text_surface, (text_x, text_y))
    font = pygame.font.Font("font.ttf", 30)

    # Display buttons
    font = pygame.font.Font("font.ttf", 30)
    play_text = font.render("PLAY", True, WHITE)
    quit_text = font.render("QUIT", True, WHITE)
    play_button_rect = play_text.get_rect(topleft=((SCREEN_WIDTH - play_text.get_width()) // 2, (SCREEN_HEIGHT - play_text.get_height()) // 2 + 80))
    quit_button_rect = quit_text.get_rect(topleft=((SCREEN_WIDTH - quit_text.get_width()) // 2, (SCREEN_HEIGHT - quit_text.get_height()) // 2 + 120))

    # Trademark text
    text = "Lipshitz Production™, 2024"
    font = pygame.font.Font("Grand9KPixel.ttf", 10)  # Choose your font and size
    text_surface = font.render(text, True, MILITANT)
    text_width, text_height = text_surface.get_size()
    text_x = (SCREEN_WIDTH - text_width) // 2
    text_y = SCREEN_HEIGHT - text_height - 10  # Adjust 20 pixels up from the bottom for some margin

    screen.blit(text_surface, (text_x, text_y))
    font = pygame.font.Font("font.ttf", 30)

    # Check for button events
    while True:
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        if play_button_rect.collidepoint(pos):
            play_text = font.render("PLAY", True, RED_DARK)
        else:
            play_text = font.render("PLAY", True, MILITANT)
        if quit_button_rect.collidepoint(pos):
            quit_text = font.render("QUIT", True, RED_DARK)
        else:
            quit_text = font.render("QUIT", True, MILITANT)

        screen.blit(play_text, play_button_rect.topleft)
        screen.blit(quit_text, quit_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(pos):
                    initialize_game()
                    return  # Return from the function to restart the game
                if quit_button_rect.collidepoint(pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()



# Main game loop       
main_menu_screen()
running = True
while running:

    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Game over logic
    if lives[0] <= 0:
        pygame.mixer.music.stop()
        game_over_sound.play()
        game_over_screen()

    # Cursor / Ship Animation
    cursor_rect.center = pygame.mouse.get_pos()
    # Check if it's time to change the cursor image
    current_time = pygame.time.get_ticks()
    if current_time - last_cursor_change_time >= cursor_change_delay:
        last_cursor_change_time = current_time
        # Move to the next cursor image
        current_cursor_index = (current_cursor_index + 1) % len(cursor_images)

    # Update red object position to make sure it does not spawn on a black object
    update_red_object_positions()

    # Create falling objects
    if random.random() < 0.04:
        # Determine speed based on score
        speed = 3 + score // 25
        if random.random() < 0.4:
            new_object = BlackFallingObject(speed)
        else:
            new_object = RedFallingObject(speed)
        # Ensure that black box objects do not spawn too close to red box objects
        while isinstance(new_object, BlackFallingObject):
            new_object.rect.x = random.randrange(0, SCREEN_WIDTH - new_object.rect.width)
            new_object.rect.y = 0
            new_object_center = new_object.rect.center
            too_close = False
            for red_object_pos in red_object_positions:
                if distance(new_object_center, red_object_pos) < 40:
                    too_close = True
                    break
            if not too_close:
                break
        all_sprites.add(new_object)
        falling_objects.add(new_object)

    # Check and spawn purple object every 15 seconds
    if pygame.time.get_ticks() > purple_spawn_timer:
        new_purple_object = PurpleObject(3)  # Start purple objects with initial speed of 3
        all_sprites.add(new_purple_object)
        purple_objects.add(new_purple_object)
        purple_spawn_timer = pygame.time.get_ticks() + 15000  # Reset timer for next purple box spawn

    # Update sprites
    all_sprites.update()

# Check for collisions between falling objects and cursor position
    for obj in falling_objects:
        if cursor_rect.colliderect(obj.rect):
            # Handle collisions
            obj.kill()  # Remove the falling object
            if isinstance(obj, BlackFallingObject):
                collision_sound_black.play()
                score += 1  # Increase score if the cursor hits a black cube
                pos = pygame.mouse.get_pos()     
                sparks = Sparks(pos[0],pos[1])
                all_sprites.add(sparks)
            elif isinstance(obj, RedFallingObject):
                collision_sound_red.play()
                lives[0] -= 1  # Deduct 1 life if the cursor hits a red cube   
                pos = pygame.mouse.get_pos()     
                explosion = Explosion(pos[0],pos[1])
                all_sprites.add(explosion)

   # Check for collisions between purple objects and cursor position
    for obj in purple_objects:
        if cursor_rect.colliderect(obj.rect):
            # Handle collisions
            obj.kill()  # Remove the purple object
            collision_sound_purple.play()
            lives[0] += 1  # Increase life counter by 1
            pos = pygame.mouse.get_pos()     
            gsparks = GSparks(pos[0],pos[1])
            all_sprites.add(gsparks)
            life_plus_timer = pygame.time.get_ticks() + 3000  # Set timer for displaying +1 LIFE text
            show_life_plus = True  # Flag to indicate displaying +1 LIFE text

    # Draw everything
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

# Cursor / Ship
    
    screen.blit(cursor_images[current_cursor_index], cursor_rect.topleft)
    # Draw the cursor hitbox (rectangle)
    # pygame.draw.rect(screen, RED, cursor_rect, 2)
    
    # Display score and lives
    heart = pygame.image.load("heart_green.png")
    heart = pygame.transform.scale(heart, (28, 28))
    heart_rect = heart.get_rect()
    screen.blit(heart, (8, 55))

    stars = pygame.image.load("star_white_2.png")
    stars = pygame.transform.scale(stars, (32, 32))
    stars_rect = stars.get_rect()
    screen.blit(stars, (7, 10))


    font = pygame.font.Font("Grand9KPixel.ttf", 22)
    score_text = font.render(f"x  {score}", True, WHITE)
    screen.blit(score_text, (45, 10))
    life_text = font.render(f"x  {lives[0]}", True, WHITE)
    screen.blit(life_text, (45, 52))

    # Display +1 LIFE text for 3 seconds when life counter increases
    if show_life_plus:
        if pygame.time.get_ticks() < life_plus_timer:
            life_plus_text = font.render("+1 LIFE", True, GREEN)
            screen.blit(life_plus_text, (150, 50))
        else:
            show_life_plus = False  # Stop displaying +1 LIFE text after 3 seconds


    clock.tick(60)

    pygame.display.flip()

# Quit Pygame
pygame.quit()