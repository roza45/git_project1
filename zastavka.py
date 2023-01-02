import os
import sys
import pygame

pygame.init()
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
    intro_text = ["ИГРА НА ДВОИХ",
                  "Правила игры",
                  "Чемпионат",
                  "Играть Пинг-Понг",
                  "Играть Танки"]

    fon = pygame.transform.scale(load_image('fon3.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    coord = []
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'), (0, 50, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        coord.append(intro_rect)
        screen.blit(string_rendered, intro_rect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                for rect in coord:
                    if rect.collidepoint(event.pos):
                        kuda = coord.index(rect)
                        if kuda == 4:
                            window = pygame.display.set_mode((WIDTH, HEIGHT))

                            tanki()
                        #     play = True
                        #     while play:
                        #         for event in pygame.event.get():
                        #             if event.type == pygame.QUIT:
                        #                 play = False
                        #         keys = pygame.key.get_pressed()
                        #         for obj in objects:
                        #             obj.update()
                        #
                        #         screen.fill('black')
                        #         for obj in objects:
                        #
                        #             obj.draw()
                        #         pygame.display.update()
                        #         clock.tick(FPS)
        pygame.display.flip()
        clock.tick(FPS)


class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        print('error')
        keys = pygame.key.get_pressed()
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(screen, 'white', self.rect.center, (x, y), 4)
def tanki():

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        keys = pygame.key.get_pressed()
        for obj in objects:
            obj.update()

        screen.fill('black')
        for obj in objects:
            obj.draw()
        pygame.display.update()
        clock.tick(FPS)


FPS = 50
STEP = 5
TILE =32
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
objects = []

tile_width = tile_height = 50
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]





start_screen()

pygame.quit()
terminate()


