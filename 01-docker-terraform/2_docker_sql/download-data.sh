FILENAME="yellow_tripdata_2024-01.parquet"

# Check if the file already exists
if [ -f "$FILENAME" ]; then
    echo "$FILENAME already exists."
else
    # If the file doesn't exist, download it
    wget https://d37ci6vzurychx.cloudfront.net/trip-data/$FILENAME
fi