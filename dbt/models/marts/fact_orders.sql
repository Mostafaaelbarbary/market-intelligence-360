select
    o.order_id,
    o.customer_id,
    o.product_id,
    o.quantity,
    o.order_date,
    p.price,
    (o.quantity * p.price) as revenue
from {{ ref('stg_orders') }} o
left join {{ ref('stg_products') }} p
    on o.product_id = p.product_id