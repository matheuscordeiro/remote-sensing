import pylandstats as pls
import rasterio
import numpy as np
import matplotlib.pyplot as plt

landscapes = []
years = list(range(2019, 2025))
values = [0.2092, 0.1736, 0.1825, 0.1180, 0.1893, 0.1688]

# Criar o gráfico
plt.plot(years, values, marker='o', linestyle='-', color='b', label='NDVI')

# Adicionar rótulos aos eixos
plt.xlabel('Years')
plt.ylabel('NDVI')

# Adicionar um título
plt.title('Average NDVI of pixels')

# Adicionar uma legenda
plt.legend()

# Adicionar uma grade
plt.grid(True)

# Exibir o gráfico
plt.show()