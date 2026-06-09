import numpy as np
import pandas as pd

from config import (
    MODEL_DATASET,
    POST_DELIVERY_DATASET,
    PRE_DELIVERY_DATASET,
    PROCESSED_DIR,
    RAW_DIR,
    TEMPORAL_DATASET,
)


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / name)


def parse_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def add_prior_group_features(
    df: pd.DataFrame,
    group_column: str,
    prefix: str,
) -> pd.DataFrame:
    ordered = df.sort_values("order_purchase_timestamp").copy()
    grouped = ordered.groupby(group_column, dropna=False)
    delay_filled = ordered["delivery_delay_days"].fillna(0)

    prior_count = grouped.cumcount()
    prior_bad_sum = grouped["bad_review"].cumsum() - ordered["bad_review"]
    prior_late_sum = grouped["is_late"].cumsum() - ordered["is_late"]
    prior_delay_sum = delay_filled.groupby(ordered[group_column], dropna=False).cumsum() - delay_filled

    ordered[f"{prefix}_prior_order_count"] = prior_count
    ordered[f"{prefix}_prior_bad_review_rate"] = prior_bad_sum / prior_count.replace(0, np.nan)
    ordered[f"{prefix}_prior_late_rate"] = prior_late_sum / prior_count.replace(0, np.nan)
    ordered[f"{prefix}_prior_avg_delay_days"] = prior_delay_sum / prior_count.replace(0, np.nan)

    feature_columns = [
        "order_id",
        f"{prefix}_prior_order_count",
        f"{prefix}_prior_bad_review_rate",
        f"{prefix}_prior_late_rate",
        f"{prefix}_prior_avg_delay_days",
    ]
    return df.merge(ordered[feature_columns], on="order_id", how="left")


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    orders = load_csv("olist_orders_dataset.csv")
    reviews = load_csv("olist_order_reviews_dataset.csv")
    items = load_csv("olist_order_items_dataset.csv")
    payments = load_csv("olist_order_payments_dataset.csv")
    products = load_csv("olist_products_dataset.csv")
    customers = load_csv("olist_customers_dataset.csv")
    sellers = load_csv("olist_sellers_dataset.csv")
    translations = load_csv("product_category_name_translation.csv")

    orders = parse_dates(
        orders,
        [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    reviews = reviews.sort_values("review_creation_date").drop_duplicates("order_id", keep="last")
    reviews["bad_review"] = (reviews["review_score"] <= 2).astype(int)

    item_features = (
        items.groupby("order_id")
        .agg(
            order_item_count=("order_item_id", "max"),
            total_price=("price", "sum"),
            total_freight=("freight_value", "sum"),
            avg_price=("price", "mean"),
            seller_count=("seller_id", "nunique"),
            product_count=("product_id", "nunique"),
        )
        .reset_index()
    )

    first_item = (
        items.sort_values(["order_id", "order_item_id"])
        .drop_duplicates("order_id")[["order_id", "product_id", "seller_id"]]
    )

    payment_features = (
        payments.groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments=("payment_installments", "max"),
            payment_type_count=("payment_type", "nunique"),
            primary_payment_type=("payment_type", lambda s: s.mode().iat[0] if not s.mode().empty else "unknown"),
        )
        .reset_index()
    )

    products = products.merge(translations, on="product_category_name", how="left")
    products["product_category"] = products["product_category_name_english"].fillna(
        products["product_category_name"]
    )
    products["product_volume_cm3"] = (
        products["product_length_cm"]
        * products["product_height_cm"]
        * products["product_width_cm"]
    )
    product_features = products[
        [
            "product_id",
            "product_category",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_volume_cm3",
        ]
    ]

    seller_features = sellers[["seller_id", "seller_state"]]
    customer_features = customers[["customer_id", "customer_state", "customer_city"]]

    dataset = (
        orders.merge(reviews[["order_id", "review_score", "bad_review"]], on="order_id", how="inner")
        .merge(item_features, on="order_id", how="left")
        .merge(first_item, on="order_id", how="left")
        .merge(payment_features, on="order_id", how="left")
        .merge(product_features, on="product_id", how="left")
        .merge(seller_features, on="seller_id", how="left")
        .merge(customer_features, on="customer_id", how="left")
    )

    dataset["delivery_time_days"] = (
        dataset["order_delivered_customer_date"] - dataset["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    dataset["estimated_delivery_days"] = (
        dataset["order_estimated_delivery_date"] - dataset["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    dataset["delivery_delay_days"] = (
        dataset["order_delivered_customer_date"] - dataset["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    dataset["approval_time_hours"] = (
        dataset["order_approved_at"] - dataset["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600
    dataset["is_late"] = (dataset["delivery_delay_days"] > 0).astype(int)
    dataset["purchase_month"] = dataset["order_purchase_timestamp"].dt.month
    dataset["purchase_dayofweek"] = dataset["order_purchase_timestamp"].dt.dayofweek
    dataset["purchase_hour"] = dataset["order_purchase_timestamp"].dt.hour
    dataset["same_state_seller_customer"] = (
        dataset["seller_state"] == dataset["customer_state"]
    ).astype(int)
    dataset["freight_ratio"] = dataset["total_freight"] / dataset["total_price"].replace(0, np.nan)

    for group_column, prefix in [
        ("seller_id", "seller"),
        ("product_category", "category"),
        ("customer_state", "customer_state"),
        ("seller_state", "seller_state"),
    ]:
        dataset = add_prior_group_features(dataset, group_column, prefix)

    modeling_columns = [
        "order_id",
        "order_purchase_timestamp",
        "bad_review",
        "review_score",
        "order_status",
        "order_item_count",
        "total_price",
        "total_freight",
        "avg_price",
        "seller_count",
        "product_count",
        "payment_value",
        "payment_installments",
        "payment_type_count",
        "primary_payment_type",
        "product_category",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_volume_cm3",
        "seller_state",
        "customer_state",
        "customer_city",
        "delivery_time_days",
        "estimated_delivery_days",
        "delivery_delay_days",
        "approval_time_hours",
        "is_late",
        "purchase_month",
        "purchase_dayofweek",
        "purchase_hour",
        "same_state_seller_customer",
        "freight_ratio",
        "seller_prior_order_count",
        "seller_prior_bad_review_rate",
        "seller_prior_late_rate",
        "seller_prior_avg_delay_days",
        "category_prior_order_count",
        "category_prior_bad_review_rate",
        "category_prior_late_rate",
        "category_prior_avg_delay_days",
        "customer_state_prior_order_count",
        "customer_state_prior_bad_review_rate",
        "customer_state_prior_late_rate",
        "customer_state_prior_avg_delay_days",
        "seller_state_prior_order_count",
        "seller_state_prior_bad_review_rate",
        "seller_state_prior_late_rate",
        "seller_state_prior_avg_delay_days",
    ]

    modeling = dataset[modeling_columns].copy()
    modeling = modeling.replace([np.inf, -np.inf], np.nan)
    modeling.to_csv(TEMPORAL_DATASET, index=False)
    modeling_for_training = modeling.drop(columns=["order_purchase_timestamp"])
    modeling_for_training.to_csv(MODEL_DATASET, index=False)

    pre_delivery_columns = [
        column
        for column in modeling.columns
        if column
        not in {
            "delivery_time_days",
            "delivery_delay_days",
            "is_late",
        }
    ]
    post_delivery_columns = modeling.columns.tolist()

    modeling[pre_delivery_columns].drop(columns=["order_purchase_timestamp"]).to_csv(
        PRE_DELIVERY_DATASET,
        index=False,
    )
    modeling[post_delivery_columns].drop(columns=["order_purchase_timestamp"]).to_csv(
        POST_DELIVERY_DATASET,
        index=False,
    )

    print(f"Saved {len(modeling_for_training):,} rows and {len(modeling_for_training.columns):,} columns")
    print(f"Bad review rate: {modeling['bad_review'].mean():.2%}")
    print(f"Output: {MODEL_DATASET}")
    print(f"Temporal output: {TEMPORAL_DATASET}")
    print(f"Pre-delivery output: {PRE_DELIVERY_DATASET}")
    print(f"Post-delivery output: {POST_DELIVERY_DATASET}")


if __name__ == "__main__":
    main()
