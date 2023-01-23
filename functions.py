import pygame
import time
import sys
import os

def results_func(timer):  # работа с файлом сохранения рекордов
    with open('results.txt', mode='r') as file:
        results = list(map(lambda x: float(x.split()[1]), file.readlines()))  # загрузка данных из файла
        results.append(timer.elapsed_time)
        results_for_display = list(
            map(lambda x: ' '.join((str(x[0] + 1) + '.', time.strftime("%M:%S", time.gmtime(x[1])))),
                enumerate(sorted(results, reverse=True)[:-1])))  # список для вывода на экран
        results = '\n'.join(list(map(lambda x: str(x[0] + 1) + '. ' + str(x[1]),  # список для сохранения  в файл
                                     enumerate(sorted(results, reverse=True)[:-1]))))
        file.close()
        with open('results.txt', mode='w') as file:
            file.writelines(results)
            file.close()
        return results_for_display


def game_over(sc, timer):
    col=(18,45,55)
    font = pygame.font.Font('font/20960.ttf', 50)
    text = font.render('Конец игры!', True, col)
    sc.blit(text, (110, 120))
    res = results_func(timer)
    font = pygame.font.Font('font/20960.ttf', 30)
    result1 = font.render(res[0], True, col)
    result2 = font.render(res[1], True, col)
    result3 = font.render(res[2], True, col)
    sc.blit(result1, (170, 210))
    sc.blit(result2, (170, 260))
    sc.blit(result3, (170, 310))


def load_image(name, colorkey=None):  # функция загрузки изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
