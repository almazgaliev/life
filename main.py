from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from random import randint, choice

# класс игры


class Game:
    def __init__(self, field=np.zeros((20, 20, 3), dtype=np.uint8)):
        # проверяет нужно ли завершить игру
        self.finish = False
        # готовит окна
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Life")

        # * self.transition[x, y]
        # * where x is value of cell
        # * and y is neighbour
        self.transitions = np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 1, 1, 0, 0, 0, 0, 0]])
        # Обработчик на клик мышкой
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

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
    def update(self, par):
        buffer = np.zeros(self.frame.shape, dtype=np.uint8)

        x_, y_ = self.alive_buffer_coord
        xm = x_-1
        ym = y_-1
        xp = (x_+1) % self.frame.shape[0]
        yp = (y_+1) % self.frame.shape[1]
        x_ = [xm, x_, xp, xm, xp, xm, x_, xp]
        y_ = [ym, ym, ym, y_, y_, yp, yp, yp]
        for x, y in zip(x_, y_):
            buffer[x, y] += 1
        self.frame = self.transitions[self.frame, buffer]
        self.alive_buffer_coord = np.where(self.frame == 1)
        self.im.set_array(self.frame)
        return self.im,

    # функция выстрела
    def onclick(self, event):
        x, y = round(event.xdata), round(event.ydata)
        print(x, y)
        self.frame[x, y] = 1
        # Если кликнули ...


pink = (255, 56, 152)
cyan = (0, 255, 255)
green = (69, 228, 69)
purple = (201, 22, 255)
red = (255, 30, 30)

size = (500, 500)
field = np.zeros(size, dtype=np.uint8)

edem0 = np.ones((2, 2))
osciilator1 = np.ones((4, 4))
osciilator1[2:, 2:] -= edem0
osciilator1[:2, :2] -= edem0
glider0 = np.array([[1, 1, 1], [0, 0, 1], [0, 1, 0]])
heavy_spaceship0 = np.array([[0, 0, 1, 1, 0],
                             [1, 1, 0, 1, 1],
                             [1, 1, 1, 1, 0],
                             [0, 1, 1, 0, 0]])
heavy_spaceship1 = np.array([[0, 0, 0, 1, 1, 0],
                             [1, 1, 1, 0, 1, 1],
                             [1, 1, 1, 1, 1, 0],
                             [0, 1, 1, 1, 0, 0]])
osciilator0 = np.array([[1, 1, 1]])
seed = np.array([[0, 1, 0], [1, 1, 1], [1, 0, 1], [0, 1, 0]])

figures = [edem0, glider0, osciilator0, osciilator1,
           seed, heavy_spaceship0, heavy_spaceship1]
for i in range(220):
    figure = choice(figures)
    figure = np.rot90(figure, k=randint(0, 4))
    x, y = randint(0, size[0]), randint(0, size[1])
    try:
        field[x:x+figure.shape[0], y:y+figure.shape[1]] = figure
    finally:
        continue

# field = np.random.randint(0, high=2, size=size)
gg = Game(field)
