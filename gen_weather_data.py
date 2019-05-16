import rasterio
import numpy as np
from affine import Affine
from pyproj import Proj, transform
import requests
import random
import time
import sys, os, glob

"""
Sample reference for atmospheric pressure range and himidity range
https://en.wikipedia.org/wiki/Atmospheric_pressure(lowest:870hpa, highest:1050hpa)
https://www.chicagotribune.com/news/ct-xpm-2011-12-16-ct-wea-1216-asktom-20111216-story.html
Pressure range: {700 - 1100} 
Humidity range(%): {1-100}
For country cities database details refer to below link:
https://simplemaps.com/data/au-cities

"""

## Generate Random Datetime for a given Date Range
def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

## Generate Pressure and humidity using min and max from config file
def gen_ph(pmin,pax,hmax,hmin):
    return  str(round(random.uniform(pmin,pmax),1))+'|'+str(random.randrange(hmax,hmin,-1))

## Temperature range for different season of the year
season_conditions = {"Summer":{"temp":(25,40),"month":(5,6,7)},
                     "Autumn":{"temp":(20,30),"month":(2,3,4)},
                     "Winter":{"temp":(-5,15),"month":(11,12,1)},
                     "Spring":{"temp":(15,20),"month":(8,9,10)}}

print("*********************** Running application to generate weather data***********************")
with open('weather_config.txt') as myfiles:
        for line in myfiles:
            if line.split(":")[0] == 'Pressure':
                pmin,pmax = int(line.split(":")[1]),int(line.split(":")[2])
            elif line.split(":")[0] == 'Humidity':  
                hmin,hmax = int(line.split(":")[1]),int(line.split(":")[2])
            elif line.split(":")[0] == 'Time_range':  
                dmin,dmax,dfrmt = line.split(":")[1],line.split(":")[2],line.split(":")[3]
                
option = input("\n Please enter the mode for data generation: \n 1=Time-based \n 2=Geo-location based \n\n Please enter (1/2):")
if option=='1':
    country = input("\n Please provide full country name (e.g. Australia):")
    
    year = input("\n Please provide year {e.g. 2014}:")
    
    if int(year) >= datetime.datetime.now().year: 
      print("The application is built to generate weather data for previous years and not forecast for current or future year")
      print("Existing application..")
      sys.exit()
      
    path = input("\n Please provide path of Country Database:")
    ## Obtain the list of cities for the country  
    weather_data = open("weather_data_"+country+"_"+year+".dat", "w")
    
    with open(glob.glob(path+country+"/*.csv")[0]) as fg:
      next(fg)
      for line in fg:
            ## Traversing through the months of the specified year      
            for i in range(1,13):
            
             ## Obtain Temperature range for a particular month of the year           
             for season_dtl,season_dtl_info in season_conditions.items():
                if i in season_dtl_info["month"]:
                    (tmin,tmax) = season_dtl_info["temp"]
                    
                    
             ## Traversing through all the days of the specified year       
             for days in range(1,calendar.monthrange(int(year),i)[1]+1):
                ## Obtain lat,long and elevation for the City
                City = line.split(",")[0]
                Lat = line.split(",")[1]
                Lon = line.split(",")[2]
                e_dtl = requests.get('https://maps.googleapis.com/maps/api/elevation/json?locations='+Lat+','+Lon+'&key=AIzaSyCBekjUKiXYLaY0J7J3zurI7gksVGicBBA')
                elevation=e_dtl.json()['results'][0]['elevation']                
                
                ## Randomly generating pressure and humidity with pre-defined range  
                pressure,humidity = round(random.uniform(pmin,pmax),1),random.randrange(hmax,hmin,-1)
                
                Local_Time = strTimeProp(datetime.datetime(int(year), i, days,0,0,0).strftime("%Y-%m-%d %H:%M:%S"),
                                         datetime.datetime(int(year), i, days,23,59,59).strftime("%Y-%m-%d %H:%M:%S"),
                                         '%Y-%m-%d %H:%M:%S',random.random())
               
                Temperature = round(random.uniform(tmax,tmin),1) 
                
                ## Logic for Weather condition
                if Temperature < 0:
                    condition = "Snow"
                elif Temperature > 0.0 and pressure >= 700 and pressure <= 1000 and humidity >= 70:
                    condition = "Rain"
                    Temperature = '+'+str(Temperature)
                else:
                    condition = "Sunny"
                    Temperature = '+'+str(Temperature)
                    
                geo = City + "|" + str(Lat) + "," + str(Lon) + "," + str(elevation)+ "|" 
                weather_dtl = str(Temperature) + "|" + condition + "|" + Local_Time + "|" + str(pressure) + "|" + str(humidity)
                #print(City,str(Lat),str(Lon),elevation,,Temperature,condition,Local_Time,ph)  
                weather_data.write(geo+weather_dtl+"\n")
    weather_data.close()
    print("\n Completed writing weather data to file weather_data_"+country+"_"+year+".dat")
