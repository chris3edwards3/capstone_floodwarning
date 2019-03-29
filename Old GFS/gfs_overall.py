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

# *** Download GFS APCP

# Identify today's date, and format it like YYMMDD00
# We use the most recent 00 forecast, or the forecast generated at midnight last night. 
now = datetime.datetime.now()
input_datetime = str(now.strftime("%Y%m%d")) + "00"

# Make a directory for raw data.
# This directory will be created in the directory where this script is saved.
# If the directory exists, it will be deleted along with all its contents.
current_directory = os.getcwd()
data_folder_path = current_directory + "/gfs_apcp_" + input_datetime
if os.path.exists(data_folder_path) == False:
    os.mkdir(data_folder_path)
else:
    shutil.rmtree(data_folder_path)
    os.mkdir(data_folder_path)

# List of all desired GFS file Id's. We use the 6-hr timesteps, and then the 12.

# The list is shorter, for testing
# file_id_list = ["006", "012", "018", "024", "030", "036", "042", "048"
                ]

# This is the entire list. Don't use for testing (comment out).
file_id_list = ["006", "012", "018", "024", "030", "036", "042", "048",
                "054", "060", "066", "072", "078", "084", "090", "096",
                "102", "108", "114", "120", "126", "132", "138", "144",
                "150", "156", "162", "168", "174", "180", "186", "192",
                "198", "204", "210", "216", "222", "228", "234", "240",
                "252", "264", "276", "288", "300", "312", "324", "336",
                "324", "336","348", "360", "372", "384"
                ]

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
    
print("Script has completed!")