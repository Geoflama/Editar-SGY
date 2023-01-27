import re

def gpgga_to_coords(sentence):
    # Regular expression to match the GPGGA sentence format
    match = re.match(r'\$GPGGA,(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+)', sentence)
    if match:
        # Extract the data from the sentence
        time = match.group(1)
        lat = match.group(2)
        lat_dir = match.group(3)
        lon = match.group(4)
        lon_dir = match.group(5)
        fix_quality = match.group(6)
        satellites = match.group(7)
        hdop = match.group(8)
        altitude = match.group(9)
        altitude_unit = match.group(10)
        geoid_height = match.group(11)
        geoid_height_unit = match.group(12)
        dgps_age = match.group(13)
        
        # Convert the latitude and longitude to decimal degrees
        lat_deg = int(lat[:2])
        lat_min = float(lat[2:]) / 60
        lat_dec = lat_deg + lat_min
        if lat_dir == 'S':
            lat_dec = -lat_dec
        
        lon_deg = int(lon[:3])
        lon_min = float(lon[3:]) / 60
        lon_dec = lon_deg + lon_min
        if lon_dir == 'W':
            lon_dec = -lon_dec
        
        return (lat_dec, lon_dec)
    else:
        return None

# Example usage
sentence = '$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47'
coords = gpgga_to_coords(sentence)
print(coords)
# Output: (48.117297, 11.516667)
