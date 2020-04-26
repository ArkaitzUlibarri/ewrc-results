select results.team,count(results.team) as number
from results 
where results.season is '1993' and results.result = '1'
group by results.team
order by number desc