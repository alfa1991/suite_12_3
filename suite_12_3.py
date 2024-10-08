import unittest

class Runner:
    def __init__(self, name, speed=5):
        """
        Инициализация объекта Runner (бегун).

        :param name: Имя бегуна.
        :param speed: Скорость бегуна (по умолчанию 5).
        """
        self.name = name  # Имя бегуна
        self.distance = 0  # Начальная дистанция
        self.speed = speed  # Скорость бегуна

    def run(self):
        """Метод для имитации бега, увеличивает дистанцию бегуна."""
        self.distance += self.speed * 2  # Увеличиваем дистанцию в два раза за "шаг"

    def walk(self):
        """Метод для имитации ходьбы, увеличивает дистанцию бегуна на его скорость."""
        self.distance += self.speed

    def __str__(self):
        """Возвращает строковое представление бегуна (его имя)."""
        return self.name

    def __eq__(self, other):
        """
        Сравнение бегуна с другим объектом.

        :param other: Объект для сравнения (может быть строкой или другим бегуном).
        :return: True, если имена равны, иначе False.
        """
        if isinstance(other, str):
            return self.name == other  # Сравниваем с именем
        elif isinstance(other, Runner):
            return self.name == other.name  # Сравниваем с другим бегуном


class Tournament:
    def __init__(self, distance, *participants):
        """
        Инициализация объекта Tournament (турнир).

        :param distance: Полная дистанция турнира.
        :param participants: Участники турнира.
        """
        self.full_distance = distance  # Полная дистанция турнира
        self.participants = list(participants)  # Список участников

    def start(self):
        """Запускает турнир и возвращает результаты."""
        finishers = {}  # Словарь для хранения финишировавших
        place = 1  # Начальное место

        # Пока есть участники
        while self.participants:
            for participant in self.participants[:]:  # Используем копию списка участников
                participant.run()  # Каждый участник пробегает "шаг"
                if participant.distance >= self.full_distance:  # Проверяем, достиг ли участник финиша
                    if place not in finishers:  # Если место еще не занято
                        finishers[place] = participant  # Сохраняем участника
                        place += 1  # Увеличиваем место
                        self.participants.remove(participant)  # Убираем финишировавшего участника

        return finishers  # Возвращаем словарь с результатами

    def display_results(self, finishers):
        """Отображает результаты турнира."""
        print("Результаты турнира:")
        for place, runner in sorted(finishers.items()):
            print(f"{place} место: {runner.name} на дистанции {runner.distance}")


class RunnerTest(unittest.TestCase):
    is_frozen = False  # По умолчанию тесты выполняются

    def test_runner_initialization(self):
        """Тестируем инициализацию бегуна."""
        runner = Runner("Бегун 1")
        self.assertEqual(runner.name, "Бегун 1")  # Проверяем имя
        self.assertEqual(runner.distance, 0)  # Проверяем начальную дистанцию
        self.assertEqual(runner.speed, 5)  # Проверяем скорость

    def test_runner_run(self):
        """Тестируем метод бега."""
        runner = Runner("Бегун 1", speed=5)
        runner.run()  # Выполняем бег
        self.assertEqual(runner.distance, 10)  # Проверяем новую дистанцию

    def test_runner_walk(self):
        """Тестируем метод ходьбы."""
        runner = Runner("Бегун 1", speed=5)
        runner.walk()  # Выполняем ходьбу
        self.assertEqual(runner.distance, 5)  # Проверяем новую дистанцию


class TournamentTest(unittest.TestCase):
    is_frozen = True  # Тесты пропускаются по умолчанию

    def test_tournament_start(self):
        """Тестируем старт турнира."""
        runner1 = Runner("Бегун 1", speed=6)
        runner2 = Runner("Бегун 2", speed=5)
        tournament = Tournament(20, runner1, runner2)  # Создаем турнир
        results = tournament.start()  # Запускаем турнир
        self.assertIn(1, results)  # Проверяем, что первое место занято

    def test_display_results(self):
        """Тестируем отображение результатов турнира."""
        runner1 = Runner("Бегун 1", speed=6)
        runner2 = Runner("Бегун 2", speed=5)
        tournament = Tournament(20, runner1, runner2)  # Создаем турнир
        results = tournament.start()  # Запускаем турнир
        tournament.display_results(results)  # Отображаем результаты


def skip_if_frozen(test_func):
    """Декоратор для пропуска тестов, если is_frozen = True."""
    def wrapper(self, *args, **kwargs):
        if getattr(self, 'is_frozen', False):
            self.skipTest('Тесты в этом кейсе заморожены')  # Пропускаем тест
        return test_func(self, *args, **kwargs)  # Выполняем тест
    return wrapper

# Применение декоратора к тестам
for method_name in dir(RunnerTest):
    if method_name.startswith('test_'):
        method = getattr(RunnerTest, method_name)
        setattr(RunnerTest, method_name, skip_if_frozen(method))

for method_name in dir(TournamentTest):
    if method_name.startswith('test_'):
        method = getattr(TournamentTest, method_name)
        setattr(TournamentTest, method_name, skip_if_frozen(method))

# Создание TestSuite и запуск тестов
if __name__ == '__main__':
    suite = unittest.TestSuite()  # Создаем экземпляр TestSuite
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))  # Добавляем тесты RunnerTest
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))  # Добавляем тесты TournamentTest

    runner = unittest.TextTestRunner(verbosity=2)  # Создаем тестовый раннер с verbosity=2
    runner.run(suite)  # Запускаем тесты
