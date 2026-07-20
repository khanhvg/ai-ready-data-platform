-- Explicit casts: DuckDB's CSV reader infers column types from sampled data,
-- so a run with zero returns (e.g. a low --max-orders demo-large override)
-- would otherwise type refund_amount/return_date as VARCHAR and break
-- downstream numeric/date aggregates in mart_returns_analysis.
select
    return_id,
    order_id,
    reason,
    cast(refund_amount as double) as refund_amount,
    cast(return_date as date) as return_date
from {{ source('raw', 'returns_refunds') }}
