import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class ChartBuilder:
    @staticmethod
    def create_payment_chart(employees):
        """График зарплат"""
        
        if not employees:
            raise ValueError("Список сотрудников пуст")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        fig.tight_layout(pad=5.0)
        
        names = [e.name for e in employees]
        payments = [e.calculate_pay() for e in employees]
        hours = [e.hours_worked for e in employees]
        
        colors = ['lightblue', 'lightgreen', 'lightcoral', 
                  'lightsalmon', 'lightseagreen', 'plum', 'gold']
        
        bar_colors = colors[:len(names)]

        # График 1: Зарплата к выплате
        bars = ax1.bar(names, payments, color=bar_colors, width=0.6)
        ax1.set_title('Зарплата к выплате', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Руб.', fontsize=10)
        ax1.set_xticklabels([])
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Имена внутри столбцов (вертикально)
        for i, (bar, name) in enumerate(zip(bars, names)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height * 0.1,
                    name,
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    rotation=90, color='black')
            
            # Значение зарплаты сверху столбца
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}'.replace(',', ' '),
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

        if payments:
            ax1.set_ylim(0, max(payments) * 1.15)

        # График 2: Часы работы
        bars2 = ax2.bar(names, hours, color=bar_colors, alpha=0.7, width=0.6)
        ax2.set_title('Часы работы', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Часы', fontsize=10)
        ax2.set_xticklabels([])
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        for i, (bar, name) in enumerate(zip(bars2, names)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height * 0.1,
                    name,
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    rotation=90, color='black')
            
            # Значение часов сверху столбца
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    str(int(hours[i])),
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

        if hours:
            ax2.set_ylim(0, max(hours) * 1.15)

        plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15, wspace=0.3)
        
        return fig
