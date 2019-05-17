select drivers.fullname,count(results.result) as number
from results 
inner join drivers on results.driver_id = drivers.id
where results.season is '1993' and results.result = '1'
group by drivers.fullname
order by number desc