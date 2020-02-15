import pygame
import random
pygame.init()

'''GLOBAL VARIABLES'''
laser_velocity = 15
width = 600
height = 600
player_x = 300
player_y = 540
wave = 0
wave_count = 1
bullets = []
enemy_bullets = []
enemies = []
enemy_tracker = []

game_over = False
game_score = 0
score_text = "Score: " + str(game_score)
lives = 3
lives_text = "Lives: " + str(lives)

player_sprite = pygame.image.load("ship.png")
clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

font = pygame.font.SysFont("bahnschrift", 20)

text = font.render(score_text, True, (0, 128, 0))
text1 = font.render(lives_text, True, (0, 128, 0))

# print(pygame.font.get_fonts())
# TODO:
#  - Increase speed as aliens decrease
#  - Rectify alien movements in enemy tracker
'''CLASSES'''


class Bullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        pygame.draw.rect(window, (180, 255, 100), (self.x, self.y, 4, 10), 0)


class Enemy(object):
    alien1 = (pygame.image.load("enemy1_1.png"), pygame.image.load("enemy1_2.png"))
    alien2 = (pygame.image.load("enemy2_1.png"), pygame.image.load("enemy2_2.png"))
    alien3 = (pygame.image.load("enemy3_1.png"), pygame.image.load("enemy3_2.png"))

    aliens_images = (alien1, alien2, alien3)
    speed = 5
    frame = 0

    def __init__(self, x, y, score, alien_type):
        self.x = x
        self.y = y
        self.score = score
        self.alien_type = alien_type

    def draw(self, window):
        window.blit(self.aliens_images[self.alien_type][self.frame], (self.x, self.y))

    def move(self):
        self.x += self.speed

    def frame_set(self):
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    def down(self):
        if self.x < 0 or self.x > 550:
            return True
        else:
            return False

    def reverse_and_down(self):
        self.speed = self.speed * -1
        self.y += 25

    def hit(self):
        for bullet in bullets:
            if self.x < bullet.x < self.x + 50 and self.y < bullet.y < self.y + 50:
                bullets.remove(bullet)
                return True
        return False

    def points(self):
        return self.score

    def fire(self):
        enemy_bullets.append(Bullet(self.x + 24, self.y + 50))


'''FUNCTIONS'''


# spawns in wave
def spawn(score):
    enemies.clear()
    for j in range(0, 3):
        for i in range(1, 8):
            enemies.append(Enemy(68 * i, 60 * j + 40, score * 10, j))

    enemy_tracker.append(enemies[0])
    enemy_tracker.append(enemies[len(enemies) - 1])


# redraws window with updated information
def redraw():
    win.fill((0, 0, 0))
    win.blit(player_sprite, (player_x, player_y))

    # score and lives manager
    global score_text
    score_text = "Score: " + str(game_score)

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

    for e1 in enemies:
        e1.draw(win)

    pygame.display.update()


def find_new_extreme(side):
    for enemy in enemies:
        if side == 0 and enemy_tracker[0].x <= enemy.x:
            enemy_tracker[0] = enemy

'''MAIN LOOP'''

# spawns in first initial wave
spawn(wave_count)
wave_count += 1

# creates game events
fire_event = pygame.USEREVENT + 1
frame_event = pygame.USEREVENT + 2
move_event = pygame.USEREVENT + 3

pygame.time.set_timer(fire_event, 900)
pygame.time.set_timer(frame_event, 200)
pygame.time.set_timer(move_event, 200)

# main loop
run = True
time_since_last_player_fire = pygame.time.get_ticks()
while run:
    clock.tick(30)

    # event handler loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == fire_event:
            index_rand = random.randint(0, len(enemies) - 1)
            enemies[index_rand].fire()
        elif event.type == frame_event:
            for enemy in enemies:
                enemy.frame_set()
        elif event.type == move_event:
            for enemy in enemies:
                enemy.move()
            print(enemy_tracker[0].x)
            if enemy_tracker[0].down() or enemy_tracker[1].down():
                for e in enemies:
                    e.reverse_and_down()

    # moves bullets, deletes bullet once it reaches ceiling
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
    for enemy in enemies:
        if enemy.hit():
            enemies.pop(enemies.index(enemy))
            if enemy_tracker[0] == enemy:
                find_new_extreme(0)
            elif enemy_tracker[1] == enemy:
                find_new_extreme(1)
            game_score += enemy.points()
            break

    for shot in enemy_bullets:
        if player_x < shot.x < player_x + 50 and player_y < shot.y < player_y + 50:
            lives -= 1
            enemy_bullets.pop(enemy_bullets.index(shot))

    # if all enemies are dead, send in next wave. wave determines alien sprites
    if len(enemies) == 0:
        wave += 1
        if wave > 2:
            wave = 0
        spawn(wave_count)
        wave_count += 1

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
