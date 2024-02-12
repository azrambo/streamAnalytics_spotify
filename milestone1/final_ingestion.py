"""
Colab file is located at
    https://colab.research.google.com/drive/1tmOzolQ5iBNjqTHTY_35NpqUs57R0xif
"""

import fastavro
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from fastavro import parse_schema
import pandas as pd
import uuid
import numpy as np
from datasets import load_dataset

# personalizable parameters
start_time = '2021-04-01T8:00:00-05:00'
end_time = '2021-04-01T10:00:00-05:00'
no_users = 10
record_count = 50

fake = Faker()

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
        {"name": "song", "type": ["null", "string"],
         "doc": "Name of song, if applicable."},
        {"name": "songId", "type": ["null", "string"],
         "doc": "Unique identifier for the song, if applicable."},
        {"name": "track_name", "type": ["null", "string"],
         "doc": "Name for the song, if applicable."},
        {"name": "genre", "type": "string", "doc": "key to group by song and listening patterns"},
        {"name": "artist", "type": ["null", "string"],
         "doc": "Name of artist, if applicable."},
        {"name": "artistId", "type": ["null", "string"],
         "doc": "Unique identifier for the artist, if applicable."},
        {"name": "playlistId", "type": ["null", "string"],
         "doc": "Unique identifier for the playlist, if applicable."},
        {"name": "duration", "type": ["null", "int"],
         "doc": "Duration of the activity in milliseconds, if applicable."},
        {"name": "userLocation", "type": ["null", "string"],
         "doc": "Location of the user at the time of activity."},
        {"name": "startTime", "type": {"type": "long", "logicalType": "timestamp-millis"},
         "doc": "Start time of the activity period, inclusive."},
        {"name": "endTime", "type": {"type": "long", "logicalType": "timestamp-millis"},
         "doc": "End time of the activity period, exclusive."},
        {"name": "deviceType", "type": {"type": "enum", "name": "DeviceType",
                                        "symbols": ["MOBILE", "DESKTOP", "TABLET", "SMART_SPEAKER"]},
         "doc": "Type of device used for the activity."},
        {"name": "valence", "type": ["null", "float"], "doc": "Measure of musical positivity."},
        {"name": "tempo", "type": ["null", "float"], "doc": "Speed or pace of a given piece."},
        {"name": "acousticness", "type": ["null", "float"], "doc": "Measure of acoustical properties."},
        {"name": "energy", "type": ["null", "float"], "doc": "Measure of intensity and activity."},
        {"name": "danceability", "type": ["null", "float"], "doc": "Measure of how suitable a track is for dancing."}
    ]
}

parsed_schema = parse_schema(schema)

dataset = 'dataset.csv'
data2 = pd.read_csv(dataset)

genres = data2['track_genre'].value_counts()
genre_options = genres.index.tolist()

def generate_records(userId, start_time, end_time):
    activity_types = ["PLAY", "PAUSE", "SKIP", "LIKE", "FOLLOW"]
    device_types = ["MOBILE", "DESKTOP", "TABLET", "SMART_SPEAKER"]
    genre = random.choice(genre_options)
    session_start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
    session_end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
    timestamp = int(datetime.utcnow().timestamp())

    location = fake.country()

    filtered_songs = data2[data2['track_genre'] == genre]
    if not filtered_songs.empty:
        sample = filtered_songs.sample(1).iloc[0]
    else:
        sample = data2.sample(1).iloc[0]

    record = {
        "userId": userId,
        "eventTime": timestamp,
        "activityType": random.choice(activity_types),
        "songId": str(sample['track_id']),
        "track_name": str(sample['track_name']),
        "genre": str(sample['track_genre']),
        "artistId": str(fake.uuid4()),
        "playlistId": str(fake.uuid4()),
        "duration": int(sample['duration_ms']),
        "userLocation": location,
        "startTime": int(session_start.timestamp() * 1000),  # Convert to milliseconds
        "endTime": int(session_end.timestamp() * 1000),  # Convert to milliseconds
        "deviceType": random.choice(device_types),
        "valence": sample.get('valence', None),
        "tempo": sample.get('tempo', None),
        "acousticness": sample.get('acousticness', None),
        "energy": sample.get('energy', None),
        "danceability": sample.get('danceability', None)
    }

    return record


users =[ { 'userId': str(uuid.uuid1()) } for _ in range(0, no_users) ]
records = [ generate_records(user['userId'], start_time, end_time) for _ in range(0, record_count) for user in users ]

records

def serialize_data(file_name, num_records):
    with open(file_name, 'wb') as out:
        fastavro.writer(out, schema, records)
    print(f"Generated {record_count} records into {file_name}")

file_name = 'synthetic_spotify_data.avro'

serialize_data(file_name, record_count)