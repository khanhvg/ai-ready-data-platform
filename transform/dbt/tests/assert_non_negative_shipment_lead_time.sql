-- Fails if any delivered shipment has a negative lead time. In-transit
-- shipments (~8% rate, null delivered_date) are excluded by design -- they
-- are a controlled scenario, not a defect (see data-generator/schema.md).
select shipment_id, order_id, ship_date, delivered_date, lead_time_days
from {{ ref('fct_shipments') }}
where delivered_date is not null
  and lead_time_days < 0
