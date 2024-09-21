import random
import pygame


SCREEN_RECT = pygame.Rect(0, 0, 1700, 1000)

FRAME_PER_SEC = 60

CREAT_ENEMY_EVENT = pygame.USEREVENT

HERO_SPEED = 5

ENEMY_FIRE = pygame.USEREVENT + 1

FRAME = pygame.USEREVENT + 2

BLOOD = pygame.USEREVENT + 3


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

        ik_1 = "./images/enemy1_down1.png"
        ik_2 = "./images/enemy1_down2.png"
        ik_3 = "./images/enemy1_down3.png"
        ik_4 = "./images/enemy1_down4.png"
        self.ik_list = [ik_1, ik_2, ik_3, ik_4]
        self.ik_signal = 0

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

    def die(self):
        self.speed = 0
        if self.ik_signal < 4:
            self.image = pygame.image.load(self.ik_list[self.ik_signal])
            self.ik_signal += 1
        elif self.ik_signal == 4:
            self.ik_signal += 1


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png")
        self.rect.y = SCREEN_RECT.height - 400
        self.rect.centerx = SCREEN_RECT.centerx

        self.speed = HERO_SPEED

        self.bullet_group = pygame.sprite.Group()
        self.fire_signal = 0

        self.image_list = ["./images/me1.png", "./images/me2.png"]
        self.image_signal = 1

        ik_1 = "./images/me_destroy_1.png"
        ik_2 = "./images/me_destroy_2.png"
        ik_3 = "./images/me_destroy_3.png"
        ik_4 = "./images/me_destroy_4.png"
        self.ik_list = [ik_1, ik_2, ik_3, ik_4]
        self.ik_signal = 0

        self.point = Point()

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

        self.speed = HERO_SPEED

        self.bullet_group = pygame.sprite.Group()
        self.fire_signal = 0
        self.point.blood = 5
        self.ik_signal = 0

        self.point.point = 0

    def fire(self):
        self.fire_signal -= 1
        if self.fire_signal in (20, 30, 40, 50, 60):
            bullet = Bullet()
            bullet.rect.x = self.rect.centerx
            bullet.rect.y = self.rect.y
            self.bullet_group.add(bullet)

    def animation(self):
        self.image = pygame.image.load(self.image_list[self.image_signal])
        if self.image_signal == 1:
            self.image_signal = 0
        elif self.image_signal == 0:
            self.image_signal = 1

    def die(self):
        self.speed = 0
        if self.ik_signal < 4:
            self.image = pygame.image.load(self.ik_list[self.ik_signal])
            self.ik_signal += 1
        elif self.ik_signal == 4:
            self.ik_signal += 1


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
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.rect.y = SCREEN_RECT.centery + self.rect.height / 2

    def update(self):
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.rect.y = SCREEN_RECT.centery + self.rect.height / 2


class Quit(GameSprite):
    def __init__(self):
        super().__init__("./images/gameover.png", 0)
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.rect.y = SCREEN_RECT.centery - self.rect.height / 2

    def update(self):
        self.rect.x = SCREEN_RECT.centerx - self.rect.width / 2
        self.rect.y = SCREEN_RECT.centery - self.rect.height / 2


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


class Point:
    def __init__(self):
        self.write_point = pygame.font.Font(None, 50)
        self.write_blood = pygame.font.Font(None, 50)
        self.color = 255, 255, 255
        self.image_point = None
        self.image_blood = None
        self.point = 0
        self.blood = 5
        self.point_rect = (0, 0)
        self.blood_rect = (0, 50)

    def generate(self):
        self.image_point = self.write_point.render(f"Your point is {self.point}", True, self.color)
        self.image_blood = self.write_blood.render(f"Your hero's blood is {self.blood}", True, self.color)


class Blood(GameSprite):
    def __init__(self):
        super().__init__("./images/blood.png", 0)
        self.speed = random.randint(1, 5)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width
        self.rect.x = random.randint(0, max_x - 57)

    def update(self):
        super().update()
        if self.rect.y > SCREEN_RECT.height:
            self.kill()


class Resume(GameSprite):
    def __init__(self):
        super().__init__("./images/resume_pressed.png", 0)
        self.rect.center = SCREEN_RECT.center
        self.signal = 0





