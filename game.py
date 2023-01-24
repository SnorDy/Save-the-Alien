import pygame
import sys
import os
from constants import *
from random import randint, choice
from timer import Timer
from buttons import Button
from functions import load_image, results_func
from main_hero import Alien

class Fireball(pygame.sprite.Sprite):  # класс фаербола
    def __init__(self, direction):
        super().__init__()
        x = 30
        y = 80
        if direction == 'd' or direction == 'up':
            self.size = (x, y)  # размеры изображения меняются в соответствии с направлением
        else:
            self.size = (y, x)
        self.k = 0
        self.anim_set = [pygame.transform.scale(load_image(os.path.abspath(f'data\\fireball_{direction}{i}.png')),
                                                self.size) for i in range(2)]
        self.image = self.anim_set[self.k]
        self.rect = self.image.get_rect()
        if direction == 'd' or direction == 'up':  # фаербол летит по направлению в игрока
            self.rect.x = game.hero.x + 20
        else:
            self.rect.y = game.hero.y + 20

        self.direction = direction
        self.speed = randint(6, 7)
        if direction == 'up':
            self.rect.y = 715  # начальные координаты появления
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
        self.image = self.anim_set[self.k // 5]
        if game.hero and pygame.sprite.collide_mask(self, game.hero):  # проверка на столкновение с персонажем
            game.hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        if self.direction == 'up' or self.direction == 'd':
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
        # удаление объекта из группы, если он за пределами экрана
        if self.rect.x > SCREEN_WIDTH + 20 or self.rect.x < -20 \
                or self.rect.y > SCREEN_HEIGHT + 20 or self.rect.y < -20:
            self.kill()
            game.fireball = False


class HorizontalIceBottom(pygame.sprite.Sprite):  # класс горизонтальных льдин снизу
    def __init__(self, time):
        super().__init__(game.ice_group)
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_bottom.png')),
                                            (500, 100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = 700

    def update(self):
        if game.hero and pygame.sprite.collide_mask(self, game.hero):  # проверка на столкновение с персонажем
            game.hero.status = 0  # флаг, определяющий состояние главного героя (жив или мертв)
            pygame.mixer.Sound("sounds/death.ogg").play()
        # удаление объекта из группы, если прошло 5 секунд
        if game.timer.elapsed_time - self.time >= 5:
            self.rect.y += 10
        elif self.rect.y != 600:
            self.rect.y -= 10
        if self.rect.y > 800:
            self.kill()
            game.hor_ice = False


class HorizontalIceTop(pygame.sprite.Sprite):  # класс горизонтальных верхних льдин
    def __init__(self, time):
        super().__init__(game.ice_group)
        pygame.mixer.Sound("sounds/ice.ogg").play()
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_top.png')),
                                            (500, 100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = -100

    def update(self):
        if game.hero and pygame.sprite.collide_mask(self, game.hero):  # проверка на столкновение с персонажем
            game.hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        # удаление объекта из группы, если прошло 5 секунд
        if game.timer.elapsed_time - self.time >= 5:
            self.rect.y -= 10
        elif self.rect.y != 0:
            self.rect.y += 10
        if self.rect.y < -100:
            self.kill()
            game.hor_ice = False


class VerticalIceLeft(pygame.sprite.Sprite):  # класс вертикальных льдин с левой стороны
    def __init__(self, time):
        super().__init__(game.ice_group)
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_vert_left.png')),
                                            (120, 700)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -100

    def update(self):
        if game.hero and pygame.sprite.collide_mask(self, game.hero):  # проверка на столкновение с персонажем
            game.hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()  # звук появления
        # удаление объекта из группы, если прошло 5 секунд
        if game.timer.elapsed_time - self.time >= 5:
            self.rect.x -= 10
        elif self.rect.x != 0:
            self.rect.x += 10
        if self.rect.x < -100:
            self.kill()
            game.vert_ice = False


class VerticalIceRight(pygame.sprite.Sprite):  # класс вертикальных льдин с правой стороны
    def __init__(self, time):
        super().__init__(game.ice_group)
        pygame.mixer.Sound("sounds/ice.ogg").play()
        self.time = time
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\ice_vert_right.png')),
                                            (120, 700)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 500

    def update(self):
        if game.hero and pygame.sprite.collide_mask(self, game.hero):  # проверка на столкновение с персонажем
            game.hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        # удаление объекта из группы, если прошло 5 секунд
        if game.timer.elapsed_time - self.time >= 5:
            self.rect.x += 10
        elif self.rect.x != 380:
            self.rect.x -= 10
        if self.rect.x > 600:
            self.kill()
            game.vert_ice = False


class Bullets(pygame.sprite.Sprite):  # класс пуль
    def __init__(self, speed1, speed2):
        super().__init__(game.bullet_group)
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
        if game.hero and pygame.sprite.collide_mask(self, game.hero):  # проверка на столкновение с персонажем
            game.hero.status = 0
            pygame.mixer.Sound("sounds/death.ogg").play()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # удаление объекта из группы, если он за пределами экрана
        if self.rect.x > SCREEN_WIDTH + 10 or self.rect.x < -10 or self.rect.y > SCREEN_HEIGHT + 10 or self.rect.y < -10:
            self.kill()


class Difficyulty(pygame.sprite.Sprite):  # класс для кнпок сложности
    def __init__(self, x, y, filename):
        super().__init__()
        self.down = False
        self.filename = filename  # имя файла изображения для определения уровня сложности 1,2,3
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\{filename}')), (50, 50))
        self.image_down = pygame.transform.scale(load_image(os.path.abspath(f'data\\{self.filename[:-4]}_down.png')),
                                                 (50, 50))
        self.rect = self.image.get_rect()
        self.text_rect = self.rect.copy()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.mouse.get_pressed(num_buttons=3)[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.down = not (self.down)
            # определение уровня сложности,чтобы при нажатии одной кнопки все осталтьные возвращались в ненажатое состояние
            if '1' in self.filename:
                if game.l2.down:
                    game.l2.down = False
                    game.l2.image, game.l2.image_down = game.l2.image_down, game.l2.image
                if game.l3.down:
                    game.l3.down = False
                    game.l3.image, game.l3.image_down = game.l3.image_down, game.l3.image
                if self.down:  # если кнопка нажата, применяю настройки в соответствии с уровнем сложности
                    game.period = (10, 20)
                    game.second = 800
                    game.speed1, game.speed2 = 2, 4
                    game.level = 'lite'
            elif '2' in self.filename:
                if game.l1.down:
                    game.l1.down = False
                    game.l1.image, game.l1.image_down = game.l1.image_down, game.l1.image
                if game.l3.down:
                    game.l3.down = False
                    game.l3.image, game.l3.image_down = game.l3.image_down, game.l3.image
                if self.down:
                    game.period = (8, 15)
                    game.second = 700
                    game.speed1, game.speed2 = 3, 6
                    game.level = 'medium'
            else:
                if game.l1.down:
                    game.l1.down = False
                    game.l1.image, game.l1.image_down = game.l1.image_down, game.l1.image
                if game.l2.down:
                    game.l2.down = False
                    game.l2.image, game.l2.image_down = game.l2.image_down, game.l2.image
                if self.down:
                    game.period = (5, 10)
                    game.second = 500
                    game.speed1, game.speed2 = 6, 8
                    game.level = 'hard'
            if not (self.down):
                game.period = (10, 20)
                game.second = 800
                game.speed1, speed2 = 2, 4

            self.image, self.image_down = self.image_down, self.image  # изменение состояния кнопки визуально


def start_btn_func():  # функция для кнопки начала новой игры, передается в конструктор Button()
    # обнуление всех переменных, тк функция используется в начале и в конце
    game.fireball = False
    game.music = False
    game.end = 0
    game.running = True
    game.hor_ice = False
    game.vert_ice = False
    game.bullet_group = pygame.sprite.Group()
    game.ice_group = pygame.sprite.Group()
    game.start_page = False
    game.timer = False
    pygame.mouse.set_visible(False)
    game.hero = Alien()


def exit_btn_func():  # функция для кнопки выхода, передается в конструктор Button()
    pygame.quit()
    sys.exit()


def main_menu_func():
    game.fireball = False
    game.hor_ice = False
    game.vert_ice = False
    game.bullet_group = pygame.sprite.Group()
    game.ice_group = pygame.sprite.Group()
    game.timer = False
    game.hero = Alien()
    game.end = 0
    game.start_page = True


class Game():
    def __init__(self):
        pygame.init()
        # создание групп спрайтов
        icon = pygame.image.load('data/alien_front0.png')
        pygame.display.set_icon(icon)
        self.level='lite'
        self.ice_group = pygame.sprite.Group()
        self.diff_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.sc = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.hero = Alien()
        self.fireball = False  # флаг наличия фаербола, нужен для контроля его появления
        font = pygame.font.Font('font/20960.ttf', 50)
        self.title = font.render('Save the Аlien', True, ((18, 45, 55)))
        font = pygame.font.Font('font/20960.ttf', 25)
        self.diff = font.render('Сложность: ', True, ((215, 241, 252)))
        self.hor_ice = False  # флаги наличия льдин, нужны для контроля их появления
        self.vert_ice = False
        self.l1 = Difficyulty(250, 630, 'level1.png')  # кнопки уровней сложности
        self.l2 = Difficyulty(300, 630, 'level2.png')
        self.l3 = Difficyulty(350, 630, 'level3.png')
        self.diff_group.add(self.l1)
        self.diff_group.add(self.l2)
        self.diff_group.add(self.l3)
        self.speed1, self.speed2 = 2, 4  # скорости пуль по умолчанию (легкий уровень)
        self.period = (15, 30)  # период появления льдин и фаербола по умолчанию (легкий уровень)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Save the Alien')
        self.start_page = True
        self.end = 0  # флаг для проверки стартового окна
        self.running = True
        self.second = 800  # задержка времени перед созданием новых пуль
        self.timer = False  # инициализация таймера происходит в самой игре, а не в меню, переменная нужна,
        # чтобы таймер не начинался заново с каждым прогоном цикла
        self.start_bg = load_image(os.path.abspath(f'data\\bg3.png'))  # загрузка стартового фона
        self.game_bg = load_image(os.path.abspath(f'data\\start_bg1.png'))  # загрузка игрового фона
        self.last = pygame.time.get_ticks()
        self.music = False  # флаг нужен для переключения музыки в разных окнах

    def start_page_func(self):
        if not (self.music):
            self.FPS = 15  # изменение фпс для нормального отслеживания нажатий на кнопки в меню
            pygame.mixer.music.load("sounds/menu_music.mp3")  # загрузка музыки для меню
            pygame.mixer.music.play(-1)  # включение музыки в меню
            self.music = True
        self.sc.blit(self.start_bg, (0, 0))
        self.sc.blit(self.title, (60, 90))
        self.sc.blit(self.diff, (115, 650))
        self.diff_group.draw(self.sc)
        self.start_btn = Button(self.buttons, self.sc, 'Начать игру', 120, 280, start_btn_func)
        self.exit_btn = Button(self.buttons, self.sc, 'Выход', 120, 380, exit_btn_func, text_x=70, text_y=18)
        self.buttons.draw(self.sc)
        self.sc.blit(self.start_btn.text, self.start_btn.text_rect)
        self.sc.blit(self.exit_btn.text, self.exit_btn.text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
        self.buttons.update()
        self.buttons.draw(self.sc)
        self.diff_group.update()

    def main_game(self):
        if not (self.music):
            self.FPS = 60
            self.period_hor_ice = randint(*self.period)
            self.period_vert_ice = randint(*self.period)
            self.fireball_period = randint(*self.period)
            pygame.mixer.music.load("sounds/game_music.mp3")
            pygame.mixer.music.play(-1)
            self.music = True
        self.sc.blit(self.game_bg, (0, 0))

        if not (self.timer):  # создание таймера, начало отчета после нажатия кнопки старта
            self.timer = Timer(self.sc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

            if event.type == pygame.MOUSEMOTION and self.hero:  # обновление персонажа при движении мышки
                self.hero.update()

        self.sc.blit(self.hero.image, self.hero.rect)
        self.hero.k += 1  # переменная для контроля времени смены кадров анимации главного героя
        if self.hero.k == 49:
            self.hero.k = 0
        # если время делится нацело на период появления льдин и их нет  на экране и время больше нуля
        if int(self.timer.elapsed_time) % self.period_hor_ice == 0 \
                and not (self.hor_ice) and int(self.timer.elapsed_time) > 0:
            HorizontalIceTop(self.timer.elapsed_time)
            HorizontalIceBottom(self.timer.elapsed_time)
            self.period_hor_ice = randint(*self.period)
            self.hor_ice = True

        if int(self.timer.elapsed_time) % self.period_vert_ice == 0 and not (self.vert_ice) \
                and int(self.timer.elapsed_time) > 0:
            VerticalIceRight(self.timer.elapsed_time)
            VerticalIceLeft(self.timer.elapsed_time)
            self.period_vert_ice = randint(*self.period)
            self.vert_ice = True

        if int(self.timer.elapsed_time) % self.fireball_period == 0 and not self.fireball \
                and int(self.timer.elapsed_time) > 0:
            self.fireball = Fireball(choice(['d', 'l', 'up', 'r']))
            self.fireball_period = randint(*self.period)

        now = pygame.time.get_ticks()

        if now - self.last >= self.second:  # задержка времени перед созданием новых пуль
            for i in range(2):  # цикл создания пуль
                Bullets(self.speed1, self.speed2)
            self.last = pygame.time.get_ticks()  # обновляется время после отображения пуль
            # обнуление таймера с момента отрисовки пуль
        if self.fireball:  # проверка на наличие фаербола, смена кадров анимации и отображение
            self.fireball.k += 1
            if self.fireball.k == 6:
                self.fireball.k = 0
            self.sc.blit(self.fireball.image, self.fireball.rect)
            self.fireball.update()

        self.bullet_group.update()
        self.bullet_group.draw(self.sc)
        self.ice_group.update()
        self.ice_group.draw(self.sc)
        self.timer.update()

    def game_over(self):
        if not (self.end):
            self.music = False
            if not (self.music):
                pygame.mixer.music.load("sounds/menu_music.mp3")
                pygame.mixer.music.play(-1)
                self.music = True
            self.sc.blit(self.start_bg, (0, 0))
            col = (18, 45, 55)
            font = pygame.font.Font('font/20960.ttf', 50)
            text = font.render('Конец игры!', True, col)
            self.sc.blit(text, (110, 60))
            res = results_func(self.timer,self.level)
            font = pygame.font.Font('font/20960.ttf', 30)
            level=font.render(f'Сложность: {self.level}', True, col)
            result1 = font.render(res[0], True, col)
            result2 = font.render(res[1], True, col)
            result3 = font.render(res[2], True, col)
            self.sc.blit(level,(110,160))
            self.sc.blit(result1, (170, 230))
            self.sc.blit(result2, (170, 280))
            self.sc.blit(result3, (170, 330))
            self.end = 1
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
        repeat_btn = Button(self.buttons, self.sc, 'Начать заново', 120, 400, start_btn_func,
                            text_x=13)  # создание кнопок
        main_menu_btn = Button(self.buttons, self.sc, 'Главное меню', 120, 490, main_menu_func, text_x=13)
        exit_btn = Button(self.buttons, self.sc, 'Выход', 120, 570, exit_btn_func, text_x=70, text_y=18)
        self.buttons.draw(self.sc)
        self.sc.blit(repeat_btn.text, repeat_btn.text_rect)
        self.sc.blit(exit_btn.text, exit_btn.text_rect)
        self.sc.blit(main_menu_btn.text, main_menu_btn.text_rect)

    def loop(self):
        while self.running:
            if self.start_page:  # работа со стартовым окном
                self.start_page_func()

            elif self.hero.status:  # сама игра
                self.main_game()

            elif not (self.hero.status):  # проверка на конец игры
                self.game_over()

            self.buttons.update()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.loop()
