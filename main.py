# necesery imports
import pygame
import random
import threading
import time



    # Clases
# creating a player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, image,shield):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.image = image
        self.shield = shield
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, pac_man):
        # drawing the player
        if curent_direction == "left":
            pac_man = pygame.transform.flip(pac_man, True, False)
        elif curent_direction == "right":
            pass
        elif curent_direction == "up":
            pac_man = pygame.transform.rotate(pac_man, 90)
        elif curent_direction == "down":
            pac_man = pygame.transform.rotate(pac_man, -90)
        screen.blit(pac_man, (self.x, self.y))

    def move(self, direction, pixel_size):
        # moving the player based on the direction
        if direction == "left":
            self.x -= pixel_size
        if direction == "right":
            self.x += pixel_size
        if direction == "up":
            self.y -= pixel_size
        if direction == "down":
            self.y += pixel_size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        #print(self.rect)

# creating a enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, state, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.state = state
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, enemy):
        # drawing the enemy
        screen.blit(enemy, (self.x, self.y))
    
    def determine_direction(self, walls):
            # the direction is determined randomly(I would like to implement a better AI for the enemies, but I am not skilled enough, so this will have to do)
        # checking if a direction is blocked by a wall and saving the possible direction
        if (self.x , self.y) in walls:
            print("in wall")
        possible_directions = ["left", "right", "up", "down"]
        try:
            # removing the direction the enemy came from(opposite direction of the current direction, if that makes sense)
            if self.direction == "left":
                possible_directions.remove("right")
            if self.direction == "right":
                possible_directions.remove("left")
            if self.direction == "up":
                possible_directions.remove("down")
            if self.direction == "down":
                possible_directions.remove("up")
        except:
            pass
        if (self.x+pixel_size , self.y) in walls:
            try:
                possible_directions.remove("right")
            except:
                pass
        if (self.x-pixel_size , self.y) in walls:
            try:
                possible_directions.remove("left")
            except:
                pass
        if (self.x , self.y+pixel_size) in walls:
            try:
                possible_directions.remove("down")
            except:
                pass
        if (self.x , self.y-pixel_size) in walls:
            try:
                possible_directions.remove("up")
            except:
                pass
        # setting the direction to a random direction from the possible directions
        # this has to be in a try block, because if the enemy moves inside the "cage", then it will have no possible directions
        try:
            self.direction = random.choice(possible_directions)
        except:
            # setting the direction to be the opposite of the current direction, this way the enemy can back out of the "cage"
            if self.direction == "left":
                self.direction = "right"
            if self.direction == "right":
                self.direction = "left"
            if self.direction == "up":
                self.direction = "down"
            if self.direction == "down":
                self.direction = "up"

    def move(self, pixel_size):
        # based on the direction the enemy will move
        if self.state == "enabled":
            if self.direction == "left":
                self.x -= pixel_size
            if self.direction == "right":
                self.x += pixel_size
            if self.direction == "up":
                self.y -= pixel_size
            if self.direction == "down":
                self.y += pixel_size
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

# creating a power up class
class Power_up(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, image):
        # drawing the power up
        screen.blit(image, (self.x, self.y))

# creating a dot class
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, image):
        # drawing the dots
        screen.blit(image, (self.x, self.y))

