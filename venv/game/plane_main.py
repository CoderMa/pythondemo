import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("game init...")
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        # 设置定时器时间--创建敌机 1S
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 设置定时器时间--发射子弹 0.5S
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄精灵和英雄精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group( self.hero)


    def start_game(self):
        print("game start...")
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()


    def __event_handler(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("ENEMY COMING...")
                # 创建敌机精灵
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            #elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                #print("MOVE RIGHT...")

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            print("move right...")
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            print("move left...")
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 碰撞检测, 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            # 英雄牺牲
            self.hero.kill()
            # 游戏结束
            PlaneGame.__game_over()


    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("game over...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    plane_game = PlaneGame()
    plane_game.start_game()
