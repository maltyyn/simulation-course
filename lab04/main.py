import tkinter as tk
from tkinter import messagebox
import random
import statistics

# Алгоритм из лекц
class BasicRNG:
    def __init__(self, seed):
        self.state = seed
        self.m = 2 ** 31 - 1  # Модуль, число Мерсена
        self.a = 1103515245  # Множитель Халла-Добелла
        self.c = 12345 #Приращение 0

    def random(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m

def autocorrelation(data, lag):
    n = len(data)
    if lag >= n:
        return 0
    mean = statistics.mean(data)
    numerator = sum((data[i] - mean) * (data[i+lag] - mean) for i in range(n - lag))
    denominator = sum((x - mean) ** 2 for x in data)
    if denominator == 0:
        return 0
    return numerator / denominator


def run_simulation():
    try:
        seed_val = int(entry_seed.get())
        n_val = int(entry_n.get())

        if n_val <= 0:
            raise ValueError

        my_rng = BasicRNG(seed_val)

        sample_custom = [my_rng.random() for _ in range(n_val)]
        sample_builtin = [random.random() for _ in range(n_val)]

        m_custom = statistics.mean(sample_custom)
        v_custom = statistics.variance(sample_custom)
        m_builtin  = statistics.mean(sample_builtin)
        v_builtin = statistics.variance(sample_builtin)

        auto_custom_1 = autocorrelation(sample_custom, 1)
        auto_custom_2 = autocorrelation(sample_custom, 2)
        auto_custom_3 = autocorrelation(sample_custom, 3)

        auto_builtin_1 = autocorrelation(sample_builtin, 1)
        auto_builtin_2 = autocorrelation(sample_builtin, 2)
        auto_builtin_3 = autocorrelation(sample_builtin, 3)

        m_theo, v_theo = 0.5, 1 / 12

        res_text = (
             f"Теория: Ср={m_theo:.4f}, Дисп={v_theo:.4f}\n"
            f"--------------------------------------\n"
            f"Мой датчик: Ср={m_custom:.4f}, Дисп={v_custom:.4f}\n"
            f"Встроенный: Ср={m_builtin:.4f}, Дисп={v_builtin:.4f}\n\n"
            f"Автокорреляция (мой датчик, лаги 1-3): {auto_custom_1:.4f}, {auto_custom_2:.4f}, {auto_custom_3:.4f}\n"
            f"Автокорреляция (встроенный, лаги 1-3):   {auto_builtin_1:.4f}, {auto_builtin_2:.4f}, {auto_builtin_3:.4f}"
        )

        label_result.config(text=res_text)

    except ValueError:
        messagebox.showerror("Ошибка", "Требуются числа > 0")

root = tk.Tk()
root.geometry("400x400")

tk.Label(root, text="Сид:").pack(pady=5)
entry_seed = tk.Entry(root)
entry_seed.insert(0, "42")
entry_seed.pack()

tk.Label(root, text="Размер выборки:").pack(pady=5)
entry_n = tk.Entry(root)
entry_n.insert(0, "100000")
entry_n.pack()

tk.Button(root, text="Расчет", command=run_simulation).pack(pady=20)

label_result = tk.Label(root, justify="left")
label_result.pack()

root.mainloop()