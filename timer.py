import pygame
import time
class Timer():  # класс таймера для контроля времени в игре
    def __init__(self,sc):
        self.sc=sc
        self.start_time = time.time()  # время начала отсчета
        self.elapsed_time = 0  # сколько прошло времени с начала отсчета

    def update(self):
        self.elapsed_time = time.time() - self.start_time
        str_time = time.strftime("%M:%S", time.gmtime(self.elapsed_time))  # получение времени в "красивом" формате
        font = pygame.font.Font('font/20960.ttf', 30)
        self.text = font.render(str_time, True, ((18, 45, 55)))
        self.sc.blit(self.text, (400, 0))