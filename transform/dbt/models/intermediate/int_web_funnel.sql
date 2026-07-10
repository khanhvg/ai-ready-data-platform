-- Rolls web_events up to one row per session (funnel-step flags + the
-- checkout event's linked order, when the deterministic checkout-order-link
-- scenario attributed one). Orphaned events (session_id pointing at no real
-- session, see stg_web_events) have no matching row in stg_web_sessions, so
-- they are naturally excluded by the join below -- already surfaced by the
-- stg_web_events warn test upstream.
with session_events as (
    select
        session_id,
        event_type,
        order_id
    from {{ ref('stg_web_events') }}
),

funnel as (
    select
        session_id,
        count(*) as event_count,
        max(case when event_type = 'page_view' then 1 else 0 end) as has_page_view,
        max(case when event_type = 'search' then 1 else 0 end) as has_search,
        max(case when event_type = 'product_view' then 1 else 0 end) as has_product_view,
        max(case when event_type = 'add_to_cart' then 1 else 0 end) as has_add_to_cart,
        max(case when event_type = 'checkout' then 1 else 0 end) as has_checkout,
        max(order_id) as attributed_order_id
    from session_events
    group by session_id
)

select
    s.session_id,
    s.customer_id,
    s.channel,
    s.device,
    s.started_at,
    s.ended_at,
    s.landing_page,
    coalesce(f.event_count, 0) as event_count,
    coalesce(f.has_page_view, 0) as has_page_view,
    coalesce(f.has_search, 0) as has_search,
    coalesce(f.has_product_view, 0) as has_product_view,
    coalesce(f.has_add_to_cart, 0) as has_add_to_cart,
    coalesce(f.has_checkout, 0) as has_checkout,
    f.attributed_order_id
from {{ ref('stg_web_sessions') }} s
left join funnel f on s.session_id = f.session_id
