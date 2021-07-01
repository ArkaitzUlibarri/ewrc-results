select ee.team,COUNT(s.driver_id) as count
from scratchs AS s
LEFT JOIN events AS e on s.event_id = e.id
LEFT JOIN entries AS ee on e.id = ee.event_id AND s.driver_id = ee.driver_id
where s.event_id in (select id from events where season is '1993')
group by ee.team
order by count desc