# function to reset the game
def reset():
    global player, enemy, num_of_enemies, enemy_coodinates, curent_direction, enemies, score, temp_score, dots, dots_list, number_of_dots, pixel_size, resized_dot, resized_pac_man, resized_enemy, width, height, column, row
    # getting the new width and height of the screen, currently causes a lot of issues
    width = int(pygame.display.get_surface().get_width())
    pixel_size = width//19
    height = pixel_size*15
    # width is set twice, because the width is not set correctly the first time(there is a float that would be rounded down or up, so the width would be off)
    width = pixel_size*19
    global screen, power_up, power_up_image, resized_power_up
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    # resetting the row and column lists
    row.clear()
    column.clear()
    for i in range(0, width, pixel_size):
        row.append(i)
    for i in range(0, height, pixel_size):
        column.append(i)

    # resizing the images
    resized_dot = pygame.transform.scale(dot_image, (pixel_size, pixel_size))
    resized_pac_man = pygame.transform.scale(pac_man, (pixel_size, pixel_size))
    resized_enemy = pygame.transform.scale(enemy_image, (pixel_size, pixel_size))
    resized_power_up = pygame.transform.scale(power_up_image, (pixel_size, pixel_size))
    # resetting the player and the enemies
    player.x = 9*pixel_size
    player.y = 5*pixel_size
    player.size = pixel_size
    player.rect = pygame.Rect(player.x, player.y, player.size, player.size)
    curent_direction = ""
    # reseting the list of coordinates of the walls
    global coords_of_walls
    coords_of_walls.clear()
    for i in range(columns):
        for j in range(rows):
            if map[i][j] == [1]:
                coords_of_walls.append((j*pixel_size, i*pixel_size))
    # resetting the enemies to have the new size and a new pixel size
    i = 0
    for enemy in enemies:
        #print("reseting enemy")
        enemy.x = enemy_coodinates[i][0]*pixel_size
        enemy.y = enemy_coodinates[i][1]*pixel_size
        enemy.size = pixel_size
        enemy.image = resized_enemy
        enemy.rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
        enemy.state = "disabled"
        i += 1
    # resetting the power up
    global power_up, rowup, columnup
    rowup = 0
    columnup = 0
    while (rowup, columnup) in coords_of_walls:
        rowup = random.choice(row)
        columnup = random.choice(column)
    power_up.x = rowup
    power_up.y = columnup
    power_up.size = pixel_size
    power_up.rect = pygame.Rect(power_up.x, power_up.y, power_up.size, power_up.size)
    # resetting the score
    global score, temp_score
    score = 0
    temp_score = 0
    # resetting the dots
    global dots, dots_list, number_of_dots
    dots = pygame.sprite.Group()
    dots_list = []
    for i in range(columns):
        for j in range(rows):
            if map[i][j] == [0]:
                dots_list.append(Dot(j*pixel_size, i*pixel_size, (255, 255, 0), 5))
                dots.add(dots_list[len(dots_list)-1])

# function to release the enemies after a certain score is reached
def releasing_enemies():
    global num_of_enemies, score, running, enemies, temp_score
    while running:
        # waiting for the score to reach 10, once it reaches 10 an enemy will be released
        if temp_score > 10:
            for enemy in enemies:
                if enemy.state == "disabled":
                    enemy.state = "enabled"
                    temp_score = 0
                    break
        time.sleep(0.5)

# function to display the game over screen
def game_over(text):
    global running, score, number_of_dots
    game_overa = True
    # main loop for the game over screen
    while game_overa:
        # setting the background color
        screen.fill((0, 0, 0))
        # displaying the text, saying if player won or lost
        font = pygame.font.Font("freesansbold.ttf", 32)
        texta = font.render(text, True, (255, 255, 255))
        screen.blit(texta, (300, 300))
        # displaying the score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (300, 350))
        # displaying how many dots are left
        dots_left = font.render("Dots left: " + str(number_of_dots-score), True, (255, 255, 255))
        screen.blit(dots_left, (300, 400))

        # updating the screen
        pygame.display.update()
        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                    game_overa = False
            if event.type == pygame.QUIT:
                running = False
                game_overa = False

# initialize pygame
pygame.init()
# setting up the screen
width = 760
height = 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# setting up the title and icon
pygame.display.set_caption("Pac Man")
icon = pygame.image.load("pac man.png")
pygame.display.set_icon(icon)

pixel_size = width//19
row = []
column = []
for i in range(0, width, pixel_size):
    row.append(i)
for i in range(0, height, pixel_size):
    column.append(i)
