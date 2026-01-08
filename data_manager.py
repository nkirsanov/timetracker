import pandas as pd
import os
import re


class DataManager:
    """
    Менеджер данных для работы с CSV файлами и сотрудниками.

    Этот класс предоставляет функционал для сохранения, загрузки
    и обработки данных сотрудников в формате CSV.

    Атрибуты:
        data_folder (str): Путь к папке для хранения данных.
        employees_file (str): Полный путь к файлу с данными сотрудников.
    """

    def __init__(self, data_folder: str = "data") -> None:
        """
        Инициализирует менеджер данных.

        Создает папку для хранения данных если она не существует
        и определяет путь к файлу сотрудников.

        Параметры:
            data_folder (str, optional): Название папки для хранения данных.
                По умолчанию "data".

        Пример:
            >>> dm = DataManager("company_data")
            >>> print(dm.data_folder)
            company_data
        """
        self.data_folder = data_folder
        os.makedirs(data_folder, exist_ok=True)
        self.employees_file = os.path.join(data_folder, "employees.csv")

    def save_employees(self, employees: list) -> bool:
        """
        Сохраняет список сотрудников в CSV файл.

        Преобразует объекты Employee в словари, создает DataFrame
        и сохраняет его в CSV файл с указанной кодировкой.

        Параметры:
            employees (list): Список объектов Employee для сохранения.

        Возвращает:
            bool: True если сохранение прошло успешно.

        Исключения:
            AttributeError: Если объект в списке не имеет ожидаемых атрибутов.
            IOError: Если не удалось записать файл.

        Пример:
            >>> employees = [emp1, emp2]
            >>> dm.save_employees(employees)
            True
        """
        data = []
        for emp in employees:
            data.append({
                'Имя': emp.name,
                'Должность': emp.position,
                'Зарплата': emp.salary,
                'Часы': emp.hours_worked,
                'К_выплате': emp.calculate_pay(),
                'Проект': emp.project if hasattr(emp, 'project') else ""
            })

        df = pd.DataFrame(data)
        df.to_csv(self.employees_file, index=False, encoding='utf-8')
        return True

    def load_employees(self) -> list:
        """
        Загружает сотрудников из CSV файла.

        Читает CSV файл, преобразует строки в объекты Employee
        и восстанавливает их состояние (часы, проект и т.д.).

        Возвращает:
            list: Список объектов Employee. Если файл не существует
                  или произошла ошибка, возвращает пустой список.

        Исключения:
            FileNotFoundError: Если файл не существует.
            ValueError: Если данные в CSV некорректны.

        """
        from employee import Employee

        if not os.path.exists(self.employees_file):
            return []

        try:
            df = pd.read_csv(self.employees_file)
            employees = []

            for _, row in df.iterrows():
                emp = Employee(
                    name=str(row['Имя']),
                    position=str(row['Должность']),
                    salary=float(row['Зарплата'])
                )
                emp.hours_worked = float(row['Часы'])

                # Загружаем проект если есть в CSV
                if 'Проект' in df.columns:
                    emp.project = str(row['Проект'])

                employees.append(emp)

            return employees
        except Exception as e:
            print(f"Ошибка загрузки сотрудников: {e}")
            return []

    def read_csv_to_df(self, file_path: str) -> pd.DataFrame:
        """
        Читает CSV файл и возвращает DataFrame без пустых строк.

        Универсальный метод для чтения любых CSV файлов.
        Автоматически удаляет строки с отсутствующими значениями.

        Параметры:
            file_path (str): Путь к CSV файлу для чтения.

        Возвращает:
            pandas.DataFrame: DataFrame с данными из файла.
            Если файл не существует или произошла ошибка чтения,
            возвращает пустой DataFrame.

        """
        try:
            df = pd.read_csv(file_path)
            return df.dropna()
        except Exception:
            return pd.DataFrame()