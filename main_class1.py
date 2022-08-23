import pygame
import sys
import time
import settings
import random
import math
pygame.init()
pygame.mixer.init()


# #动画
# tick=pygame.time.Clock()
# frameNumber = 6 #图片帧数
# fps = 10
# fcclock = pygame.time.Clock()
# n= 0


#屏幕
screen_image=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_rect=screen_image.get_rect()
background_image=pygame.image.load('resources/image/背景图1.png').convert()
background_rect=background_image.get_rect()
background_rect.center=screen_rect.center

background2_image = pygame.image.load('resources/image/背景图2.png').convert()
background2_rect = background2_image.get_rect()
background2_rect.center = screen_rect.center

background3_image = pygame.image.load('resources/image/背景图3.png').convert()
background3_rect = background3_image.get_rect()
background3_rect.center = screen_rect.center


pygame.display.set_caption('U are jb')

SCREEN_WIDTH = screen_rect.width
SCREEN_HEIGHT = screen_rect.height

start_op=1
start_image=pygame.image.load('resources/image/dz开始图.png')
start_rect=start_image.get_rect()
start_rect.center=screen_rect.center

game_over_op = True

#bullet
bullets=pygame.sprite.Group()
alien_bullets=pygame.sprite.Group()
alien_bullets_option=0 #怪物子弹开关
freqency=0
alien_freqency=0

bullet_choose_image=pygame.image.load('resources/image/dzyan green.png')
bullet_choose_rect=bullet_choose_image.get_rect()
bullet_choose_rect.x=0
bullet_choose_rect.bottom=screen_rect.bottom
choose=1

bullet_num_blue = 0
bullet_num_purple = 0
bullet_num_orange = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed




class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_img):
       pygame.sprite.Sprite.__init__(self)
       self.image = alien_img
       self.rect = self.image.get_rect()
       self.speed = 2
       self.down_index = 0
       self.bullet_option = False
    def move(self):
        self.rect.top += self.speed

class Alien1(pygame.sprite.Sprite):
    def __init__(self,alien_path,init_pos):
        pygame.sprite.Sprite.__init__(self)
        alien_img =pygame.image.load(alien_path)
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.down_index = 0
        self.bullet_option = False
    def move(self,player):
        x = player.rect.x - self.rect.x
        y = player.rect.y - self.rect.y
        mo = math.sqrt(x*x + y*y)
        x = x/ mo
        y = y/mo
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed
alien1_count =1

class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家对象精灵图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家精灵图片索引
        self.is_hit = False                             # 玩家是否被击中
        self.freqency =0
        self.attack_frame = 0
        self.attacking = False
        self.hitbox = pygame.sprite.Sprite
        self.hitbox.rect = pygame.Rect(0,0,self.rect.width + 100 ,self.rect.height + 100)



    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

    def attack(self):
        #sound.play(EVENT_ATTACKING)
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > 30:
            self.attack_frame = 0
            self.attacking = False
        #print('result: '+str(self.attack_frame//3 + 6) + ' ' + 'num: '+str(self.attack_frame))j
        screen_image.blit(self.image[self.attack_frame//10 + 6],self.rect)
        #修正了攻击距离的问题
            # Update the current attack frame
        self.attack_frame += 1

ship_current_speedx =0
ship_current_speedy= 0
ship_acc_x=0
ship_acc_y=0
moving_op =0 # 0--normal 1--acc

#道具
class Property(pygame.sprite.Sprite):
    def __init__(self, property_path,property_op):
       pygame.sprite.Sprite.__init__(self)
       property_img = pygame.image.load(property_path)
       self.image = property_img
       self.rect = self.image.get_rect()
       self.speed = 2
       self.down_index = 0
       self.property_op = property_op
    def move(self):
        self.rect.top += self.speed
pro_fre = 1
props = pygame.sprite.Group()
shield_op = False
shield_count = 1
shield_image = pygame.image.load('resources/image/shield.png')
shield_rect = shield_image.get_rect()


#特殊技能
special_ability_num = 1
special_ability_count = 0
special_ability_img = pygame.image.load('resources/image/大型书本的召唤魔法书召唤的影响(TomeOfSummonin_爱给网_aigei_com.png')
special_ability_rect = special_ability_img.get_rect()
special_ability_op = False



# boss
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midtop = init_pos
        self.speed = 3
        self.bullet_op = 1

    def move(self):
        self.rect.top += self.speed

    def move_follow(self,player):
        x = player.rect.x - self.rect.x
        y = player.rect.y - self.rect.y
        mo = math.sqrt(x*x + y*y)
        x = x/ mo
        y = y/mo
        self.rect.x += x * self.speed
        self.rect.y += y * self.speed

class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_image, boss_rect,boss_life):
       pygame.sprite.Sprite.__init__(self)
       self.image = []
       for i in range(len(boss_rect)):
           self.image.append(boss_image.subsurface(boss_rect[i]).convert_alpha())
       self.rect = boss_rect[0]
       self.speed = 0.5
       self.down_index = 0
       self.img_index = 0
       self.frequency =0
       self.isdefeated = False
       self.life = boss_life
       self.boss_bullets = pygame.sprite.Group()
       self.count =1
       self.recover_op = False
       self.recover_count = 0
       self.follow_op = False
       self.moving_count = 0
       self.bullet_op = False
    def move(self):
        if self.rect.top <= 50:
            self.rect.top += self.speed

    def drawlife(self,max_life):
        pygame.draw.rect(screen_image,(0,0,0),(screen_rect.centerx-max_life*2,0,max_life*4,20))
        pygame.draw.rect(screen_image,(255,0,0),(screen_rect.centerx-max_life*2,0,self.life *4 ,20))

    def openfire(self,bullet_path,bullet_pos,bullet_op):
        bullet_img = pygame.image.load(bullet_path)
        bullet = BossBullet(bullet_img,bullet_pos)
        bullet.bullet_op = bullet_op
        self.boss_bullets.add(bullet)

    def move_follow(self,player,speed):
        x = player.rect.x - self.rect.x
        y = player.rect.y - self.rect.y
        mo = math.sqrt(x*x + y*y)
        x = x/ mo
        y = y/mo
        self.rect.x += x * speed
        self.rect.y += y * speed
    def moveback(self,speed):
        x = (screen_rect.centerx - 0.5 *self.rect.width) -self.rect.x
        y = 0 - self.rect.y
        mo = math.sqrt(x * x + y * y)
        if self.rect.y> 0:
            x = x / mo
            y = y / mo
            self.rect.x += x * speed
            self.rect.y += y * speed

boss1_image = pygame.image.load('resources/image/boss1.png')
boss2_image = pygame.image.load('resources/image/boss2.png')
boss3_image = pygame.image.load('resources/image/boss3.png')

boss_rect = []
boss_rect.append(pygame.Rect(0,0,228,228))
boss_rect.append(pygame.Rect(228,0,228,228))
boss_rect.append(pygame.Rect(456,0,228,228))
boss_rect.append(pygame.Rect(684,0,228,228))
boss_rect.append(pygame.Rect(912,0,228,228))
boss_rect.append(pygame.Rect(1140,0,228,228))
boss_rect.append(pygame.Rect(1368,0,228,228))
boss_rect.append(pygame.Rect(1596,0,228,228))

boss2_rect =[]
boss2_rect.append(pygame.Rect(0,1117,293,300))
boss2_rect.append(pygame.Rect(310,1117,293,300))
boss2_rect.append(pygame.Rect(620,1117,293,300))
boss2_rect.append(pygame.Rect(945,1117,293,300))
boss2_rect.append(pygame.Rect(0,852,247,265))
boss2_rect.append(pygame.Rect(247,851,247,265))
boss2_rect.append(pygame.Rect(497,851,247,265))
boss2_rect.append(pygame.Rect(744,852,247,265))

boss3_rect = []
boss3_rect.append(pygame.Rect(0,1176,235,241))
boss3_rect.append(pygame.Rect(235,1176,235,241))
boss3_rect.append(pygame.Rect(470,1176,235,241))
boss3_rect.append(pygame.Rect(705,1176,235,241))
boss3_rect.append(pygame.Rect(235,935,235,241))
boss3_rect.append(pygame.Rect(470,935,235,241))
boss3_rect.append(pygame.Rect(705,935,235,241))
boss3_rect.append(pygame.Rect(0,935,235,241))


boss1 = Boss(boss1_image,boss_rect,100)
boss1.rect.midbottom = screen_rect.midtop
boss2 = Boss(boss2_image,boss2_rect,200)
boss2.rect.midbottom = screen_rect.midtop

boss3 = Boss(boss3_image,boss3_rect,300)
boss3.rect.midbottom = screen_rect.midtop

ability_op = 0
ability_count = 0
ability_img = pygame.image.load('resources/image/技能.png')
ability_rect = ability_img.get_rect()
ability_rect.center = boss1.rect.center

recover_img = pygame.image.load('resources/image/spr 盾(spr_shield)_爱给网_aigei_com.png')
recover_rect = recover_img.get_rect()
j= 0

filename = 'resources/image/shoot2.png'
plane_img = pygame.image.load(filename)

# 设置玩家相关参数
player_rect = []
player_rect.append(pygame.Rect(0, 123, 99, 123))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(99, 123, 99, 123))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))

