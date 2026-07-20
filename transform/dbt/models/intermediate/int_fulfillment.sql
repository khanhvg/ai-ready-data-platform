-- lead_time_days is only computed when delivered_date is non-null -- the
-- ~8% in-transit scenario (stg_shipments) intentionally has no delivered_date
-- yet, so it stays null here rather than being backfilled.
select
    sh.shipment_id,
    sh.order_id,
    sh.carrier,
    sh.ship_date,
    sh.delivered_date,
    sh.ship_status,
    case
        when sh.delivered_date is not null
            then date_diff('day', sh.ship_date::date, sh.delivered_date::date)
    end as lead_time_days,
    sh.ship_status = 'delivered' as is_on_time,
    sh.ship_status = 'delayed' as is_delayed,
    sh.ship_status = 'in_transit' as is_in_transit,
    r.return_id,
    r.reason as return_reason,
    r.refund_amount,
    r.return_date,
    r.return_id is not null as is_returned
from {{ ref('stg_shipments') }} sh
left join {{ ref('stg_returns_refunds') }} r on sh.order_id = r.order_id
