select driver_id,drivers.fullname,count(stage_name) as count
from leaders 
inner join drivers on drivers.id = leaders.driver_id
where event_id in (select id from events where season is '1993')
group by driver_id
order by count desc