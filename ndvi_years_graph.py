import pylandstats as pls
import rasterio
import numpy as np
import matplotlib.pyplot as plt

landscapes = []
years = list(range(2017, 2025))
values = [0.1382, 0.1646, 0.1579, 0.1656, 0.1248, 0.1873, 0.1522, 0.2076]

# Criar o gráfico
plt.plot(years, values, marker='o', linestyle='-', color='b', label='NDVI')

# Adicionar rótulos aos eixos
plt.xlabel('Years')
plt.ylabel('NDVI')

# Adicionar um título
plt.title('Average NDVI of pixels - Landsat 8')

# Adicionar uma legenda
plt.legend()

# Adicionar uma grade
plt.grid(True)

# Exibir o gráfico
plt.show()