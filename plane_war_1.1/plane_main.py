import pygame.sprite

from plane_sprites import *

pygame.init()


class PlayGame(object):
    def __init__(self):
        print("游戏初始化")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREAT_ENEMY_EVENT, 500)
        pygame.time.set_timer(ENEMY_FIRE, 1500)
        self.fire = 4
        self.points = 0

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
        self.enemy_fire_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        self.new_game = NewGame()
        self.new_game_group = pygame.sprite.Group(self.new_game)

        self.mouse = Mouse()
        self.mouse_group = pygame.sprite.Group(self.mouse)

    def play(self):

        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__circle()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlayGame.__game_over(self)
            elif event.type == CREAT_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
                self.enemy_fire_group.add(enemy)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.hero.fire_signal <= 0:
                    self.hero.fire_signal = 70

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero.rect.y -= HERO_SPEED
        if keys[pygame.K_s]:
            self.hero.rect.y += HERO_SPEED
        if keys[pygame.K_a]:
            self.hero.rect.x -= HERO_SPEED
        if keys[pygame.K_d]:
            self.hero.rect.x += HERO_SPEED

        if keys[pygame.K_r] and self.hero.blood < 0:
            self.new_game.rect.center = (10000, 10000)
            self.hero.resurrection()
        if keys[pygame.K_t] and self.hero.blood < 0:
            PlayGame.__game_over(self)

    def __check_collide(self):
        for enemy in self.enemy_group:
            pygame.sprite.groupcollide(self.hero.bullet_group, enemy.bullete_group, True, True)
            enemy_bullet = pygame.sprite.spritecollide(enemy, self.hero.bullet_group, True)
            enemy_bullete = pygame.sprite.spritecollide(self.hero, enemy.bullete_group, True)
            if len(enemy_bullet) > 0:
                enemy.blood -= 1
            if enemy.blood <= 0:
                enemy.remove(self.enemy_group)
                self.points += enemy.scores
            if len(enemy_bullete) > 0:
                self.hero.blood -= 0.5

        enemy_hero = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemy_hero) > 0:
            self.hero.blood -= 1

        mouse_left = pygame.mouse.get_pressed()[0]
        if pygame.sprite.collide_mask(self.mouse, self.new_game) and mouse_left:
            self.new_game.rect.center = (10000, 10000)
            self.hero.resurrection()

    def __circle(self):
        self.hero.fire()

        for enemy in self.enemy_group:
            if enemy.fire_signal == 1:
                enemy.fire()

    def __update_sprites(self):
        self.mouse_group.update()
        self.mouse_group.draw(self.screen)

        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

        for enemy in self.enemy_fire_group:
            enemy.bullete_group.update()
            enemy.bullete_group.draw(self.screen)

        if self.hero.blood < 0:
            self.hero.rect.center = (10000, 10000)
            self.new_game_group.update()
            self.new_game_group.draw(self.screen)

    def __game_over(self):
        print("游戏结束")
        print("你的得分是 %d" % self.points)
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlayGame()

    game.play()
