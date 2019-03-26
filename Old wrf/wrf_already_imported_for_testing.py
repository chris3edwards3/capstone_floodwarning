# ******** FOR TESTING ******** AFTER DOWNLOADING ************
# Script to download WRF, import into QGIS,and process
# © Feb 18, 2019 - Chris Edwards, Jake Lewis, Hunter Williams

# Data Information:
    # URL: https://www.nco.ncep.noaa.gov/pmb/products/hiresw/
    # Model: AWIPS 3.8km Puerto Rico ARW (NCAR Advanced Research WRF) 
    #      (The 2.5km doesn't include the DR) (filename says it's 5km)
    # Data Access: GRIB2 via http
    # This model runs twice a day, at 6:00 and 18:00. We use the 6:00
    # We use the 24- and 48-hr accumulated precipitation in kg/m^2
    # Filename eg: hiresw.t06z.arw_5km.f24.pr.grib2
    # The variable APCP (Total Precipitation) is stored in Raster Band 282

print("Script Has Started!")

import os
import shutil
import datetime
import urllib.request
import qgis.core


# *** Download the GRIB2 files from the internet

# Identify today's date in the form YYYYMMDD 
now = datetime.datetime.now()
input_datetime = str(now.strftime("%Y%m%d"))

# Make a directory for raw data.
    # This directory will be created in the same directory where this script is saved.
    # If the directory already exists, it will be deleted along with all its contents.
current_directory = os.getcwd()
new_folder_path = current_directory + "/wrf_" + input_datetime
#if os.path.exists(new_folder_path) == False:
    #os.mkdir(new_folder_path)
#else:
    #shutil.rmtree(new_folder_path)
    #os.mkdir(new_folder_path)

## Download the 24-hr file to the new folder 
data_url_24 = "https://www.ftp.ncep.noaa.gov/data/nccf/com/hiresw/prod/hiresw." + input_datetime + "/hiresw.t06z.arw_5km.f24.pr.grib2"
    ## 48-hr grib2 filename and path
grib_filename_24 = "wrf_" + input_datetime +"_f24.grib2"
grib_path_24 = new_folder_path + "/" + grib_filename_24
    ## download through url
#urllib.request.urlretrieve(data_url_24, grib_path_24)
#print(grib_filename_24 + " has downloaded.")

# Create Raster Layer
target_ras_24 = QgsRasterLayer(grib_path_24, grib_filename_24)
# Necessary input for Raster Calculator
target_24 = QgsRasterCalculatorEntry()
target_24.raster = target_ras_24
target_24.bandNumber = 282
target_24.ref = grib_filename_24 + '@282'
    # List of Calculator Entries
entries = [target_24]
    # 24-hr APCP accumulation Tiff File name and path
tiff_filename_24 = "wrf_apcp_" + input_datetime +"_24.tif"
tiff_path_24 = new_folder_path + "/" + tiff_filename_24

# Raster Calculator. Simply extracting band 282
calc = QgsRasterCalculator (grib_filename_24 + '@282 * 1', tiff_path_24 , 'GTiff', target_ras_24.extent(), target_ras_24.width(), target_ras_24.height(), entries)
calc.processCalculation()

# Save new raster as a QGIS Layer
apcp_00to24 = QgsRasterLayer(tiff_path_24, tiff_filename_24)
# Import the Raster into QGIS
iface.addRasterLayer(tiff_path_24, tiff_filename_24)
print(tiff_filename_24 + " has imported.")


# Download the 48-hr file to the new folder
data_url_48 = "https://www.ftp.ncep.noaa.gov/data/nccf/com/hiresw/prod/hiresw." + input_datetime + "/hiresw.t06z.arw_5km.f48.pr.grib2"
    # 48-hr grib2 filename and path
grib_filename_48 = "wrf_" + input_datetime +"_f48.grib2"
grib_path_48 = new_folder_path + "/" + grib_filename_48
    # download through url
#urllib.request.urlretrieve(data_url_48, grib_path_48)
#print(grib_filename_48 + " has downloaded.")

# Create Raster Layer
target_ras_48 = QgsRasterLayer(grib_path_48, grib_filename_48)
# Necessary input for Raster Calculator
target_48 = QgsRasterCalculatorEntry()
target_48.raster = target_ras_48
target_48.bandNumber = 282
target_48.ref = grib_filename_48 + '@282'
    # List of Calculator Entries
entries = [target_24, target_48]
    # 48-hr APCP accumulation Tiff File name and path
tiff_filename_48 = "wrf_apcp_" + input_datetime +"_48.tif"
tiff_path_48 = new_folder_path + "/" + tiff_filename_48

# Raster Calculator: 
# Total 48-hr accumulation subtract the 24-hr accumulation to get the final 24-hr accumulation.
calc = QgsRasterCalculator (grib_filename_48 + '@282 - ' + grib_filename_24 +'@282', tiff_path_48 , 'GTiff', target_ras_48.extent(), target_ras_48.width(), target_ras_48.height(), entries)
calc.processCalculation()

# Save new raster as a QGIS Layer
apcp_24to48 = QgsRasterLayer(tiff_path_24, tiff_filename_24)
# Import the Raster into QGIS
iface.addRasterLayer(tiff_path_48, tiff_filename_48)
print(tiff_filename_48 + " has imported.")


# *** Zonal Statistics to average Precipitation 
#           (Raster Calculator was done when importing correct band)



print("Script has completed!")