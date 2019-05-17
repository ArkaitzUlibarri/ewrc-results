select events.season,events.edition,events.name, count(scratchs.stage_name) as count
from events 
inner join scratchs on events.id = scratchs.event_id
where scratchs.driver_id = 848
group by events.season,events.edition
order by season,events.season_event_id asc