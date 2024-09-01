import sys
import numpy as np
import rasterio
import earthpy.plot as ep
import earthpy.spatial as es

year = sys.argv[1]

# Caminho para a imagem TIFF
image_path = f"/Users/matheuscordeiro/workspace-jupyter/data/sentinel_mean_images_year/sentinel2_caatinga_{year}.tif"

# Carregar as bandas
with rasterio.open(image_path) as src:
    red_band = src.read(4)  # Banda Red (banda 4, por exemplo)
    # nir_band = src.read(5)  # Banda NIR (banda 5 Landsat, por exemplo)
    nir_band = src.read(8)  # Banda NIR (banda 8 Sentinel por exemplo)

ndvi = es.normalized_diff(nir_band, red_band)
titles = [f"Sentinel 2 - NDVI - {year}"]

# Turn off bytescale scaling due to float values for NDVI
ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, title=titles, vmin=-1, vmax=1)
print(np.mean(ndvi))
