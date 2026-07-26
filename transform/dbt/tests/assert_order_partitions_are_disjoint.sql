select accepted.order_id
from {{ ref('accepted_orders') }} as accepted
inner join {{ ref('quarantine_orders') }} as quarantined
    on accepted.order_id = quarantined.order_id
