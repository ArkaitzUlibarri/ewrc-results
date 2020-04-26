SELECT events.season,events.season_event_id as ID,events.edition,events.name,drivers.fullname,results.car,results.team
FROM events 
LEFT JOIN results on events.id = results.event_id AND results.result like '1' 
LEFT JOIN drivers on results.driver_id = drivers.id 
WHERE events.season='1993' 
ORDER BY events.season,events.season_event_id