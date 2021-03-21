SELECT events.season,drivers.fullname,codrivers.fullname,car,team,category,
COUNT(result) AS starts,
SUM(result = '1') AS victories, 
SUM(result = '1' OR result = '2' OR result = '3') AS podiums, 
SUM(CAST(result AS INTEGER) IS NOT result) AS DNF
FROM events
INNER JOIN results ON events.id = results.event_id
INNER JOIN drivers ON results.driver_id = drivers.id
INNER JOIN codrivers ON results.codriver_id = codrivers.id
WHERE drivers.fullname LIKE '%Sainz%' 
GROUP BY events.season
ORDER BY events.season ASC