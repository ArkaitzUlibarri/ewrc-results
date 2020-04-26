select drivers.fullname,count(results.result) as number
from results 
inner join drivers on results.driver_id = drivers.id
where results.season is '1993' and (result = '1' or result = '2' or result = '3')
group by drivers.fullname
order by number desc