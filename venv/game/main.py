import pygame
from plane_sprites import *

pygame.init()
# print("zheshiyouxidaima")


screen = pygame.display.set_mode((400, 700))
bg = pygame.image.load("./images/bg.png")
screen.blit(bg, (0, 0))

hero = pygame.image.load("./images/heroplane.png")
screen.blit(hero, (150, 400))

pygame.display.update()

clock = pygame.time.Clock()

hero_rect = pygame.Rect(150, 400, 128, 128)

enemy1 = GameSprite("./images/enemy1.png")
enemy2 = GameSprite("./images/enemy2.png", 2)
enemy_group = pygame.sprite.Group(enemy1, enemy2)

# time.sleep(1000)
# 游戏循环-》意味着游戏的正式开始
while True:
    clock.tick(60)
    event_list = pygame.event.get()

    # if len(event_list)> 0:
    # print(event_list)

    for event in event_list:
        if event.type == pygame.QUIT:
            print("游戏退出...")
            # quit卸载pygame的所有模块
            pygame.quit()
            # 直接终止当前正在执行的程序
            exit()

    hero_rect.y -= 1

    if hero_rect.y <= -128:
        hero_rect.y = 700
    screen.blit(bg, (0, 0))
    screen.blit(hero, hero_rect)

    #
    enemy_group.update()
    enemy_group.draw(screen)

    pygame.display.update()

pygame.quit()
