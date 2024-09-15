# https://howtothink.readthedocs.io/en/latest/PvL_H.html

import numpy as np
import rasterio
import pylandstats as pls
from matplotlib import pyplot
import tablib

# Constants
PATH_IMAGES = "/Users/matheuscordeiro/Documents/Doutorado/Disciplinas/Sensoriamento remoto/Trabalho 2/mapbiomas"
IMAGE_NAME = "mapbiomas-brazil-collection-90"
RESOLUTION = 30
YEARS = list(range(1985, 2024))
FOREST = 1
HERBACEOUS = 10
FARMING = 14
NON_VEGETATED_AREA = 22
WATER = 26
CLASSES = [FOREST, HERBACEOUS, FARMING, NON_VEGETATED_AREA, WATER]
CLASSES_COLORS = {
    FOREST: "#1f8d49",
    HERBACEOUS: "#ad975a",
    FARMING: "#FFFF66",
    NON_VEGETATED_AREA: "#d4271e",
    WATER: "#0000FF"
}

def reduce_mapbiomas_classes(x: np.ndarray):
    cond = [
        np.isin(x, [3, 4, 5, 6, 49]),
        np.isin(x, [11, 12, 32, 29, 50]),
        np.isin(x, [15, 18, 19, 39, 20, 40, 62, 41, 36, 46, 47, 35, 48, 9, 21]),
        np.isin(x, [23, 24, 30, 25]),
        np.isin(x, [33, 31, 27]),
    ]
    choice = [
        x.dtype.type(FOREST),
        x.dtype.type(HERBACEOUS),
        x.dtype.type(FARMING),
        x.dtype.type(NON_VEGETATED_AREA),
        x.dtype.type(WATER),
    ]
    return np.select(cond, choice, default=x)


def pre_processing():
    images = []
    for year in YEARS:
        with rasterio.open(f"{PATH_IMAGES}/{IMAGE_NAME}-{year}.tif") as src:
            image = src.read(1)
            print(year)
        images.append(reduce_mapbiomas_classes(image))
    return images


images =  pre_processing()
content_patch_density = []
content_edge_density = []
content_total_core_area = []
content_number_of_disjunct_core_areas = []
rows_patch_density = {}
rows_edge_density = {}
rows_total_core_area = {}
rows_number_of_disjunct_core_areas = {}
for index, obj in enumerate(images):
    ls = pls.Landscape(obj, res=(RESOLUTION, RESOLUTION))
    class_metrics_df = ls.compute_class_metrics_df(metrics=['patch_density', 'edge_density', 'total_core_area', 'number_of_disjunct_core_areas'])
    
    # patch_density
    for class_val in CLASSES:
        rows_patch_density.setdefault(class_val, []).append(class_metrics_df['patch_density'][class_val])
    content_patch_density.append([YEARS[index]] + class_metrics_df['patch_density'].tolist())
    
    # edge_density
    for class_val in CLASSES:
        rows_edge_density.setdefault(class_val, []).append(class_metrics_df['edge_density'][class_val])
    content_edge_density.append([YEARS[index]] + class_metrics_df['edge_density'].tolist())

    # total_core_area
    for class_val in CLASSES:
        rows_total_core_area.setdefault(class_val, []).append(class_metrics_df['total_core_area'][class_val])
    content_total_core_area.append([YEARS[index]] + class_metrics_df['total_core_area'].tolist())

    # number_of_disjunct_core_areas
    for class_val in CLASSES:
        rows_number_of_disjunct_core_areas.setdefault(class_val, []).append(class_metrics_df['number_of_disjunct_core_areas'][class_val])
    content_number_of_disjunct_core_areas.append([YEARS[index]] + class_metrics_df['number_of_disjunct_core_areas'].tolist())


