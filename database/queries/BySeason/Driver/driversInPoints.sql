select events.name,results.dorsal,results.car,results.team,drivers.fullname,results.result
from results 
inner join events on results.event_id = events.id
inner join drivers on results.driver_id = drivers.id
where results.season is '1997' and CAST(results.result AS INTEGER) <= 6 AND results.result  GLOB '*[0-9]*'
order by events.name,results.result asc