player_rect.append(pygame.Rect(0, 0, 99, 123))
player_rect.append(pygame.Rect(116, 0, 99, 123))
player_rect.append(pygame.Rect(227, 0, 99, 123))
player_rect.append(pygame.Rect(347, 0, 99, 123))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
alien_rect = pygame.Rect(534, 612, 57, 43)
alien_img = plane_img.subsurface(alien_rect)
alien_down_imgs = []
alien_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
alien_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
alien_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
alien_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

aliens = pygame.sprite.Group()
aliens_bullets =pygame.sprite.Group()
alien_image = pygame.image.load('resources/image/alien.png')
aliens1 = pygame.sprite.Group()

#近战平a
#attack_option = False


# 音乐
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/鸡.wav')
death_sound=pygame.mixer.Sound('resources/sound/你干嘛.wav')
boss1_sound_1 = pygame.mixer.Sound('resources/sound/丽丽技能1~1.mp3')
pass_sound = pygame.mixer.Sound('resources/sound/谢谢！(素材分享群：658331608，获取更多素材).mp3')
boss1_sound_2 = pygame.mixer.Sound('resources/sound/理塘~1.mp3')
special_ability_sound = pygame.mixer.Sound('resources/sound/魔法释放－时空转移_爱给网_aigei_com.wav')
prop_sound = pygame.mixer.Sound('resources/sound/拾取宝石的钟声03 - 皮卡- Gem_ 钟声(Pickup_爱给网_aigei_com.mp3')
initial_sound = pygame.mixer.Sound('resources/sound/姐姐哥哥我是丁真 我想为你导航好吗.mp3')
special_ability_sound.set_volume(1)
prop_sound.set_volume(1)
initial_sound.set_volume(0.3)
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(1)
death_sound.set_volume(0.3)
boss1_sound_1.set_volume(3)
pass_sound.set_volume(1)
boss1_sound_2.set_volume(1.2)
pygame.mixer.music.load('resources/sound/晚美无瑕 - Zood [mqms2].mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)

pass_sound_op = True
change_sound = False
boss1_sound_2_op = True
#关卡

total_level =1
pass_image=pygame.image.load('resources/image/通关图.png')
pass_rect = pass_image.get_rect()
pass_rect.center= screen_rect.center
ispass = False
isboss = False
isgameend = False
gameend_img = pygame.image.load('resources/image/gameend img.png')
gameend_rect = gameend_img.get_rect()
gameend_rect.center = screen_rect.center

# 文字
txt_font=pygame.font.SysFont(None,48)

moving_left=False
moving_right=False
moving_up=False
moving_down=False
bullet_option=False

#结束
end_image=pygame.image.load('resources/image/end_img.jpg')
end_rect=end_image.get_rect()
end_rect.center=screen_rect.center

total_life=0

#按钮
botton_image=pygame.image.load('resources/image/丁真 结束图1.png')
botton_rect=botton_image.get_rect()
botton_rect.center=screen_rect.center
play_font=pygame.font.SysFont(None,48)
play_image=play_font.render('CONTINUE',True,settings.bg_color1,settings.bg_color3)
play_rect=play_image.get_rect()
play_rect.centerx=botton_rect.centerx
play_rect.y = screen_rect.centery + 100

#得分
score=0
alien_points=100
high_score= 0
level =1



clock = pygame.time.Clock()
while True:

    clock.tick(60)

    if not isboss and change_sound:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resources/sound/晚美无瑕 - Zood [mqms2].mp3')
        pygame.mixer.music.play(-1, 0.0)
        change_sound = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_a or event.key==pygame.K_LEFT:
                moving_left=True
            if event.key == pygame.K_d or event.key==pygame.K_RIGHT:
                moving_right=True
            if event.key == pygame.K_w or event.key==pygame.K_UP:
                moving_up=True
            if event.key == pygame.K_s or event.key==pygame.K_DOWN:
                moving_down=True
            if event.key == pygame.K_SPACE :
                bullet_option=True
            if event.key == pygame.K_j:
                player.attacking = True
            if event.key == pygame.K_k:
                if special_ability_num>0:
                    special_ability_num -= 1
                    special_ability_sound.play()
                    aliens.empty()
                    aliens1.empty()
                    alien_bullets.empty()
                    boss1.boss_bullets.empty()
                    boss2.boss_bullets.empty()
                    boss3.boss_bullets.empty()
                    special_ability_op =True

            if event.key == pygame.K_1:
                choose=1
            if event.key == pygame.K_2:
                choose = 2
            if event.key == pygame.K_3:
                choose = 3
            if event.key == pygame.K_4:
                choose = 4

        elif event.type== pygame.KEYUP:
            if event.key == pygame.K_a or event.key==pygame.K_LEFT:
                moving_left=False
            if event.key == pygame.K_d or event.key==pygame.K_RIGHT:
                moving_right=False
            if event.key == pygame.K_w or event.key==pygame.K_UP:
                moving_up=False
            if event.key == pygame.K_s or event.key==pygame.K_DOWN:
                moving_down=False
            if event.key == pygame.K_SPACE:
                bullet_option = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # 重开以及开始游戏
            mouse_pose=pygame.mouse.get_pos()
            if play_rect.collidepoint(mouse_pose):
                level =0
                if ispass ==True:
                    total_level += 1
                if total_life <= settings.max_life:
                    total_life=settings.max_life
                pygame.mouse.set_visible(False)
                isboss = False
                ispass = False
                pass_sound_op =True
                boss1_sound_2_op = True
                game_over_op = True
                boss1.life = 100
                boss2.life = 200
                boss3.life = 300
                boss1.rect.midbottom =screen_rect.midtop
                boss2.rect.midbottom =screen_rect.midtop
                boss3.rect.midbottom =screen_rect.midtop
                bullets.empty()
                alien_bullets.empty()
                aliens.empty()
                aliens1.empty()
                props.empty()
                player.rect.midbottom = screen_rect.midbottom
                start_op=0
                ship_current_speedy =0
                ship_current_speedx =0
                ship_acc_x=0
                ship_acc_y =0
                moving_op =0
                moving_down = False
                moving_up = False
                moving_right = False
                moving_left = False
                if total_level ==3:
                    change_sound = False
                if total_level != 4:
                    initial_sound.play()
    # print('(%d,%d)'%(ship_rect.x,ship_rect.y))

    # bullets
    freqency += 1
    if bullet_option == True and freqency % settings.bullet_fre == 0 and len(bullets) < settings.max_bullet_num:
        if choose == 1:  # 普通弹药

            bullet_sound.play()
            new_bullet_image = pygame.image.load('resources/image/yan green.png')
            new_bullet = Bullet(new_bullet_image,player.rect.center)
            bullets.add(new_bullet)
        if choose == 2 and bullet_num_blue > 0:  # 分裂弹
            bullet_num_blue-=1
            bullet_sound.play()
            new_bullet_image = pygame.image.load('resources/image/yan blue.png')
            new_bullet = Bullet(new_bullet_image,player.rect.center)
            bullets.add(new_bullet)
        if choose == 3 and bullet_num_orange >0:  # 三连发
            bullet_num_orange -=1
            for i in range(3):
                bullet_sound.play()
                new_bullet_image = pygame.image.load('resources/image/yan orange.png')
                new_bullet = Bullet(new_bullet_image, (player.rect.centerx+ 30 *(i-1) , player.rect.centery))
                bullets.add(new_bullet)
        if choose == 4 and bullet_num_purple>0:  # 穿透弹
            bullet_num_purple -=1
            bullet_sound.play()
            new_bullet_image = pygame.image.load('resources/image/yan purple.png')
            new_bullet = Bullet(new_bullet_image, player.rect.center)
            bullets.add(new_bullet)
    if freqency >= settings.bullet_fre:
        freqency = 0



    # print(str(freqency) + ' ' +str(len(bullets)) + ' ' + str(bullet_option) + ' ' + str(settings.bullet_fre))

    # 控制移动
    if moving_op == 1:
        if moving_up and not moving_down:  # 上下
            ship_acc_y = -settings.ship_acc
        elif moving_down and not moving_up:
            ship_acc_y = settings.ship_acc
        else:  # 无动力
            if abs(ship_current_speedy) < 1e-6:
                ship_acc_y = 0
            elif ship_current_speedy > 0:
                ship_acc_y = -settings.stop_acc
            elif ship_current_speedy < 0:
                ship_acc_y = settings.stop_acc

        if moving_left and not moving_right:  # 左右
            ship_acc_x = -settings.stop_acc
        elif moving_right and not moving_left:
            ship_acc_x = settings.stop_acc
        else:  # 无动力
            if abs(ship_current_speedx) < 1e-6:
                ship_acc_x = 0
            elif ship_current_speedx > 0:
                ship_acc_x = -settings.stop_acc
            elif ship_current_speedx < 0:
                ship_acc_x = settings.stop_acc

        ship_current_speedx += ship_acc_x
        ship_current_speedy += ship_acc_y

        if ship_current_speedx > settings.ship_speed:
            ship_current_speedx = settings.ship_speed
        if ship_current_speedx < -settings.ship_speed:
            ship_current_speedx = -settings.ship_speed
        if ship_current_speedy > settings.ship_speed:
            ship_current_speedy = settings.ship_speed
        if ship_current_speedy < -settings.ship_speed:
            ship_current_speedy = -settings.ship_speed

        if player.rect.bottom <= screen_rect.bottom and player.rect.y >= 0:
            player.rect.y += ship_current_speedy
        elif player.rect.bottom > screen_rect.bottom:
            player.rect.bottom = screen_rect.bottom
        elif player.rect.y < 0:
            player.rect.y = 0

        if player.rect.x >= 0 and player.rect.right <= screen_rect.right:
            player.rect.x += ship_current_speedx
        elif player.rect.x < 0:
            player.rect.x = 0
        elif player.rect.right > screen_rect.right:
            player.rect.right = screen_rect.right

        print('x:' + str(ship_current_speedx) + ' ' + 'y:' + str(ship_current_speedy))


    elif moving_op == 0: #正常
        if moving_up :
            player.moveUp()
        if moving_down :
            player.moveDown()
        if moving_right :
            player.moveRight()
        if moving_left :
            player.moveLeft()

    #子弹图标
    if choose == 1:
        bullet_choose_image = pygame.image.load('resources/image/dzyan green.png')
        moving_op = 0
    if choose == 2:
        bullet_choose_image = pygame.image.load('resources/image/dzyan blue.png')
        moving_op = 0
    if choose == 3:
        bullet_choose_image = pygame.image.load('resources/image/dzyan orange.png')
        moving_op = 1
    if choose == 4:
        bullet_choose_image = pygame.image.load('resources/image/dzyan purple.png')
        moving_op = 0

    # 统计信息
    txt = 'remain life: ' + str(total_life)
    txt_image = txt_font.render(txt, True, settings.bg_color3, settings.bg_color1)
    txt_rect = txt_image.get_rect()

    score_str = 'score: ' + str(score)
    score_font = pygame.font.SysFont(None, 48)
    score_image = score_font.render(score_str, True, settings.bg_color1, settings.bg_color3)
    score_rect = score_image.get_rect()
    score_rect.right = screen_rect.right - 20
    score_rect.top = screen_rect.top + 20

    high_score_str = 'highest: ' + str(high_score)
    high_score_font = pygame.font.SysFont(None, 48)
    high_score_image = high_score_font.render(high_score_str, True, settings.bg_color1, settings.bg_color3)
    high_score_rect = high_score_image.get_rect()
    high_score_rect.top = score_rect.top + 50
    high_score_rect.right = screen_rect.right - 20

    level_str = 'level: ' + str(level)
    level_font = pygame.font.SysFont(None, 48)
    level_image = level_font.render(level_str, True, settings.bg_color1, settings.bg_color3)
    level_rect = level_image.get_rect()
    level_rect.top = high_score_rect.top + 50
    level_rect.right = screen_rect.right - 20

    if choose == 1:
        bullet_cnum_str ='num: infinite'
    if choose == 2:
        bullet_cnum_str ='num: '+str(bullet_num_blue)
    if choose == 3:
        bullet_cnum_str = 'num: '+str(bullet_num_orange)
    if choose == 4:
        bullet_cnum_str = 'num: '+str(bullet_num_purple)
    bullet_cnum_font = pygame.font.SysFont(None,48)
    bullet_cnum_image = bullet_cnum_font.render(bullet_cnum_str,True,settings.bg_color1,settings.bg_color3)
    bullet_cnum_rect = bullet_cnum_image.get_rect()
    bullet_cnum_rect.x = 0
    bullet_cnum_rect.bottom = screen_rect.bottom



    #道具
    pro_fre += 1
    if pro_fre == 300 :
        i=random.randint(1,6)
        if i ==1:
            prop = Property('resources/image/prop1.png',i)
        if i == 2:
            prop = Property('resources/image/prop2.png',i)
        if i == 3:
            prop = Property('resources/image/prop3.png',i)
        if i == 4:
            prop = Property('resources/image/prop4.png',i)
        if i == 5:
            prop = Property('resources/image/prop5.png',i)
        if i == 6:
            prop = Property('resources/image/prop6.png',i)
        prop.rect.x = random.randint(0,screen_rect.right-prop.rect.width)
        prop.rect.bottom =screen_rect.top
        props.add(prop)
        pro_fre = 1

    #alien
    if len(aliens) <= 5 and not isboss:  # alien数目少于5 就刷新
        level += 1
        for i in range(settings.alien_number):
            if total_level ==1:
                alien_image = pygame.image.load('resources/image/alien.png')
            if total_level ==2:
                alien_image = pygame.image.load('resources/image/alien1.png')
            alien1 = Alien(alien_image)
            alien1.rect.bottom = 0
            alien1.rect.x = random.randint(0, 1500)
            aliens.add(alien1)

        # 节奏加快
        settings.alien_speed *= settings.speedup_scale
        if settings.alien_speed > 10:
            settings.alien_speed = 10
        # settings.ship_speed *= settings.speedup_scale
        if settings.ship_speed > 15:
            settings.ship_speed = 15
        settings.bullet_speed *= settings.speedup_scale
        if settings.alien_number < 20:
            settings.alien_number += 1

        if int(settings.bullet_fre / settings.speedup_scale) >= settings.least_bullet_fre:
            settings.bullet_fre = int(settings.bullet_fre / settings.speedup_scale)
        else:
            settings.bullet_fre = settings.least_bullet_fre
        # freqency=0
        settings.max_bullet_num *= settings.speedup_scale

    if total_level == 2 and not isboss: #第二关新加入alien
        if alien1_count <800:
            alien1_count += 1
        else:
            alien1_count = 1
        if alien1_count % 200 == 0 and len(aliens1) <= 4 and level >=5:
            for i in range(settings.alien1_number):
                alien1_left = pygame.sprite.Sprite
                alien1_right = pygame.sprite.Sprite
                alien1_left = Alien1('resources/image/alien1_l.png',(-alien1_left.rect.width,random.randint(screen_rect.top,screen_rect.bottom)))
                alien1_right = Alien1('resources/image/alien1_r.png',(screen_rect.right,random.randint(screen_rect.top,screen_rect.bottom)))
                aliens1.add(alien1_right)
                aliens1.add(alien1_left)

    # 关卡
    if total_level == 1:
        alien_bullets_option = 0
        if level >= 15:
            isboss = True
    if total_level == 2:
        alien_bullets_option = 1
        if level >= 15:
            isboss = True
    if total_level == 3:
        isboss = True
        settings.bullet_fre = 5
        settings.max_bullet_num = 50
        settings.bullet_speed = 4
    if total_level == 4:
        isgameend = True

    #绘制
    if total_life>0  and not ispass and not isgameend:
        # screen_image.fill(settings.bg_color1)
        screen_image.fill(0)
        if total_level ==1:
            screen_image.blit(background_image,background_rect)
        if total_level ==2:
            screen_image.blit(background2_image, background2_rect)
        if total_level == 3:
            screen_image.blit(background3_image,background3_rect)
        screen_image.blit(txt_image, txt_rect)
        screen_image.blit(bullet_choose_image, bullet_choose_rect)


        if isboss:
            if total_level == 1:  #boss1
                if boss1_sound_2_op == True:
                    boss1_sound_2.play()
                    boss1_sound_2_op = False
                if boss1.frequency < 31:
                    boss1.frequency +=1
                else:
                    boss1.frequency = 0
                if boss1.life > 50:
                    screen_image.blit(boss1.image[boss1.img_index], boss1.rect)
                else:
                    screen_image.blit(boss1.image[boss1.img_index+4],boss1.rect)
                boss1.img_index = boss1.frequency // 8
                boss1.move()
                boss1.drawlife(100)
                for bullet in boss1.boss_bullets:
                    screen_image.blit(bullet.image, bullet.rect)
                    bullet.move()
                    if bullet.rect.bottom < 0:
                        boss1.boss_bullets.remove(bullet)

            if total_level == 2: #boss2
                # if boss2_sound_2_op == True:
                #     boss2_sound_2.play()
                #     boss2_sound_2_op = False
                if boss2.frequency < 31:
                    boss2.frequency +=1
                else:
                    boss2.frequency = 0
                if boss2.life >= 100:
                    screen_image.blit(boss2.image[boss2.img_index], boss2.rect)
                else:
                    screen_image.blit(boss2.image[boss2.img_index+4],boss2.rect)
                boss2.img_index = boss2.frequency // 8
                boss2.move()
                boss2.drawlife(200)
                for bullet in boss2.boss_bullets:
                    screen_image.blit(bullet.image, bullet.rect)
                    if bullet.bullet_op == 1:
                        bullet.move()
                    if bullet.bullet_op == 2:
                        bullet.move_follow(player)
                    if bullet.rect.bottom < 0:
                        boss2.boss_bullets.remove(bullet)
                if boss2.recover_op: #回血模式
                    boss2.recover_count += 1
                    recover_rect.center = boss2.rect.center
                    screen_image.blit(recover_img,recover_rect)
                    if boss2.recover_count >= 100:
                        boss2.recover_count = 0
                        boss2.recover_op =False

            if total_level == 3:
                # if boss2_sound_2_op == True:
                #     boss2_sound_2.play()
                #     boss2_sound_2_op = False
                if boss3.frequency < 31:
                    boss3.frequency += 1
                else:
                    boss3.frequency = 0
                if boss3.life >= 150:
                    screen_image.blit(boss3.image[boss3.img_index], boss3.rect)
                else:
                    screen_image.blit(boss3.image[boss3.img_index + 4], boss3.rect)
                boss3.img_index = boss3.frequency // 8
                boss3.move()
                boss3.drawlife(300)
                for bullet in boss3.boss_bullets:
                    screen_image.blit(bullet.image, bullet.rect)
                    if bullet.bullet_op == 1:
                        bullet.move()
                    if bullet.bullet_op == 2:
                        bullet.move_follow(player)
                    if bullet.rect.bottom < 0:
                        boss3.boss_bullets.remove(bullet)
                if boss3.recover_op:  # 回血模式
                    boss3.recover_count += 1
                    recover_rect.center = boss3.rect.center
                    screen_image.blit(recover_img, recover_rect)
                    if boss3.recover_count >= 100:
                        boss3.recover_count = 0
                        boss3.recover_op = False


        # 更换图片索引使飞机有动画效果
        screen_image.blit(player.image[player.img_index], player.rect)
        if player.freqency < 15:
            player.freqency += 1
        else:
            player.freqency = 0
        player.img_index = player.freqency // 8

        if player.attacking:  # 攻击
            player.attack()


        #道具
        for prop in props:
            prop.move()
            screen_image.blit(prop.image,prop.rect)
            if prop.rect.top >screen_rect.bottom:
                props.remove(prop)

        screen_image.blit(score_image,score_rect)
        screen_image.blit(high_score_image,high_score_rect)
        screen_image.blit(level_image,level_rect)
        screen_image.blit(bullet_cnum_image,bullet_cnum_rect)
        for bullet in bullets:
            screen_image.blit(bullet.image,bullet.rect)
            bullet.rect.y -= settings.bullet_speed
            if bullet.rect.bottom<0:
                bullets.remove(bullet)

        #special ability
        if special_ability_op == True:
            special_ability_count += 1
            special_ability_rect.center = player.rect.center
            screen_image.blit(special_ability_img,special_ability_rect)
            if special_ability_count == 50:
                special_ability_count =0
                special_ability_op = False


        #boss
        if isboss:
            if total_level == 1:              #第一关的boss
                if not change_sound:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('resources/sound/理塘路~1.mp3')
                    pygame.mixer.music.play(-1, 0.0)
                    change_sound =True
                boss1.count += 1
                if boss1.count ==2001:
                    boss1.count =1
                bullet_hitboss = pygame.sprite.spritecollide(boss1,bullets,True)
                if bullet_hitboss:
                    boss1.life -=1
                    score += 100
                player_hitboss = pygame.sprite.collide_rect(boss1,player)
                if player_hitboss:
                    if not shield_op:
                        total_life -= 1
                        death_sound.play()
                        bullets.empty()
                        aliens.empty()
                        alien_bullets.empty()
                        props.empty()
                        screen_image.blit(end_image, end_rect)
                        pygame.display.flip()
                        time.sleep(0.5)
                        player.rect.midbottom = screen_rect.midbottom
                if boss1.life <= 0:
                    score += 1000
                    if score >= high_score:
                        high_score = score
                    ispass = True

                # 发射子弹 技能
                if boss1.count % 100 == 0:
                        boss1.openfire('resources/image/丽丽子弹.jpeg',(random.randint(0,1500),-30),1)
                        boss1.openfire('resources/image/丽丽子弹.jpeg',(random.randint(0,1500),-30),1)
                        boss1.openfire('resources/image/丽丽子弹.jpeg',(random.randint(0,1500),-30),1)
                        boss1.openfire('resources/image/丽丽子弹.jpeg',(random.randint(0,1500),-30),1)
                        boss1.openfire('resources/image/丽丽子弹.jpeg',(random.randint(0,1500),-30),1)
                if boss1.count % 200 == 0:
                        for i in range(10):
                            boss1.openfire('resources/image/yan red.png',(boss1.rect.centerx-225 + i*50,boss1.rect.bottom),1)

                duang_boss =pygame.sprite.groupcollide(boss1.boss_bullets , bullets,True, True)
                if duang_boss:
                    enemy1_down_sound.play()
                    if choose == 2:  # 分裂弹
                        for item in duang_boss.keys():
                            bullet_sound.play()
                            new_bullet = pygame.sprite.Sprite()
                            new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                            new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                            new_bullet.rect.midbottom = (item.rect.centerx - 50, item.rect.top + 20)
                            bullets.add(new_bullet)
                            bullet_sound.play()
                            new_bullet = pygame.sprite.Sprite()
                            new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                            new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                            new_bullet.rect.midbottom = (item.rect.centerx + 50, item.rect.top + 20)
                            bullets.add(new_bullet)

                if pygame.sprite.spritecollideany(player, boss1.boss_bullets):  # 碰到飞船
                    if not shield_op:
                        total_life -= 1
                        death_sound.play()
                        bullets.empty()
                        aliens.empty()
                        alien_bullets.empty()
                        props.empty()
                        boss1.boss_bullets.empty()
                        screen_image.blit(end_image, end_rect)
                        pygame.display.flip()
                        time.sleep(0.5)
                        player.rect.midbottom = screen_rect.midbottom
                    else:
                        enemy1_down_sound.play()
                        boss1.boss_bullets.remove(pygame.sprite.spritecollideany(player, boss1.boss_bullets))
                if boss1.life <= 50:
                    if boss1.count % 400 == 0:
                        bullets.empty()
                        boss1_sound_1.play()
                        ability_op = 1
                    if ability_op ==1:
                        ability_count += 1
                        screen_image.blit(ability_img, ability_rect)
                        if ability_count == 10:
                            ability_op =0
                            ability_count=0


            if total_level ==2: #第二关boss
                if not change_sound:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('resources/sound/Lazer Boomerang - Time to Pretend.mp3')
                    pygame.mixer.music.play(-1, 20.0)
                    change_sound =True
                boss2.count += 1
                if boss2.count ==2001:
                    boss2.count =1
                if boss2.count ==2001:
                    boss2.count =1
                bullet_hitboss = pygame.sprite.spritecollide(boss2,bullets,True)
                if bullet_hitboss:
                    if boss2.recover_op:
                        if boss2.life+2 <=200:
                            boss2.life +=2
                        else:
                            boss2.life == 200
                    else:
                        boss2.life -=1
                    score += 100
                player_hitboss = pygame.sprite.collide_rect(boss2,player)
                if player_hitboss:
                    if not shield_op:
                        total_life -= 1
                        death_sound.play()
                        bullets.empty()
                        aliens.empty()
                        alien_bullets.empty()
                        props.empty()
                        boss2.boss_bullets.empty()
                        screen_image.blit(end_image, end_rect)
                        pygame.display.flip()
                        time.sleep(0.5)
                        player.rect.midbottom = screen_rect.midbottom
                if boss2.life <= 0:
                    score += 1000
                    if score >= high_score:
                        high_score = score
                    ispass = True

                # 技能
                if boss2.count % 200 == 0 :
                    for i in range(settings.alien1_number + 1):
                        alien1_left = pygame.sprite.Sprite
                        alien1_right = pygame.sprite.Sprite
                        alien1_left = Alien1('resources/image/alien1_l.png', (-alien1_left.rect.width, random.randint(screen_rect.top, screen_rect.bottom)))
                        alien1_right = Alien1('resources/image/alien1_r.png',(screen_rect.right, random.randint(screen_rect.top, screen_rect.bottom)))
                        aliens1.add(alien1_right)
                        aliens1.add(alien1_left)

                if boss2.count % 100 == 0:
                    for i in range(5):
                        boss2.openfire('resources/image/投球机.png',(random.randint(0,1500),-30),1)
                if boss2.count % 300 == 0:
                    for i in range(3):
                        boss2.openfire('resources/image/airpod.png', (random.randint(0, 1500), -30), 2)



                if boss2.life <= 100: #半血
                    boss2.rect.x += boss2.speed*10
                    if boss2.rect.right >= screen_rect.right or boss2.rect.left <= screen_rect.left :
                        boss2.speed = -boss2.speed

                    if boss2.count % 500 == 0:
                        boss2.recover_op = True

                    if boss2.count % 400 == 0:
                        #boss2_sound_1.play()
                        ability_op = 1
                    if ability_op ==1:
                        ability_count += 1
                        bullets.empty()
                        screen_image.blit(ability_img, ability_rect)
                        if ability_count == 10:
                            ability_op =0
                            ability_count=0

                #碰撞
                duang_boss = pygame.sprite.groupcollide(boss2.boss_bullets, bullets, True, True)
                if duang_boss:
                    enemy1_down_sound.play()
                    if choose == 2:  # 分裂弹
                        for item in duang_boss.keys():
                            bullet_sound.play()
                            new_bullet = pygame.sprite.Sprite()
                            new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                            new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                            new_bullet.rect.midbottom = (item.rect.centerx - 50, item.rect.top + 20)
                            bullets.add(new_bullet)
                            bullet_sound.play()
                            new_bullet = pygame.sprite.Sprite()
                            new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                            new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                            new_bullet.rect.midbottom = (item.rect.centerx + 50, item.rect.top + 20)
                            bullets.add(new_bullet)
                if pygame.sprite.spritecollideany(player, boss2.boss_bullets):  # 碰到飞船
                    if not shield_op:
                        total_life -= 1
                        death_sound.play()
                        bullets.empty()
                        aliens.empty()
                        alien_bullets.empty()
                        props.empty()
                        boss2.boss_bullets.empty()
                        screen_image.blit(end_image, end_rect)
                        pygame.display.flip()
                        time.sleep(0.5)
                        player.rect.midbottom = screen_rect.midbottom
                    else:
                        enemy1_down_sound.play()
                        boss2.boss_bullets.remove(pygame.sprite.spritecollideany(player, boss2.boss_bullets))

            if total_level == 3: #第三关
                if not change_sound:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("resources/sound/JUPITER - BALLIN'.mp3")
                    pygame.mixer.music.play(-1, 20.0)
                    change_sound =True
                boss3.count += 1
                if boss3.count ==2001:
                    boss3.count =1
                if boss3.count ==2001:
                    boss3.count =1
                bullet_hitboss = pygame.sprite.spritecollide(boss3,bullets,True)
                if bullet_hitboss:
                    if boss3.recover_op:
                        if boss3.life+2 <=300:
                            boss3.life +=2
                        else:
                            boss3.life == 300
                    else:
                        boss3.life -=1
                    score += 100
                player_hitboss = pygame.sprite.collide_rect(boss3,player)
                if player_hitboss:
                    if not shield_op:
                        total_life -= 1
                        death_sound.play()
                        bullets.empty()
                        aliens.empty()
                        alien_bullets.empty()
                        props.empty()
                        boss3.boss_bullets.empty()
                        screen_image.blit(end_image, end_rect)
                        pygame.display.flip()
                        time.sleep(0.5)
                        player.rect.midbottom = screen_rect.midbottom
                if boss3.life <= 0:
                    score += 1000
                    if score >= high_score:
                        high_score = score
                    ispass = True

                #技能
                if boss3.count % 200 == 0:
                    for i in range(10):
                        boss3.openfire('resources/image/传统香烟.png',(random.randint(0,1500),-30),2)

                if boss3.count % 500 == 0 and boss3.life <= 150:
                    boss3.bullet_op = True

                if boss3.bullet_op == True:
                    j += 1
                    if j % 10 == 0:
                        bullet_tmp_img = pygame.image.load('resources/image/传统香烟1.png')
                        bullet_tmp_rect = bullet_tmp_img.get_rect()
                        num = int(screen_rect.width / (bullet_tmp_rect.width + 10))
                        for i in range(num):
                            boss3.openfire('resources/image/传统香烟1.png',(10+(bullet_tmp_rect.width + 10)*i,-50),1)
                    if j == 50:
                        boss3.bullet_op =False
                        j = 0

                if boss3.count % 400 == 0:
                    boss3.follow_op = True

                if boss3.follow_op:
                        boss3.moving_count += 1
                        if boss3.moving_count < 50:
                            boss3.move_follow(player,8)
                        else:
                            boss3.moveback(20)
                        if boss3.moving_count == 200:
                            boss3.moving_count = 0
                            boss3.follow_op = False

                if boss3.life <= 150:
                    if boss3.count % 500 == 0:
                        boss3.recover_op = True

                    # if boss3.count % 400 == 0:
                    #     for i



                #碰撞
                duang_boss = pygame.sprite.groupcollide(boss3.boss_bullets, bullets, True, True)
                if duang_boss:
                    enemy1_down_sound.play()
                    if choose == 2:  # 分裂弹
                        for item in duang_boss.keys():
                            bullet_sound.play()
                            new_bullet = pygame.sprite.Sprite()
                            new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                            new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                            new_bullet.rect.midbottom = (item.rect.centerx - 50, item.rect.top + 20)
                            bullets.add(new_bullet)
                            bullet_sound.play()
                            new_bullet = pygame.sprite.Sprite()
                            new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                            new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                            new_bullet.rect.midbottom = (item.rect.centerx + 50, item.rect.top + 20)
                            bullets.add(new_bullet)
                if pygame.sprite.spritecollideany(player, boss3.boss_bullets):  # 碰到飞船
                    if not shield_op:
                        total_life -= 1
                        death_sound.play()
                        bullets.empty()
                        aliens.empty()
                        alien_bullets.empty()
                        props.empty()
                        boss3.boss_bullets.empty()
                        boss3.rect.midtop = screen_rect.midtop
                        boss3.follow_op = False
                        screen_image.blit(end_image, end_rect)
                        pygame.display.flip()
                        time.sleep(0.5)
                        player.rect.midbottom = screen_rect.midbottom
                    else:
                        enemy1_down_sound.play()
                        boss3.boss_bullets.remove(pygame.sprite.spritecollideany(player, boss3.boss_bullets))
        # 生命值
        love_group = pygame.sprite.Group()
        for i in range(total_life):
            love = pygame.sprite.Sprite()
            love.image = pygame.image.load('resources/image/比心.png')
            love.rect = love.image.get_rect()
            love.rect.y = 50
            love.rect.x = 10 + (love.rect.width + 10) * i
            screen_image.blit(love.image,love.rect)

        #ability图标
        for i in  range(special_ability_num):
            abi = pygame.sprite.Sprite()
            abi.image = pygame.image.load('resources/image/技能图标_140(skill_icon_140)_爱给网_aigei_com.png')
            abi.rect = abi.image.get_rect()
            abi.rect.bottom = screen_rect.bottom
            abi.rect.right = screen_rect.right - (10 +(abi.rect.width + 10 ) * i)
            screen_image.blit(abi.image,abi.rect)

        # aliens
        alien_freqency += 1
        for alien in aliens:
            alien.rect.y+= settings.alien_speed
            if alien.rect.y>= screen_rect.bottom: #到底就删掉
                aliens.remove(alien)
            # 为带子弹的怪
            if alien_bullets_option==1 and alien_freqency % settings.alien_bullet_fre ==0 and len(alien_bullets)< settings.max_alien_bullet_num:
                bullet_sound.play()
                new_alien_bullet = pygame.sprite.Sprite()
                new_alien_bullet.image = pygame.image.load('resources/image/yan red.png')
                new_alien_bullet.rect = pygame.Rect(0, 0, 10, 30)
                new_alien_bullet.rect.top = alien.rect.bottom -10
                new_alien_bullet.rect.centerx = alien.rect.centerx
                alien_bullets.add(new_alien_bullet)
            if alien_freqency >= settings.alien_bullet_fre:
                alien_freqency = 0
        aliens.draw(screen_image)

        if total_level == 2:
            for alien in aliens1: #alien1
                alien.move(player)
                if alien.rect.bottom <= screen_rect.top or alien.rect.top >= screen_rect.bottom:
                    aliens1.remove(alien)
            aliens1.draw(screen_image)

        # alien_bullets
        for alien_bullet in alien_bullets:
            alien_bullet.rect.y += settings.alien_speed +settings.bullet_speed
            if alien_bullet.rect.y >= screen_rect.bottom: #到底就删除
                alien_bullets.remove(alien_bullet)
        alien_bullets.draw(screen_image)


        # 子弹与外星人碰撞
        if choose==4:
            duang = pygame.sprite.groupcollide(bullets, aliens, False, True)
            duang_1 = pygame.sprite.groupcollide(bullets, aliens1, False, True)
        else:
            duang = pygame.sprite.groupcollide(bullets, aliens, True, True)
            duang_1 = pygame.sprite.groupcollide(bullets, aliens1, True, True)# 子弹与外星人碰撞 返回一个字典
        # print(duang)
        duang1=pygame.sprite.groupcollide(bullets,alien_bullets,True,True)

        if duang:
            enemy1_down_sound.play()
            if choose==2: #分裂弹
                for item in duang.keys():
                    bullet_sound.play()
                    new_bullet = pygame.sprite.Sprite()
                    new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                    new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                    new_bullet.rect.midbottom = (item.rect.centerx-50,item.rect.top+20)
                    bullets.add(new_bullet)
                    bullet_sound.play()
                    new_bullet = pygame.sprite.Sprite()
                    new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                    new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                    new_bullet.rect.midbottom = (item.rect.centerx + 50, item.rect.top + 20)
                    bullets.add(new_bullet)
            for item in duang.values():
                score += alien_points * len(item)  #更新分数
            if score > high_score:
                high_score= score       #更新最高分
        if duang_1:
            enemy1_down_sound.play()
            if choose == 2:  # 分裂弹
                for item in duang_1.keys():
                    bullet_sound.play()
                    new_bullet = pygame.sprite.Sprite()
                    new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                    new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                    new_bullet.rect.midbottom = (item.rect.centerx - 50, item.rect.top + 20)
                    bullets.add(new_bullet)
                    bullet_sound.play()
                    new_bullet = pygame.sprite.Sprite()
                    new_bullet.image = pygame.image.load('resources/image/yan blue.png')
                    new_bullet.rect = pygame.Rect(0, 0, 10, 30)
                    new_bullet.rect.midbottom = (item.rect.centerx + 50, item.rect.top + 20)
                    bullets.add(new_bullet)
            for item in duang_1.values():
                score += alien_points * len(item)  # 更新分数
            if score > high_score:
                high_score = score  # 更新最高分



        # 子弹 alien碰到飞船
        if pygame.sprite.spritecollideany(player,aliens) or pygame.sprite.spritecollideany(player,alien_bullets) or pygame.sprite.spritecollideany(player,aliens1) :
            if not shield_op:
                total_life-=1
                death_sound.play()
                bullets.empty()
                aliens.empty()
                aliens1.empty()
                props.empty()
                boss2.boss_bullets.empty()
                boss3.boss_bullets.empty()
                alien_bullets.empty()
                screen_image.blit(end_image, end_rect)
                pygame.display.flip()
                time.sleep(0.5)
                player.rect.midbottom=screen_rect.midbottom
            else:
                enemy1_down_sound.play()
                aliens.remove( pygame.sprite.spritecollideany(player,aliens))
                alien_bullets.remove(pygame.sprite.spritecollideany(player,alien_bullets))
                aliens1.remove(pygame.sprite.spritecollideany(player,aliens1))
        #道具
        duang_prop = pygame.sprite.spritecollideany(player,props)
        if duang_prop:
            prop_sound.play()
            if duang_prop.property_op == 1:
                bullet_num_orange += 30
            if duang_prop.property_op == 2:
                bullet_num_purple += 30
            if duang_prop.property_op == 3:
                bullet_num_blue += 30
            if duang_prop.property_op == 4 and total_life<5:
                total_life += 1
            if duang_prop.property_op == 5:
                shield_op = True
            if duang_prop.property_op == 6:
                special_ability_num += 1
            props.remove(duang_prop)
        #护盾
        if shield_op == True:
            shield_count += 1
            shield_rect.center = player.rect.center
            screen_image.blit(shield_image,shield_rect)
            if shield_count >= 500:
                shield_count = 1
                shield_op = False
        #平a
        player.hitbox.rect.center = player.rect.center
        if pygame.sprite.spritecollideany(player.hitbox,aliens) or pygame.sprite.spritecollideany(player.hitbox,alien_bullets) or pygame.sprite.spritecollideany(player.hitbox, boss1.boss_bullets) or pygame.sprite.spritecollideany(player.hitbox, boss2.boss_bullets) or pygame.sprite.spritecollideany(player.hitbox, boss3.boss_bullets) or pygame.sprite.spritecollideany(player.hitbox,aliens1):
            if player.attacking:
                aliens.remove(pygame.sprite.spritecollideany(player.hitbox, aliens))
                alien_bullets.remove(pygame.sprite.spritecollideany(player.hitbox, alien_bullets))
                boss1.boss_bullets.remove(pygame.sprite.spritecollideany(player.hitbox, boss1.boss_bullets))
                boss2.boss_bullets.remove(pygame.sprite.spritecollideany(player.hitbox, boss2.boss_bullets))
                boss3.boss_bullets.remove(pygame.sprite.spritecollideany(player.hitbox, boss3.boss_bullets))
                aliens1.remove(pygame.sprite.spritecollideany(player.hitbox,aliens1))
                #print(pygame.sprite.spritecollideany(player.hitbox, alien_bullets))
                score += 100
                if score > high_score:
                    high_score =score
                enemy1_down_sound.play()


    elif total_life <= 0 :

        if start_op==1: #显示开始图
            screen_image.blit(start_image,start_rect)

        if start_op==0: #非开始页面 而是游戏结束时
            screen_image.blit(botton_image,botton_rect)
            if game_over_op:
                game_over_sound.play()
                game_over_op = False

        screen_image.blit(play_image,play_rect)
        pygame.mouse.set_visible(True)
        settings.ship_speed, settings.bullet_speed, settings.alien_speed ,settings.alien_number,settings.bullet_fre, settings.max_bullet_num = settings.speed_list #重置游戏速度
        score = 0  #重置分数



    elif total_life >0 and ispass:  #进入下一关卡
        pygame.mouse.set_visible(True)
        if pass_sound_op:
            pass_sound.play()
            pass_sound_op = False
        settings.ship_speed, settings.bullet_speed, settings.alien_speed, settings.alien_number, settings.bullet_fre, settings.max_bullet_num = settings.speed_list  # 重置游戏速度
        score = 0  # 重置分数
        screen_image.blit(pass_image, pass_rect)
        screen_image.blit(play_image, play_rect)

    elif total_life>0 and isgameend: #游戏结束
        pygame.mixer.music.stop()
        screen_image.blit(gameend_img,gameend_rect)
        high_score_rect.center = screen_rect.center
        screen_image.blit(high_score_image, high_score_rect)


    pygame.display.flip()