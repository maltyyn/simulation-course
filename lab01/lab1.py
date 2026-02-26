import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

inputs = {}
root = tk.Tk()
root.geometry("1200x700")

fields = [("Высота, м", "h", 0),
          ("Скорость, м/с", "v", 20),
          ("Угол, град", "a", 45),
          ("Сопротивление k", "k", 0.1),
          ("Шаг dt, с", "dt", 0.1)]
panel = tk.Frame(root)
panel.pack(side="left", padx=10, fill="y")

for i, (label, key, val) in enumerate(fields):
    tk.Label(panel, text=label).grid(row=i, column=0, sticky="w")
    inputs[key] = tk.DoubleVar(value=val)
    tk.Entry(panel, textvariable=inputs[key], width=10).grid(row=i, column=1, pady=2)

def run_sim(compare=False):
    dts = [0.1, 0.01, 0.001, 0.0001] if compare else [inputs["dt"].get()]
    if compare: clear()
    for dt in dts:
        xs, ys, rng, max_y, fv = simulate(dt)
        table.insert("", "end", values=(f"{dt:.4f}", f"{rng:.2f}", f"{max_y:.2f}", f"{fv:.1f}"))
        plot_line(xs, ys, f"dt={dt}")


def clear():
    ax.clear()
    ax.grid(True)
    ax.set(xlabel="Дальность", ylabel="Высота")
    table.delete(*table.get_children())

tk.Button(panel, text="Запуск", command=lambda: run_sim(False)).grid(row=len(fields), column=0, columnspan=2, sticky="we")
tk.Button(panel, text="Сравнить (dt)", command=lambda: run_sim(True)).grid(row=len(fields)+1, column=0, columnspan=2, sticky="we")
tk.Button(panel, text="Очистить", command=clear).grid(row=len(fields)+2, column=0, columnspan=2, sticky="we")



def simulate(dt):
    h, v, a, k = [inputs[k].get() for k in ("h","v","a","k")]
    a = np.radians(a)
    x = 0.0; y = h; g = 9.81
    vx, vy = v * np.cos(a), v * np.sin(a)
    xs, ys = [x], [y]
    max_y = h
    while True:
        px, py = x, y
        vx -= k * vx * dt
        vy += (-g - k * vy) * dt
        x += vx * dt
        y += vy * dt
        xs.append(x)
        ys.append(max(y,0))
        max_y = max(max_y, y)
        if y <= 0:
            xs[-1] = px + (x - px) * py / (py - y)
            ys[-1] = 0
            break
    return xs, ys, xs[-1], max_y, np.hypot(vx, vy)

fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

def plot_line(xs, ys, label):
    ax.plot(xs, ys, lw=2, label=label)
    ax.legend()
    ax.set_xlim(-2, max(ax.get_xlim()[1], max(xs)*1.1))
    ax.set_ylim(-2, max(ax.get_ylim()[1], max(ys)*1.1))
    canvas.draw_idle()


table = ttk.Treeview(root, columns=(1,2,3,4), show="headings", height=5)
for i, head in enumerate(["Шаг, с","Дальность, м","Макс. высота, м","Скорость в конце, м/с"],1):
    table.heading(i, text=head)
table.pack(side="bottom", fill="x")
clear()

root.mainloop()
