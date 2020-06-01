import csv
import os
import geopy
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import io

import reverse_geocoder as rg

files_list = os.listdir("BlackMarbleLandOnly")

county_light_vals = {}
num_exceptions = 0

# Processed every so iterations
querable_coords = list()

# List of float values
current_pixel_values = []

geo = rg.RGeocoder(mode=2, verbose=True, stream=io.StringIO(open('rg_cities1000.txt', encoding='utf-8').read()))

for curr_file in files_list:
    curr_path = "BlackMarbleLandOnly/" + str(curr_file)

    with open(curr_path) as csv_file:
        # csv_reader = csv.reader(csv_file, delimiter = ',')

        # Ignore null bytes
        csv_reader = csv.reader((x.replace('\0', '') for x in csv_file), delimiter = ',')

        line_count = 0
        i = 0
        j = 0

        for row in csv_reader:

            # If not the header line and not above lat 71.4 (highest point in U.S.)
            if line_count != 0 and float(row[0]) <= 71.4:
                try:
                    # print("Attempting to process val at: " + str(line_count))
                    curr_lat = int(float(row[0]))
                    curr_lon = int(float(row[1]))
                    pixel_val = float(row[2])

                    curr_tuple = (curr_lat, curr_lon)

                    # Add it to list of values that need to be appended
                    current_pixel_values.append(pixel_val)
                    querable_coords.append(curr_tuple)
                except:
                    num_exceptions += 1
                    
            

            # Process what is so far every 25000 entries
            if(i == 1500):
                i = 0
                querable_coords = tuple(querable_coords)
                results_list = rg.search(querable_coords)

                # Iterate through the list and check if it exists in the dictionary
                
                counter = 0

                for item in results_list:
                    if(j == 500 ):
                            print("Processing values at Latitude: " + str(row[0]))
                            print("Processing county " + item['admin2'] + " in the great state of " + item['admin1'])
                            j = 0


                    if(item['cc'] == 'US'):
                        state = item['admin1']
                        county = item['admin2']
                        
                            


                        if state == 'New York':
                                print("State: " + state + " | County: " + county + " | Lat: " + str(row[0]) + " Lon: " +str(row[1]))

                        # Creating the key:
                        key = (state, county)
                        val = current_pixel_values[counter]

                        # If it already exists, then append
                        if key in county_light_vals.keys():
                            
                            # Get existing value
                            curr_value_list = county_light_vals[key]
                            curr_value_list.append(val)
                            county_light_vals[key] = curr_value_list

                        # Create a new element
                        else:
                            county_light_vals[key] = [val]

                    counter += 1

                # Clear the data
                querable_coords = list()
                current_pixel_values = []

            i += 1



            line_count += 1
            j += 1


        print("Finished reading last row from the csv")



        if(len(querable_coords) >= 1):
            print("Final Processing of values at Latitude: " + str(row[0]))
            querable_coords = tuple(querable_coords)
            results_list = rg.search(querable_coords)
            i = 0

            # Iterate through the list and check if it exists in the dictionary
            
            counter = 0

            for item in results_list:

                # Check if the county is in the US
                if(item['cc'] == 'US'):
                    county = item['admin2']
                    state = item['admin1']

                    # Creating the key:
                    key = (state, county)
                    val = current_pixel_values[counter]

                    # If it already exists, then append
                    if key in county_light_vals.keys():
                        
                        # Get existing value
                        curr_value_list = county_light_vals[key]
                        curr_value_list.append(val)
                        county_light_vals[key] = curr_value_list

                    # Create a new element
                    else:
                        county_light_vals[key] = [val]
                
                counter += 1

            # Clear the data
            querable_coords = list()
            current_pixel_values = []

print("Done processing, Number exceptions: " + str(num_exceptions))

# For each county in the final dictionary, take the mean
# Writing into single file
with open('county_avg_radiances', 'w', newline = '') as csvfile:
    fieldnames = ['state', 'county', 'radiance']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()

    tf = True

    for key in county_light_vals.keys():
        list_floats = county_light_vals[key]

        if(tf):
            print(list_floats)
            tf = False

        sum = 0
        for ele in list_floats:
            sum += ele

        avg = sum / len(list_floats)
        writer.writerow({'state' : key[0], 'county' : key[1], 'radiance' : avg})
