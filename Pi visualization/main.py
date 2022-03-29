import numpy as np
import pygame
import time

pygame.init()

with open("settings.txt") as f:
    FPS = int(f.readline())
    if FPS > 150: FPS = 150

    limit = int(f.readline())

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()


class Line:
    def __init__(self, x, y, x1, y1):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1

    def draw(self):
        pygame.draw.line(screen, pygame.Color(255, 255, 255), (self.x, self.y), (self.x1, self.y1))


class Sprite:
    def __init__(self):
        self.x = self.new_x = width / 2
        self.y = self.new_y = height / 2
        self.step = 16.6 * FPS

        self.digits = open("1 million pi.txt", "r").read()
        self.counter = 0

        self.lines = []

    def update(self, dt):
        if self.counter < len(self.digits) and self.counter < limit:
            if self.digits[self.counter].isdigit():
                self.new_x = self.x + self.step * np.cos(np.deg2rad(36 * int(self.digits[self.counter]))) * dt
                self.new_y = self.y - self.step * np.sin(np.deg2rad(36 * int(self.digits[self.counter]))) * dt
                if self.new_x < 0 or self.new_x > width or self.new_y < 0 or self.new_y > height:
                    self.zoom_out()

                    self.new_x = self.x + self.step * np.cos(np.deg2rad(36 * int(self.digits[self.counter]))) * dt
                    self.new_y = self.y - self.step * np.sin(np.deg2rad(36 * int(self.digits[self.counter]))) * dt

                self.counter += 1

        self.lines.append(Line(self.x, self.y, self.new_x, self.new_y))

        self.x = self.new_x
        self.y = self.new_y

    def zoom_out(self):
        screen.fill(pygame.Color(0, 0, 0))

        (x0, y0) = (self.lines[0].x, self.lines[0].y)
        for ln in self.lines:
            dist_x = ln.x1 - ln.x
            dist_y = ln.y1 - ln.y
            save_x = x0 + (dist_x / 2)
            save_y = y0 + (dist_y / 2)

            pygame.draw.line(screen, pygame.Color(255, 255, 255), (x0, y0), (save_x, save_y))
            ln.x = x0
            ln.y = y0
            ln.x1 = save_x
            ln.y1 = save_y
            (x0, y0) = (save_x, save_y)

        self.x = x0
        self.y = y0
        self.step /= 2


sprite = Sprite()

prev_time = time.time()
deltaTime = 0

running = True
paused = False


def add_text(text, x, y, size):
    text_o = pygame.font.SysFont("Arial", size)
    rend = text_o.render(text, True, pygame.Color(100, 255, 255))
    screen.blit(rend, (x, y))


def pause():
    global paused, running
    while paused:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    paused = False
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = False


while running:
    pygame.time.Clock().tick(FPS)

    curr_time = time.time()
    deltaTime = curr_time - prev_time
    if deltaTime >= (1 / FPS):
        deltaTime = (1 / FPS)
    prev_time = curr_time

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = True
                pause()

    screen.fill(pygame.Color(0, 0, 0))
    if not paused:
        add_text("lines drawn: " + str(sprite.counter), 0, 0, 20)
        add_text("(max) lines per sec: " + str(FPS), 0, 20, 20)
    sprite.update(deltaTime)

    for line in sprite.lines:
        line.draw()

    pygame.display.flip()
