select drivers.fullname,results.driver_id
from results 
inner join events on results.event_id = events.id
inner join drivers on results.driver_id = drivers.id
where results.season is '1997' and CAST(results.result AS INTEGER) <= 6 AND results.result  GLOB '*[0-9]*'
GROUP BY results.driver_id