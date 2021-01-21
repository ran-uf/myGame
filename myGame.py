import pygame
import sys
import numpy as np


class MyObject(pygame.sprite.Sprite):
    def __init__(self, screen=None):
        super().__init__()
        self.moving = True
        self.image = None
        self.rect = None
        if screen is None:
            self.screen = pygame.display.set_mode((1200, 800))
        else:
            self.screen = screen
        self.pos = np.random.random(2)

    def next_pos(self):
        direction = np.random.random() * 2 * np.pi
        delta_x, delta_y = np.cos(direction), np.sin(direction)
        self.pos[0] += delta_x
        self.pos[1] += delta_y

    def blit(self):
        self.screen.blit(self.image, self.rect)


class Food(MyObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.image = pygame.image.load('images/food.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = int(np.random.random() * self.screen_rect.width)
        self.rect.centery = int(np.random.random() * self.screen_rect.height)

    def update(self):
        self.screen.blit(self.image, self.rect)


class Killer(MyObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.image = pygame.image.load('images/killer.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = int(np.random.random() * self.screen_rect.width)
        self.rect.centery = int(np.random.random() * self.screen_rect.height)

    def update(self):
        self.screen.blit(self.image, self.rect)


class NoneObject(MyObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.image = pygame.image.load('images/grass.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = int(np.random.random() * self.screen_rect.width)
        self.rect.centery = int(np.random.random() * self.screen_rect.height)

    def update(self):
        self.screen.blit(self.image, self.rect)


class Agent(MyObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen_rect = screen.get_rect()
        self.moving = False
        self.event_key = None
        self.image = pygame.image.load('images/agent.png')
        self.rect = self.image.get_rect()
        self.rect.centery = int(self.screen_rect.height * 0.7)
        self.rect.centerx = self.screen_rect.width // 2

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def move(self, direction):
        if direction == pygame.K_RIGHT:
            if self.rect.centerx < self.screen_rect.width:
                self.rect.centerx += 1
        elif direction == pygame.K_LEFT:
            if self.rect.centerx > 0:
                self.rect.centerx -= 1
        elif direction == pygame.K_UP:
            if self.rect.centery > 0:
                self.rect.centery -= 1
        elif direction == pygame.K_DOWN:
            if self.rect.centery < self.screen_rect.height:
                self.rect.centery += 1

    def update(self):
        if self.event_key is not None:
            if self.moving:
                self.move(self.event_key)
        self.blit()


class MyGame:
    def __init__(self, wnd_sz=None, bg_color=None):
        self.wnd_sz = wnd_sz
        self.bg_color = bg_color
        if wnd_sz is None:
            self.wnd_sz = (1200, 800)
        if bg_color is None:
            self.bg_color = (230, 230, 230)

        self.screen = pygame.display.set_mode((self.wnd_sz[0], self.wnd_sz[1]))
        self.agent = Agent(self.screen)
        self.foods = pygame.sprite.Group()
        self.none_objects = pygame.sprite.Group()
        self.killers = pygame.sprite.Group()
        for i in range(10):
            self.foods.add(Food(self.screen))
            self.none_objects.add(NoneObject(self.screen))
            self.killers.add(Killer(self.screen))

        self.score = 0

    def update(self, score):
        self.screen.fill(self.bg_color)
        self.agent.update()
        for food in self.foods.sprites():
            food.update()
        for killer in self.killers.sprites():
            killer.update()
        for o in self.none_objects.sprites():
            o.update()

        self.screen.blit(score.render("scores: " + str(self.score), True, pygame.Color(255, 0, 0), pygame.Color(230, 230, 230)),
                         (50, 50))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.agent.moving = True
                self.agent.event_key = event.key
            elif event.type == pygame.KEYUP:
                self.agent.moving = False

        ls = pygame.sprite.spritecollide(self.agent, self.foods, True)
        n = len(ls)
        if n != 0:
            self.score += n
            for i in range(n):
                self.foods.add(Food(self.screen))

        ls = pygame.sprite.spritecollide(self.agent, self.killers, False)
        if len(ls) != 0:
            text = pygame.font.Font('freesansbold.ttf', 115)
            self.screen.blit(text.render('killed', True, pygame.Color(255, 0, 0), pygame.Color(230, 230, 230)), (500, 300))
            pygame.display.flip()
            close = False
            while not close:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

    def run(self):
        pygame.init()
        pygame.display.set_caption("myGame")
        score = pygame.font.Font('freesansbold.ttf', 30)

        while True:
            # fill color
            self.check_events()

            self.update(score)

            # visualiaze the window
            pygame.display.flip()


if __name__ == "__main__":
    gm = MyGame()
    gm.run()
