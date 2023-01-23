import pygame
import sys
import os
from main_hero import Alien
from constants import *
from random import randint, choice
import time
from functions import game_over, load_image


class Fireball(pygame.sprite.Sprite):  # класс фаербола
    def __init__(self, direction):
        super().__init__()
        x = 30
        y = 80
        if direction == 'd' or direction == 'up':
            self.size = (x, y)#размеры изображения меняются в соответствии с направлением
        else:
            self.size = (y, x)
        self.k = 0
        self.anim_set = [pygame.transform.scale(load_image(os.path.abspath(f'data\\fireball_{direction}{i}.png')),
                                                self.size) for i in range(2)]
        self.image = self.anim_set[self.k]
        self.rect = self.image.get_rect()
        if direction == 'd' or direction == 'up':#фаербол летит по направлению в игрока
            self.rect.x = hero.x + 20
        else:
            self.rect.y = hero.y + 20

        self.direction = direction
        self.speed = randint(6, 7)
        if direction == 'up':
            self.rect.y = 715#начальные координаты появления
            self.speed = -self.speed
        elif direction == 'd':
            self.rect.y = -15

        elif direction == 'l':
            self.rect.x = 515
            self.speed = -self.speed
        if direction == 'r':
            self.rect.x = -15
        pygame.mixer.Sound("sounds/fireball.ogg").play()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global fireball
        self.image = self.anim_set[self.k // 5]
        if hero and pygame.sprite.collide_mask(self, hero):  # проверка на столкновение с персонажем
            hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        if self.direction == 'up' or self.direction == 'd':
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
        # удаление объекта из группы, если он за пределами экрана
        if self.rect.x > SCREEN_WIDTH + 20 or self.rect.x < -20 \
                or self.rect.y > SCREEN_HEIGHT + 20 or self.rect.y < -20:
            self.kill()
            fireball = False


class Bullets(pygame.sprite.Sprite):  # класс пуль
    def __init__(self, speed1, speed2):
        super().__init__(bullet_group)
        self.size = randint(15, 23)
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\bullet2.png')), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.speed_x = randint(speed1, speed2)
        self.speed_y = randint(speed1, speed2)
        self.rect.x = choice([-10, randint(1, SCREEN_WIDTH - self.size), SCREEN_WIDTH + 10])
        if self.rect.x == -10 or self.rect.x == SCREEN_WIDTH + 10:
            self.rect.y = choice([-10, SCREEN_HEIGHT + 10, randint(1, SCREEN_HEIGHT - self.size)])
        else:
            self.rect.y = choice([-10, SCREEN_HEIGHT + 10])
        if self.rect.x == SCREEN_WIDTH + 10:
            self.speed_x = -self.speed_x
        if self.rect.y == SCREEN_HEIGHT + 10:
            self.speed_y = -self.speed_y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if hero and pygame.sprite.collide_mask(self, hero):  # проверка на столкновение с персонажем
            hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # удаление объекта из группы, если он за пределами экрана
        if self.rect.x > SCREEN_WIDTH + 10 or self.rect.x < -10 or self.rect.y > SCREEN_HEIGHT + 10 or self.rect.y < -10:
            self.kill()


class HorizontalIceBottom(pygame.sprite.Sprite):  # класс горизонтальных льдин снизу
    def __init__(self, time):
        super().__init__(ice_group)
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_bottom.png')),
                                            (500, 100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = 700

    def update(self):
        global hor_ice
        if hero and pygame.sprite.collide_mask(self, hero):  # проверка на столкновение с персонажем
            hero.status = 0#флаг, определяющий состояние главного героя (жив или мертв)
            pygame.mixer.Sound("sounds/death.ogg").play()
        # удаление объекта из группы, если прошло 5 секунд
        if timer.elapsed_time - self.time >= 5:
            self.rect.y += 10
        elif self.rect.y != 600:
            self.rect.y -= 10
        if self.rect.y > 800:
            self.kill()
            hor_ice = False


class HorizontalIceTop(pygame.sprite.Sprite):  # класс горизонтальных верхних льдин
    def __init__(self, time):
        super().__init__(ice_group)
        pygame.mixer.Sound("sounds/ice.ogg").play()
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_top.png')),
                                            (500, 100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = -100

    def update(self):
        global hero
        global hor_ice
        if hero and pygame.sprite.collide_mask(self, hero):  # проверка на столкновение с персонажем
            hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        # удаление объекта из группы, если прошло 5 секунд
        if timer.elapsed_time - self.time >= 5:
            self.rect.y -= 10
        elif self.rect.y != 0:
            self.rect.y += 10
        if self.rect.y < -100:
            self.kill()
            hor_ice = False


class VerticalIceLeft(pygame.sprite.Sprite):  # класс вертикальных льдин с левой стороны
    def __init__(self, time):
        super().__init__(ice_group)
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_vert_left.png')),
                                            (120, 700)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -100

    def update(self):
        global vert_ice
        if hero and pygame.sprite.collide_mask(self, hero):  # проверка на столкновение с персонажем
            hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()# звук появления
        # удаление объекта из группы, если прошло 5 секунд
        if timer.elapsed_time - self.time >= 5:
            self.rect.x -= 10
        elif self.rect.x != 0:
            self.rect.x += 10
        if self.rect.x < -100:
            self.kill()
            vert_ice = False


class VerticalIceRight(pygame.sprite.Sprite):  # класс вертикальных льдин с правой стороны
    def __init__(self, time):
        super().__init__(ice_group)
        pygame.mixer.Sound("sounds/ice.ogg").play()
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_vert_right.png')),
                                            (120, 700)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 500

    def update(self):
        global vert_ice
        if hero and pygame.sprite.collide_mask(self, hero):  # проверка на столкновение с персонажем
            hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        # удаление объекта из группы, если прошло 5 секунд
        if timer.elapsed_time - self.time >= 5:
            self.rect.x += 10
        elif self.rect.x != 380:
            self.rect.x -= 10
        if self.rect.x > 600:
            self.kill()
            vert_ice = False


class Button(pygame.sprite.Sprite):  # универсальный класс  для создания кнопок
    def __init__(self, text, x, y, func=print, font_size=30, text_x=35, text_y=12):
        super().__init__(buttons)
        font = pygame.font.Font('font/20960.ttf', font_size)
        self.text = font.render(text, True, ((18, 45, 55)))
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\button.png')), (250, 70))
        self.rect = self.image.get_rect()
        self.text_rect = self.rect.copy()
        self.rect.x = x
        self.rect.y = y
        self.text_rect.x = self.rect.x + text_x
        self.text_rect.y = self.rect.y + text_y
        self.image.blit(self.text, self.text_rect)
        self.func = func

    def update(self):
        global sc
        if event.type == pygame.MOUSEBUTTONDOWN and event.__dict__['button'] == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\button_down.png')), (250, 70))
                sc.blit(self.image, self.rect)
                sc.blit(self.text, self.text_rect)
                pygame.display.flip()
                self.func()
        self.kill()


class Difficyulty(pygame.sprite.Sprite):#класс для кнпок сложности
    def __init__(self, x, y, filename):
        super().__init__()
        self.down = False
        self.filename = filename#имя файла изображения для определения уровня сложности 1,2,3
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\{filename}')), (50, 50))
        self.image_down = pygame.transform.scale(load_image(os.path.abspath(f'data\\{self.filename[:-4]}_down.png')),
                                                 (50, 50))
        self.rect = self.image.get_rect()
        self.text_rect = self.rect.copy()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global sc, spped1, speed2, period
        global l1, l2, l3, diff_group, period_hor_ice, period_vert_ice, fireball_period, second
        if pygame.mouse.get_pressed(num_buttons=3)[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.down = not (self.down)
            #определение уровня сложности,чтобы при нажатии одной кнопки все осталтьные возвращались в ненажатое состояние
            if '1' in self.filename:
                if l2.down:
                    l2.down = False
                    l2.image, l2.image_down = l2.image_down, l2.image
                if l3.down:
                    l3.down = False
                    l3.image, l3.image_down = l3.image_down, l3.image
                if self.down:# если кнопка нажата, применяю настройки в соответствии с уровнем сложности
                    period = (10, 20)
                    second = 800
                    speed1, speed2 = 2, 4
            elif '2' in self.filename:
                if l1.down:
                    l1.down = False
                    l1.image, l1.image_down = l1.image_down, l1.image
                if l3.down:
                    l3.down = False
                    l3.image, l3.image_down = l3.image_down, l3.image
                if self.down:
                    period = (8, 15)
                    second = 700
                    speed1, speed2 = 3, 6
            else:
                if l1.down:
                    l1.down = False
                    l1.image, l1.image_down = l1.image_down, l1.image
                if l2.down:
                    l2.down = False
                    l2.image, l2.image_down = l2.image_down, l2.image
                if self.down:
                    period = (5, 10)
                    second = 500
                    speed1, speed2 = 6, 8
            if not (self.down):
                period = (10, 20)
                second = 800
                speed1, speed2 = 2, 4
            self.image, self.image_down = self.image_down, self.image#изменение состояния кнопки визуально


def start_btn_func():  # функция для кнопки начала новой игры, передается в конструктор Button()
    #обнуление всех переменных, тк функция используется в начале и в конце
    global music
    global timer, end, hero, running, start_page
    global bullet_group, ice_group
    global hor_ice, vert_ice, fireball
    fireball = False
    music = False
    end=0
    running=True
    hor_ice = False
    vert_ice = False
    bullet_group = pygame.sprite.Group()
    ice_group = pygame.sprite.Group()
    start_page = False
    timer=False
    pygame.mouse.set_visible(False)
    hero = Alien()


def exit_btn_func():  # функция для кнопки выхода, передается в конструктор Button()
    pygame.quit()
    sys.exit()


def main_menu_func():
    global timer, end, hero, running, start_page
    global bullet_group, ice_group
    global hor_ice, vert_ice, fireball
    fireball = False
    hor_ice = False
    vert_ice = False
    bullet_group = pygame.sprite.Group()
    ice_group = pygame.sprite.Group()
    timer = False
    hero = Alien()
    end = 0
    start_page = True


class Timer():  # класс таймера для контроля времени в игре
    def __init__(self):
        self.start_time = time.time()  # время начала отсчета
        self.elapsed_time = 0  # сколько прошло времени с начала отсчета

    def update(self):
        self.elapsed_time = time.time() - self.start_time
        str_time = time.strftime("%M:%S", time.gmtime(self.elapsed_time))  # получение времени в "красивом" формате
        font = pygame.font.Font('font/20960.ttf', 30)
        self.text = font.render(str_time, True, ((18, 45, 55)))
        sc.blit(self.text, (400, 0))


if __name__ == '__main__':
    pygame.init()
    # создание групп спрайтов
    ice_group = pygame.sprite.Group()
    diff_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    sc = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    hero = Alien()
    fireball = False  # флаг наличия фаербола, нужен для контроля его появления
    font = pygame.font.Font('font/20960.ttf', 50)
    title = font.render('Save the Аlien', True, ((18, 45, 55)))
    font = pygame.font.Font('font/20960.ttf', 25)
    diff = font.render('Сложность: ', True, ((18, 45, 55)))
    hor_ice = False  # флаги наличия льдин, нужны для контроля их появления
    vert_ice = False
    l1 = Difficyulty(140, 630, 'level1.png')  # кнопки уровней сложности
    l2 = Difficyulty(190, 630, 'level2.png')
    l3 = Difficyulty(240, 630, 'level3.png')
    diff_group.add(l1)
    diff_group.add(l2)
    diff_group.add(l3)
    speed1, speed2 = 2, 4  # скорости пуль по умолчанию (легкий уровень)
    period = (15, 30)  # период появления льдин и фаербола по умолчанию (легкий уровень)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Save the Alien')
    start_page = True
    difficult_page = False
    end = 0  # флаг для проверки стартового окна
    running = True
    second = 800  # задержка времени перед созданием новых пуль
    timer = False  # инициализация таймера происходит в самой игре, а не в меню, переменная нужна,
    # чтобы таймер не начинался заново с каждым прогоном цикла
    start_bg = load_image(os.path.abspath(f'data\\bg3.png'))  # загрузка стартового фона
    game_bg = load_image(os.path.abspath(f'data\\start_bg1.png'))  # загрузка игрового фона
    last = pygame.time.get_ticks()
    music = False  # флаг нужен для переключения музыки в разных окнах
    while running:
        if start_page:  # работа со стартовым окном
            if not (music):
                FPS = 15  # изменение фпс для нормального отслеживания нажатий на кнопки в меню
                pygame.mixer.music.load("sounds/menu_music.mp3")  # загрузка музыки для меню
                pygame.mixer.music.play(-1)  # включение музыки в меню
                music = True
            sc.blit(start_bg, (0, 0))
            sc.blit(title, (80, 90))
            sc.blit(diff, (5, 650))
            diff_group.draw(sc)
            start_btn = Button('Начать игру', 120, 260, start_btn_func)
            exit_btn = Button('Выход', 120, 340, exit_btn_func, text_x=70, text_y=18)
            buttons.draw(sc)
            sc.blit(start_btn.text, start_btn.text_rect)
            sc.blit(exit_btn.text, exit_btn.text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            buttons.update()
            buttons.draw(sc)
            diff_group.update()
        elif hero.status:  # сама игра
            if not (music):
                FPS = 60
                period_hor_ice = randint(*period)
                period_vert_ice = randint(*period)
                fireball_period = randint(*period)
                pygame.mixer.music.load("sounds/game_music.mp3")
                pygame.mixer.music.play(-1)
                music = True
            sc.blit(game_bg, (0, 0))

            if not (timer):  # создание таймера, начало отчета после нажатия кнопки старта
                timer = Timer()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.MOUSEMOTION and hero:  # обновление персонажа при движении мышки
                    hero.update()
                    pos = pygame.mouse.get_pos()

            sc.blit(hero.image, hero.rect)
            hero.k += 1  # переменная для контроля времени смены кадров анимации главного героя
            if hero.k == 49:
                hero.k = 0
            # если время делится нацело на период появления льдин и их нет  на экране и время больше нуля
            if int(timer.elapsed_time) % period_hor_ice == 0 and not (hor_ice) and int(timer.elapsed_time) > 0:
                HorizontalIceTop(timer.elapsed_time)
                HorizontalIceBottom(timer.elapsed_time)
                period_hor_ice = randint(*period)
                hor_ice = True

            if int(timer.elapsed_time) % period_vert_ice == 0 and not (vert_ice) and int(timer.elapsed_time) > 0:
                VerticalIceRight(timer.elapsed_time)
                VerticalIceLeft(timer.elapsed_time)
                period_vert_ice = randint(*period)
                vert_ice = True

            if int(timer.elapsed_time) % fireball_period == 0 and not fireball and int(timer.elapsed_time) > 0:
                fireball = Fireball(choice(['d', 'l', 'up', 'r']))
                fireball_period = randint(*period)

            now = pygame.time.get_ticks()

            if now - last >= second:  # задержка времени перед созданием новых пуль
                for i in range(2):  # цикл создания пуль
                    Bullets(speed1, speed2)
                last = pygame.time.get_ticks()  # обновляется время после отображения пуль
                # обнуление таймера с момента отрисовки пуль
            if fireball:  # проверка на наличие фаербола, смена кадров анимации и отображение
                fireball.k += 1
                if fireball.k == 6:
                    fireball.k = 0
                sc.blit(fireball.image, fireball.rect)
                fireball.update()

            bullet_group.update()
            bullet_group.draw(sc)
            ice_group.update()
            ice_group.draw(sc)
            timer.update()
        elif not (hero.status):  # проверка на конец игры
            if not (end):
                music = False
                if not (music):
                    pygame.mixer.music.load("sounds/menu_music.mp3")
                    pygame.mixer.music.play(-1)
                    music = True
                sc.blit(start_bg, (0, 0))
                game_over(sc, timer)  # функция для рисования окна конца игры
                end = 1
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            repeat_btn = Button('Начать заново', 120, 400, start_btn_func, text_x=13)  # создание кнопок
            main_menu_btn = Button('Главное меню', 120, 490, main_menu_func, text_x=13)
            exit_btn = Button('Выход', 120, 570, exit_btn_func, text_x=70, text_y=18)
            buttons.draw(sc)
            sc.blit(repeat_btn.text, repeat_btn.text_rect)
            sc.blit(exit_btn.text, exit_btn.text_rect)
            sc.blit(main_menu_btn.text, main_menu_btn.text_rect)
        buttons.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
