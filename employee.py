class Employee:
    """
    Класс, представляющий сотрудника компании.

    Атрибуты:
        name (str): Полное имя сотрудника.
        position (str): Должность сотрудника.
        salary (float): Месячный оклад сотрудника.
        hours_worked (float): Общее количество отработанных часов в текущем расчетном периоде.
        project (str): Название проекта, над которым работает сотрудник.

    Методы:
        add_hours(hours): Добавляет отработанные часы.
        calculate_pay(): Рассчитывает заработную плату на основе отработанных часов.
        assign_project(project_name): Назначает сотрудника на проект.
        reset_hours(): Обнуляет счетчик отработанных часов (например, после выплаты).
        get_info(): Возвращает базовую информацию о сотруднике.
    """

    def __init__(self, name: str, position: str, salary: float) -> None:
        """
        Конструктор для создания экземпляра класса Employee.

        Параметры:
            self: Экземпляр класса Employee. (Объяснение: `self` - это ссылка на текущий экземпляр объекта.
                   Через него мы обращаемся к атрибутам и методам этого объекта.)
            name (str): Полное имя сотрудника.
            position (str): Должность сотрудника.
            salary (float): Месячный оклад сотрудника. Должен быть положительным числом.

        Исключения:
            ValueError: Если salary <= 0.
        """
        self.name = name
        self.position = position
        if salary <= 0:
            raise ValueError("Зарплата должна быть положительным числом.")
        self.salary = salary
        self.hours_worked = 0.0
        self.project = "Не назначен"

    def add_hours(self, hours: float) -> None:
        """
        Добавляет отработанные часы к общему счетчику сотрудника.

        Параметры:
            self: Экземпляр класса Employee.
            hours: Количество часов для добавления. Должно быть положительным.

        Исключения:
            ValueError: Если hours <= 0.
        """
        if hours <= 0:
            raise ValueError("Количество часов должно быть положительным.")
        self.hours_worked += hours
        print(f"Сотруднику {self.name} добавлено {hours} часов. Всего: {self.hours_worked}")

    def calculate_pay(self) -> float:
        """
        Рассчитывает заработную плату на основе отработанных часов.
        Формула: (месячный оклад / 160) * отработанные часы.

        Параметр:
            self: Экземпляр класса Employee.

        Возвращает:
            float: Сумма к выплате.
        """
        hourly_rate = self.salary / 160
        pay = hourly_rate * self.hours_worked
        return round(pay, 2)  # Округляем до копеек

    def assign_project(self, project_name: str) -> None:
        """
        Назначает или изменяет проект сотрудника.

        Параметры:
            self: Экземпляр класса Employee.
            project_name (str): Название проекта.
        """
        old_project = self.project
        self.project = project_name
        print(f"Сотрудник {self.name} переведен с проекта '{old_project}' на проект '{self.project}'.")
