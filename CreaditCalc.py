import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror
import csv

class CreditCalculator:
    def __init__(self, master):
        self.master = master
        self.width = 1100
        self.height = 500
        self.master.geometry(str(self.width) + 'x' + str(self.height))
        self.master.title('Кредитный калькулятор')
        
        # Инициализация переменных
        self.radioStatus1 = tk.StringVar(value='Аннуитентный')
        self.radioStatus = tk.StringVar(value='Уменьшить платеж')
        self.status = tk.IntVar(value=0)
        
        
        self.createLabelsAndFields()
        
        self.master.bind('<Return>', lambda e: self.gettingInformation())
        self.master.bind('<Delete>', lambda e: self.restart())

    def createLabelsAndFields(self):
        x = 10
        y = 10
        self.x = x
        self.main = ttk.Frame(self.master, width=1000, height=500)

        self.creditSumL = ttk.Label(text="Сумма кредита")
        self.creditSumL.grid(row=0, column=0, sticky='w', padx=x)
        self.creditSumF = ttk.Entry(width=30)
        self.creditSumF.grid(row=1, column=0, padx=x, sticky='w')
        ttk.Label(text='руб.').grid(row=1, column=1, sticky='w')

        self.creditPerL = ttk.Label(text="Процент")
        self.creditPerL.grid(row=2, column=0, sticky='w', padx=x)
        self.creditPerF = ttk.Entry(width=30)
        self.creditPerF.grid(row=3, column=0, padx=x, sticky='w')
        ttk.Label(text='%').grid(row=3, column=1, sticky='w')

        self.creditTermL = ttk.Label(text="Срок")
        self.creditTermL.grid(row=2, column=2, sticky='w', padx=x)
        self.creditTermF = ttk.Entry(width=10)
        self.creditTermF.grid(row=3, column=2, padx=x, sticky='w')
        ttk.Label(text='мес.').grid(row=3, column=3, sticky='w')

        n = 1
        for i in ['Аннуитентный', 'Дифференцированный']:
            ttk.Radiobutton(text=i, variable=self.radioStatus1, value=i).grid(row=3+n, column=0, sticky='w', pady=5, padx=10)
            n += 1

        self.checkB = ttk.Checkbutton(text='Дополнительные функции', variable=self.status, command=self.flagChanged)
        self.checkB.grid(row=6, column=0, sticky='w', padx=x, pady=y)

        ttk.Button(text='Рассчитать', command=self.gettingInformation).grid(row=50, column=0, columnspan=4)
        ttk.Button(text='Сброс', command=self.restart).grid(row=50, column=1, columnspan=4)

        self.togleFrame = ttk.Frame(self.master)
        self.togleFrame.grid(row=7, column=0, padx=x, pady=y, sticky='w')
        self.togleFrame.grid_forget()

    def flagChanged(self):
        if self.status.get() == 1:
            self.togleFrame.grid(columnspan=4, row=7, column=0, pady=10, sticky='w')
            ttk.Label(self.togleFrame, text='Досрочное погашение').grid(row=0, column=0, sticky='w')

            self.earlyPaySumL = ttk.Label(self.togleFrame, text='Сумма досрочного погашения')
            self.earlyPaySumL.grid(row=1, column=0, sticky='w', padx=self.x)
            self.earlyPaySumF = ttk.Entry(self.togleFrame, width=30)
            self.earlyPaySumF.grid(row=2, column=0, sticky='w', padx=self.x)
            ttk.Label(self.togleFrame, text='руб.').grid(row=2, column=1, sticky='w')

            self.periodL = ttk.Label(self.togleFrame, text='Периодичность')
            self.periodL.grid(row=3, column=0, sticky='w', padx=self.x)
            self.variants = ['Каждый месяц','Каждые 2 месяца','Каждые полгода','Каждый год']
            self.periodVar = tk.StringVar()
            self.periodS = ttk.Combobox(self.togleFrame, textvariable=self.periodVar, values=self.variants)
            self.periodS.current(0)
            self.periodS.grid(row=4, column=0, sticky='w', padx=self.x)

            self.beginL = ttk.Label(self.togleFrame, text='Начиная с')
            self.beginL.grid(row=3, column=2, sticky='w', padx=self.x)
            self.beginF = ttk.Entry(self.togleFrame, width=10)
            self.beginF.grid(row=4, column=2, sticky='w', padx=self.x)
            ttk.Label(self.togleFrame, text='мес.').grid(row=4, column=3, sticky='w')

            n = 1
            self.selectFrame = ttk.Frame(self.togleFrame)
            self.selectFrame.grid(row=5, column=0, sticky='w')
            ttk.Label(self.selectFrame, text="Стратегия").grid(row=0, column=0, sticky='w', pady=10, columnspan=4)
            for i in ['Уменьшить платеж', 'Уменьшить срок']:
                ttk.Radiobutton(self.selectFrame, text=i, variable=self.radioStatus, value=i).grid(row=n, column=0, sticky='w', pady=5, padx=10)
                n += 1
        else:
            self.togleFrame.grid_forget()

    def gettingInformation(self):
        try:
            self.creditSum = float(self.creditSumF.get())
            self.creditPer = float(self.creditPerF.get()) / 1200  # Месячная ставка
            self.creditTerm = int(self.creditTermF.get())
            
            if self.status.get() == 1:
                self.earlyPaySum = float(self.earlyPaySumF.get())
                self.begin = int(self.beginF.get())
                self.period = self.getPeriodValue()
            else:
                self.earlyPaySum = 0
                self.begin = self.creditTerm + 1  # Чтобы не срабатывало
                self.period = 1

            self.calculation()

        except ValueError:
            showerror('Ошибка', 'Проверьте правильность введенных данных')
        except ZeroDivisionError:
            showerror('Ошибка', 'Некорректные параметры кредита')

    def getPeriodValue(self):
        if self.periodS.get() == self.variants[0]: return 1
        if self.periodS.get() == self.variants[1]: return 2
        if self.periodS.get() == self.variants[2]: return 6
        if self.periodS.get() == self.variants[3]: return 12
        return 1

    def calculation(self):
        sp = []
        self.over = 0
        self.ost = self.creditSum
        
        if self.radioStatus1.get() == 'Аннуитентный':
            self.payment = (self.creditSum * self.creditPer * (1 + self.creditPer)**self.creditTerm) / ((1 + self.creditPer)**self.creditTerm - 1)
            
            for i in range(1, self.creditTerm + 1):
                if self.ost <= 0: break
                    
                self.percents = self.ost * self.creditPer
                self.dolg = self.payment - self.percents
                self.d = 0

                # Проверяем нужно ли делать досрочный платеж
                if (self.status.get() == 1 and 
                    i >= self.begin and 
                    (i - self.begin) % self.period == 0):
                    self.d = self.earlyPaySum
                    
                    if self.radioStatus.get() == 'Уменьшить платеж':
                        # Пересчитываем платеж
                        remaining_term = self.creditTerm - i
                        self.payment = (self.ost - self.d) * self.creditPer * (1 + self.creditPer)**remaining_term / ((1 + self.creditPer)**remaining_term - 1)
                        self.dolg = self.payment - self.percents

                # Корректируем последний платеж
                if self.ost < self.dolg + self.d:
                    self.dolg = self.ost
                    self.d = 0

                total_payment = self.dolg + self.percents + self.d
                self.ost -= self.dolg + self.d
                self.over += self.percents

                if self.ost < 0.01:  # Убираем копейки
                    self.ost = 0

                sp.append((
                    i,
                    round(total_payment, 2),
                    round(self.percents, 2),
                    round(self.dolg, 2),
                    round(self.d, 2),
                    round(self.ost, 2)
                ))

        elif self.radioStatus1.get() == 'Дифференцированный':
            base_payment = self.creditSum / self.creditTerm
            
            for i in range(1, self.creditTerm + 1):
                if self.ost <= 0: break
                    
                self.percents = self.ost * self.creditPer
                self.dolg = base_payment
                self.d = 0

                # Проверяем нужно ли делать досрочный платеж
                if (self.status.get() == 1 and 
                    i >= self.begin and 
                    (i - self.begin) % self.period == 0):
                    self.d = self.earlyPaySum
                    
                    if self.radioStatus.get() == 'Уменьшить срок':
                        self.dolg += self.d / (self.creditTerm - i + 1)

                # Корректируем последний платеж
                if self.ost < self.dolg + self.d:
                    self.dolg = self.ost
                    self.d = 0

                total_payment = self.dolg + self.percents + self.d
                self.ost -= self.dolg + self.d
                self.over += self.percents

                if self.ost < 0.01:  # Убираем копейки
                    self.ost = 0

                sp.append((
                    i,
                    round(total_payment, 2),
                    round(self.percents, 2),
                    round(self.dolg, 2),
                    round(self.d, 2),
                    round(self.ost, 2)
                ))
               
                

        self.tabCreate(sp=sp)

    def tabCreate(self, sp):
        if hasattr(self, 'infoFrame'):
            self.infoFrame.destroy()
            
        self.infoFrame = ttk.Frame(self.master, width=500, height=600, borderwidth=1, relief='solid')
        self.infoFrame.grid(row=0, column=8, rowspan=50)
        
        ttk.Label(self.infoFrame, text='ВЫВОД').grid(row=0, column=0, pady=10)
        ttk.Label(self.infoFrame, text=f'Переплата: {round(self.over, 2)}').grid(row=0, column=1, pady=10)
        
        columns = ('month', 'payment', 'percent', 'dolg', 'early', 'ost')
        self.table = ttk.Treeview(self.infoFrame, columns=columns, show='headings')
        
        self.table.heading('month', text='Месяц')
        self.table.heading('payment', text='Платеж')
        self.table.heading('percent', text='Процент')
        self.table.heading('dolg', text='Долг')
        self.table.heading('early', text='Досрочное погашение')
        self.table.heading('ost', text='Остаток')

        self.table.column("#1", stretch='no', width=50)
        self.table.column("#2", stretch='no', width=100)
        self.table.column("#3", stretch='no', width=100)
        self.table.column("#4", stretch='no', width=100)
        self.table.column("#5", stretch='no', width=150)
        self.table.column("#6", stretch='no', width=100)

        for i in sp:
            self.table.insert('', tk.END, values=i)

        scrollbar = ttk.Scrollbar(self.infoFrame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=1, column=1, sticky='nsew')
        scrollbar.grid(row=1, column=0, sticky='ns')
        
        ttk.Button(self.infoFrame, text='Сохранить', command=self.save_to_txt).grid(row=2, column=0)
        
        
        self.infoFrame.grid_rowconfigure(1, weight=1)
        self.infoFrame.grid_columnconfigure(1, weight=1)

    def restart(self):
        self.creditSumF.delete(0, tk.END)
        self.creditPerF.delete(0, tk.END)
        self.creditTermF.delete(0, tk.END)
        
        if self.status.get() == 1:
            self.earlyPaySumF.delete(0, tk.END)
            self.beginF.delete(0, tk.END)
            self.periodS.set('')
        
        if hasattr(self, 'infoFrame'):
            self.infoFrame.destroy()

    def save_to_txt(self):
        headers = [self.table.heading(col)['text'] for col in self.table['columns']]
        all_items = self.table.get_children()
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
        )
        
        if filepath:
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(headers)
                for item in all_items:
                    writer.writerow([self.table.set(item, col) for col in self.table['columns']])

window = tk.Tk()
app = CreditCalculator(window)
window.mainloop()