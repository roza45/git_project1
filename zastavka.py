import os
import sys
import pygame
from random import randint
died = ''
pygame.init()
fontUI = pygame.font.Font(None, 30)
def load_image(name, colorkey='black'):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    main_text = ["ИГРА НА ДВОИХ",
                  "Правила игры",
                  "Чемпионат",
                  "Играть Пинг-Понг",
                  "Играть Танки"]
    chet1 = chet2 = 0
    fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_koord = 50
    koord = []
    for line in main_text:
        string_rendered = font.render(line, 1, pygame.Color('white'), (0, 50, 0))
        text_rect = string_rendered.get_rect()
        text_koord += 10
        text_rect.top = text_koord
        text_rect.x = 10
        text_koord += text_rect.height
        koord.append(text_rect)
        screen.blit(string_rendered, text_rect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                for rect in koord:
                    if rect.collidepoint(event.pos):
                        kuda = koord.index(rect)
                        if kuda == 4:
                            tanki()
        pygame.display.flip()
        clock.tick(FPS)

class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(screen, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                screen.blit(text, rect)
                i += 1
class Tank:
    def __init__(self, color, px, py, step, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, tile - 3, tile - 3)
        self.step = step
        self.moveSpeed = 2
        self.hp = 5

        self.shotime = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        keys = pygame.key.get_pressed()
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.step = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.step = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.step = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.step = 2

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotime == 0:
            dx = steps[self.step][0] * self.bulletSpeed
            dy = steps[self.step][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotime = self.shotDelay

        if self.shotime > 0:
            self.shotime -= 1

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        x = self.rect.centerx + steps[self.step][0] * 30
        y = self.rect.centery + steps[self.step][1] * 30
        pygame.draw.line(screen, 'white', self.rect.center, (x, y), 4)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            global died
            died = self.color

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(screen, 'yellow', (self.px, self.py), 2)
class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        screen.blit(imB, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

def tanki():
    global died
    for _ in range(50):
        while True:
            x = randint(0, WIDTH // tile - 1) * tile
            y = randint(0, HEIGHT // tile - 1) * tile
            rect = pygame.Rect(x, y, tile, tile)
            fined = False
            for obj in objects:
                if rect.colliderect(obj.rect):
                    fined = True

            if not fined:
                break

        Block(x, y, tile)
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        for bullet in bullets:
            bullet.update()
        c = 0
        for obj in objects:
            if obj.type == 'tank':
                c += 1
            obj.update()
        ui.update()
        screen.fill('black')
        if c != 2:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 50)
            text = font.render(f'deed {died}', True, 'green')
            screen.blit(text, (250, 250))
            pygame.display.update()
        else:
            for bullet in bullets:
                bullet.draw()
            for obj in objects:
                obj.draw()
            ui.draw()
            pygame.display.update()
            clock.tick(FPS)
    start_screen()



FPS = 50
steps = 5
tile =32
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
objects = []
bullets = []
imageblock = load_image('box.png')
imB = pygame.transform.scale(imageblock, (tile, tile))


tile_width = tile_height = 50
Tank('blue', 90, 260, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 640, 260, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))
steps = [[0, -1], [1, 0], [0, 1], [-1, 0]]
ui = UI()




start_screen()

pygame.quit()
terminate()



