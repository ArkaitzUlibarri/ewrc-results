select  events.season,events.edition,events.name,leaders.stage_number,leaders.stage_name
from events 
inner join leaders on events.id = leaders.event_id
where events.season is '1993' and leaders.driver_id = 848