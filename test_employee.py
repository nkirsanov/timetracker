import unittest
from employee import Employee

class TestEmployeeQuick(unittest.TestCase):
    """Тесты для класса Employee"""
    
    def test_initialization_and_basic_methods(self):
        """Тест 1: Проверка создания сотрудника и базовых методов"""
        emp = Employee("Иван Иванов", "Программист", 100000)
        
        self.assertEqual(emp.name, "Иван Иванов")
        self.assertEqual(emp.position, "Программист")
        self.assertEqual(emp.salary, 100000)
        self.assertEqual(emp.hours_worked, 0)
        self.assertEqual(emp.project, "Не назначен")
        
        emp.add_hours(160)
        self.assertEqual(emp.hours_worked, 160)
        self.assertEqual(emp.calculate_pay(), 100000)
        
        # Проверка на отрицательные часы
        with self.assertRaises(ValueError):
            emp.add_hours(-50)
        
        # Проверка что часы не изменились
        self.assertEqual(emp.hours_worked, 160)
        
        # Назначаем проект
        emp.assign_project("Веб-сайт компании")
        self.assertEqual(emp.project, "Веб-сайт компании")
    
    def test_invalid_salary(self):
        """Тест 2: Проверка валидации зарплаты"""
        with self.assertRaises(ValueError):
            Employee("Тест", "Должность", -10000)
        
        with self.assertRaises(ValueError):
            Employee("Тест", "Должность", 0)
    

if __name__ == "__main__":
    unittest.main()