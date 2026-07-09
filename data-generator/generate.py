#!/usr/bin/env python3
"""Deterministic, multi-table synthetic retail data generator.

Writes CSV files to data/raw/ plus a manifest.json describing the run
(profile, seed, row counts, checksums, quality summary). All randomness
flows through a single seeded random.Random instance so the same
--seed/--profile always reproduces byte-identical output.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from faker import Faker

SCALE_PROFILES = {
    "small": dict(customers=200, products=150, stores=20, orders=1_000),
    "medium": dict(customers=2_000, products=500, stores=50, orders=15_000),
    "large": dict(customers=20_000, products=2_000, stores=150, orders=150_000),
}

# Controlled data-quality scenario rates (fraction of rows affected).
DUPLICATE_RATE = 0.004
NULL_OPTIONAL_RATE = 0.03
INVALID_STATUS_RATE = 0.01
LATE_ARRIVING_RATE = 0.02
ORPHAN_FK_RATE = 0.004

VALID_ORDER_STATUSES = ["completed", "cancelled", "returned", "pending"]
INVALID_ORDER_STATUS_VALUES = ["UNKNOWN", "N/A", "error", ""]
PAYMENT_METHODS = ["credit_card", "debit_card", "cash", "digital_wallet", "bank_transfer"]
LOYALTY_TIERS = ["bronze", "silver", "gold", "platinum"]
LOYALTY_TIER_WEIGHTS = [0.50, 0.30, 0.15, 0.05]
CHANNELS = ["online", "offline"]
STORE_TYPES = ["flagship", "standard", "outlet", "online"]

REGIONS = [
    {"region": "North America", "cities": ["New York", "Toronto", "Chicago", "Vancouver"]},
    {"region": "Europe", "cities": ["London", "Berlin", "Paris", "Amsterdam"]},
    {"region": "Southeast Asia", "cities": ["Ho Chi Minh City", "Hanoi", "Bangkok", "Singapore"]},
    {"region": "East Asia", "cities": ["Tokyo", "Seoul", "Taipei"]},
    {"region": "Oceania", "cities": ["Sydney", "Auckland"]},
]

CATEGORIES = [
    {"name": "Apparel", "min_price": 15.0, "max_price": 150.0},
    {"name": "Footwear", "min_price": 25.0, "max_price": 220.0},
    {"name": "Electronics", "min_price": 20.0, "max_price": 1200.0},
    {"name": "Home & Kitchen", "min_price": 10.0, "max_price": 400.0},
    {"name": "Beauty & Personal Care", "min_price": 5.0, "max_price": 90.0},
    {"name": "Sports & Outdoors", "min_price": 12.0, "max_price": 350.0},
    {"name": "Toys & Games", "min_price": 8.0, "max_price": 120.0},
    {"name": "Groceries", "min_price": 2.0, "max_price": 45.0},
]

# Seasonality: relative order-volume weight per calendar month (index 0 = Jan).
MONTH_SEASONALITY = [0.7, 0.65, 0.75, 0.8, 0.85, 0.9, 0.95, 0.9, 0.85, 1.0, 1.3, 1.6]

RETURN_REASONS = [
    "wrong_size", "defective", "not_as_described", "changed_mind", "late_delivery", "duplicate_order",
]
REVIEW_TEXTS = [
    "Great quality, would buy again.",
    "Arrived late but product is good.",
    "Not what I expected, packaging was damaged.",
    "Excellent value for the price.",
    "Works as advertised.",
    "Customer service was very helpful.",
    "Would not recommend, quality issues.",
    "Perfect fit and fast shipping.",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def daterange_days(start: date, end: date) -> int:
    return (end - start).days


@dataclass
class GenContext:
    rnd: random.Random
    faker: Faker
    profile: str
    seed: int
    order_start: date
    order_end: date


def build_regions_and_stores(ctx: GenContext, n_stores: int):
    regions = []
    for i, r in enumerate(REGIONS, start=1):
        regions.append({"region_id": i, "region_name": r["region"], "cities": r["cities"]})

    stores = []
    for store_id in range(1, n_stores + 1):
        region = ctx.rnd.choice(regions)
        city = ctx.rnd.choice(region["cities"])
        channel = "online" if ctx.rnd.random() < 0.2 else "offline"
        store_type = "online" if channel == "online" else ctx.rnd.choice(
            ["flagship", "standard", "outlet"]
        )
        stores.append(
            {
                "store_id": store_id,
                "store_name": f"{region['region_name'].split()[0]} {store_type.title()} {store_id}",
                "store_type": store_type,
                "channel": channel,
                "region_id": region["region_id"],
                "city": city,
            }
        )
    return regions, stores


def build_categories_and_products(ctx: GenContext, n_products: int):
    categories = []
    for i, c in enumerate(CATEGORIES, start=1):
        categories.append(
            {
                "category_id": i,
                "category_name": c["name"],
                "min_price": c["min_price"],
                "max_price": c["max_price"],
            }
        )

    products = []
    for product_id in range(1, n_products + 1):
        cat = ctx.rnd.choice(categories)
        price = round(ctx.rnd.uniform(cat["min_price"], cat["max_price"]), 2)
        sku = f"SKU-{cat['category_id']:02d}-{product_id:06d}"
        products.append(
            {
                "product_id": product_id,
                "sku": sku,
                "product_name": f"{cat['category_name']} Item {product_id}",
                "category_id": cat["category_id"],
                "unit_price": price,
                "is_active": ctx.rnd.random() > 0.03,
            }
        )
    return categories, products


def build_customers(ctx: GenContext, n_customers: int, regions):
    customers = []
    signup_start = ctx.order_start - timedelta(days=730)
    signup_span = daterange_days(signup_start, ctx.order_end)
    for customer_id in range(1, n_customers + 1):
        region = ctx.rnd.choice(regions)
        city = ctx.rnd.choice(region["cities"])
        tier = ctx.rnd.choices(LOYALTY_TIERS, weights=LOYALTY_TIER_WEIGHTS, k=1)[0]
        signup_date = signup_start + timedelta(days=ctx.rnd.randint(0, signup_span))
        first = ctx.faker.first_name()
        last = ctx.faker.last_name()
        email = f"{first.lower()}.{last.lower()}{customer_id}@example.test"
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first,
                "last_name": last,
                "email": email,
                "region_id": region["region_id"],
                "city": city,
                "loyalty_tier": tier,
                "signup_date": signup_date.isoformat(),
                "is_active": ctx.rnd.random() > 0.05,
            }
        )
    return customers


def build_promotions(ctx: GenContext):
    campaigns = [
        ("New Year Sale", 1, 15, 0.10, 0.20),
        ("Spring Refresh", 60, 90, 0.05, 0.15),
        ("Summer Clearance", 170, 200, 0.10, 0.25),
        ("Back to School", 220, 245, 0.05, 0.15),
        ("Black Friday", 320, 328, 0.20, 0.40),
        ("Holiday Season", 335, 360, 0.10, 0.30),
    ]
    promotions = []
    year = ctx.order_start.year
    for i, (name, start_doy, end_doy, min_d, max_d) in enumerate(campaigns, start=1):
        start = date(year, 1, 1) + timedelta(days=start_doy - 1)
        end = date(year, 1, 1) + timedelta(days=end_doy - 1)
        promotions.append(
            {
                "promotion_id": i,
                "promo_name": name,
                "discount_pct": round(ctx.rnd.uniform(min_d, max_d), 2),
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "channel": ctx.rnd.choice(["online", "offline", "all"]),
            }
        )
    return promotions


def month_weighted_date(ctx: GenContext) -> date:
    total_days = daterange_days(ctx.order_start, ctx.order_end)
    weights = []
    days = []
    d = ctx.order_start
    for offset in range(total_days + 1):
        d = ctx.order_start + timedelta(days=offset)
        weights.append(MONTH_SEASONALITY[d.month - 1])
        days.append(d)
    return ctx.rnd.choices(days, weights=weights, k=1)[0]


def active_promotion_for(promotions, order_date: date, channel: str):
    candidates = [
        p
        for p in promotions
        if date.fromisoformat(p["start_date"]) <= order_date <= date.fromisoformat(p["end_date"])
        and p["channel"] in (channel, "all")
    ]
    return candidates[0] if candidates else None


def build_orders_and_items(ctx: GenContext, n_orders: int, customers, stores, products, promotions):
    orders = []
    order_items = []
    payments = []
    returns = []
    inventory_movements = []

    active_products = [p for p in products if p["is_active"]] or products
    order_item_id = 1
    return_id = 1
    movement_id = 1

    for order_id in range(1, n_orders + 1):
        customer = ctx.rnd.choice(customers)
        store = ctx.rnd.choice(stores)
        channel = store["channel"]
        order_date = month_weighted_date(ctx)
        promo = active_promotion_for(promotions, order_date, channel)

        status = ctx.rnd.choices(
            VALID_ORDER_STATUSES, weights=[0.82, 0.06, 0.05, 0.07], k=1
        )[0]
        if ctx.rnd.random() < INVALID_STATUS_RATE:
            status = ctx.rnd.choice(INVALID_ORDER_STATUS_VALUES)

        payment_method = ctx.rnd.choice(PAYMENT_METHODS)

        recorded_at = datetime.combine(order_date, datetime.min.time(), tzinfo=timezone.utc)
        is_late_arriving = ctx.rnd.random() < LATE_ARRIVING_RATE
        if is_late_arriving:
            recorded_at = recorded_at + timedelta(days=ctx.rnd.randint(3, 14))

        n_items = ctx.rnd.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.15, 0.1, 0.05], k=1)[0]
        order_total = 0.0
        chosen_products = ctx.rnd.sample(active_products, k=min(n_items, len(active_products)))
        for prod in chosen_products:
            qty = ctx.rnd.randint(1, 4)
            discount_pct = promo["discount_pct"] if promo else 0.0
            unit_price = prod["unit_price"]
            line_total = round(qty * unit_price * (1 - discount_pct), 2)
            order_total += line_total

            product_id_fk = prod["product_id"]
            if ctx.rnd.random() < ORPHAN_FK_RATE:
                product_id_fk = 9_000_000 + product_id_fk  # intentionally dangling FK

            order_items.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product_id_fk,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "discount_pct": discount_pct if discount_pct else None,
                    "line_total": line_total,
                }
            )
            order_item_id += 1

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "store_id": store["store_id"],
                "order_date": order_date.isoformat(),
                "recorded_at": recorded_at.isoformat(),
                "channel": channel,
                "status": status,
                "payment_method": payment_method,
                "promotion_id": promo["promotion_id"] if promo else None,
                "order_total": round(order_total, 2),
            }
        )

        payments.append(
            {
                "payment_id": order_id,
                "order_id": order_id,
                "payment_method": payment_method,
                "amount": round(order_total, 2),
                "payment_status": "paid" if status in ("completed", "returned") else (
                    "failed" if status == "cancelled" else "pending"
                ),
                "payment_date": order_date.isoformat(),
            }
        )

        if status == "returned":
            returned_item = ctx.rnd.choice(chosen_products)
            returns.append(
                {
                    "return_id": return_id,
                    "order_id": order_id,
                    "reason": ctx.rnd.choice(RETURN_REASONS),
                    "refund_amount": round(returned_item["unit_price"], 2),
                    "return_date": (order_date + timedelta(days=ctx.rnd.randint(2, 20))).isoformat(),
                }
            )
            return_id += 1

    # Inventory movements: a lightweight independent stream keyed off products/stores.
    for prod in active_products:
        offline_stores = [s for s in stores if s["channel"] == "offline"] or stores
        store = ctx.rnd.choice(offline_stores)
        for _ in range(ctx.rnd.randint(1, 3)):
            movement_type = ctx.rnd.choices(
                ["restock", "sale", "return", "adjustment"], weights=[0.35, 0.4, 0.15, 0.1], k=1
            )[0]
            move_date = ctx.order_start + timedelta(
                days=ctx.rnd.randint(0, daterange_days(ctx.order_start, ctx.order_end))
            )
            inventory_movements.append(
                {
                    "movement_id": movement_id,
                    "product_id": prod["product_id"],
                    "store_id": store["store_id"],
                    "movement_type": movement_type,
                    "quantity": ctx.rnd.randint(1, 50),
                    "movement_date": move_date.isoformat(),
                }
            )
            movement_id += 1

    return orders, order_items, payments, returns, inventory_movements


def build_reviews(ctx: GenContext, customers, products, n_reviews: int):
    reviews = []
    for review_id in range(1, n_reviews + 1):
        reviews.append(
            {
                "review_id": review_id,
                "product_id": ctx.rnd.choice(products)["product_id"],
                "customer_id": ctx.rnd.choice(customers)["customer_id"],
                "rating": ctx.rnd.choices([1, 2, 3, 4, 5], weights=[0.05, 0.05, 0.15, 0.35, 0.4], k=1)[0],
                "review_text": ctx.rnd.choice(REVIEW_TEXTS),
                "review_date": (
                    ctx.order_start
                    + timedelta(days=ctx.rnd.randint(0, daterange_days(ctx.order_start, ctx.order_end)))
                ).isoformat(),
            }
        )
    return reviews


def inject_optional_nulls(ctx: GenContext, rows: list[dict], fields: list[str]):
    for row in rows:
        for field in fields:
            if field in row and ctx.rnd.random() < NULL_OPTIONAL_RATE:
                row[field] = None


def inject_duplicates(ctx: GenContext, rows: list[dict]) -> list[dict]:
    if not rows:
        return rows
    n_dupes = max(1, int(len(rows) * DUPLICATE_RATE))
    dupes = [dict(r) for r in ctx.rnd.sample(rows, k=min(n_dupes, len(rows)))]
    return rows + dupes


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    checksum = hashlib.sha256(path.read_bytes()).hexdigest()
    return len(rows), checksum


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(SCALE_PROFILES), default="small")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "raw"
    )
    args = parser.parse_args()

    scale = SCALE_PROFILES[args.profile]
    rnd = random.Random(args.seed)
    faker = Faker()
    faker.seed_instance(args.seed)

    order_end = date(2026, 6, 30)
    order_start = order_end - timedelta(days=364)

    ctx = GenContext(rnd=rnd, faker=faker, profile=args.profile, seed=args.seed,
                      order_start=order_start, order_end=order_end)

    regions, stores = build_regions_and_stores(ctx, scale["stores"])
    categories, products = build_categories_and_products(ctx, scale["products"])
    customers = build_customers(ctx, scale["customers"], regions)
    promotions = build_promotions(ctx)
    orders, order_items, payments, returns, inventory_movements = build_orders_and_items(
        ctx, scale["orders"], customers, stores, products, promotions
    )
    n_reviews = max(20, scale["orders"] // 8)
    reviews = build_reviews(ctx, customers, products, n_reviews)

    # Controlled data-quality scenarios.
    inject_optional_nulls(ctx, customers, ["email"])
    inject_optional_nulls(ctx, orders, ["promotion_id"])
    inject_optional_nulls(ctx, reviews, ["review_text"])
    orders = inject_duplicates(ctx, orders)
    customers = inject_duplicates(ctx, customers)

    tables = {
        "regions.csv": (
            [{"region_id": r["region_id"], "region_name": r["region_name"]} for r in regions],
            ["region_id", "region_name"],
        ),
        "stores.csv": (
            stores,
            ["store_id", "store_name", "store_type", "channel", "region_id", "city"],
        ),
        "product_categories.csv": (
            [
                {"category_id": c["category_id"], "category_name": c["category_name"],
                 "min_price": c["min_price"], "max_price": c["max_price"]}
                for c in categories
            ],
            ["category_id", "category_name", "min_price", "max_price"],
        ),
        "products.csv": (
            products,
            ["product_id", "sku", "product_name", "category_id", "unit_price", "is_active"],
        ),
        "customers.csv": (
            customers,
            ["customer_id", "first_name", "last_name", "email", "region_id", "city",
             "loyalty_tier", "signup_date", "is_active"],
        ),
        "promotions.csv": (
            promotions,
            ["promotion_id", "promo_name", "discount_pct", "start_date", "end_date", "channel"],
        ),
        "orders.csv": (
            orders,
            ["order_id", "customer_id", "store_id", "order_date", "recorded_at", "channel",
             "status", "payment_method", "promotion_id", "order_total"],
        ),
        "order_items.csv": (
            order_items,
            ["order_item_id", "order_id", "product_id", "quantity", "unit_price",
             "discount_pct", "line_total"],
        ),
        "payments.csv": (
            payments,
            ["payment_id", "order_id", "payment_method", "amount", "payment_status", "payment_date"],
        ),
        "inventory_movements.csv": (
            inventory_movements,
            ["movement_id", "product_id", "store_id", "movement_type", "quantity", "movement_date"],
        ),
        "returns_refunds.csv": (
            returns,
            ["return_id", "order_id", "reason", "refund_amount", "return_date"],
        ),
        "reviews.csv": (
            reviews,
            ["review_id", "product_id", "customer_id", "rating", "review_text", "review_date"],
        ),
    }

    manifest = {
        "profile": args.profile,
        "seed": args.seed,
        "generated_at": utc_now().isoformat(),
        "order_date_range": {"start": order_start.isoformat(), "end": order_end.isoformat()},
        "tables": {},
        "quality_summary": {
            "duplicate_rate_target": DUPLICATE_RATE,
            "null_optional_rate_target": NULL_OPTIONAL_RATE,
            "invalid_status_rate_target": INVALID_STATUS_RATE,
            "late_arriving_rate_target": LATE_ARRIVING_RATE,
            "orphan_fk_rate_target": ORPHAN_FK_RATE,
            "invalid_status_values_used": INVALID_ORDER_STATUS_VALUES,
        },
    }

    args.out.mkdir(parents=True, exist_ok=True)
    for filename, (rows, fieldnames) in tables.items():
        row_count, checksum = write_csv(args.out / filename, rows, fieldnames)
        manifest["tables"][filename] = {"row_count": row_count, "sha256": checksum}

    manifest_path = args.out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    total_rows = sum(t["row_count"] for t in manifest["tables"].values())
    print(f"Generated profile={args.profile} seed={args.seed} -> {args.out}")
    print(f"Total rows across {len(tables)} tables: {total_rows}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
