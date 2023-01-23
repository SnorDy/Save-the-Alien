import pygame
import os
import sys


class Alien(pygame.sprite.Sprite):  # класс главного персонажа
    def __init__(self):
        super().__init__()
        self.frames = dict()
        # загрузка списков с кадрами анимации главного героя
        self.anim_set_up = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_up{i}.png')),
                                                   (70, 70)).convert_alpha() for i in range(3)]
        self.anim_set_up_l = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_up_l{i}.png')),
                                                     (70, 70)).convert_alpha() for i in range(3)]
        self.anim_set_up_r = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_up_r{i}.png')),
                                                     (70, 70)).convert_alpha() for i in range(3)]
        self.anim_set_down = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_down{i}.png')),
                                                     (70, 70)).convert_alpha() for i in range(3)]
        self.anim_set_down_l = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_down_l{i}.png')),
                                                       (70, 70)).convert_alpha() for i in range(3)]
        self.anim_set_down_r = [pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_down_r{i}.png')),
                                                       (70, 70)).convert_alpha() for i in range(3)]
        for el in ['front1', 'l1', 'r1', ]:
            self.frames[el] = pygame.transform.scale(load_image(os.path.abspath(f'data\\alien_{el}.png')), (70, 70))
        self.cur_frame = 'front1'
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        self.status = 1
        self.k = 0
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
            if self.rect.x>440:
                self.rect.x=440
            if self.rect.y>630:
                self.rect.y=630
            if isinstance(self.cur_frame, list):
                self.image = self.cur_frame[self.k // 24]
            else:
                self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)

def load_image(name, colorkey=None):  # функция загрузки изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

