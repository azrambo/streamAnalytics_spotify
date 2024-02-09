import fastavro
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from fastavro import parse_schema
import uuid
from datasets import load_dataset


# Initialize Faker
fake = Faker()

genre = load_dataset('khepplewhite/SpotifyData')

genre.features



# +
sample_names = ['Alice Johnson', 'Bob Smith', 'Carol Williams']

# Custom Provider
class CustomNameProvider(BaseProvider):
    def sample_name(self):
        return random.choice(sample_names)

# Create a Faker instance and add the custom provider
fake = Faker()
fake.add_provider(CustomNameProvider)

# Generate data using the custom provider
for _ in range(5):
    print(fake.sample_name())
# -

# ### NameSpace: com.spotify.wrapped
# ### name: UserActivity

# Define your AVRO schema
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
        {"name": "songId", "type": ["null", "string"],
         "doc": "Unique identifier for the song, if applicable."},
        {"name": "genre", "type": "string", "doc": "key to group by song and listening patterns"},
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
         "doc": "Type of device used for the activity."}
    ]
}

parsed_schema = parse_schema(schema)
parsed_schema['fields']


def generate_records(userId):
    activity_types = ["PLAY", "PAUSE", "SKIP", "LIKE", "FOLLOW"]
    device_types = ["MOBILE", "DESKTOP", "TABLET", "SMART_SPEAKER"]
    
    record =  {
        "userId": userId,
        "eventTime": int(datetime.utcnow().timestamp()),
        "activityType": random.choice(activity_types),
        "songId": fake.uuid4() if random.choice([True, False]) else None,
        "genre": random.choice(["Pop", "Rock", "Jazz", "Classical", "Electronic"]),
        "artistId": fake.uuid4() if random.choice([True, False]) else None,
        "playlistId": fake.uuid4() if random.choice([True, False]) else None,
        "duration": random.randint(1000, 300000) if random.choice([True, False]) else None,
        "userLocation": fake.country(),
        "startTime": int(datetime.utcnow().timestamp()),
        "endTime": int(datetime.utcnow().timestamp()),
        "deviceType": random.choice(device_types)
                        }
                        
    return record

# Below the parameters of number of users and records can be personalized

no_users = 100
record_count = 100

# +
users =[ { 'userId': str(uuid.uuid1()) } for _ in range(0,no_users) ]
records = [ generate_records(user['userId']) for _ in range(0, record_count) for user in users ]

len(records)
# -

top_3_records_generated = records[0:3]
top_3_records_generated


def serialize_data(file_name, num_records):
    with open(file_name, 'wb') as out:
        fastavro.writer(out, schema, records)

# +
file_name = 'synthetic_spotify_data.avro'    
    
serialize_data(file_name, record_count)
print(f"Generated {record_count} records into {file_name}")

# +
with open('synthetic_spotify_data.avro', 'rb') as out:
    schema_plus_record=out.read()

schema_plus_record[:1000]
# -

len(schema_plus_record), len(schema_plus_record)/(2**10)
