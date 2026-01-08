import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_manager import DataManager
from analysis import ChartBuilder
import os

class TimeTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет времени")
        self.root.geometry("1000x950")
        
        self.data = DataManager()
        self.employees = self.data.load_employees()

        # Список проектов
        self.projects = [
            "Веб-сайт компании",
            "Мобильное приложение",
            "База данных",
            "Аналитика",
            "Тестирование",
            "Администрирование"
        ]

        if not self.employees:
            self.create_example()

        self.current_selection = 0
        self.setup_ui()

        if self.employees:
            self.listbox.selection_set(0)
            self.on_select(None)

    def create_example(self):
        from employee import Employee
        self.employees = [
            Employee("Иван", "Программист", 100000),
            Employee("Мария", "Дизайнер", 80000),
            Employee("Алексей", "Тестировщик", 70000)
        ]
        self.employees[0].add_hours(160)
        self.employees[0].project = "Веб-сайт компании"
        self.employees[1].add_hours(120)
        self.employees[1].project = "Мобильное приложение"
        self.employees[2].add_hours(140)
        self.employees[2].project = "Тестирование"

    def setup_ui(self):
        # Основной контейнер
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        tk.Label(content_frame, text="Учет времени", font=('Arial', 14, 'bold')).pack(pady=10)

        # Список сотрудников
        tk.Label(content_frame, text="Список сотрудников:").pack(anchor='w', padx=15)

        list_frame = tk.Frame(content_frame)
        list_frame.pack(fill=tk.X, padx=20, pady=5)

        self.listbox = tk.Listbox(list_frame, height=6,
                                 selectbackground='lightblue', selectmode=tk.SINGLE,
                                 exportselection=False)
        list_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=list_scrollbar.set)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.update_list()

        # Форма редактирования
        form_frame = tk.LabelFrame(content_frame, text="Редактирование сотрудника", padx=15, pady=15)
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Имя
        tk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        # Должность
        tk.Label(form_frame, text="Должность:").grid(row=1, column=0, sticky='w', pady=5)
        self.position_entry = tk.Entry(form_frame, width=30)
        self.position_entry.grid(row=1, column=1, pady=5, padx=5)

        # Зарплата
        tk.Label(form_frame, text="Зарплата:").grid(row=2, column=0, sticky='w', pady=5)
        self.salary_entry = tk.Entry(form_frame, width=30)
        self.salary_entry.grid(row=2, column=1, pady=5, padx=5)

        # Проект
        tk.Label(form_frame, text="Проект:").grid(row=3, column=0, sticky='w', pady=5)
        self.project_combo = ttk.Combobox(form_frame, values=self.projects, width=27, state='readonly')
        self.project_combo.grid(row=3, column=1, pady=5, padx=5)
        self.project_combo.bind('<FocusIn>', self.preserve_selection)
        self.project_combo.bind('<FocusOut>', self.preserve_selection)

        # Часы
        tk.Label(form_frame, text="Добавить часов:").grid(row=4, column=0, sticky='w', pady=5)
        self.hours_entry = tk.Entry(form_frame, width=30)
        self.hours_entry.grid(row=4, column=1, pady=5, padx=5)
        self.hours_entry.insert(0, "8")

        # Кнопки управления сотрудником и данные - ВСЕ В ОДНОМ РЯДУ
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        # Кнопки управления сотрудником
        tk.Button(btn_frame, text="Сохранить", command=self.save_employee, width=12,
                 bg='green', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Добавить часы", command=self.add_hours, width=12,
                 bg='blue', fg='white').pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Удалить", command=self.delete_employee, width=12,
                 bg='red', fg='white').pack(side=tk.LEFT, padx=2)
        
        # Кнопка "Очистить все" тоже в том же ряду
        tk.Button(btn_frame, text="Очистить все", command=self.clear_data,
                 bg='darkred', fg='white', width=12).pack(side=tk.LEFT, padx=2)

        # Новый сотрудник
        new_frame = tk.LabelFrame(content_frame, text="Новый сотрудник", padx=15, pady=15)
        new_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(new_frame, text="Имя:").pack(side=tk.LEFT, padx=5)
        self.new_name = tk.Entry(new_frame, width=15)
        self.new_name.pack(side=tk.LEFT, padx=5)

        tk.Label(new_frame, text="Должность:").pack(side=tk.LEFT, padx=5)
        self.new_position = tk.Entry(new_frame, width=15)
        self.new_position.pack(side=tk.LEFT, padx=5)
        self.new_position.insert(0, "")

        tk.Label(new_frame, text="Зарплата:").pack(side=tk.LEFT, padx=5)
        self.new_salary = tk.Entry(new_frame, width=10)
        self.new_salary.pack(side=tk.LEFT, padx=5)
        self.new_salary.insert(0, "100000")

        tk.Label(new_frame, text="Проект:").pack(side=tk.LEFT, padx=5)
        self.new_project_combo = ttk.Combobox(new_frame, values=self.projects, width=13, state='readonly')
        self.new_project_combo.pack(side=tk.LEFT, padx=5)

        tk.Button(new_frame, text="Добавить", command=self.add_employee,
                 bg='darkgreen', fg='white').pack(side=tk.LEFT, padx=10)

        # График
        graph_frame = tk.LabelFrame(content_frame, text="Статистика", padx=15, pady=15)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.graph_area = tk.Frame(graph_frame)
        self.graph_area.pack(fill=tk.BOTH, expand=True)

        self.show_chart()

    def preserve_selection(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            self.current_selection = selection[0]

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for emp in self.employees:
            project_info = f" ({emp.project})" if hasattr(emp, 'project') and emp.project else ""
            self.listbox.insert(tk.END, f"{emp.name} - {emp.position}{project_info}")

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            if self.employees and hasattr(self, 'current_selection'):
                try:
                    self.listbox.selection_set(self.current_selection)
                    selection = (self.current_selection,)
                except:
                    if self.employees:
                        self.listbox.selection_set(0)
                        selection = (0,)

        if not selection:
            return

        self.current_selection = selection[0]
        emp = self.employees[selection[0]]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, emp.name)

        self.position_entry.delete(0, tk.END)
        self.position_entry.insert(0, emp.position)

        self.salary_entry.delete(0, tk.END)
        self.salary_entry.insert(0, str(emp.salary))

        if hasattr(emp, 'project') and emp.project:
            self.project_combo.set(emp.project)
        else:
            self.project_combo.set("")

    def save_employee(self):
        selection = self.listbox.curselection()
        if not selection:
            if hasattr(self, 'current_selection') and self.current_selection < len(self.employees):
                self.listbox.selection_set(self.current_selection)
                selection = (self.current_selection,)

        if not selection:
            messagebox.showwarning("Ошибка", "Выберите сотрудника")
            return

        emp = self.employees[selection[0]]

        emp.name = self.name_entry.get()
        emp.position = self.position_entry.get()

        try:
            emp.salary = float(self.salary_entry.get())
        except:
            messagebox.showerror("Ошибка", "Неправильная зарплата")
            return

        emp.project = self.project_combo.get()

        self.update_list()
        self.show_chart()
        
        try:
            self.data.save_employees(self.employees)
            messagebox.showinfo("Успех", "Изменения сохранены и данные записаны в файл")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные в файл: {e}")

    def add_hours(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите сотрудника")
            return

        try:
            hours = float(self.hours_entry.get())
        except:
            messagebox.showerror("Ошибка", "Введите число часов")
            return

        emp = self.employees[selection[0]]
        emp.add_hours(hours)

        self.update_list()
        self.show_chart()
        messagebox.showinfo("Успех", f"Добавлено {hours} часов")

    def delete_employee(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите сотрудника")
            return

        emp = self.employees[selection[0]]
        if messagebox.askyesno("Удалить", f"Удалить сотрудника {emp.name}?"):
            self.employees.pop(selection[0])
            self.update_list()
            self.show_chart()
            
            try:
                self.data.save_employees(self.employees)
            except:
                pass

    def add_employee(self):
        name = self.new_name.get().strip()
        position = self.new_position.get().strip()

        try:
            salary = float(self.new_salary.get())
        except:
            messagebox.showerror("Ошибка", "Неправильная зарплата")
            return

        if not name:
            messagebox.showerror("Ошибка", "Введите имя")
            return

        from employee import Employee
        emp = Employee(name, position, salary)

        project = self.new_project_combo.get()
        if project:
            emp.project = project

        self.employees.append(emp)

        self.update_list()
        self.new_name.delete(0, tk.END)
        self.new_position.delete(0, tk.END)
        self.new_position.insert(0, "Сотрудник")
        self.new_salary.delete(0, tk.END)
        self.new_salary.insert(0, "100000")
        self.new_project_combo.set("")
        
        try:
            self.data.save_employees(self.employees)
        except:
            pass

    def show_chart(self):
        """Используем ChartBuilder из analysis.py для создания графиков"""
        for widget in self.graph_area.winfo_children():
            widget.destroy()

        if not self.employees:
            tk.Label(self.graph_area, text="Нет данных для отображения графика").pack(pady=50)
            return

        # Используем ChartBuilder для создания графика
        fig = ChartBuilder.create_payment_chart(self.employees)
        
        canvas = FigureCanvasTkAgg(fig, self.graph_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_data(self):
        if messagebox.askyesno("Очистить", "Удалить все данные?"):
            self.employees = []
            self.update_list()
            self.show_chart()
            
            try:
                if os.path.exists(self.data.employees_file):
                    os.remove(self.data.employees_file)
            except:
                pass
