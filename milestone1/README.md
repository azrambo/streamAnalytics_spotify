# Milestone 1: Designing A Data Feed for Spotify Wrapped

## Description
This project's first milestone tackles data generation in a specific format that supports the performance of structurization in the streaming context. 
Through AVRO schema design, the data generation attempts to assimilate real-life behaviors an patterns expected in spotify's daily users.

### Objectives
- Develop an AVRO schema for the Spotify Wrapped data feed, defining data structures for song plays, user interactions, and other relevant data points.

- Create scripts to generate synthetic data simulating the streaming experiences of both a single user and multiple, independent users. This involves producing realistic, time-series data reflecting typical user interaction patterns with a music streaming service.

## Getting Started

### Dependencies

The dependencies present in the project are not listed as requirements, but will be installed automatically in `main.py` to function. The dependencies are:

* `fastavro` for schema parsing and data serialization.
* `Faker` for assistance in synthetic data generation.
* `pandas` and `numpy` for data wrangling and structurization.

### Installation
- The files must be in the same directory in order for the reference of `dataset.csv` to properly work, and this way the path of the data refers to it directly without the need of defining a path.

### Execution
- How to run the program:
    - Download `dataset.csv`, and `main.py`.
    - Direct to your terminal and then run `main.py`. Make sure the `dataset.csv` file is in the same directory as `main.py`.

For Unix/Linux/Mac
```bash
echo "Running main script..."
python main.py
```

For Windows
```batch
@echo off
echo Running main script...
python main.py
```
- Program's Parameter Manipulation:

     - The program maintains personalizable parameters to define the number of users and the number of records that will be participating in the data generation for the AVRO file. This way, the configuration allows generation of AVRO files for a single user with multiple records as well as multiple users and records.
     - The parameters can be manipulated by chaging `num_users` and `record_count`.

## Design of the Synthetic Data Generation Scripts

- **Namespace**: `com.spotify.wrapped`
- **Type**: `record`
- **Name**: `UserActivity`

## Fields

| Field Name    | Type                 | Description                                              |
|---------------|----------------------|----------------------------------------------------------|
| `userId`      | `string`             | Unique identifier for the user.                          |
| `eventTime`   | `long` (timestamp)   | The timestamp when activity occurred, in milliseconds    |
| `activityType`| `enum`               | Type of activity performed. values: `PLAY`, `PAUSE`, `SKIP`, `LIKE`, `FOLLOW`. |
| `song`        | `string` (nullable)  | Name of song, if applicable.                             |
| `songId`      | `string` (nullable)  | Unique identifier for the song, if applicable.           |
| `genre`       | `string`             | Key to group by song and listening patterns.             |
| `artist`      | `string` (nullable)  | Name of artist, if applicable.                           |
| `artistId`    | `string` (nullable)  | Unique identifier for the artist, if applicable.         |
| `playlistId`  | `string` (nullable)  | Unique identifier for the playlist, if applicable.       |
| `duration`    | `int` (nullable)     | Duration of the activity in milliseconds, if applicable. |
| `userLocation`| `string` (nullable)  | Location of the user at the time of activity.            |
| `startTime`   | `long` (timestamp)   | Start time of the activity period, inclusive.            |
| `endTime`     | `long` (timestamp)   | End time of the activity period, exclusive.              |
| `deviceType`  | `enum`               | Type of device used. values: `MOBILE`, `DESKTOP`, `TABLET`, `SMART_SPEAKER`. |
| `valence`     | `float` (nullable)   | Measure of musical positivity.                           |
| `tempo`       | `float` (nullable)   | Speed or pace of a given piece.                          |
| `acousticness`| `float` (nullable)   | Measure of acoustical properties.                        |
| `energy`      | `float` (nullable)   | Measure of intensity and activity.                       |
| `danceability`| `float` (nullable)   | Measure of how suitable a track is for dancing.          |

## Challenges Encountered
The synthetic data should behave in a realistic and predictable pattern per user, emphasizing consistency among a user's preference and behavior in the context of musical interests. Opting for defining a user's interests and maintaining these behaviors and patterns consistent among the numerous records gave major difficulty. 

Out of that data ingestion partitions (User Activity, User Information, and Song Metadata), the most challenging phases were both user activity and song metadata. Being able to properly match a song with the user's predefined genre preference showed many constraints towards indexing the chosen track along with its metadata information. Furthermore, it is understandable how user activity highly depends on genre preference. Still, assigning a user's specific actions based on the genre which might not match an interest also gave a lot of constraints.

Overall, these challenges encountered emerged from the projects vision and planning towards the proper alignment of the synthetic data with the project's realistic Spotify data context. Most of these challenges relate to the expectation of a single user maintaining their personality and user information genuine and consistent, which is what the team strives for given that the data generation is still a work in progress.

## Synthetic Data Alignment to Context

The parsed schema contains a set of values specifically related to the data requirements to stablish a user's Spotify Wrapped. From this context, the synthetic data can be partitioned into user activity, user information, and song metadata (including artists and song measurements). These partitions allowed a clearer vision towards the data fields needed to define a user's personality based on their preferences and behavioural patterns. 

The generation of synthetic data properly aligns with the parsed schema as true values from the `dataset.csv` to match a user's song choice (which is based from predetermined genre dominant preference) along with the proper song metadata and artist. This way, a user will contain multiple number of records that will create a structure and an idea of a specific user's personality. 

## Next Steps
Given the unexpected realization of the complexity in data generation, the primary objective will be to explore the alternatives into creating a user's personality into the matching probabilities of 16 possible personalities in order to make patterns more logical and attached to a specific behavior.

Furthermore, the team aims to research more within the aspect of adding more user information data and diversify the data sources available for an increase in the versatility of data fields required to support the membership of the 16 personalities possible.
