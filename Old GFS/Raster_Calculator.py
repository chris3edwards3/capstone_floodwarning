from qgis.core import *
from qgis.analysis import *
from qgis.utils import *
import os
import PyQt5

target_ras_input = 'C:/Users/User/Desktop/Capstone/TEST/24hour/f006.grb'
target_ras = QgsRasterLayer(target_ras_input,"6_AM")
iface.addRasterLayer (target_ras_input, "6_AM")

initial_ras_input = 'C:/Users/User/Desktop/Capstone/TEST/24hour/f012.grb'
initial_ras = QgsRasterLayer(initial_ras_input,"12_PM")
iface.addRasterLayer (initial_ras_input, "12_PM")

print("Rasters added")

target = QgsRasterCalculatorEntry()
target.raster = target_ras
target.bandNumber = 1
target.ref = '6_AM@1'

initial = QgsRasterCalculatorEntry()
initial.raster = initial_ras
initial.bandNumber = 1
initial.ref = '12_PM@1'

entries = [ target , initial ]

final_output = 'C:/Users/User/Desktop/Capstone/TEST/24hour/accumulation.tif' 
calc = QgsRasterCalculator ( '6_AM@1 + 12_PM@1', final_output , 'GTiff', target_ras.extent(), target_ras.width(), target_ras.height(), entries )
print("new file path made")
calc.processCalculation()

print("calculator was successful")

iface.addRasterLayer (final_output, "Accumulation")