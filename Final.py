import pygame
import random
pygame.init()
'***GLOBAL VARIABLES***'
laser_velocity = 15
width = 600
height = 600
player_x = 300
player_y = 540
bullets = []
enemy_bullets = []
enemies = [[], [], []]
run = True
game_over = False
wave_count = 10
score = 0
score_text = "Score: " + str(score)
lives = 3
lives_text = "Lives: " + str(lives)

player_sprite = pygame.image.load("ship.png")
clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

font = pygame.font.SysFont("bahnschrift", 20)

text = font.render(score_text, True, (0, 128, 0))
text1 = font.render(lives_text, True, (0, 128, 0))

# TODO:
#  - Add restart button??
#  - Add hit points for aliens??
'***CLASSES***'


class Bullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        pygame.draw.rect(window, (180, 255, 100), (self.x, self.y, 4, 10), 0)


class Enemy(object):
    # Enemy pictures
    alien1 = (pygame.image.load("enemy1_1.png"), pygame.image.load("enemy1_2.png"))
    alien2 = (pygame.image.load("enemy2_1.png"), pygame.image.load("enemy2_2.png"))
    alien3 = (pygame.image.load("enemy3_1.png"), pygame.image.load("enemy3_2.png"))

    aliens_images = (alien1, alien2, alien3)
    # speed is the number of pixel aliens move and frame is for frame alternator
    speed = 5
    frame = 0

    # initialization
    def __init__(self, x, y, point_value, alien_type):
        self.x = x
        self.y = y
        self.point_value = point_value
        self.alien_type = alien_type

    # draws alien in new position
    def draw(self, window):
        window.blit(self.aliens_images[self.alien_type][self.frame], (self.x, self.y))

    # moves alien
    def move(self):
        self.x += self.speed

    # alternates between 0 1
    def frame_alternator(self):
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    # checks if alien should move down
    def down_check(self):
        if self.x < 10  or self.x > 540:
            return True
        else:
            return False

    # reverses direction and shifts down
    def reverse_and_down(self):
        self.speed = self.speed * -1
        self.y += 20
        # offsets the last movement before frame updates
        self.x += 2 * self.speed

    # hit detection and deletes bullet
    def hit(self):
        for bullet in bullets:
            if self.x < bullet.x < self.x + 50 and self.y < bullet.y < self.y + 50:
                bullets.pop(bullets.index(bullet))
                return True
        return False

    # retrieves alien point value
    def get_point_value(self):
        return self.point_value

    # spawns alien bullet
    def fire(self):
        enemy_bullets.append(Bullet(self.x + 24, self.y + 50))


'***METHODS***'


# spanws aliens
def spawn(enemy_score_value):
    for j in range(3):
        for i in range(6):
            enemies[j].append(Enemy(68 * i + 15, 60 * j + 40, enemy_score_value * 10, j))


# redundant, possibly useful for restarting the game
def start():
    spawn(10)
    global run
    run = True


# determines whether the aliens should be moved down
def down_shifter():
    length_0 = len(enemies[0]) - 1
    length_1 = len(enemies[1]) - 1
    length_2 = len(enemies[2]) - 1
    if len(enemies[0]) > 0:
        if enemies[0][0].down_check() or enemies[0][length_0].down_check():
            return True
    if len(enemies[1]) > 0:
        if enemies[1][0].down_check() or enemies[1][length_1].down_check():
            return True
    if len(enemies[2]) > 0:
        if enemies[2][0].down_check() or enemies[2][length_2].down_check():
            return True
    return False


# randomly picks occupied row
def occupied_row():
    row_index = random.randint(0, 2)
    while len(enemies[row_index]) == 0:
        row_index = random.randint(0, 2)
    return row_index


# draws the images
def redraw():
    win.fill((0, 0, 0))
    win.blit(player_sprite, (player_x, player_y))

    # score and lives manager
    global score_text
    score_text = "Score: " + str(score)

    global text
    text = font.render(score_text, True, (0, 128, 0))
    win.blit(text, (10, 10))

    global lives_text
    lives_text = "Lives: " + str(lives)

    global text1
    text1 = font.render(lives_text, True, (0, 128, 0))
    win.blit(text1, (500, 10))

    # bullets and enemies
    for bullet in bullets:
        bullet.draw(win)

    for e_bullet in enemy_bullets:
        e_bullet.draw(win)

    for e in enemies:
        for i in range(len(e)):
            e[i].draw(win)

    pygame.display.update()


start()

# creates game events and their corresponding timers
fire_event = pygame.USEREVENT + 1
frame_event = pygame.USEREVENT + 2
move_event = pygame.USEREVENT + 3
pygame.time.set_timer(fire_event, 900)
pygame.time.set_timer(frame_event, 200)
pygame.time.set_timer(move_event, 200)
time_since_last_player_fire = pygame.time.get_ticks()
while run:
    clock.tick(30)

    # event handler loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == fire_event:
            index1_rand = occupied_row()
            index2_rand = random.randint(0, len(enemies[index1_rand]) - 1)
            enemies[index1_rand][index2_rand].fire()
        elif event.type == frame_event:
            for enemy in enemies:
                for i in range(len(enemy)):
                    enemy[i].frame_alternator()
        elif event.type == move_event:
            for enemy_list in enemies:
                for enemy in enemy_list:
                    enemy.move()
            if down_shifter():
                for e in enemies:
                    for i in e:
                        i.reverse_and_down()
        if len(enemies[0]) + len(enemies[1]) + len(enemies[2]) == 10:
            pygame.time.set_timer(frame_event, 50)
            pygame.time.set_timer(move_event, 50)

    # moves bullets, deletes bullet once it reaches floor or ceiling
    for shot in bullets:
        if shot.y > 0:
            shot.y -= laser_velocity
        else:
            bullets.pop(bullets.index(shot))

    # moves enemy bullets, deletes bullet once it reaches floor
    for shot in enemy_bullets:
        if shot.y < height:
            shot.y += laser_velocity
        else:
            enemy_bullets.pop(enemy_bullets.index(shot))

    # hit box detection for enemies and aliens
    for i in range(len(enemies)):
        for ship in enemies[i]:
            if ship.hit():
                score += ship.get_point_value()
                enemies[i].pop(enemies[i].index(ship))

    for shot in enemy_bullets:
        if player_x < shot.x < player_x + 50 and player_y < shot.y < player_y + 50:
            lives -= 1
            enemy_bullets.pop(enemy_bullets.index(shot))

    # checks if all aliens are dead
    if len(enemies[0]) == 0 and len(enemies[1]) == 0 and len(enemies[2]) == 0:
        wave_count += 10
        bullets.clear()
        enemy_bullets.clear()
        spawn(wave_count)
        pygame.time.set_timer(move_event, 200)
        pygame.time.set_timer(frame_event, 200)
        pygame.time.delay(500)

    # game over scenario
    if lives <= 0:
        game_over = True
        break

    # key listener
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and player_x - 10 > 0:
        player_x -= 10
    elif key[pygame.K_RIGHT] and player_x + 60 < width:
        player_x += 10
    if key[pygame.K_SPACE] and len(bullets) < 3 and pygame.time.get_ticks() - time_since_last_player_fire > 200:
        time_since_last_player_fire = pygame.time.get_ticks()
        bullets.append(Bullet(player_x + 24, player_y))
    redraw()

# if game ends displays game over text until player exits window
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
    text_game_over = font.render("GAMEOVER", True, (255, 0, 0))
    win.blit(text_game_over, (250, 250))
    pygame.display.update()

pygame.quit()