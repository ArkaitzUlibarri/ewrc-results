select  events.season,events.edition,events.name,scratchs.stage_number,scratchs.stage_name
from events 
inner join scratchs on events.id = scratchs.event_id
where events.season is '1993' and scratchs.driver_id = 848