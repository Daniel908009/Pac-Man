# necesery imports
import pygame
import random
import threading
import time



    # Clases
# creating a player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, pac_man):
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
        if direction == "left":
            self.x -= pixel_size
        if direction == "right":
            self.x += pixel_size
        if direction == "up":
            self.y -= pixel_size
        if direction == "down":
            self.y += pixel_size

# creating a enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, state):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.state = state

    def draw(self, enemy):
        screen.blit(enemy, (self.x, self.y))
    
    def determine_direction(self, directions):
        # the most temporary solution to the problem, will be changed later
        self.direction = random.choice(["left", "right", "up", "down"])

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

# creating a dot class
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, image):
        screen.blit(image, (self.x, self.y))

# function to reset the game
def reset():
    # resetting the player and the enemies
    global player, enemy, num_of_enemies, enemy_coodinates, curent_direction, enemies
    player.x = 9*pixel_size
    player.y = 5*pixel_size
    curent_direction = ""
    i = 0
    for enemy in enemies:
        enemy.state = "disabled"
        enemy.x = enemy_coodinates[i][0]*pixel_size
        enemy.y = enemy_coodinates[i][1]*pixel_size
        i += 1
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
                    print(enemy.state)
                    break
        time.sleep(0.5)

        # first attempt at releasing the enemies failed
    #first_enemy_released = False
    #second_enemy_released = False
    #third_enemy_released = False
    #fourth_enemy_released = False
    #temp = []
    #for enemy in enemies:
    #    temp.append(enemy)
    #while running:
    #    if score > 10 and temp[0].state == "disabled":
    #        temp[0].state = "enabled"
    #        first_enemy_released = True
    #        print(temp[0].state)
    #    time.sleep(1)

# initialize pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((760, 600))
# setting up the title and icon
pygame.display.set_caption("Pac Man")
icon = pygame.image.load("pac man.png")
pygame.display.set_icon(icon)

pixel_size = 40
row = []
column = []
for i in range(0, 760, pixel_size):
    row.append(i)
for i in range(0, 600, pixel_size):
    column.append(i)
# creating a map of the walls, currently it will be done manually
map = [[[1],[1],[1],[],[],[],[],[],[1],[],[1],[],[],[],[],[],[1],[1],[1]], 
       [[1],[],[],[],[],[],[1],[],[1],[],[1],[],[1],[],[],[],[],[],[1]], 
       [[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1],[],[1]], 
       [[],[],[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[1],[],[]], 
       [[],[],[1],[],[],[],[],[1],[1],[],[1],[1],[],[],[],[],[1],[],[]], 
       [[],[],[],[],[],[1],[],[],[],[2],[],[],[],[1],[],[],[],[],[]], 
       [[],[],[],[],[1],[1],[],[1],[1],[2],[1],[1],[],[1],[1],[],[],[],[]], 
       [[],[1],[1],[],[],[1],[],[1],[2],[2],[2],[1],[],[1],[],[],[1],[1],[]], 
       [[],[],[],[],[],[],[],[1],[2],[2],[2],[1],[],[],[],[],[],[],[]], 
       [[],[1],[1],[1],[],[],[],[1],[1],[1],[1],[1],[],[],[],[1],[1],[1],[]], 
       [[],[],[],[],[],[1],[],[],[],[],[],[],[],[1],[],[],[],[],[]], 
       [[],[],[1],[],[],[1],[],[],[1],[1],[1],[],[],[1],[],[],[1],[],[]], 
       [[1],[],[1],[],[1],[1],[],[],[],[],[],[],[],[1],[1],[],[1],[],[1]], 
       [[1],[],[],[],[],[],[],[1],[1],[],[1],[1],[],[],[],[],[],[],[1]], 
       [[1],[1],[1],[],[],[],[],[1],[1],[],[1],[1],[],[],[],[],[1],[1],[1]]]

rows = len(row)
columns = len(column)
#print(rows, columns)

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

# creating the enemies
num_of_enemies = 4
enemy_image = pygame.image.load("ghost.png")
resized_enemy = pygame.transform.scale(enemy_image, (pixel_size, pixel_size))
enemy = []
enemy_coodinates = [[9, 7], [8, 7], [10, 7], [9, 8]]
enemies = pygame.sprite.Group()
for i in range(num_of_enemies):
    enemy.append(Enemy(enemy_coodinates[i][0]*pixel_size, enemy_coodinates[i][1]*pixel_size, (255, 0, 0), pixel_size, "disabled"))
    enemies.add(enemy[i])

# creating the player
pac_man = pygame.image.load("pac man image.png")
# resizing the image
resized_pac_man = pygame.transform.scale(pac_man, (pixel_size, pixel_size))
player = Player(9*pixel_size, 5*pixel_size, (0, 255, 0), pixel_size)
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

    # drawing the enemies
    for enemy in enemies:
        enemy.draw(resized_enemy)

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # checking for key presses to set the direction of the player
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
        player.x = 760
    if player.x > 760:
        player.x = 0
    if player.y < 0:
        player.y = 560
    if player.y > 560:
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
        print("You win!")
        running = False
    
    # drawing the player
    player.draw(resized_pac_man)

    # drawing grid, this is mainly for debugging
    for i in range(rows):
        pygame.draw.line(screen, (255, 255, 255), (row[i], 0), (row[i], 600))
    for i in range(columns):
        pygame.draw.line(screen, (255, 255, 255), (0, column[i]), (760, column[i]))

    # moving the enemies
    for enemy in enemies:
        # checking in which direction the enemy can move
        # if the enemy can move in multiple directions, the enemy will randomly choose a direction
        directions = []
        if enemy.x - pixel_size >= 0:
            if map[enemy.y//pixel_size][(enemy.x//pixel_size)-1] != [1]:
                directions.append("left")
        if enemy.x + pixel_size < 760:
            if map[enemy.y//pixel_size][(enemy.x//pixel_size)+1] != [1]:
                directions.append("right")
        if enemy.y - pixel_size >= 0:
            if map[(enemy.y//pixel_size)-1][enemy.x//pixel_size] != [1]:
                directions.append("up")
        if enemy.y + pixel_size < 600:
            if map[(enemy.y//pixel_size)+1][enemy.x//pixel_size] != [1]:
                directions.append("down")
        #print(directions)

        # the actual movement of the enemies
        enemy.determine_direction(directions)
        enemy.move(pixel_size)
        directions.clear()
    
    # checking for collision between player and enemies
    for enemy in enemies:
        if player.x == enemy.x and player.y == enemy.y:
            print("Game Over!")
            running = False

    # setting the frame rate
    pygame_clock.tick(4)

    # updating the screen
    pygame.display.update()

# quiting pygame
pygame.quit()