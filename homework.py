from typing import Dict, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info_message: str = ('Тип тренировки: {training_type}; '
                         'Длительность: {duration:.3f} ч.; '
                         'Дистанция: {distance:.3f} км; '
                         'Ср. скорость: {speed:.3f} км/ч; '
                         'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.info_message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определить каллории')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренеровка: бег."""

    RUN_COEFF_1: float = 18
    RUN_COEFF_2: float = 20

    def get_spent_calories(self) -> float:
        # noinspection TaskProblemsInspection
        return (self.RUN_COEFF_1
                * self.get_mean_speed() -
                self.RUN_COEFF_2) * self.weight / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WLK_COEFF_1: float = 0.035
    WLK_COEFF_2: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # noinspection TaskProblemsInspection
        return (self.WLK_COEFF_1 * self.weight +
                (self.get_mean_speed() ** 2 // self.height) * self.WLK_COEFF_2 * self.weight) * 60 * self.duration


# noinspection TaskProblemsInspection
class Swimming(Training):
    """Тренировка: плавание."""

    SWM_COEFF_1: float = 1.1
    SWM_COEFF_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Расстояние в бассейне"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() +
                self.SWM_COEFF_1) * self.SWM_COEFF_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout = Dict[str, Type[Training]]

    work: workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in work:
        raise NotImplementedError('Возможно исключение')

    return work[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
