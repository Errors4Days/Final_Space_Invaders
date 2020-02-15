import pygame
pygame.init()

laser_velocity = 15
width = 600
height = 600
player_x = 300
player_y = 540
bullets = []
enemies = []
player_sprite = pygame.image.load("ship.png")
clock = pygame.time.Clock()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")


# Has a single wave with six ships
# Working components: alien movements, player movements, hit detection

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
    speed = 2

    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score

    def draw(self, window):
        self.move()
        frame = (self.x/6) % 2
        frame = int(frame)
        window.blit(self.alien1[frame], (self.x, self.y))

    def move(self):
        self.x += self.speed

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
                return True
        return False

    def points(self):
        return self.score


# redraws window with updated information
def redraw():
    win.fill((0, 0, 0))
    win.blit(player_sprite, (player_x, player_y))

    for enemy in enemies:
        enemy.draw(win)

    if enemies[0].down() or enemies[len(enemies) - 1].down():
        for e in enemies:
            e.reverse_and_down()

    for shots in bullets:
        shots.draw(win)

    pygame.display.update()


# spawns in first initial wave
for i in range(1, 7):
    enemies.append(Enemy(68 * i, 10, 10))

# main loop
run = True
while run:
    clock.tick(30)
    # exit loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # moves bullets, deletes bullet once it reaches ceiling
    for shot in bullets:
        if shot.y > 0:
            shot.y -= laser_velocity
        else:
            bullets.pop(bullets.index(shot))

    removal_list = []
    for e in enemies:
        if e.hit():
            bullets.pop()
            enemies.pop(enemies.index(e))
            break

    # key listener
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and player_x - 10 > 0:
        player_x -= 10
    elif key[pygame.K_RIGHT] and player_x + 60 < width:
        player_x += 10

    if key[pygame.K_SPACE] and len(bullets) < 1:
        bullets.append(Bullet(player_x + 24, player_y))

    redraw()

pygame.quit()
