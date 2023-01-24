import pygame
from functions import load_image
import os


class Button(pygame.sprite.Sprite):  # универсальный класс  для создания кнопок
    def __init__(self, group, sc, text, x, y, func=print, font_size=30, text_x=35, text_y=12):
        super().__init__(group)
        font = pygame.font.Font('font/20960.ttf', font_size)
        self.text = font.render(text, True, ((18, 45, 55)))
        self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\button.png')), (250, 70))
        self.rect = self.image.get_rect()
        self.text_rect = self.rect.copy()
        self.rect.x = x
        self.sc = sc
        self.rect.y = y
        self.text_rect.x = self.rect.x + text_x
        self.text_rect.y = self.rect.y + text_y
        self.image.blit(self.text, self.text_rect)
        self.func = func

    def update(self):
        if pygame.mouse.get_pressed(num_buttons=3)[0] and self.rect.collidepoint(pygame.mouse.get_pos()) == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = pygame.transform.scale(load_image(os.path.abspath(f'data\\button_down.png')), (250, 70))
                self.sc.blit(self.image, self.rect)
                self.sc.blit(self.text, self.text_rect)
                pygame.display.flip()
                self.func()
        self.kill()
