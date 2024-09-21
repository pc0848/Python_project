import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 1700, 1000)

FRAME_PER_SEC = 60

CREAT_ENEMY_EVENT = pygame.USEREVENT

HERO_SPEED = 5


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    def __init__(self, x, y):
        super().__init__("./images/background.png")
        self.rect.x = 479 * x
        self.rect.y = 699 * y

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed = random.randint(1, 5)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png")
        self.rect.y = SCREEN_RECT.height - 400
        self.rect.centerx = SCREEN_RECT.centerx

        self.bullet_group = pygame.sprite.Group()

    def update(self):
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height
        if self.rect.y < -self.rect.height:
            self.rect.y = SCREEN_RECT.height
        if self.rect.x > SCREEN_RECT.width:
            self.rect.x = -self.rect.width
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_RECT.width

    def fire(self):
        for i in (0, 20, 40):
            bullet = Bullet()
            bullet.rect.x = self.rect.centerx
            bullet.rect.y = self.rect.y - i
            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
