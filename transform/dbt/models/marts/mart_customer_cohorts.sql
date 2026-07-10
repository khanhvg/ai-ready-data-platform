-- Monthly signup-cohort view: customer volume and lifetime revenue per cohort,
-- broken out by loyalty tier for the customer-demo narrative.
with cohorts as (
    select
        customer_id,
        loyalty_tier,
        date_trunc('month', signup_date::date) as cohort_month
    from {{ ref('dim_customers') }}
),

customer_revenue as (
    select
        customer_id,
        sum(order_total) as lifetime_revenue,
        count(*) as completed_orders
    from {{ ref('fct_orders') }}
    where status = 'completed'
    group by customer_id
)

select
    c.cohort_month,
    c.loyalty_tier,
    count(distinct c.customer_id) as customer_count,
    coalesce(sum(cr.completed_orders), 0) as total_orders,
    round(coalesce(sum(cr.lifetime_revenue), 0), 2) as total_revenue,
    round(coalesce(sum(cr.lifetime_revenue), 0) / count(distinct c.customer_id), 2) as revenue_per_customer
from cohorts c
left join customer_revenue cr on c.customer_id = cr.customer_id
group by c.cohort_month, c.loyalty_tier
order by c.cohort_month, c.loyalty_tier
