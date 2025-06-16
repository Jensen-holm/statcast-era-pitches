SELECT game_date, bat_speed, swing_length
FROM pitches
WHERE
    YEAR(game_date) =?
    AND bat_speed IS NOT NULL
LIMIT 10;