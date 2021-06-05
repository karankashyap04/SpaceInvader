import random
import math

import pygame
from pygame import mixer  # mixer helps with sounds and music

# Initializing PyGame
pygame.init()

# Creating game screen (i.e. game window/surface)
screen = pygame.display.set_mode((800, 600))
# parameters inside another set of brackets because passed as tuple; 800-> width; 600-> height (values in px)

# Default game window title is "pygame window". Changing this:
pygame.display.set_caption("Space Invaders")


# Background image:
# Image attribution: www.wallpaperscraft.com
background = pygame.image.load('background.jpg')

# Background music:
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 causes it to play infinitely on loop


# Creating player
# Image attribution: Icon made by Freepik (https://www.freepik.com) from Flaticon (www.flaticon.com)
playerImg = pygame.image.load('player.png')
# X and Y coordinates for image placement (note: top-left is (0,0); values increase towards right and bottom)
playerX = 368  # slightly less than half of width to account for width of image (64x64px)
playerY = 480  # lower part of screen

# We will use this later to move the player; will assign value later to control movement speed
playerX_change = 0


def player(x, y):  # Call function inside while running loop so player is displayed in every frame of the game
    # Drawing image of player on game window (need to draw after loading it)
    screen.blit(playerImg, (x, y))


# Creating enemy (creating as lists since we will have multiple enemies)
# Image attribution: Icon made by Freepik (https://www.freepik.com) from Flaticon (www.flaticon.com)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    # Want the enemy to spawn at a random position where 0 <= enemyX <= 736, and 50 <= enemyY <= 150
    enemyX.append(random.randint(0, 736 - 1))  # Keeping at 736-1 = 735 to be safe
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)



def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Creating bullet
# Image attribution: Icon made by Icongeek26 (https://www.flaticon.com/authors/icongeek26) from Flaticon (www.flaticon.com)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480 - 32  # Accounting for height of bullet image
bulletY_change = 10
bullet_state = "ready"  # ready state: can't see bullet on screen; fire state: bullet is currently moving


def fire_bullet(x, y):
    global bullet_state  # Accessing bullet_state variable which was defined outside the function
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y))


#Detecting if bullet and enemy have collided:
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))  # Standard euclidean distance formula in 2 dimensions
    if distance <= 27:
        return True
    return False


# Logging player score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)  # Freesansbold is a free pygame font; (Note: .ttf is just the inbuilt extension)
# Note: here, 32 is the font size

scoreX = 10
scoreY = 10

def show_score(x, y):
    # For text like this, first you have to render it, then you can blit it on the screen
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Display Game Over Screen
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# We need the game to continue running until the user quits it
# Creating an infinite loop that only terminates when the user clicks the cross button
running = True
while running:  # Game loop
    # Inside this loop, need to include all the events that happen within our game window

    # Default game window is plain black. Changing this INSIDE the while running loop (unlike when we changed the title) because this change is WITHIN the game window
    # and should persist as long as the game is played
    # screen.fill((245, 169, 236))  # Passing RGB values as a tuple

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Loop iterates through each event happening in the game window as the user plays the game, and in each iteration, we check the if condition below:

        # Check if cross button clicked (if QUIT is the event that happened)
        if event.type == pygame.QUIT:
            running = False  # Terminate loop if cross pressed

        # Check if any key is pressed by the user (Note: KEYDOWN checks if any key is pressed, not just down arrow)
        if event.type == pygame.KEYDOWN:
            # Check if left or right arrow pressed:
            if event.key == pygame.K_LEFT:
                playerX_change = -3  # Can change value to adjust movement speed; right now, value adjusted by 3 px per iteration
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            # Check if spacebar pressed:
            if event.key == pygame.K_SPACE and bullet_state == "ready":  # Also check if prev. bullet is still on screen; don't call fire_bullet() if still on screen
                # Bullet firing sound:
                bullet_Sound = mixer.Sound('laser.wav')  # Use mixer.Sound (not mixer.music, like before) because this is a short sound, not long music like background music
                bullet_Sound.play()

                bulletX = playerX  # Current x-coordinate of spaceship
                fire_bullet(bulletX, bulletY)
        # Check if any key is released (Note: KEYDOWN is if a key is pressed down; KEYUP is if a key is released)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Updating spaceship position
    playerX += playerX_change

    # Setting boundaries for spaceship movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Need to account for spaceship img width (i.e. 800-64 = 736)
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Check if game over:
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # If it is at 2000, it is out of the screen
            game_over_text()
            break

        # Updating enemy position
        enemyX[i] += enemyX_change[i]

        # Change enemy direction when it hits boundary, also move down by a little bit
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Checking for collisions (between enemy and bullet):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # Note: isCollision() returns a boolean value
        if collision:
            # Explosion sound:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

            bullet_state = "ready"
            bulletY = 480 - 32
            score_value += 1
            # Reset enemy coordinates: effectively cause enemy to respawn somewhere on the top
            enemyX[i] = random.randint(0, 736 - 1)
            enemyY[i] = random.randint(50, 150)

        # Calling enemy() function to draw enemy
        enemy(enemyX[i], enemyY[i], i)

    # Calling player() function to draw player. Calling after screen.fill because player needs to be drawn on top of screen background
    player(playerX, playerY)


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480 - 32
        bullet_state = "ready"  # Reset bullet_state to "ready" once the bullet is off the screen

    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)

    # Display score
    show_score(scoreX, scoreY)

    # Updating game window at end of while loop: when the next iteration starts, next game frame is shown.
    # To reflect the changes to the display caused by all the statements executed in the current iteration, update the display
    pygame.display.update()
