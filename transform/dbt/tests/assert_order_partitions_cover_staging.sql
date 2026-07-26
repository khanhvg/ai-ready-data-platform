with partitioned as (
    select order_id from {{ ref('accepted_orders') }}
    union all
    select order_id from {{ ref('quarantine_orders') }}
),
coverage_failures as (
    select order_id from {{ ref('stg_orders') }}
    except
    select order_id from partitioned
),
unexpected_rows as (
    select order_id from partitioned
    except
    select order_id from {{ ref('stg_orders') }}
)

select order_id from coverage_failures
union all
select order_id from unexpected_rows
