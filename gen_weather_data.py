import random
import time
import calendar
import sys

"""
Sample reference for atmospheric pressure range and himidity range
https://en.wikipedia.org/wiki/Atmospheric_pressure(lowest:870hpa, highest:1050hpa)
https://www.chicagotribune.com/news/ct-xpm-2011-12-16-ct-wea-1216-asktom-20111216-story.html
Pressure range: {700 - 1100} 
Humidity range(%): {1-100}
"""


## Generate Random Datetime for a given Date Range
def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

## Temperature range for different season of the year
season_conditions = {"Summer":{"temp":(25,40),"month":(5,6,7)},
                     "Autumn":{"temp":(20,30),"month":(2,3,4)},
                     "Winter":{"temp":(-5,15),"month":(11,12,1)},
                     "Spring":{"temp":(15,20),"month":(8,9,10)}}


print("*********************** Running application to generate weather data***********************")
option = input("\n Please enter the mode for data generation: \n 1=Time-based \n 2=Geo-location based \n\n Please enter (1/2):")
if option=='1':
    country = input("\n Please provide full country name (e.g. Australia)") 
    year = input("\n Please provide year {format: YYYY}") 
elif option=='2':
    print('geo')
else:
    print("Invalid option selected. Exiting application...")
    sys.exit()
                    
cities_list = ['Melbourne','Sydney','Brisbane']

for City in cities_list:
               
        ## Traversing through the months of the specified year      
        for i in range(1,13):
            
            ## Obtain Temperature range for a particular month of the year           
            for season_dtl,season_dtl_info in season_conditions.items():
                if i in season_dtl_info["month"]:
                    (tmin,tmax) = season_dtl_info["temp"]
                    season=season_dtl
                    
            ## Traversing through the days of the specified year       
            for days in range(1,calendar.monthrange(int(year),i)[1]+1):
                sign=''
                Lat = 31
                Lon = 154
                elevation = 39
                
                ## Randomly generating pressure and humidity with pre-defined range - Pressure(700,1200) 
                pressure = round(random.uniform(700,1100),1)
                humidity = random.randrange(100,1,-1)
                Local_Time = strTimeProp(year+'-'+str(i)+'-'+str(days)+' 00:00:00',year+'-'+str(i)+'-'+str(days)+' 23:59:59',
                                         '%Y-%m-%d %H:%M:%S', random.random())
                Temperature = round(random.uniform(tmax,tmin),1)
            
                if Temperature > 0.0:
                    sign = '+'
            
                if Temperature < 0:
                    condition = "Snow"
                elif Temperature > 0.0 and pressure >= 700 and pressure <= 100 and humidity >= 70:
                    condition = "Rain"
                else:
                    condition = "Sunny"
    
                print(City,str(Lat),str(Lon),elevation,i,sign+str(Temperature),season,condition,Local_Time,pressure,humidity)
        
     
