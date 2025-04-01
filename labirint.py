from pygame import *

RED = (255, 0, 0)
GREEN = (0, 255, 51)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

win_width = 700
win_height = 500
display.set_caption('Игра лабиринт')
window = display.set_mode((win_width, win_height))
picture = transform.scale(image.load('white-wall-textures.jpg'), (win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, width, height, x, y, x_speed, y_speed):
        super().__init__(player_image, width, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platform_touched:
                 
                self.rect.right = min(self.rect.right, p.rect.left)
                self.x_speed = 0
        elif self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                self.x_speed = 0

        self.rect.y += self.y_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platform_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                self.y_speed = 0
        elif self.y_speed < 0:
            for p in platform_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
                self.y_speed = 0


    def fire(self):
        bullet = Bullet('weapon.png', 20, 10, self.rect.right, self.rect.centery, 15)  
        bullets.add(bullet)





class Enemy(GameSprite):
    direction = "left"

    def __init__(self, enemy_image, width, height, x, y, x_speed, left_border, right_border):
        super().__init__(enemy_image, width, height, x, y)
        self.x_speed = x_speed
        self.left_border = left_border
        self.right_border = right_border

    def update(self):
        if self.rect.x <= self.left_border:
            self.direction = 'right'
        if self.rect.x >= self.right_border:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.x_speed
        else:
            self.rect.x += self.x_speed


class Bullet(GameSprite):
    def __init__(self,bullet_image,width, height, x, y, x_speed):
        super().__init__(bullet_image, width, height, x, y)
        self.x_speed = x_speed

    def update(self):
        self.rect.x += self.x_speed
        if self.rect.x > win_width + 10:
            self.kill()


        if sprite.spritecollideany(self, barriers):
            self.kill()  







bullets = sprite.Group()

wall_1 = GameSprite('platform_h.png', 180, 80, 200, 250)
wall_2 = GameSprite('platform_v.png', 50, 120, 400, 100)
wall_3 = GameSprite('platform_v.png', 50, 150, 550, 300)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)

player = Player('hero.png', 50, 50, 50, 50, 0, 0)

packman = Player('enemy2.png', 80, 60, 320, 100, 2, 0)  
final_sprite = GameSprite('enemy.png', 80, 60, 520, 220)
monster = Enemy('enemy.png', 80, 60, 520, 220, 2, 450, 600)  


monsters = sprite.Group()
monsters.add(monster) 
monsters.add(packman) 

win = transform.scale(image.load('game-over_1.png'), (win_width, win_height))

finish = False
run = True
while run:
    time.delay(60)

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed = -10
            elif e.key == K_RIGHT:
                player.x_speed = 10
            elif e.key == K_UP:
                player.y_speed = -10
            elif e.key == K_DOWN:
                player.y_speed = 10
            elif e.key == K_SPACE:
                player.fire()



        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0



    if finish != True:
        window.blit(picture, (0, 0))
        wall_1.reset()
        wall_2.reset()
        wall_3.reset()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.update
        player.update()


        sprite.groupcollide(monsters, bullets, True, True)

        if sprite.collide_rect(player,final_sprite):
            finish = True
            window.blit(win,(0,0))

    display.update()