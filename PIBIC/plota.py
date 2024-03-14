import matplotlib.pyplot as plt
import numpy as np

def funcao_filtro(x, x0, G0, WA, sigma1, sigma2, sigma3):
  return G0 * ((2 * (x - x0) / (sigma1 * WA)) ** sigma2 + 1) ** (-2 * sigma3)

x = np.linspace(0, 20, 2000)
y = []
x0 = 10
sigma1 = 3
sigma2 = 2
sigma3 = 2
G0 = 1
WA = 3

for i in x:
  y.append(funcao_filtro(i, x0, G0, WA, sigma1, sigma2, sigma3))

plt.scatter(x, y)
plt.grid(True)
plt.xlabel("X")
plt.ylabel("G(x)")

plt.show()