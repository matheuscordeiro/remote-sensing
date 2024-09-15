import pylandstats as pls
import rasterio
import numpy as np
import matplotlib.pyplot as plt

landscapes = []
years = list(range(2017, 2023))
file_path = "/Users/matheuscordeiro/workspace-jupyter/data/sentinel/landsat_caatinga"

for year in years:
    with rasterio.open(f"{file_path}_{year}.tif") as file:
        image = file.read(1)
    image = np.nan_to_num(image).astype(np.uint8)
    landscapes.append(pls.Landscape(image, res=(image.shape[0], image.shape[1])))

spatio_temporal = pls.SpatioTemporalAnalysis(landscapes, dates=years)
spatio_temporal.plot_landscapes(legend=False)

# plt.savefig('landscape_plot.png', dpi=300, bbox_inches='tight')

# Mostrar o gráfico (opcional)
plt.show()