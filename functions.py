import pygame
import time
import sys
import os

def results_func(timer,level):  # работа с файлом сохранения рекордов
    if level =='lite':
        num =1
    elif level =='medium':
        num=2
    elif level == 'hard':
        num=3
    with open(f'results_l{num}.txt', mode='r') as file:
        results = list(map(lambda x: float(x.split()[1]), file.readlines()))  # загрузка данных из файла
        results.append(timer.elapsed_time)
        results_for_display = list(
            map(lambda x: ' '.join((str(x[0] + 1) + '.', time.strftime("%M:%S", time.gmtime(x[1])))),
                enumerate(sorted(results, reverse=True)[:-1])))  # список для вывода на экран
        results = '\n'.join(list(map(lambda x: str(x[0] + 1) + '. ' + str(x[1]),  # список для сохранения  в файл
                                     enumerate(sorted(results, reverse=True)[:-1]))))
        file.close()
        with open(f'results_l{num}.txt', mode='w') as file:
            file.writelines(results)
            file.close()
        return results_for_display





def load_image(name, colorkey=None):  # функция загрузки изображений
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
