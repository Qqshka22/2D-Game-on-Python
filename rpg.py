import pygame
import random
from pygame.constants import MOUSEBUTTONDOWN

#Настройки окна
WIDTH = 800
HEIGHT = 500
FPS = 90

#Настройка цвета
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

#Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#Время
lastTime = 0
currentTime = 0

# Персонаж
x = WIDTH // 2
y = HEIGHT // 2
hero = pygame.Rect(x, y, 60, 50)
heroImg = pygame.image.load('razorinv.png')

# Противники
enemies = []
enemycd = 5
enemyImage = pygame.image.load('invaderinv.png').convert()
enemyRect = enemyImage.get_rect()
we = enemyRect.width
he = enemyRect.height
points = 0

# Звезд
stars = []
starcd = 10
starImg = pygame.image.load('starinv.png')
starRect = starImg.get_rect()
ws = enemyRect.width 
hs = enemyRect.height

# Пули
wb = 2
hb = 5
bulletImg = pygame.image.load("bullet.png")
bullets = []
isShot = False

# Шрифты
pointsT = pygame.font.SysFont('comic sans ms', 50)
gameover = pygame.font.SysFont('comic sans ms', 50)

# Текст
gameover_text = gameover.render('GAME OVER', 1, WHITE)

# restart
restart_img = pygame.image.load('reset.png.png')
restart_img = pygame.transform.scale(restart_img, (100, 80))
restart = pygame.Rect((WIDTH // 2) - 50, (HEIGHT // 2) - 10, 120, 100)
click = pygame.Rect(0,0,3,3)


ecran = 'game'
#Переменные движения
moving = ''
GO = ''
running = True
while running:

    if ecran == 'game':
        screen.fill(BLACK)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_a:
                    moving = 'LEFT'
                if i.key == pygame.K_d:
                    moving = 'RIGHT'
                if i.key == pygame.K_w:
                    moving = 'UP'
                if i.key == pygame.K_s:
                    moving = 'DOWN'

            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    isShot = True
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_a or i.key == pygame.K_d or i.key == pygame.K_w or i.key == pygame.K_s:
                    moving = 'STOP'
        
        # Передвижение персонажа
        if moving == 'LEFT' and hero.left > 0:
            hero.left -= 10
        if moving == 'RIGHT' and hero.right < WIDTH:
            hero.left += 10
        if moving == 'UP' and hero.top > 0:
            hero.top -= 10
        if moving == 'DOWN' and hero.bottom < HEIGHT:
            hero.top += 10

        # Отрисовка счета
        points_text = pointsT.render('Очки: ' + str(points), 1, WHITE)
        screen.blit(points_text, (10,10))
            
    # ПУЛИ
        # Создание пуль
        if isShot:
            bulRect = pygame.Rect(hero.left + 33, hero.top + 5, wb, hb)
            bullets.append(bulRect)
            isShot = False
        
        # Отрисовка пуль
        for bullet in bullets:
            screen.blit(bulletImg, (bullet.left, bullet.top))
            bullet.top -= 5
            
        #Удаление пуль
        index_bul = 0
        for b in bullets:
            if b.bottom < -5:
                bullets.pop(index_bul)
            index_bul += 1
            
    # ЗАХВАТЧИКИ
        currentTime = pygame.time.get_ticks()
        # Создание противников
        if currentTime - lastTime > enemycd:
            x_enemy = random.randint(we, WIDTH - we)
            enemies.append(pygame.Rect(x_enemy, -he, we, he))
            lastTime = currentTime
            enemycd = random.randint(100, 5000)
        
        # Отрисовка противников
        for enemy in enemies:
            screen.blit(enemyImage, (enemy.left, enemy.top))
            enemy.top += 2
        
        index_enemy = 0
        # Удаление противников
        for enemy in enemies:
            if enemy.top > HEIGHT:
                del enemies[index_enemy]
    # столкновение
        for enemy in enemies:
            if hero.colliderect(enemy):
                ecran = 'game_over'

        for bullet in bullets:
            for enemy in  enemies:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    points += 1

    # ЗВЕЗДЫ
        starcd -= 1
        if starcd < 0:
            x_star = random.randint(0,WIDTH-ws)
            star = pygame.Rect(x_star, -hs , ws, hs)
            stars.append(star)
            starcd = random.randint(20, 40)
        
        for star in stars:
            screen.blit(starImg, (star.left, star.top))
            star.top += 4
            if star.top > HEIGHT:
                stars.remove(star)  

        #Отрисовка персонажа
        screen.blit(heroImg, (hero.left, hero.top))
    
    if ecran == 'game_over':

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            if i.type == MOUSEBUTTONDOWN:
                if i.button == 1:
                    click.left = i.pos[0]
                    click.top = i.pos[1]
                    if click.colliderect(restart):
                        ecran = 'game'
        screen.fill(BLACK)
        screen.blit(gameover_text, (50, 200))
        screen.blit(restart_img, (restart.left, restart.top))

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()