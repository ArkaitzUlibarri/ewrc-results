select car,team,count(team) as number
from results 
where season is '1993' and (result = '1' or result = '2' or result = '3')
group by team
order by number desc