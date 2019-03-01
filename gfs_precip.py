# Script to Download GFS data & process using QGIS
# Began on Feb 18, 2019 - Chris Edwards, Jake Lewis, Hunter Williams
# Jake was here a second time. Just to check.

print("Script Has Started!")

import os
import urllib.request
import qgis.core

input_yr = "2019"
input_mo = "02"
input_dy = "20"
input_hr = "00"
input_datetime = input_yr + input_mo + input_dy + input_hr

# Make a directory for raw data
current_directory = r"C:\Users\chris\Documents\QGIS\Projects\QGIS_TEST"
data_folder_path = current_directory + r"\gfs_" + input_datetime
os.mkdir(data_folder_path)

# List of all desired file Id's
file_id_list = ["006", "012", "018", "024"]

 #Jake's Test
 #Jake's Test
 #Jake's Test
 #Jake's Test
 #Jake's Test
 #Jake's Test
 

# Loop to download and import rasters
for i in range(len(file_id_list)):
    
    # Download the file to this raw_data directory
    data_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f" + file_id_list[i] + "&all_lev=on&var_APCP=on&subregion=&leftlon=282&rightlon=295&toplat=24&bottomlat=16&dir=%2Fgfs." + input_datetime
    filename = "apcp_" + input_datetime +"_f" + file_id_list[i] + ".grb"
    data_file_path = data_folder_path + r"\gfs_" + filename
    urllib.request.urlretrieve(data_url, data_file_path)

    # Import the Raster
    iface.addRasterLayer(data_file_path, "gfs_" + filename)

    print("File has downloaded and imported!")