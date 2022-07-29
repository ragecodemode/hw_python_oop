from typing import Dict, Type

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; ' 
               f'Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.')


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
        return InfoMessage(
            training_type = self.__class__.__name__,
            duration = self.duration,
            distance = self.get_distance(),
            speed = self.get_mean_speed(),
            calories = self.get_spent_calories()
        )


class Running(Training):
    """Тренеровка: бег."""
    run_coeff_calorie_1: float = 18
    run_coeff_calorie_2: float = 20

    def get_spent_calories(self) -> float:
        return (self.run_coeff_calorie_1 * self.get_mean_speed() -
                self.run_coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    wlk_coeff_calorie_1: float = 0.035
    wlk_coeff_calorie_2: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.wlk_coeff_calorie_1 * self.weight + (self.get_mean_speed() ** 2 // self.height)
                * self.wlk_coeff_calorie_2 * self.weight) * 60 * self.duration


class Swimming(Training):
    """Тренировка: плавание."""
    swm_coeff_calorie_1: float = 1.1
    swm_coeff_calorie_2: float = 2
    LEN_STEP: float = 1.38
    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Расстояние в бассейне"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.swm_coeff_calorie_1) * self.swm_coeff_calorie_2 * self.weight


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

