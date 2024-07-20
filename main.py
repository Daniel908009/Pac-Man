# necesery imports
import pygame
import random




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
            #pac_man = pygame.image.load("pac man.png")
            pac_man = pygame.transform.flip(pac_man, True, False)
        elif curent_direction == "right":
            #pac_man = pygame.image.load("pac man.png")
            pass
        elif curent_direction == "up":
            #pac_man = pygame.image.load("pac man.png")
            pac_man = pygame.transform.rotate(pac_man, 90)
        elif curent_direction == "down":
            #pac_man = pygame.image.load("pac man.png")
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
    def __init__(self, x, y, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, enemy):
        screen.blit(enemy, (self.x, self.y))

    def move(self, direction, pixel_size):
        if direction == "left":
            self.x -= pixel_size
        if direction == "right":
            self.x += pixel_size
        if direction == "up":
            self.y -= pixel_size
        if direction == "down":
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
    pass


# initialize pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600))
# setting up the title and icon
pygame.display.set_caption("Pac Man")
icon = pygame.image.load("pac man.png")
pygame.display.set_icon(icon)

pixel_size = 40
row = []
column = []
for i in range(0, 800, pixel_size):
    row.append(i)
for i in range(0, 600, pixel_size):
    column.append(i)
#print(row , column)
# creating a map of the walls, currently it will be done manually
map = [[[1],[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[1],[1]], 
       [[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[1]], 
       [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
       [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]], 
       [[],[],[],[],[],[],[],[1],[1],[],[1],[1],[],[],[],[],[],[],[],[]], 
       [[],[],[],[],[],[1],[],[],[],[],[0],[],[],[1],[],[],[],[],[],[]], 
       [[],[],[],[],[1],[1],[],[1],[1],[0],[1],[1],[],[1],[1],[],[],[],[],[]], 
       [[],[],[],[],[],[1],[],[1],[0],[0],[0],[1],[],[1],[],[],[],[],[],[]], 
       [[],[],[],[],[],[],[],[1],[0],[0],[0],[1],[],[],[],[],[],[],[],[]], 
       [[],[],[],[],[],[],[],[1],[1],[1],[1],[1],[],[],[],[],[],[],[],[]], 
       [[],[],[],[],[],[1],[],[],[],[],[],[],[],[1],[],[],[],[],[],[]], 
       [[],[],[],[],[],[1],[],[],[],[],[],[],[],[1],[],[],[],[],[],[]], 
       [[],[],[],[],[1],[1],[],[],[],[],[],[],[],[1],[1],[],[],[],[],[]], 
       [[1],[],[],[],[],[],[],[1],[1],[],[1],[1],[],[],[],[],[],[],[],[1]], 
       [[1],[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[1],[1]]]

rows = len(row)
columns = len(column)
#print(rows, columns)
#print(len(map), len(map[0]))

dots = pygame.sprite.Group()
dots_list = []
dot_image = pygame.image.load("dot.png")
resized_dot = pygame.transform.scale(dot_image, (pixel_size, pixel_size))

# filing the remaining map with 0 for empty space
for i in range(columns):
    for j in range(rows):
        if map[i][j] == []:
            map[i][j].append(0)
            # creating the dots
            dots_list.append(Dot(j*pixel_size, i*pixel_size, (255, 255, 0), 5))
            dots.add(dots_list[len(dots_list)-1])

# creating the enemies
num_of_enemies = 4
enemy_image = pygame.image.load("ghost.png")
resized_enemy = pygame.transform.scale(enemy_image, (pixel_size, pixel_size))
enemy = []
enemy_coodinates = [[9, 7], [8, 7], [10, 7], [9, 8]]
enemies = pygame.sprite.Group()
for i in range(num_of_enemies):
    enemy.append(Enemy(enemy_coodinates[i][0]*pixel_size, enemy_coodinates[i][1]*pixel_size, (255, 0, 0), pixel_size))
    enemies.add(enemy[i])

# creating the player
pac_man = pygame.image.load("pac man.png")
# resizing the image
resized_pac_man = pygame.transform.scale(pac_man, (pixel_size, pixel_size))
player = Player(9*pixel_size, 5*pixel_size, (0, 255, 0), pixel_size)
curent_direction = ""
pygame_clock = pygame.time.Clock()

running = True
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
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                #print("left")
                if curent_direction == "right":
                    pass
                else:
                    curent_direction = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                #print("right")
                if curent_direction == "left":
                    pass
                else:
                    curent_direction = "right"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                #print("up")
                if curent_direction == "down":
                    pass
                else:
                    curent_direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                #print("down")
                if curent_direction == "up":
                    pass
                else:
                    curent_direction = "down"
            if event.key == pygame.K_r or event.key == pygame.K_r:
                #print("reset")
                reset()
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
    if player.x < 0:
        player.x = 0
    if player.x > 760:
        player.x = 760
    if player.y < 0:
        player.y = 0
    if player.y > 560:
        player.y = 560
    
    # checking for collision between player and dots
    for dot in dots:
        if player.x == dot.x and player.y == dot.y:
            dots.remove(dot)
            dots_list.remove(dot)
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
    
    # drawing the player
    player.draw(resized_pac_man)

    # drawing grid, this is mainly for debugging
    for i in range(rows):
        pygame.draw.line(screen, (255, 255, 255), (row[i], 0), (row[i], 600))
    for i in range(columns):
        pygame.draw.line(screen, (255, 255, 255), (0, column[i]), (800, column[i]))

    # updating the enemies
    #enemies.update()
    #for i in range(num_of_enemies):
        #enemy[i].move()

    # setting the frame rate
    pygame_clock.tick(4)

    # updating the screen
    pygame.display.update()

# quiting pygame
pygame.quit()