import pygame

from plane_sprites import *

pygame.init()


class PlayGame(object):
    def __init__(self):
        print("游戏初始化")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREAT_ENEMY_EVENT, 500)

    def __create_sprites(self):
        bg_00 = Background(0, 0)
        bg_10 = Background(1, 0)
        bg_20 = Background(2, 0)
        bg_30 = Background(3, 0)
        bg_01 = Background(0, 1)
        bg_11 = Background(1, 1)
        bg_21 = Background(2, 1)
        bg_31 = Background(3, 1)
        bg_02 = Background(0, 2)
        bg_12 = Background(1, 2)
        bg_22 = Background(2, 2)
        bg_23 = Background(3, 2)
        self.bg_group = pygame.sprite.Group(
            bg_00, bg_10, bg_20, bg_30,
            bg_01, bg_11, bg_21, bg_31,
            bg_02, bg_12, bg_22, bg_23)

        self.enemy_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)


    def play(self):

        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlayGame.__game_over()
            elif event.type == CREAT_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.hero.fire()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero.rect.y -= HERO_SPEED
        if keys[pygame.K_s]:
            self.hero.rect.y += HERO_SPEED
        if keys[pygame.K_a]:
            self.hero.rect.x -= HERO_SPEED
        if keys[pygame.K_d]:
            self.hero.rect.x += HERO_SPEED

    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            PlayGame.__gamwwwwe_over()

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlayGame()

    game.play()
