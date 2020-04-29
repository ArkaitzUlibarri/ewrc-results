SELECT images.event_id,events.season,events.name, count(images.event_id) AS counter
FROM images
LEFT JOIN events ON images.event_id = events.id
GROUP BY images.event_id
ORDER BY events.season