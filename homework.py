class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration * self.H_IN_M)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KOEF_1 = 0.035
    KOEF_2 = 0.029
    KMH_IN_MS = 0.278
    M_IN_CM = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        calories = ((self.KOEF_1 * self.weight + ((self.get_mean_speed()
                     * self.KMH_IN_MS)**2 / (self.height / self.M_IN_CM))
                     * self.KOEF_2 * self.weight)
                    * (self.duration * self.H_IN_M))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    KOEF_3 = 1.1
    KOEF_4 = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        avg_speed = (self.length_pool * self.count_pool
                     / self.M_IN_KM / self.duration)
        return avg_speed

    def get_spent_calories(self):
        calories = ((self.get_mean_speed() + self.KOEF_3)
                    * self.KOEF_4 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    type_list = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in type_list:
        return type_list[workout_type](*data)


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
