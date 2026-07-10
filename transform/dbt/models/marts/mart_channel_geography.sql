-- Completed-order revenue by sales channel, region, and city.
select
    o.channel,
    st.region_name,
    st.city,
    count(*) as completed_order_count,
    round(sum(o.order_total), 2) as revenue,
    round(sum(o.order_total) / count(*), 2) as avg_order_value
from {{ ref('fct_orders') }} o
inner join {{ ref('dim_stores') }} st on o.store_id = st.store_id
where o.status = 'completed'
group by o.channel, st.region_name, st.city
order by revenue desc