# creating a map of the walls, currently it will be done manually
map = [[[1],[1],[1],[1],[1],[1],[1],[1],[1],[],[1],[1],[1],[1],[1],[1],[1],[1],[1]], 
       [[1],[],[],[],[1],[],[],[],[1],[],[1],[],[],[],[1],[],[],[],[1]], 
       [[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1]], 
       [[],[],[1],[],[1],[],[1],[],[],[],[],[],[1],[],[1],[],[1],[],[]], 
       [[],[],[1],[],[],[],[1],[1],[1],[],[1],[1],[1],[],[],[],[1],[],[]], 
       [[],[],[1],[],[1],[],[],[],[],[2],[],[],[],[],[1],[],[1],[],[]], 
       [[],[],[],[],[1],[1],[],[1],[1],[2],[1],[1],[],[1],[1],[],[],[],[]], 
       [[],[1],[1],[],[],[1],[],[1],[2],[2],[1],[1],[],[1],[],[],[1],[1],[]], 
       [[],[],[],[],[],[],[],[1],[1],[2],[2],[1],[],[],[],[],[],[],[]], 
       [[],[1],[1],[1],[],[],[],[1],[1],[1],[1],[1],[],[],[],[1],[1],[1],[]], 
       [[],[],[],[],[],[1],[],[],[],[],[],[],[],[1],[],[],[],[],[]], 
       [[],[],[1],[],[1],[1],[],[1],[1],[1],[1],[1],[],[1],[1],[],[1],[],[]], 
       [[1],[],[1],[],[1],[1],[],[],[],[],[],[],[],[1],[1],[],[1],[],[1]], 
       [[1],[],[],[],[],[],[],[1],[1],[],[1],[1],[],[],[],[],[],[],[1]], 
       [[1],[1],[1],[1],[1],[1],[1],[1],[1],[],[1],[1],[1],[1],[1],[1],[1],[1],[1]]]

rows = len(row)
columns = len(column)

# creating a list of the coordinates of the walls
coords_of_walls = []
for i in range(columns):
    for j in range(rows):
        if map[i][j] == [1]:
            coords_of_walls.append((j*pixel_size, i*pixel_size))

dots = pygame.sprite.Group()
dots_list = []
dot_image = pygame.image.load("dot.png")
resized_dot = pygame.transform.scale(dot_image, (pixel_size, pixel_size))
number_of_dots = 0

# filing the remaining map with 0 for empty space
for i in range(columns):
    for j in range(rows):
        if map[i][j] == []:
            map[i][j].append(0)
            # creating the dots
            dots_list.append(Dot(j*pixel_size, i*pixel_size, (255, 255, 0), 5))
            dots.add(dots_list[len(dots_list)-1])
            number_of_dots += 1

# creating the power up in place of one of the dots, chosen randomly
power_up_image = pygame.image.load("power_up.png")
resized_power_up = pygame.transform.scale(power_up_image, (pixel_size, pixel_size))
# picking a random position for the power up, until it is not in a wall
rowup = 0
columnup = 0
while (rowup, columnup) in coords_of_walls:
    rowup = random.choice(row)
    columnup = random.choice(column)
power_up = Power_up(rowup, columnup, pixel_size)

# creating the enemies
num_of_enemies = 4
enemy_image = pygame.image.load("ghost.png")
resized_enemy = pygame.transform.scale(enemy_image, (pixel_size, pixel_size))
enemy = []
# starting coordinates of the enemies
enemy_coodinates = [[9, 7], [8, 7], [10, 8], [9, 8]]
enemies = pygame.sprite.Group()
for i in range(num_of_enemies):
    enemy.append(Enemy(enemy_coodinates[i][0]*pixel_size, enemy_coodinates[i][1]*pixel_size, (255, 0, 0), pixel_size, "disabled", resized_enemy))
    enemies.add(enemy[i])

# creating the player
pac_man = pygame.image.load("pac man image.png")
# resizing the image
resized_pac_man = pygame.transform.scale(pac_man, (pixel_size, pixel_size))
player = Player(9*pixel_size, 5*pixel_size, (0, 255, 0), pixel_size, resized_pac_man, False)
curent_direction = ""
score = 0
temp_score = 0

# setting up the clock
pygame_clock = pygame.time.Clock()

# setting up the game loop
running = True
# setting up a thread for the release of the enemies
thread1 = threading.Thread(target=releasing_enemies)
thread1.start()

