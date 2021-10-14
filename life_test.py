from unittest import TestCase, main
import numpy as np
from main import update

frame_size = (20, 20)


class Test(TestCase):
    def setUp(self) -> None:  # запускается перед каждым тестом
        self.frame = np.zeros(frame_size, dtype=np.uint8)
        self.transitions = np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 1, 1, 0, 0, 0, 0, 0]])
        return super().setUp()

    def edem_test0(self):  # сады эдема стабильные и не меняются
        edem = np.ones((2, 2))
        self.frame[2:4, 2:4] = edem
        frame_source = self.frame.copy()
        alives = np.where(self.frame == 1)
        self.frame, alives = update(self.frame, alives, self.transitions)
        self.assertEqual(self.frame.all(), frame_source.all())

    def edem_test1(self):
        edem = np.array([[0, 1, 0], [1, 0, 1], [1, 0, 1], [0, 1, 0]])
        self.frame[1:5, 1:4] = edem
        frame_source = self.frame.copy()
        alives = np.where(self.frame == 1)
        self.frame, alives = update(self.frame, alives, self.transitions)
        self.assertEqual(self.frame.all(), frame_source.all())

    def oscillator_test(self):  # осциляторы возвращаются в исходное состояние через определенное кол-во тиков
        oscillator = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
        self.frame[1:3, 1:3] = oscillator
        frame_source = self.frame.copy()
        alives = np.where(self.frame == 1)
        self.frame, alives = update(self.frame, alives, self.transitions)
        self.assertEqual(self.frame.all(), frame_source.transpose().all())  # на первом тике фигурка поворачивается на 90 градусов
        self.frame, alives = update(self.frame, alives, self.transitions)
        self.assertEqual(self.frame.all(), frame_source.all())  # на втором тике фигурка поворачивается еще на 90 градусов

    def death_test(self):  # тест смерти клетки без соседей
        death = np.array([[1]])
        self.frame[3, 4] = death
        frame1 = self.frame.copy()
        alives = np.where(self.frame == 1)
        self.frame, alives = update(self.frame, alives, self.transitions)
        self.assertEqual(np.zeros(frame_size).all(), frame1.transpose().all())


# сады эдема тестируют переходы из живой клетки в живую
# осциляторы тестируют переходы из живой клетки в в мертвую и рождения новых клеток
# таким образом тестируется +- все возможные исходы функции апдейт

if __name__ == '__main__':
    main()
