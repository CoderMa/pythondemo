import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 400, 700)
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 调用父类方法实现精灵的创建（image/rect/speed）
        super().__init__("./images/bg.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        # 调用父类方法，创建敌机精灵，指定敌机图片
        super().__init__("./images/enemy1.png")
        # 随机敌机的随机初始速度
        self.speed = random.randint(1, 3)
        # 随机敌机的初始位置
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self, *args):
        # 调用父类方法保持垂直方向的飞行
        super().update()

        # 判断是否飞出屏幕如果是，需要从精灵组中删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            print("need to be deleted from enemy group...")
            # kill 方法可以将精灵从所有精灵组中移出， 精灵就会被自动销毁以调用__del__方法
            self.kill()

    def __del__(self):
        # print("di ji gua la %s" % self.rect)
        pass


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        # 调用父类方法设置image & speed
        super().__init__("./images/heroplane.png", 0)
        # 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄在水平方向移动
        self.rect.x += self.speed

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("fashe zidan")
        # 创建子弹精灵
        for i in range(0, 3):
            # print(i)
            bullet = Bullet()
            # 设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 60
            bullet.rect.centerx = self.rect.centerx
            # 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet2.png", -2)

    def update(self, *args):
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()


    def __del__(self):
        print("bullet is deleted")
