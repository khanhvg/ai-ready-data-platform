-- Return rate/refund by reason, dominant product category, and region. A
-- returned order can span multiple item categories; each return is tagged
-- with its highest-line-total category (row_number = 1) so refund_amount is
-- counted exactly once per return, not fanned out across every category.
with return_category as (
    select
        r.return_id,
        r.order_id,
        r.reason,
        r.refund_amount,
        p.category_name,
        row_number() over (partition by r.return_id order by oi.line_total desc) as rn
    from {{ ref('fct_returns') }} r
    left join {{ ref('fct_order_items') }} oi on r.order_id = oi.order_id
    left join {{ ref('dim_products') }} p on oi.product_id = p.product_id
),

return_primary as (
    select * from return_category where rn = 1
)

select
    rp.reason,
    rp.category_name,
    st.region_name,
    count(*) as return_count,
    round(sum(rp.refund_amount), 2) as total_refund_amount,
    round(avg(rp.refund_amount), 2) as avg_refund_amount
from return_primary rp
inner join {{ ref('fct_orders') }} o on rp.order_id = o.order_id
inner join {{ ref('dim_stores') }} st on o.store_id = st.store_id
group by rp.reason, rp.category_name, st.region_name
order by total_refund_amount desc
