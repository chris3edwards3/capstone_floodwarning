# **** Es nececario guardar el Proyecto de QGIS antes de ejecutar el script! ****
# **** You must save the QGIS Project before executing this script! ****

# Script to download GFS data, load into QGIS, and process
# © Feb 18, 2019 - Chris Edwards, Jake Lewis, Hunter Williams

# Data Information:
    # URL: https://nomads.ncep.noaa.gov/
    # Model: GFS 0.25 Degree 
    # Data Access: grib filter, by http
    # This model runs 4 times a day, at 0:00, 6:00, 12:00 and 18:00. We use the 0:00
    # We use the 6- and 12-hr accumulation intervals (APCP)
    # Filename eg: gfs.t00z.pgrb2.0p25.f006
    # The variable APCP (Total Precipitation) has units of kg/m^2


print("Script Has Started!")

import os
import shutil
import datetime
import urllib.request
import qgis.core
from PyQt5.QtCore import QVariant

# *** Download GFS APCP

# Identify today's date, and format it like YYMMDD00
# We use the most recent 00 forecast, or the forecast generated at midnight last night. 
now = datetime.datetime.now()
input_datetime = str(now.strftime("%Y%m%d")) + "00"

# Make a directory for raw data.
    # This directory will be created in the same directory where this script is saved.
    # If the directory already exists, it will be deleted along with all its contents.
current_directory = QgsProject.instance().homePath()
data_folder_path = current_directory + "/gfs_" + input_datetime
if os.path.exists(data_folder_path) == False:
    os.mkdir(data_folder_path)
else:
    shutil.rmtree(data_folder_path)
    os.mkdir(data_folder_path)
# List of all desired GFS file Id's. We use the 6-hr timesteps, and then the 12.

# The list is shorter, for testing
file_id_list = ["006", "012", "018", "024", "030", "036", "042", "048"]

# This is the entire list. Don't use for testing (comment out).
#file_id_list = ["006", "012", "018", "024", "030", "036", "042", "048",
#                "054", "060", "066", "072", "078", "084", "090", "096",
#                "102", "108", "114", "120", "126", "132", "138", "144",
#                "150", "156", "162", "168", "174", "180", "186", "192",
#                "198", "204", "210", "216", "222", "228", "234", "240",
#                "252", "264", "276", "288", "300", "312", "324", "336",
#                "324", "336","348", "360", "372", "384"
#                ]

# Loop to download and import rasters from the NOMADS database, GFS 0.25 Degree
for i in range(len(file_id_list)):
    # Download the file to the new raw-data directory
    data_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f" + file_id_list[i] + "&all_lev=on&var_APCP=on&subregion=&leftlon=282&rightlon=295&toplat=24&bottomlat=16&dir=%2Fgfs." + input_datetime
    filename = "gfs_apcp_" + input_datetime +"_f" + file_id_list[i] + ".grb"
    data_file_path = data_folder_path + "/" + filename
    urllib.request.urlretrieve(data_url, data_file_path)

    # Import the Raster into QGIS
    iface.addRasterLayer(data_file_path, filename)

    print(filename + " has downloaded and imported.")
    
print("All files have downloaded - next step = Raster Calculator")

# *** Setup raster layer variables for hours 00-24 for use in raster calculator

Hours_00_06 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f006.grb"
Hrs00_06 = QgsRasterLayer(Hours_00_06,"Hours 00 to 06")

Hours_06_12 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f012.grb"
Hrs06_12 = QgsRasterLayer(Hours_06_12,"Hours 06 to 12")

Hours_12_18 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f018.grb"
Hrs12_18 = QgsRasterLayer(Hours_12_18,"Hours 12 to 18")

Hours_18_24 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f024.grb"
Hrs18_24 = QgsRasterLayer(Hours_18_24,"Hours 18 to 24")

print("Hours 0-24 raster variables created")

H00_06 = QgsRasterCalculatorEntry()
H00_06.raster = Hrs00_06
H00_06.bandNumber = 1
H00_06.ref = '00_06@1'

H06_12 = QgsRasterCalculatorEntry()
H06_12.raster = Hrs06_12
H06_12.bandNumber = 1
H06_12.ref = '06_12@1'

H12_18 = QgsRasterCalculatorEntry()
H12_18.raster = Hrs12_18
H12_18.bandNumber = 1
H12_18.ref = '12_18@1'

H18_24 = QgsRasterCalculatorEntry()
H18_24.raster = Hrs18_24
H18_24.bandNumber = 1
H18_24.ref = '18_24@1'

entries = [ H00_06 , H06_12 , H12_18 , H18_24 ]

# *** Run raster calculator for Hours 00-24

daily_total_0_24 = data_folder_path + "/gfs_apcp_" + input_datetime + "Hrs00_24_daily_total.tif" 
calc_00_24 = QgsRasterCalculator ( '00_06@1 + 06_12@1 + 12_18@1 + 18_24@1', daily_total_0_24 , 'GTiff', Hrs00_06.extent(), Hrs00_06.width(), Hrs00_06.height(), entries )
print("new file path made")
calc_00_24.processCalculation()

