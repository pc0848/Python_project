import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 1700, 1000)

FRAME_PER_SEC = 60

CREAT_ENEMY_EVENT = pygame.USEREVENT

HERO_SPEED = 5

ENEMY_FIRE = pygame.USEREVENT + 1


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
        self.rect.x = random.randint(0, max_x - 57)
        self.blood = random.randint(1, 3)
        self.fire_signal = random.randint(1, 2)
        self.scores = self.blood
        self.fire_space = 15
        self.fire_time = 100
        self.bullete_group = pygame.sprite.Group()
        self.bullete_fire_group = pygame.sprite.Group()

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.kill()

    def fire(self):
        if self.fire_time == 0:
            self.fire_space -= 1
            if self.fire_space in (0, 5, 10):
                bullete = BulletE()
                bullete.rect.x = self.rect.centerx
                bullete.rect.y = self.rect.y
                self.bullete_group.add(bullete)
                if self.fire_space == 0:
                    self.fire_time = 100
                    self.fire_space = 15

        else:
            self.fire_time -= 1


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png")
        self.rect.y = SCREEN_RECT.height - 400
        self.rect.centerx = SCREEN_RECT.centerx

        self.bullet_group = pygame.sprite.Group()
        self.fire_signal = 0
        self.blood = 5

    def update(self):
        if self.rect.y > SCREEN_RECT.height:
            self.rect.y = -self.rect.height
        if self.rect.y < -self.rect.height:
            self.rect.y = SCREEN_RECT.height
        if self.rect.x > SCREEN_RECT.width:
            self.rect.x = -self.rect.width
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_RECT.width

    def resurrection(self):
        self.rect.y = SCREEN_RECT.height - 400
        self.rect.centerx = SCREEN_RECT.centerx

        self.bullet_group = pygame.sprite.Group()
        self.fire_signal = 0
        self.blood = 5

    def fire(self):
        self.fire_signal -= 1
        if self.fire_signal in (20, 30, 40, 50, 60):
            bullet = Bullet()
            bullet.rect.x = self.rect.centerx
            bullet.rect.y = self.rect.y
            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png", -4)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class NewGame(GameSprite):
    def __init__(self):
        super().__init__("./images/again.png", 0)
        self.rect.center = SCREEN_RECT.center

    def update(self):
        self.rect.center = SCREEN_RECT.center


class Mouse(GameSprite):
    def __init__(self):
        super().__init__("./images/mouse.png", 0)
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class BulletE(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet2.png")
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_RECT.height:
            self.kill()
