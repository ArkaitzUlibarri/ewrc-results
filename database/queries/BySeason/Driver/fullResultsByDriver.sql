SELECT events.season_event_id as ID,events.edition,events.name,results.car_number,drivers.fullname,codrivers.fullname,results.plate,results.car,results.team,results.result
FROM events 
LEFT JOIN results on events.id = results.event_id
LEFT JOIN drivers on results.driver_id = drivers.id
LEFT JOIN codrivers on results.codriver_id = codrivers.id 
WHERE  events.season='1993' and drivers.id = 848
ORDER BY events.season,events.season_event_id