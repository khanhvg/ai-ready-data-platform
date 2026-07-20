-- Date spine sized to the observed order-date range (min/max across
-- stg_orders), which comfortably covers every other date-typed column in the
-- warehouse (shipments, purchase orders, web sessions all fall within the
-- order window by construction in data-generator/generate.py).
with bounds as (
    select
        min(order_date)::date as min_date,
        max(order_date)::date as max_date
    from {{ ref('stg_orders') }}
),

spine as (
    select unnest(generate_series(
        (select min_date from bounds),
        (select max_date from bounds),
        interval 1 day
    )) as date_day
)

select
    date_day,
    extract(year from date_day) as year,
    extract(quarter from date_day) as quarter,
    extract(month from date_day) as month,
    extract(day from date_day) as day,
    extract(dow from date_day) as day_of_week,
    strftime(date_day, '%A') as day_name,
    strftime(date_day, '%B') as month_name,
    date_trunc('week', date_day)::date as week_start,
    date_trunc('month', date_day)::date as month_start
from spine