# Graph patch density
pyplot.plot(YEARS, rows_patch_density[FOREST], label='Forest', color=CLASSES_COLORS[FOREST])
pyplot.plot(YEARS, rows_patch_density[HERBACEOUS], label='Herbaceous and Shrubby Vegetation', color=CLASSES_COLORS[HERBACEOUS])
pyplot.plot(YEARS, rows_patch_density[FARMING], label='Farming', color=CLASSES_COLORS[FARMING])
pyplot.plot(YEARS, rows_patch_density[NON_VEGETATED_AREA], label='Non vegetated area', color=CLASSES_COLORS[NON_VEGETATED_AREA])
pyplot.xlabel('Year')
pyplot.ylabel('Patch Density')
pyplot.legend()
pyplot.savefig(f'{PATH_IMAGES}/patch_density.png')

pyplot.clf()

# Graph edge density
pyplot.plot(YEARS, rows_edge_density[FOREST], label='Forest', color=CLASSES_COLORS[FOREST])
pyplot.plot(YEARS, rows_edge_density[HERBACEOUS], label='Herbaceous and Shrubby Vegetation', color=CLASSES_COLORS[HERBACEOUS])
pyplot.plot(YEARS, rows_edge_density[FARMING], label='Farming', color=CLASSES_COLORS[FARMING])
pyplot.plot(YEARS, rows_edge_density[NON_VEGETATED_AREA], label='Non vegetated area', color=CLASSES_COLORS[NON_VEGETATED_AREA])
pyplot.xlabel('Year')
pyplot.ylabel('Edge Density')
pyplot.legend()
pyplot.savefig(f'{PATH_IMAGES}/edge_density.png')

pyplot.clf()

# Graph total core area
pyplot.plot(YEARS, rows_total_core_area[FOREST], label='Forest', color=CLASSES_COLORS[FOREST])
pyplot.plot(YEARS, rows_total_core_area[HERBACEOUS], label='Herbaceous and Shrubby Vegetation', color=CLASSES_COLORS[HERBACEOUS])
pyplot.plot(YEARS, rows_total_core_area[FARMING], label='Farming', color=CLASSES_COLORS[FARMING])
pyplot.plot(YEARS, rows_total_core_area[NON_VEGETATED_AREA], label='Non vegetated area', color=CLASSES_COLORS[NON_VEGETATED_AREA])
pyplot.xlabel('Year')
pyplot.ylabel('Total Core Area')
pyplot.legend()
pyplot.savefig(f'{PATH_IMAGES}/total_core_area.png')

pyplot.clf()

# Graph total core area
pyplot.plot(YEARS, rows_number_of_disjunct_core_areas[FOREST], label='Forest', color=CLASSES_COLORS[FOREST])
pyplot.plot(YEARS, rows_number_of_disjunct_core_areas[HERBACEOUS], label='Herbaceous and Shrubby Vegetation', color=CLASSES_COLORS[HERBACEOUS])
pyplot.plot(YEARS, rows_number_of_disjunct_core_areas[FARMING], label='Farming', color=CLASSES_COLORS[FARMING])
pyplot.plot(YEARS, rows_number_of_disjunct_core_areas[NON_VEGETATED_AREA], label='Non vegetated area', color=CLASSES_COLORS[NON_VEGETATED_AREA])
pyplot.xlabel('Year')
pyplot.ylabel('Number of disjunct core areas')
pyplot.legend()
pyplot.savefig(f'{PATH_IMAGES}/number_of_disjunct_core_areas.png')

headers = ["Year", "Forest", "Herbaceous and Shrubby Vegetation", "Farming", "Non vegetated area", "Water"]
sheet_patch_density = tablib.Dataset(*content_patch_density, headers=headers)
sheet_patch_density.title = "Patch Density"
sheet_edge_density = tablib.Dataset(*content_edge_density, headers=headers)
sheet_edge_density.title = "Edge Density"
sheet_total_core_area = tablib.Dataset(*content_total_core_area, headers=headers)
sheet_total_core_area.title = "Total Core Area"
sheet_number_of_disjunct_core_areas = tablib.Dataset(*content_number_of_disjunct_core_areas, headers=headers)
sheet_number_of_disjunct_core_areas.title = "Number of Disjunct Core Areas"
book = tablib.Databook(
    (sheet_patch_density, sheet_edge_density, sheet_total_core_area, sheet_number_of_disjunct_core_areas)
)

# save data in xlsx file
with open(f"{PATH_IMAGES}/metrics.xlsx", "wb") as file:
    file.write(book.export("xlsx"))