# the game main loop
while running:

    # setting the background color
    screen.fill((0, 0, 0))

    # drawing the walls of the map
    for i in range(columns):
        for j in range(rows):
            if map[i][j] == [1]:
                pygame.draw.rect(screen, (0, 0, 255), (j*pixel_size, i*pixel_size, pixel_size, pixel_size))
    
    # drawing the dots
    for dot in dots:
        dot.draw(resized_dot)
    
    # drawing the power up
    power_up.draw(resized_power_up)

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # checking for key presses to set the direction of the player or reset the game
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if curent_direction == "right":
                    pass
                else:
                    curent_direction = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if curent_direction == "left":
                    pass
                else:
                    curent_direction = "right"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if curent_direction == "down":
                    pass
                else:
                    curent_direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if curent_direction == "up":
                    pass
                else:
                    curent_direction = "down"
            if event.key == pygame.K_r or event.key == pygame.K_r:
                reset()

    # moving the player
    if curent_direction == "left":
        player.move("left", pixel_size)
    if curent_direction == "right":
        player.move("right", pixel_size)
    if curent_direction == "up":
        player.move("up", pixel_size)
    if curent_direction == "down":
        player.move("down", pixel_size)
    else:
        pass

    # checking for collision between player and walls
    # if a collision is detected the player will be teleported to the other side of the screen
    if player.x < 0:
        player.x = width
    if player.x > width:
        player.x = 0
    if player.y < 0:
        player.y = height - pixel_size
    if player.y > height - pixel_size:
        player.y = 0
    
    # checking for collision between player and dots
    for dot in dots:
        if player.x == dot.x and player.y == dot.y:
            dots.remove(dot)
            dots_list.remove(dot)
            score += 1
            temp_score += 1
            break

    # checking for collision between player and inner walls
    for i in range(columns):
        for j in range(rows):
            if map[i][j] == [1]:
                if player.x == j*pixel_size and player.y == i*pixel_size:
                    if curent_direction == "left":
                        player.x += pixel_size
                    if curent_direction == "right":
                        player.x -= pixel_size
                    if curent_direction == "up":
                        player.y += pixel_size
                    if curent_direction == "down":
                        player.y -= pixel_size
                    break
    
    # checking for win
    if score == number_of_dots:
        game_over("You win!")

    # drawing grid, this is mainly for debugging
    for i in range(rows):
        pygame.draw.line(screen, (255, 255, 255), (row[i], 0), (row[i], height))
    for i in range(columns):
        pygame.draw.line(screen, (255, 255, 255), (0, column[i]), (width, column[i]))

    # moving the enemies
    for enemy in enemies:
        # checking if the enemy is enabled
        if enemy.state == "enabled":
            # if the enemy has a wall in the direction it is moving, it will change direction
            try:
                if enemy.direction == "left":
                    if (enemy.x-pixel_size, enemy.y) in coords_of_walls:
                        enemy.determine_direction(coords_of_walls)
                if enemy.direction == "right":
                    if (enemy.x+pixel_size, enemy.y) in coords_of_walls:
                        enemy.determine_direction(coords_of_walls)
                if enemy.direction == "up":
                    if (enemy.x, enemy.y-pixel_size) in coords_of_walls:
                        enemy.determine_direction(coords_of_walls)
                if enemy.direction == "down":
                    if (enemy.x, enemy.y+pixel_size) in coords_of_walls:
                        enemy.determine_direction(coords_of_walls)
                # actual movement of the enemy
                enemy.move(pixel_size)
            except:
                # this should only happen if the enemy doesnt have a direction yet
                enemy.determine_direction(coords_of_walls)
                
    # checking if enemy colided with outer walls, if yes it will be teleported to the other side of the screen
    for enemy in enemies:
        if enemy.x < 0:
            enemy.x = width - pixel_size
        if enemy.x > width - pixel_size:
            enemy.x = 0
        if enemy.y < 0:
            enemy.y = height - pixel_size
        if enemy.y > height - pixel_size:
            enemy.y = 0
        
    # checking for collision between the player and the power up
    if pygame.sprite.collide_rect(player, power_up):
        # creating a new power up
        power_up.x = random.choice(row)
        power_up.y = random.choice(column)
        power_up.rect = pygame.Rect(power_up.x, power_up.y, power_up.size, power_up.size)
        # applying a shield to the player
        player.shield = True
        resized_pac_man = pygame.transform.scale(pygame.image.load("shielded.png"), (pixel_size, pixel_size))
        
    # drawing the player
    player.draw(resized_pac_man)

    # drawing the enemies
    for enemy in enemies:
        enemy.draw(resized_enemy)
    
    # checking for collision between player and enemies
    if pygame.sprite.spritecollide(player, enemies, False):
        if player.shield:
            player.shield = False
            resized_pac_man = pygame.transform.scale(pygame.image.load("pac man image.png"), (pixel_size, pixel_size))
        else:
            game_over("You lost!")

    # setting the frame rate
    pygame_clock.tick(4)

    # updating the screen
    pygame.display.update()

# quiting pygame
pygame.quit()