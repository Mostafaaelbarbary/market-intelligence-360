select
    external_product_id,
    product_name,
    category,
    price as market_price,
    rating,
    brand
from {{ source('raw', 'raw_market_data') }}