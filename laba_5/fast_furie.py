import numpy as np
import matplotlib.pyplot as plt

# Функция для анализа
def f(x):
    return np.sin(x) + 0.5 * np.cos(2*x)

# Параметры сигнала
a, b = -np.pi, np.pi  # Интервал
N = 128             # Количество точек (лучше степень двойки)

# Дискретизация сигнала
x = np.linspace(a, b, N, endpoint=False)
y = f(x)

# Быстрое преобразование Фурье (FFT)
fft_coeffs = np.fft.fft(y)
freqs = np.fft.fftfreq(N, d=(b-a)/N)  # Частоты в Герцах

# Амплитудный спектр (нормированный)
amplitude = np.abs(fft_coeffs) / N * 2  # Умножаем на 2 для симметричного спектра
amplitude[0] /= 2  # Постоянная составляющая не дублируется

# Визуализация
plt.figure(figsize=(12, 6))

# Исходный сигнал
plt.subplot(2, 1, 1)
plt.plot(x, y, label='Исходный сигнал')
plt.title('Исходный сигнал: $f(x) = \sin(x) + 0.5 \cos(2x)$')
plt.xlabel('Время (сек)')
plt.ylabel('Амплитуда')
plt.grid()

# Амплитудный спектр
plt.subplot(2, 1, 2)
plt.stem(freqs[:N//2], amplitude[:N//2], 'r', markerfmt='ro', basefmt=" ")
plt.title('Амплитудный спектр (FFT)')
plt.xlabel('Частота (Гц)')
plt.ylabel('Амплитуда')
plt.grid()

plt.tight_layout()
plt.show()

# Вывод основных частот
print("Основные частоты:")
for i in np.where(amplitude > 0.1)[0]:
    if freqs[i] >= 0:
        print(f"Частота: {freqs[i]:.2f} Гц, Амплитуда: {amplitude[i]:.4f}")