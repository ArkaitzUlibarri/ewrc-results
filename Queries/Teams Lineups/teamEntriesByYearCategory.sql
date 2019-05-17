select entries.car,entries.team,drivers.fullname,count(entries.team) as number,entries.category
from entries 
inner join events on entries.event_id = events.id
inner join drivers on entries.driver_id = drivers.id
where events.season is '1993' and entries.team IS NOT NULL
group by drivers.fullname,entries.team,entries.category
order by category,team,number desc