import pygame
import sys
import os
from constants import *
from random import randint, choice
import time
import sqlite3
import os


class Alien(pygame.sprite.Sprite):# класс главного персонажа
    def __init__(self):
        super().__init__()
        self.frames = dict()
        #загрузка списков с кадрами анимации главного героя
        self.anim_set_up = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_up{i}.png')),
                                                   (70, 70)) for i in range(3)]
        self.anim_set_up_l = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_up_l{i}.png')),
                                                     (70, 70)) for i in range(3)]
        self.anim_set_up_r = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_up_r{i}.png')),
                                                     (70, 70)) for i in range(3)]
        self.anim_set_down=[pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_down{i}.png')),
                                                     (70, 70)) for i in range(3)]
        self.anim_set_down_l=[pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_down_l{i}.png')),
                                                     (70, 70)) for i in range(3)]
        self.anim_set_down_r=[pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_down_r{i}.png')),
                                                     (70, 70)) for i in range(3)]
        for el in ['front1', 'l1', 'r1',]:
            self.frames[el] = pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_{el}.png')), (70, 70))
        self.cur_frame = 'front1'
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        self.status = 1
        self.k=0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.mouse.get_focused():
            self.x, self.y = pygame.mouse.get_pos()
            # условия для выбора текущей анимации
            if self.rect.x > self.x and self.y > self.rect.y:
                self.cur_frame = self.anim_set_down_l
            elif self.rect.y < self.y and self.x == self.rect.x:
                self.cur_frame = self.anim_set_down
            elif self.rect.y > self.y and self.x == self.rect.x:
                self.cur_frame = self.anim_set_up
            elif self.rect.x > self.x and self.y == self.rect.y:
                self.cur_frame = 'l1'
            elif self.rect.x < self.x and self.y == self.rect.y:
                self.cur_frame = 'r1'
            elif self.rect.x < self.x and self.y > self.rect.y:
                self.cur_frame = self.anim_set_down_r
            elif self.rect.x > self.x and self.y < self.rect.y:
                self.cur_frame = self.anim_set_up_l
            elif self.rect.x < self.x and self.y < self.rect.y:
                self.cur_frame = self.anim_set_up_r
            self.rect.x = self.x
            self.rect.y = self.y
            if isinstance(self.cur_frame,list):
                self.image = self.cur_frame[self.k//24]
            else:
                self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)


class Button(pygame.sprite.Sprite):# универсальный класс  для создания кнопок
    def __init__(self, text, func=print):
        super().__init__()
        font = pygame.font.Font('font/20960.ttf', 30)
        self.text = font.render(text, True, (0, 0, 0))
        self.image = pygame.Surface([220, 60])
        self.rect = self.image.get_rect()
        self.text_rect = self.rect.copy()
        self.rect.x = 150
        self.rect.y = 300
        self.text_rect.x = self.rect.x + 20
        self.text_rect.y = self.rect.y + 5
        self.image.fill((100,200,200))
        self.func = func

    def update(self):
        global start_page
        if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__['button'] == 1 and start_page:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.func()


def start_btn_func():# функция для кнопки старта, передается в конструктор Button()
    global start_page
    start_page = False
    pygame.mouse.set_visible(False)


class Bullets(pygame.sprite.Sprite):#класс пуль
    def __init__(self):
        super().__init__(bullets)
        self.size = randint(9, 12)
        self.image = pygame.Surface([self.size, self.size])
        self.rect = self.image.get_rect()
        self.speed_x = randint(2, 4)
        self.speed_y = randint(2, 4)
        self.rect.x = choice([-10, randint(1, SCREEN_WIDTH - self.size), SCREEN_WIDTH + 10])
        if self.rect.x == -10 or self.rect.x == SCREEN_WIDTH + 10:
            self.rect.y = choice([-10, SCREEN_HEIGHT + 10, randint(1, SCREEN_HEIGHT - self.size)])
        else:
            self.rect.y = choice([-10, SCREEN_HEIGHT + 10])
        if self.rect.x == SCREEN_WIDTH + 10:
            self.speed_x = -self.speed_x
        if self.rect.y == SCREEN_HEIGHT + 10:
            self.speed_y = -self.speed_y
        self.image.fill('blue')

    def update(self):
        if alien and pygame.sprite.collide_mask(self, alien):#проверка на столкновение с персонажем
            alien.status = 0
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # удаление объекта из группы, если он за пределами экрана
        if self.rect.x > SCREEN_WIDTH + 10 or self.rect.x < -10 or self.rect.y > SCREEN_HEIGHT + 10 or self.rect.y < -10:
            self.kill()


class GameOver():
    def __init__(self):
        sc.fill('white')
        font = pygame.font.Font('font/20960.ttf', 30)
        self.text = font.render('Конец игры!', True, (0, 0, 0))
        sc.blit(self.text, (170, 150))


class Timer():# класс таймера для контроля времени в игре
    def __init__(self):
        self.start_time = time.time()
        font = pygame.font.Font('font/20960.ttf', 30)

    def update(self):
        elapsed_time = time.time() - self.start_time
        str_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        font = pygame.font.Font('font/20960.ttf', 30)
        self.text = font.render(str_time, True, (0, 0, 0))
        sc.blit(self.text, (400, 0))


def load_image(name, colorkey=None):# функция загрузки изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    pygame.init()
    bullets = pygame.sprite.Group()
    pygame.init()
    clock = pygame.time.Clock()
    sc = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    alien = Alien()
    start_page = True  # флаг для проверки стартового окна
    start_btn = Button('Начать игру', start_btn_func)
    running = True
    second = 800#задержка времени перед созданием новых пуль
    timer = False
    bg = load_image(os.path.abspath(f'data\\background2.png'))
    last = pygame.time.get_ticks()
    while running:
        sc.blit(bg, (0, 0))
        if start_page:  # работа со стартовым окном
            sc.blit(start_btn.image, start_btn.rect)#отображение кнопки и текста на ней
            sc.blit(start_btn.text, start_btn.text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            start_btn.update()
        else:  # сама игра
            if not (timer):#создание таймера, начало отчета после нажатия кнопки старта
                timer = Timer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEMOTION and alien:#обновление персонажа при движении мышки
                    alien.update()
            sc.blit(alien.image, pygame.mouse.get_pos())
            now = pygame.time.get_ticks()
            if now - last >= second:  # задержка времени перед созданием новых пуль
                for i in range(2):
                    Bullets()
                last = pygame.time.get_ticks()#обнуление таймера с момента отрисовки пуль
            bullets.update()
            bullets.draw(sc)
            timer.update()
        if not (alien.status):# проверка на конец игры
            sc.fill('white')
            pygame.mouse.set_visible(True)
            GameOver()
        clock.tick(60)
        pygame.display.flip()
        alien.k+=1#переменная для контроля времени смены кадров анимации
        if alien.k==49:
            alien.k=0
    pygame.quit()
    sys.exit()
