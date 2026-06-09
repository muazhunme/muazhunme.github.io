# Data Dictionary

Main processed file:

```text
data/processed/order_risk_modeling.csv
```

Additional processed files:

```text
data/processed/order_risk_pre_delivery.csv
data/processed/order_risk_post_delivery.csv
```

The pre-delivery file removes delivery outcome columns that would not be known before the customer receives the order. The post-delivery file keeps them.

Target:

| Column | Meaning |
|---|---|
| `bad_review` | Binary target. `1` when review score is 1 or 2, otherwise `0`. |
| `review_score` | Original customer review score from 1 to 5. Kept for analysis, removed during classification training. |

Identifiers:

| Column | Meaning |
|---|---|
| `order_id` | Unique order identifier. Removed before model training. |

Order and delivery features:

| Column | Meaning |
|---|---|
| `order_status` | Final order status. |
| `delivery_time_days` | Days between purchase and customer delivery. |
| `estimated_delivery_days` | Days between purchase and estimated delivery date. |
| `delivery_delay_days` | Days delivered after estimated delivery. Negative means early. |
| `approval_time_hours` | Hours between purchase and approval. |
| `is_late` | `1` if delivered after estimated delivery date. |
| `purchase_month` | Purchase month. |
| `purchase_dayofweek` | Day of week, where Monday is 0. |
| `purchase_hour` | Purchase hour of day. |

Item and seller features:

| Column | Meaning |
|---|---|
| `order_item_count` | Number of items in the order. |
| `total_price` | Sum of item prices. |
| `total_freight` | Sum of freight charges. |
| `avg_price` | Average item price. |
| `seller_count` | Number of unique sellers in the order. |
| `product_count` | Number of unique products in the order. |
| `seller_state` | Seller state code. |
| `same_state_seller_customer` | `1` if seller and customer are in the same state. |

Payment features:

| Column | Meaning |
|---|---|
| `payment_value` | Total payment value for the order. |
| `payment_installments` | Maximum number of installments used. |
| `payment_type_count` | Number of payment types used. |
| `primary_payment_type` | Most common payment type for the order. |

Product features:

| Column | Meaning |
|---|---|
| `product_category` | English product category when available. |
| `product_name_lenght` | Product name length from source data. |
| `product_description_lenght` | Product description length from source data. |
| `product_photos_qty` | Number of product photos. |
| `product_weight_g` | Product weight in grams. |
| `product_volume_cm3` | Product length x height x width. |

Customer location features:

| Column | Meaning |
|---|---|
| `customer_state` | Customer state code. |
| `customer_city` | Customer city. |

Derived cost feature:

| Column | Meaning |
|---|---|
| `freight_ratio` | Freight cost divided by item price. |

Historical prior-risk features:

| Column Pattern | Meaning |
|---|---|
| `seller_prior_order_count` | Number of previous orders for the seller at the time of purchase. |
| `seller_prior_bad_review_rate` | Seller's previous bad-review rate before this order. |
| `seller_prior_late_rate` | Seller's previous late-delivery rate before this order. |
| `seller_prior_avg_delay_days` | Seller's previous average delivery delay before this order. |
| `category_prior_*` | Same historical features grouped by product category. |
| `customer_state_prior_*` | Same historical features grouped by customer state. |
| `seller_state_prior_*` | Same historical features grouped by seller state. |

These features are calculated using prior orders in time order, which is safer than calculating group averages using the full dataset.

## Training Exclusions

The baseline training script excludes:

- `order_id`, because it is an identifier.
- `review_score`, because it directly creates the target and would leak the answer.
