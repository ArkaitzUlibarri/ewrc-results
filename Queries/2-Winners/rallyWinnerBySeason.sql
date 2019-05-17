SELECT events.season_event_id as ID,events.edition,events.name,drivers.fullname,results.car,results.team
FROM events 
LEFT JOIN results on events.id = results.event_id 
LEFT JOIN drivers on results.driver_id = drivers.id 
WHERE events.season='1993' and results.result like '1' 
ORDER BY season_event_id