#############################################################################################################################
# Script Name :  gen_weather_data.py
# Purpose : This script generated plausible weather considering two different aspects for 
            weather generation(i.e. Time-based, Geo-location based)
            
            The time-based segment of the code does the following:
            User input:
            ==========
            Country:(e.g. Australia)
            Year:(e.g. 2017)
            Path for country details:(e.g./user/jully/)
            
            1. Validates the year and exits if current or future year is provided as the program
               generates data instead of forecast
            2. Generated daily data for every city of the specified country.
               The country data(list of cities,latitude and longitude) is expected to be 
               in the following location: $(USER_INPUT_PATH}/{USER_INPUT_COUNTRY}/
               For country cities database details refer to below link:
               https://simplemaps.com/data/au-cities
            3. Perform Google API call to obtain elevation of the cities based on latitude and longitude
            4. Generates temperature as per month to season applicability across majority 
               countries(not all)
               e.g. Jan - Winter - Temp range - (-5,-15)
            5. Pressure and humidty are generated per min and max recorded value around the world
               that is stored in a config file "weather_config.txt" and is expected to be 
               in the same path as the code:
                Sample reference for atmospheric pressure range and himidity range
                https://en.wikipedia.org/wiki/Atmospheric_pressure(lowest:870hpa, highest:1050hpa)
                https://www.chicagotribune.com/news/ct-xpm-2011-12-16-ct-wea-1216-asktom-20111216-story.html
                Pressure range: {700 - 1100} 
                Humidity range(%): {1-100}
            6. There is one output file generated for every country that
               contains all cities daily weather data for the specified year. The output file is 
               created in the same path as the script and has following naming convention:
               weather_data_${USER_INPUT_COUNTRY}_${USER_INPUT_YEAR}.dat
            The geo-location based segment of the code does the following:
            User input:
            ===========
            Path of the  tif file:(e.g./user/jully/)
            
            1. This segment generated weather data for every latitude and longitude from the
               tif files located in the path ${USER_INPUT_PATH}
            2. Perform Google API call to obtain elevation of the cities based on latitude and longitude
            3. Generates temperature as per month to season applicability across majority 
               countries(not all)
            4. Pressure and humidty are generated per min and max recorded value around the world
               that is stored in a config file "weather_config.txt" and is expected to be 
               in the same path as the code:
                Sample reference for atmospheric pressure range and himidity range
                https://en.wikipedia.org/wiki/Atmospheric_pressure(lowest:870hpa, highest:1050hpa)
                https://www.chicagotribune.com/news/ct-xpm-2011-12-16-ct-wea-1216-asktom-20111216-story.html
                Pressure range: {700 - 1100} 
                Humidity range(%): {1-100}
            5. The Local time date range(min,max) is passed from the same 
               config file ("weather_config.txt") for randomly generating Local Time 
            6. There is one output file generated for every tif file read 
               The output file is created in the same path as the script and has following 
               naming convention:
               $(TIF_FILENAME}_weather_data.dat.dat
               
#Program Exit points:
               1. Invalid option provided by user in choosing segment
               2. Current or future year provided for time-based segment
               3. No Tif files to process for geo-based segment
               4. No Country files available to process for time-based segment
               
# Out of Scope:
            1. Temperature generation as per seasons applicable in each 
               country(for e.g. Africa and Singapore does not have winter season)
            2. Aspects  of weather generation excluding Time and geo-location
# Parameters : No parameters required
# Python Version: Python3
# Execution : python3  gen_weather_data.py
# Additional Python Package installation: 
                          rasterio
                          pyproj 
                          requests
# Version maintenance:
# Version           Author               Date        Changes
# ------------------------------------------------------------
# 1.0               Jully               05/16/2019   Initial
# Test Cases:
              1. Temperature for both segments generating as per Local time(Month--> Season)
                 applicability 
              2. Elevation details from Google API call providing correct details or not
              3. Randomness of the pressure  and humidity as per defined range
              4. Weather condition checks(Snow, Rain, Summer) logic check
              5. Program exit points checks
              6. Loop checks
##############################################################################################################################
