select s.id,s.event_id,e.name,s.stage_number,s.stage_name,s.driver_id,d.fullname,ee.team,ee.car
from scratchs AS s
LEFT JOIN drivers AS d on d.id = s.driver_id
LEFT JOIN events AS e on s.event_id = e.id
LEFT JOIN entries AS ee on e.id = ee.event_id AND s.driver_id = ee.driver_id
where s.event_id in (select id from events where season is '1993')