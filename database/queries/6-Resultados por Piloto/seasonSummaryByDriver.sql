select drivers.fullname,car,team,category,COUNT(result) as starts,sum(result = '1') as victories, sum(result = '1' or result = '2' or result = '3') as podiums, sum(CAST(result AS INTEGER) IS NOT result) as DNF,count(scratchs.id) as scratchs
from results
inner join drivers on results.driver_id = drivers.id
inner join events on results.event_id = events.id
inner join scratchs on scratchs.event_id = events.id
where drivers.fullname like '%Sainz%' and events.season is '1993'