#!/bin/bash

# Input file
file="gpsdata.txt"

# Output file
output="geocoordinates.txt"

# Loop through each line of the input file
while read -r line; do

  # Check if the line starts with '$GPGGA' (indicating it is a valid GPS data line)
  if [[ $line == GPGGA* ]]; then

    # Split the line into an array using the comma delimiter
    IFS=',' read -ra data <&#8203;`oaicite:{"index":0,"invalid_reason":"Malformed citation << \"$line\"\n\n    # Extract the latitude and longitude values (in the format DDMM.MMMM)\n    lat=${data[2]}\n    lon=${data[4]}\n\n    # Extract the latitude and longitude hemisphere (N/S and E/W)\n    lat_hemi=${data[3]}\n    lon_hemi=${data[5]}\n\n    # Convert the latitude and longitude to decimal degrees\n    # (DD + (MM.MMMM / 60))\n    lat_deg=$(echo \"$lat / 100\" | bc -l)\n    lat_min=$(echo \"$lat - ($lat_deg * 100)\" | bc -l)\n    lat_dec=$(echo \"$lat_deg + ($lat_min / 60)\" | bc -l)\n    lon_deg=$(echo \"$lon / 100\" | bc -l)\n    lon_min=$(echo \"$lon - ($lon_deg * 100)\" | bc -l)\n    lon_dec=$(echo \"$lon_deg + ($lon_min / 60)\" | bc -l)\n\n    # Apply the hemisphere sign to the latitude and longitude values\n    if [[ $lat_hemi == \"S\" ]]; then\n      lat_dec=$(echo \"$lat_dec * -1\" | bc -l)\n    fi\n    if [[ $lon_hemi == \"W\" ]]; then\n      lon_dec=$(echo \"$lon_dec * -1\" | bc -l)\n    fi\n\n    # Append the decimal latitude and longitude to the output file\n    echo \"$lat_dec, $lon_dec\" >>"}`&#8203; $output
  fi
done < "$file"

echo "GPS data converted to geographic coordinates and saved to $output"
