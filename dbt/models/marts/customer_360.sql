with customer_orders as (

    select
        customer_id,
        count(order_id) as total_orders,
        sum(revenue) as total_revenue,
        avg(revenue) as avg_order_value
    from {{ ref('fact_orders') }}
    group by customer_id

),

customer_base as (

    select
        customer_id,
        first_name,
        last_name,
        email,
        country
    from {{ ref('dim_customers') }}

)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.country,
    coalesce(o.total_orders, 0) as total_orders,
    coalesce(o.total_revenue, 0) as total_revenue,
    coalesce(o.avg_order_value, 0) as avg_order_value
from customer_base c
left join customer_orders o
    on c.customer_id = o.customer_id