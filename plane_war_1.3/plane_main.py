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
        pygame.time.set_timer(ENEMY_FIRE, 1500)
        pygame.time.set_timer(FRAME, 5)
        pygame.time.set_timer(BLOOD, 10000)
        self.fire = 4

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
        self.game_over = Quit()
        self.new_game_group = pygame.sprite.Group(self.new_game, self.game_over)

        self.mouse = Mouse()
        self.mouse_group = pygame.sprite.Group(self.mouse)

        self.blood_group = pygame.sprite.Group()

        self.resume = Resume()
        self.resume_group = pygame.sprite.Group(self.resume)

    def play(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.resume.signal += 1

            if self.resume.signal >= 2:
                self.resume.signal = 0

            if self.resume.signal == 0:
                self.clock.tick(FRAME_PER_SEC)
                self.__event_handler()
                self.__circle()
                self.__check_collide()
                self.__animation()
                self.__update_sprites()
                pygame.display.update()
            elif self.resume.signal == 1:
                self.clock.tick(FRAME_PER_SEC)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        PlayGame.__game_over(self)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_t]:
                    self.__game_over()
                self.resume_group.update()
                self.resume_group.draw(self.screen)
                pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlayGame.__game_over(self)
            elif event.type == CREAT_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
                self.enemy_fire_group.add(enemy)
            elif event.type == BLOOD:
                blood = Blood()
                self.blood_group.add(blood)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero.rect.y -= self.hero.speed
        if keys[pygame.K_s]:
            self.hero.rect.y += self.hero.speed
        if keys[pygame.K_a]:
            self.hero.rect.x -= self.hero.speed
        if keys[pygame.K_d]:
            self.hero.rect.x += self.hero.speed

        if keys[pygame.K_SPACE]:
            if self.hero.fire_signal <= 0:
                self.hero.fire_signal = 70

        if keys[pygame.K_r] and self.hero.point.blood < 0 and self.hero.ik_signal == 5:
            self.new_game.rect.center = (10000, 10000)
            self.hero.resurrection()
        if keys[pygame.K_t] and self.hero.point.blood < 0:
            PlayGame.__game_over(self)

    def __check_collide(self):
        for enemy in self.enemy_group:
            pygame.sprite.groupcollide(self.hero.bullet_group, enemy.bullete_group, True, True)
            enemy_bullet = pygame.sprite.spritecollide(enemy, self.hero.bullet_group, True)
            enemy_bullete = pygame.sprite.spritecollide(self.hero, enemy.bullete_group, True)
            if len(enemy_bullet) > 0:
                enemy.blood -= 1
            if len(enemy_bullete) > 0:
                self.hero.point.blood -= 0.5

        enemy_hero = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemy_hero) > 0:
            self.hero.point.blood -= 1
            self.hero.point.point += enemy.blood

        mouse_left = pygame.mouse.get_pressed()[0]
        if pygame.sprite.collide_mask(self.mouse, self.new_game) and mouse_left and self.hero.ik_signal:
            self.new_game.rect.center = (10000, 10000)
            self.hero.resurrection()
        if pygame.sprite.collide_mask(self.mouse, self.game_over) and mouse_left:
            self.__game_over()
        hero_blood = pygame.sprite.spritecollide(self.hero, self.blood_group, True)
        if len(hero_blood) > 0:
            self.hero.point.blood += 1

    def __circle(self):
        self.hero.fire()

        for enemy in self.enemy_group:
            if enemy.fire_signal == 1 and enemy.blood > 0:
                enemy.fire()

    def __animation(self):
        for event in pygame.event.get():
            if event.type == FRAME and self.hero.point.blood >= 0:
                self.hero.animation()
            if event.type == FRAME and self.hero.point.blood < 0:
                self.hero.die()
            for enemy in self.enemy_group:
                if event.type == FRAME and enemy.blood <= 0:
                    enemy.die()
                if enemy.blood <= 0 and enemy.ik_signal == 5:
                    enemy.remove(self.enemy_group)
                    self.hero.point.point += enemy.scores

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

        if self.hero.point.blood < 0 and self.hero.ik_signal == 5:
            self.hero.rect.center = (10000, 10000)
            self.new_game_group.update()
            self.new_game_group.draw(self.screen)

        self.hero.point.generate()
        self.screen.blit(self.hero.point.image_point, self.hero.point.point_rect)
        self.screen.blit(self.hero.point.image_blood, self.hero.point.blood_rect)

        self.blood_group.update()
        self.blood_group.draw(self.screen)

    def __game_over(self):
        print("游戏结束")
        print("你的得分是 %d" % self.hero.point.point)
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlayGame()

    game.play()
