# necesery imports
import pygame
import random




    # Clases
# creating a player class
class Player:
    def __init__(self, x, y, color, size):
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
class Enemy():
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, direction, pixel_size):
        if direction == "left":
            self.x -= pixel_size
        if direction == "right":
            self.x += pixel_size
        if direction == "up":
            self.y -= pixel_size
        if direction == "down":
            self.y += pixel_size

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

#enemies = pygame.sprite.Group()
pixel_size = 40
row = []
column = []
for i in range(0, 800, pixel_size):
    row.append(i)
for i in range(0, 600, pixel_size):
    column.append(i)
#print(row , column)
map = []
for i in range(len(row)):
    map.append([])
    for j in range(len(column)):
        map[i].append(0)
#print(map)
rows = len(row)
columns = len(column)

num_of_enemies = 4
enemy = []
for i in range(num_of_enemies):
    enemy.append(Enemy(random.choice(row), random.choice(column), (255, 0, 0), pixel_size))

# creating the player
pac_man = pygame.image.load("pac man.png")
# resizing the image
resized_pac_man = pygame.transform.scale(pac_man, (pixel_size, pixel_size))
player = Player(random.choice(row), random.choice(column), (0, 255, 0), pixel_size)
curent_direction = ""
pygame_clock = pygame.time.Clock()

#for i in range(num_of_enemies):
 #   enemy = Enemy(random.randint(0, 800), random.randint(0, 600), (255, 0, 0), 20)
  #  enemies.add(enemy)

running = True
while running:

    # setting the background color
    screen.fill((0, 0, 0))

    # drawing grid, this is mainly for debugging
    for i in range(rows):
        pygame.draw.line(screen, (255, 255, 255), (row[i], 0), (row[i], 600))
    for i in range(columns):
        pygame.draw.line(screen, (255, 255, 255), (0, column[i]), (800, column[i]))

    # drawing the player
    player.draw(resized_pac_man)

    # drawing the enemies
    #for enemy in enemies:
        #enemy.draw()
    for i in range(num_of_enemies):
        enemy[i].draw()

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                print("left")
                curent_direction = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                print("right")
                curent_direction = "right"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                print("up")
                curent_direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                print("down")
                curent_direction = "down"
            if event.key == pygame.K_r or event.key == pygame.K_r:
                print("reset")
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