## Schema Details

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
