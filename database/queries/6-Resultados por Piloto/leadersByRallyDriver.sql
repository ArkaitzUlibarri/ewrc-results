select events.season,events.edition,events.name, count(leaders.stage_name) as count
from events 
inner join leaders on events.id = leaders.event_id
where leaders.driver_id = 848
group by events.season,events.edition
order by season,events.season_event_id asc