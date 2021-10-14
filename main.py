from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from random import randint, choice


def update(frame, alive_buffer_coord, transitions):
    buffer = np.zeros(frame.shape, dtype=np.uint8)
    x_, y_ = alive_buffer_coord
    xm = x_-1
    ym = y_-1
    xp = (x_+1) % frame.shape[0]
    yp = (y_+1) % frame.shape[1]
    x_ = [xm, x_, xp, xm, xp, xm, x_, xp]
    y_ = [ym, ym, ym, y_, y_, yp, yp, yp]
    for x, y in zip(x_, y_):
        buffer[x, y] += 1
    frame = transitions[frame, buffer]
    alive_buffer_coord = np.where(frame == 1)
    return frame, alive_buffer_coord


# класс игры
class Game:
    def __init__(self,
                 field=np.zeros((20, 20, 3), dtype=np.uint8),
                 rules=None):
        # проверяет нужно ли завершить игру
        self.finish = False
        # готовит окна
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Life")

        # * self.transition[i, j]
        # * where i is value of cell
        # * and j is number of neighbours
        self.transitions = np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 1, 1, 0, 0, 0, 0, 0]])

        if rules is not None:
            self.transitions = rules
        # Обработчик на клик мышкой
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        # подготовка изображения-массива
        self.frame = field
        self.alive_buffer_coord = np.where(self.frame == 1)
        # визуализация с анимацией
        self.im = plt.imshow(self.frame)

        # запуск анимации self.fig - окно для анимации
        # self.update - функция отрисовки каждого кадра
        # self.init_target - функция, которая отработает перед
        # запуском анимациии
        # self.end_game - функция-обман для matplotlib.
        # Matplotlib требует точного количества кадров для завершения анимации.
        # Мы же сделаем бесконечный генератор.
        # interval - количество миллисекунд, после которых снова вызывается
        # функция self.update
        self.ani = FuncAnimation(self.fig, self.update,
                                 init_func=self.init_target,
                                 frames=self.end_game,
                                 blit=True,
                                 interval=20)
        plt.axis('off')
        plt.show()

    # остановит игру
    def end_game(self):
        i = 0
        while not self.finish:
            i += 1
            yield i

    # функция инициализациии
    def init_target(self):
        return self.im,

    # функция отрисовки
    def update(self, param):
        self.frame, self.alive_buffer_coord = update(
            self.frame, self.alive_buffer_coord, self.transitions)
        self.im.set_data(self.frame)
        return self.im,

    # TODO drawing
    def onclick(self, event):
        x, y = round(event.xdata), round(event.ydata)
        print(x, y)
        self.frame[x, y] = 1
        # Если кликнули ...


if __name__ == "__main__":
    size = (600, 600)  # размер поля
    field = np.zeros(size, dtype=np.uint8)

    # генерация всяких живых фигур
    edem0 = np.ones((2, 2))  # сад эдема

    osciilator1 = np.ones((4, 4))  # осцилятор с частотой 2 тика
    osciilator1[2:, 2:] -= edem0
    osciilator1[:2, :2] -= edem0

    glider0 = np.array([[1, 1, 1], [0, 0, 1], [0, 1, 0]])  # glider 1

    heavy_spaceship0 = np.array([[0, 0, 1, 1, 0],  # glider 2
                                [1, 1, 0, 1, 1],
                                [1, 1, 1, 1, 0],
                                [0, 1, 1, 0, 0]])

    heavy_spaceship1 = np.array([[0, 0, 0, 1, 1, 0],  # glider 3
                                [1, 1, 1, 0, 1, 1],
                                [1, 1, 1, 1, 1, 0],
                                [0, 1, 1, 1, 0, 0]])

    osciilator0 = np.array([[1, 1, 1]])  # осцилятор с частотой 2 тика

    seed = np.array([[0, 1, 0], [1, 1, 1], [1, 0, 1],
                    [0, 1, 0]])  # создает цветок с 4 лепестками

    figures = [edem0, glider0, osciilator0, osciilator1,
               seed, heavy_spaceship0, heavy_spaceship1]

    for i in range(920):
        figure = choice(figures)
        figure = np.rot90(figure, k=randint(0, 4))
        x, y = randint(0, size[0]), randint(0, size[1])
        try:
            field[x:x+figure.shape[0], y:y+figure.shape[1]] = figure
        finally:
            continue

    # запуск игры
    gg = Game(field)
