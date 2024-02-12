# Required installations (Uncomment if needed)
# !pip install fastavro
# !pip install faker
# !pip install pandas

import fastavro
from faker import Faker
import random
from datetime import datetime
import pandas as pd
import uuid
from fastavro import parse_schema

# To fake the data we will use faker
fake = Faker()

# Function to generate record for 1 user
def generate_records(userId, start_time, end_time, data, genre_options):
    # define different parameters that can be useful for a project like this, identifiers for the user
    activity_types = ["PLAY", "PAUSE", "SKIP", "LIKE", "FOLLOW"]
    device_types = ["MOBILE", "DESKTOP", "TABLET", "SMART_SPEAKER"]
    genre = random.choice(genre_options)
    session_start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
    session_end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
    timestamp = int(datetime.utcnow().timestamp())

    location = fake.country()
    # songs that have a genre
    filtered_songs = data[data['track_genre'] == genre]
    if not filtered_songs.empty:
        sample = filtered_songs.sample(1).iloc[0]
    else:
        sample = data.sample(1).iloc[0]
    # initialize list for records
    record = {
        "userId": userId,
        "eventTime": timestamp,
        "activityType": random.choice(activity_types),
        "songId": str(sample['track_id']),
        "genre": str(sample['track_genre']),
        "artistId": str(fake.uuid4()),
        "playlistId": str(fake.uuid4()),
        "duration": int(sample['duration_ms']),
        "userLocation": location,
        "startTime": int(session_start.timestamp() * 1000),
        "endTime": int(session_end.timestamp() * 1000),
        "deviceType": random.choice(device_types),
        "valence": sample.get('valence', None),
        "tempo": sample.get('tempo', None),
        "acousticness": sample.get('acousticness', None),
        "energy": sample.get('energy', None),
        "danceability": sample.get('danceability', None)
    }

    return record

# generates multiple records based on different users
def generate_multiple_records(start_time, end_time, no_users, record_count, data, genre_options):
    records = []
    users = [str(uuid.uuid4()) for _ in range(no_users)]
    for user in users:
        for _ in range(record_count):
            record = generate_records(user, start_time, end_time, data, genre_options)
            records.append(record)
    return records

# function to create avro file from the records generated 
def serialize_data(file_name, records, parsed_schema): 
    with open(file_name, 'wb') as out:
        fastavro.writer(out, parsed_schema, records)
    print(f"Generated {len(records)} records into {file_name}")


def main():
    # main function for organizing purposes
    schema = {
        "namespace": "com.spotify.wrapped",
        "type": "record",
        "name": "UserActivity",
        "fields": [
            {"name": "userId", "type": "string", "doc": "Unique identifier for the user."},
            {"name": "eventTime", "type": {"type": "long", "logicalType": "timestamp-millis"},
             "doc": "The timestamp when the activity occurred, in milliseconds since epoch."},
            {"name": "activityType", "type": {"type": "enum", "name": "ActivityType",
                                              "symbols": ["PLAY", "PAUSE", "SKIP", "LIKE", "FOLLOW"]},
             "doc": "Type of activity performed."},
            {"name": "song", "type": ["null", "string"], "doc": "Name of song, if applicable."},
            {"name": "songId", "type": ["null", "string"], "doc": "Unique identifier for the song, if applicable."},
            {"name": "genre", "type": "string", "doc": "key to group by song and listening patterns"},
            {"name": "artist", "type": ["null", "string"], "doc": "Name of artist, if applicable."},
            {"name": "artistId", "type": ["null", "string"], "doc": "Unique identifier for the artist, if applicable."},
            {"name": "playlistId", "type": ["null", "string"], "doc": "Unique identifier for the playlist, if applicable."},
            {"name": "duration", "type": ["null", "int"], "doc": "Duration of the activity in milliseconds, if applicable."},
            {"name": "userLocation", "type": ["null", "string"], "doc": "Location of the user at the time of activity."},
            {"name": "startTime", "type": {"type": "long", "logicalType": "timestamp-millis"}, "doc": "Start time of the activity period, inclusive."},
            {"name": "endTime", "type": {"type": "long", "logicalType": "timestamp-millis"}, "doc": "End time of the activity period, exclusive."},
            {"name": "deviceType", "type": {"type": "enum", "name": "DeviceType", "symbols": ["MOBILE", "DESKTOP", "TABLET", "SMART_SPEAKER"]}, "doc": "Type of device used for the activity."},
            {"name": "valence", "type": ["null", "float"], "doc": "Measure of musical positivity."},
            {"name": "tempo", "type": ["null", "float"], "doc": "Speed or pace of a given piece."},
            {"name": "acousticness", "type": ["null", "float"], "doc": "Measure of acoustical properties."},
            {"name": "energy", "type": ["null", "float"], "doc": "Measure of intensity and activity."},
            {"name": "danceability", "type": ["null", "float"], "doc": "Measure of how suitable a track is for dancing."}
        ]
    }

    parsed_schema = parse_schema(schema)

    # adjust to your path, for some reason github folder is not working for me
    dataset = '/Users/alirammal/Github/streamAnalytics_spotify/milestone1/dataset.csv'
    data = pd.read_csv(dataset)

    # identify genres as we are selecting them for our aspect of realism
    genres = data['track_genre'].value_counts()
    genre_options = genres.index.tolist()

    # define parameters for records
    start_time = '2021-04-01T8:00:00-05:00'
    end_time = '2021-04-01T10:00:00-05:00'
    no_users = 10
    record_count = 50

    # create multiple records 
    records = generate_multiple_records(start_time, end_time, no_users, record_count, data, genre_options)

    # create avro file 
    file_name = 'synthetic_spotify_data.avro'
    serialize_data(file_name, records, parsed_schema)

if __name__ == "__main__":
    main()

