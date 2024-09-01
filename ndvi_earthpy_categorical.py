import sys
import numpy as np
import rasterio
import earthpy.plot as ep
import earthpy.spatial as es
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

year = sys.argv[1]

# Caminho para a imagem TIFF
image_path = f"/Users/matheuscordeiro/workspace-jupyter/data/sentinel_mean_images_year/sentinel2_caatinga_{year}.tif"

# Carregar as bandas
with rasterio.open(image_path) as src:
    red_band = src.read(4)  # Banda Red (banda 4, por exemplo)
    # nir_band = src.read(5)  # Banda NIR (banda 5, por exemplo)
    nir_band = src.read(8)  # Banda NIR (banda 8 Sentinel por exemplo)

ndvi = es.normalized_diff(nir_band, red_band)
titles = [f"Sentinel 2 - NDVI - {year}"]

# Create classes and apply to NDVI results
ndvi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
ndvi_landsat_class = np.digitize(ndvi, ndvi_class_bins)

# Apply the nodata mask to the newly classified NDVI data
ndvi_landsat_class = np.ma.masked_where(
    np.ma.getmask(ndvi), ndvi_landsat_class
)
np.unique(ndvi_landsat_class)

# Define color map
nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
nbr_cmap = ListedColormap(nbr_colors)

# Define class names
ndvi_cat_names = [
    "No Vegetation",
    "Bare Area",
    "Low Vegetation",
    "Moderate Vegetation",
    "High Vegetation",
]

# Get list of classes
classes = np.unique(ndvi_landsat_class)
classes = classes.tolist()
# The mask returns a value of none in the classes. remove that
classes = classes[0:5]

# Plot your data
fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title(
    f"Sentinel 2 - NDVI classes - {year}",
    fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()
plt.show()