SELECT events.season_event_id as ID,events.edition,events.name,results.dorsal,drivers.fullname,results.plate,results.car,results.team,results.result
FROM events 
LEFT JOIN results on events.id = results.event_id
LEFT JOIN drivers on results.driver_id = drivers.id 
WHERE  events.season='1995' and drivers.id = 1398
ORDER BY events.season,events.season_event_id