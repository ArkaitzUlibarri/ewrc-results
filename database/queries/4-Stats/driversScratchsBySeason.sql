select driver_id,drivers.fullname,count(stage_name) as cuenta
from scratchs 
inner join drivers on drivers.id = scratchs.driver_id
where event_id in (select id from events where season is '1993')
group by driver_id
order by cuenta desc