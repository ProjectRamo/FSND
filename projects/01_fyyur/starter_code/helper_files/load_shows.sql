
INSERT INTO "Show"( id,date_time, venue_id, artist_id)
VALUES (1, timestamp '"2019-05-21 21:30:00"', 1, 4)
RETURNING *;

INSERT INTO "Show"( id,date_time, venue_id, artist_id)
VALUES (2, timestamp '"2019-05-15 23:00:00"', 3, 5)
RETURNING *;

