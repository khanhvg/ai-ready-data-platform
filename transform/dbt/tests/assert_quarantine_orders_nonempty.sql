select 1 as failure
where (select count(*) from {{ ref('quarantine_orders') }}) = 0
