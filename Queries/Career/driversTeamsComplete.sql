select events.season as year,drivers.fullname,car,team,category,COUNT(result) as starts,sum(result = '1') as victories, sum(result = '1' or result = '2' or result = '3') as podiums, sum(CAST(result AS INTEGER) IS NOT result) as DNF
from results
inner join events on results.event_id = events.id
inner join drivers on results.driver_id = drivers.id
where drivers.fullname like '%Panizzi%' 
group by events.season
order by events.season asc