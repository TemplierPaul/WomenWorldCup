Create Table out_SQL AS
select STR_TO_DATE(Date, '%d/%m/%Y')                                       AS Date,
       Day,
       DAY(STR_TO_DATE(Date, '%d/%m/%Y'))                                  as MonthDay,
       MONTH(STR_TO_DATE(Date, '%d/%m/%Y'))                                as Month,
       YEAR(STR_TO_DATE(Date, '%d/%m/%Y'))                                 as Year,
       A,
       B,
       `Score A`,
       `Score B`,
       `Score A` - `Score B`                                               as Diff,
       if(`Score A` = `Score B`, 'D', if(`Score B` > `Score A`, 'B', 'A')) as Result
from matches

select Day,
       A
from matches

SELECT Column_name, data_type
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'matches'

select `Date`,
       `Score A`,
       A,
       B,
       Competition,
       A like 'United States' as A_MURICA
from matches

SELECT Column_name, data_type
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'matches'

create table edition select distinct Competition, Competition as New_Competition from matches

select *
from matches left join (select distinct Competition as Comp, Competition as New_Competition from matches) as C on matches.Competition = C.Comp

SELECT COUNT(*) as c FROM matches