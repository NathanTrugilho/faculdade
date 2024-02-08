import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Gerar dados
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

# Criar figura
fig = plt.figure()

# Adicionar subplot 3D
ax = fig.add_subplot(111, projection='3d')

# Plotar superfície
surf = ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')

# Adicionar barra de cores
fig.colorbar(surf, shrink=0.5, aspect=5)

# Adicionar título e rótulos dos eixos
ax.set_title('Superfície 3D')
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_zlabel('Eixo Z')

# Adicionar marcadores
ax.scatter(0, 0, 0, color='red', marker='o', label='Origem')
ax.scatter(x[::10], y[::10], z[::10], color='blue', marker='x', label='Pontos selecionados')

# Adicionar legenda
ax.legend()

# Mostrar gráfico
plt.show()