print("Hours 0-24 calculator was successful")

iface.addRasterLayer (daily_total_0_24, "Hours 0-24 Accumulation")

# *** Setup raster layer variables for hours 24-48 for use in raster calculator

Hours_24_30 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f030.grb"
Hrs24_30 = QgsRasterLayer(Hours_24_30,"Hours 24 to 30")

Hours_30_36 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f036.grb"
Hrs30_36 = QgsRasterLayer(Hours_30_36,"Hours 30 to 36")

Hours_36_42 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f042.grb"
Hrs36_42 = QgsRasterLayer(Hours_36_42,"Hours 36 to 42")

Hours_42_48 = data_folder_path + "/gfs_apcp_" + input_datetime + "_f048.grb"
Hrs42_48 = QgsRasterLayer(Hours_42_48,"Hours 42 to 48")

print("Hours 24-48 raster variables created")

H24_30 = QgsRasterCalculatorEntry()
H24_30.raster = Hrs24_30
H24_30.bandNumber = 1
H24_30.ref = '24_30@1'

H30_36 = QgsRasterCalculatorEntry()
H30_36.raster = Hrs30_36
H30_36.bandNumber = 1
H30_36.ref = '30_36@1'

H36_42 = QgsRasterCalculatorEntry()
H36_42.raster = Hrs36_42
H36_42.bandNumber = 1
H36_42.ref = '36_42@1'

H42_48 = QgsRasterCalculatorEntry()
H42_48.raster = Hrs42_48
H42_48.bandNumber = 1
H42_48.ref = '42_48@1'

entries = [ H24_30 , H30_36 , H36_42 , H42_48 ]

# *** Run raster calculator for hours 24-48

daily_total_24_48 = data_folder_path + "/gfs_apcp_" + input_datetime + "_Hrs24_48_daily_total.tif" 
calc_24_48 = QgsRasterCalculator ( '24_30@1 + 30_36@1 + 36_42@1 + 42_48@1', daily_total_24_48 , 'GTiff', Hrs24_30.extent(), Hrs24_30.width(), Hrs24_30.height(), entries )
print("new file path made")
calc_24_48.processCalculation()

print("Hours 24-48 calculator was successful")

iface.addRasterLayer (daily_total_24_48, "Hours 24-48 Accumulation")

print("Raster Calculator complete, next step = Zonal Statistics")

# *** Zonal Statistics to average Precipitation 


#specify polygon shapefile ADJUST PATH TO WORK ON ANY MACHINE
shapefile_path = current_directory + "/ffgs_gfs_shp/ffgs.shp"	  #edit path to match location of shapefile on user's device
ffgs_shp = QgsVectorLayer(shapefile_path,'FFGS','ogr')		#Stores the shapefile layer as a variable

gfs_00to24 = QgsRasterLayer(daily_total_0_24,"Hours 0-24 Accumulation")

# usage - QgsZonalStatistics (QgsVectorLayer: polygonLayer, rasterLayer: QgsRasterLayer,, const QString attributePrefix="desired_prefix", int rasterBand=1)
#Overlay the raster on to the shapefile and find the mean precip forecast for each basin. Adds attribute table to shapefile with precip values
zoneStat = QgsZonalStatistics (ffgs_shp, gfs_00to24, '00-24', 1, QgsZonalStatistics.Mean)
zoneStat.calculateStatistics(None)

print('0-24 hour mean was created')

gfs_24to48 = QgsRasterLayer(daily_total_24_48,"Hours 24-48 Accumulation")

zoneStat = QgsZonalStatistics (ffgs_shp, gfs_24to48, '24-48', 1, QgsZonalStatistics.Mean)
zoneStat.calculateStatistics(None)
#           (Raster Calculator was done when importing correct band)

print('24-48 hour mean was created')


# *** Add new fields to the shapefile. Example: "Ind_00-24" = Potential to flood, 0-24 hours.
print("Añadiendo Campo (Adding Field...)")
layer_provider=ffgs_shp.dataProvider()
layer_provider.addAttributes([QgsField("Ind_00-24",QVariant.Double), 
                              QgsField("Ind_24-48",QVariant.Double)])
ffgs_shp.updateFields()


# *** Calculate fields. Will it flood? ffgs_mm - 0-24Mean = Ind_00-24 
#		Negative means it will flood. Positive means there isn't enought water to flood.
print("Calculando Atributos (Calculating Attributes...")
def calculate_attributes():
    with edit(ffgs_shp):
        for feature in ffgs_shp.getFeatures():
            feature.setAttribute(feature.fieldNameIndex('Ind_00-24'), feature['ffgs_mm']-feature['00-24mean'])
            ffgs_shp.updateFeature(feature)
    with edit(ffgs_shp):
        for feature in ffgs_shp.getFeatures():
            feature.setAttribute(feature.fieldNameIndex('Ind_24-48'), feature['ffgs_mm']-feature['24-48mean'])
            ffgs_shp.updateFeature(feature)
calculate_attributes()


# *** Add Shapefile to the Map
iface.addVectorLayer(shapefile_path, "modificado_", 'ogr')

print("Proceso terminado con éxito (Process successfully finished).")
