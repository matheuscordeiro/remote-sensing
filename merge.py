import os
from osgeo import gdal

# Listar todos os arquivos GeoTIFF na pasta
dir_path = '/Users/matheuscordeiro/Documents/Doutorado/Disciplinas/Sensoriamento remoto/caatinga_pb/export/'
tif_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.tif')]

# Nome do arquivo de saída
output_tif = '/Users/matheuscordeiro/Documents/Doutorado/Disciplinas/Sensoriamento remoto/caatinga_pb/merged_output.tif'

# Executar o merge
gdal.Warp(output_tif, tif_files, format='GTiff')