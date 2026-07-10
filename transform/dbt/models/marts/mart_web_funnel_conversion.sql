-- Session -> event -> order conversion by device and channel. Sources from
-- int_web_funnel (session-grain funnel rollup) rather than a core dimension,
-- since web sessions aren't promoted to a dedicated dim in this model --
-- int_web_funnel is the single reusable join for this mart.
select
    f.channel,
    f.device,
    count(*) as session_count,
    sum(f.has_checkout) as checkout_session_count,
    count(distinct case when o.order_id is not null then f.session_id end) as converted_session_count,
    round(
        100.0 * count(distinct case when o.order_id is not null then f.session_id end) / count(*),
        1
    ) as conversion_pct,
    round(coalesce(sum(o.order_total), 0), 2) as attributed_revenue
from {{ ref('int_web_funnel') }} f
left join {{ ref('fct_orders') }} o
    on f.attributed_order_id = o.order_id and o.status = 'completed'
group by f.channel, f.device
order by conversion_pct desc
