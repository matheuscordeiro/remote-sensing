import pylandstats as pls
import rasterio
import numpy as np
import matplotlib.pyplot as plt

landscapes = []
years = list(range(2017, 2023))
file_path = "/Users/matheuscordeiro/workspace-jupyter/data/sentinel/landsat_caatinga"
values = []
for year in years:
    with rasterio.open(f"{file_path}_{year}.tif") as file:            
        # Supondo que o NIR (infravermelho próximo) seja a banda 4 e o Red seja a banda 3
        nir_band = file.read(4).astype('float32')  # Banda NIR
        red_band = file.read(3).astype('float32')  # Banda Red

    # Calcular o NDVI usando a fórmula NDVI = (NIR - Red) / (NIR + Red)
    ndvi = (nir_band - red_band) / (nir_band + red_band)

    # Tratar divisão por zero e valores NaN
    ndvi = np.nan_to_num(ndvi, nan=0)
    valid_ndvi = ndvi[(ndvi >= -1) & (ndvi <= 1)]  # Filtrar valores válidos
    ndvi_mean = np.mean(valid_ndvi)
    print(f"{year}: {ndvi_mean}")

    values.append(ndvi_mean)

# Criar o gráfico
plt.plot(years, values, marker='o', linestyle='-', color='b', label='NDVI')

# Adicionar rótulos aos eixos
plt.xlabel('Anos')
plt.ylabel('NDVI')

# Adicionar um título
plt.title('Média do NDVI nos pixels')

# Adicionar uma legenda
plt.legend()

# Adicionar uma grade
plt.grid(True)

# Exibir o gráfico
plt.show()