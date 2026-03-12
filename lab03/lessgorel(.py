import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

N = 60
# 0-Пустырь, 1-Огонь, 2-Мол.Листва, 3-Ст.Листва, 4-Мол.Хвоя, 5-Ст.Хвоя
colors = ['#2b2b2b', '#ff6600', '#90ee90', '#228b22', '#40e0d0', '#004400']
labels = ['Пустырь', 'Огонь (горит долго)', 'Мол. Листва (15%)', 'Ст. Листва (30%)', 'Мол. Хвоя (60%)',
          'Ст. Хвоя (90%)']
cmap = ListedColormap(colors)
probs = {2: 0.25, 3: 0.15, 4: 0.3, 5: 0.5}

grid = np.random.choice([0, 2, 3, 4, 5], (N, N), p=[0.2, 0.2, 0.2, 0.2, 0.2])

fig, ax = plt.subplots(figsize=(8, 9))
plt.subplots_adjust(bottom=0.2)
img = ax.imshow(grid, cmap=cmap, vmin=0, vmax=5, interpolation='nearest')
ax.axis('off')
ax.legend(handles=[plt.plot([], [], marker="s", ms=10, ls="", color=colors[i], label=labels[i])[0] for i in range(6)],
          loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=8, frameon=False)


def update(frame):
    global grid
    nxt = grid.copy()

    for y in range(N):
        for x in range(N):
            state = grid[y, x]

            if state == 1:
                if np.random.rand() < 0.2:
                    nxt[y, x] = 0
            elif state == 0:
                if np.random.rand() < 0.0002:
                    nxt[y, x] = 2
            elif state > 1:
                y_min, y_max, x_min, x_max = max(0, y - 1), min(N, y + 2), max(0, x - 1), min(N, x + 2)
                if 1 in grid[y_min:y_max, x_min:x_max]:
                    if np.random.rand() < probs[state]:
                        nxt[y, x] = 1

    grid = nxt
    img.set_data(grid)
    return img,


def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        grid[int(event.ydata + 0.5), int(event.xdata + 0.5)] = 1

fig.canvas.mpl_connect('button_press_event', on_click)
ani = FuncAnimation(fig, update, interval=60, blit=True, cache_frame_data=False)
plt.show()