elif option=='2':
  path = input("Please provide path for the TIFF files")
  if len(glob.glob(path+"*.tif")) == 0:
    print("No files to process. Exiting application..")
    sys.exit()
    
  # Reading tiff files
  for img_file in glob.glob(path+"*.tif"):
    # Read raster
    with rasterio.open(img_file) as r:
        T0 = r.affine  # upper-left pixel corner affine transform
        p1 = Proj(r.crs)
        A = r.read_band(1)  # pixel values

    # All rows and columns
    cols, rows = np.meshgrid(np.arange(A.shape[1]), np.arange(A.shape[0]))

    # Get affine transform for pixel centres
    T1 = T0 * Affine.translation(0.5, 0.5)
    # Function to convert pixel row/column index (from 0) to easting/northing at centre
    rc2en = lambda r, c: (c, r) * T1

    # Based on the size of the data this will take some time TODO: Need to parallelize the process
    eastings, northings = np.vectorize(rc2en, otypes=[np.float, np.float])(rows, cols)

    # Project all longitudes, latitudes
    p2 = Proj(proj='latlong', datum='WGS84')
    longs, lats = transform(p1, p2, eastings, northings)

    weather_data = open(img_file+"_weather_data.dat", "w") 

    # Sample data is generate in a sequential process. TODO: Need to parallelize the process
    for r in range(0, len(longs)):
        s_long = longs[r]
        s_lats = lats[r]

        for i in range(0, len(s_long)):
            
                #r = requests.get('http://iatageo.com/getCode/' + str(s_lats[i]) + '/' + str(s_long[i]))
                #geocity = r.json()['IATA']
                geocity = "MEL"
                elevation = 39
                Local_Time = strTimeProp( datetime.datetime.strptime(dmin,dfrmt.rstrip("\r\n")).strftime("%Y-%m-%d %H:%M:%S"),
                                      datetime.datetime.strptime(dmax,dfrmt.rstrip("\r\n")).strftime("%Y-%m-%d %H:%M:%S")
                                      ,'%Y-%m-%d %H:%M:%S', random.random())
                
                lcl_mnth = Local_Time.split('-')[1]
                for season_dtl,season_dtl_info in season_conditions.items():
                  if lcl_mnth in season_dtl_info["month"]:
                    (tmin,tmax) = season_dtl_info["temp"]
                    
                pressure,humidity = round(random.uniform(pmin,pmax),1),random.randrange(hmax,hmin,-1)
                
                Temperature = round(random.uniform(tmax,tmin),1) 
                
                ## Logic for Weather condition
                if Temperature < 0:
                    condition = "Snow"
                elif Temperature > 0.0 and pressure >= 700 and pressure <= 1000 and humidity >= 70:
                    condition = "Rain"
                    Temperature = '+'+str(Temperature)
                else:
                    condition = "Sunny"
                    Temperature = '+'+str(Temperature)
                    
                geo = str(geocity) + "|" + str(Lat) + "," + str(Lon) + "," + str(elevation)+ "|" 
                weather_dtl = str(Temperature) + "|" + condition + "|" + Local_Time + "|" + str(pressure) + "|" + str(humidity)
                #print(City,str(Lat),str(Lon),elevation,,Temperature,condition,Local_Time,ph)  
                weather_data.write(geo+weather_dtl+"\n")
    weather_data.close()
else:
    print("Invalid option selected. Exiting application...")
    sys.exit()
    
