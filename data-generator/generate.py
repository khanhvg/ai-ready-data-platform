#!/usr/bin/env python3
"""Deterministic, multi-table synthetic retail data generator.

Writes CSV files to data/raw/ plus a manifest.json describing the run
(profile, seed, row counts, checksums, quality summary). All randomness
flows through a single seeded random.Random instance so the same
--seed/--profile always reproduces byte-identical CSVs (same row content,
same per-file sha256 checksums in the manifest). manifest.json itself is
NOT byte-identical across runs: it embeds a wall-clock `generated_at`
timestamp that changes every run by design (it records when that run
happened, for demo/debugging evidence).

High-volume tables (orders, order_items, payments, returns_refunds,
shipments, web_events) are streamed row-by-row straight to disk instead of
being accumulated as Python lists, so peak memory stays bounded regardless
of scale profile. Only a compact per-order summary
(order_id -> (customer_id, store_id, order_date, status)) is kept across
the order loop, feeding shipments and the web_events checkout-linkage
scenario without holding full order/item rows.
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
    "small": dict(customers=200, products=150, stores=20, orders=1_000, suppliers=10, web_sessions=200),
    "medium": dict(customers=2_000, products=500, stores=50, orders=15_000, suppliers=25, web_sessions=3_000),
    "large": dict(customers=20_000, products=2_000, stores=150, orders=150_000, suppliers=80, web_sessions=45_000),
    "demo-large": dict(
        customers=20_000, products=2_000, stores=150, orders=90_000, suppliers=100, web_sessions=40_000
    ),
}

# Controlled data-quality scenario rates (fraction of rows affected).
DUPLICATE_RATE = 0.004
NULL_OPTIONAL_RATE = 0.03
INVALID_STATUS_RATE = 0.01
LATE_ARRIVING_RATE = 0.02
ORPHAN_FK_RATE = 0.004
IN_TRANSIT_RATE = 0.08
WEB_EVENT_ORPHAN_RATE = 0.004
PO_ORPHAN_PRODUCT_RATE = 0.02

# Business-realism (not data-quality-defect) tuning knobs.
CHECKOUT_ORDER_LINK_RATE = 0.6
DANGLING_FK_OFFSET = 9_000_000

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

CARRIERS = ["FedEx", "UPS", "DHL", "USPS", "Local Courier"]
PO_STATUSES = ["received", "pending", "cancelled"]
PO_STATUS_WEIGHTS = [0.80, 0.15, 0.05]
PO_ITEM_COUNT_CHOICES = [1, 2, 3, 4, 5, 6]
PO_ITEM_COUNT_WEIGHTS = [0.20, 0.25, 0.25, 0.15, 0.10, 0.05]

WEB_CHANNELS = ["organic", "paid_search", "email", "social", "direct"]
WEB_DEVICES = ["desktop", "mobile", "tablet"]
LANDING_PAGES = ["/home", "/search", "/category", "/product", "/promotions", "/cart"]
EVENT_TYPES = ["page_view", "search", "product_view", "add_to_cart", "checkout"]
EVENT_TYPE_WEIGHTS = [0.45, 0.15, 0.20, 0.12, 0.08]
EVENTS_PER_SESSION_CHOICES = [1, 2, 3, 4, 5]
EVENTS_PER_SESSION_WEIGHTS = [0.35, 0.30, 0.20, 0.10, 0.05]


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


class StreamWriter:
    """Writes CSV rows to `path` while incrementally hashing the exact bytes
    written, so the returned sha256 always matches the on-disk file with no
    second read-back pass. Used for both streamed high-volume tables (each
    `writerow` call is issued as a row is produced) and small in-memory
    tables (via `write_table` below)."""

    def __init__(self, path: Path, fieldnames: list[str]):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._file = path.open("w", newline="", encoding="utf-8")
        self._hash = hashlib.sha256()
        self._csv_writer = csv.DictWriter(self, fieldnames=fieldnames, extrasaction="ignore")
        self._csv_writer.writeheader()
        self.count = 0

    def write(self, s: str) -> int:
        self._hash.update(s.encode("utf-8"))
        return self._file.write(s)

    def writerow(self, row: dict) -> None:
        self._csv_writer.writerow(row)
        self.count += 1

    def close(self) -> tuple[int, str]:
        self._file.close()
        return self.count, self._hash.hexdigest()


def write_table(path: Path, fieldnames: list[str], rows) -> tuple[int, str]:
    writer = StreamWriter(path, fieldnames)
    for row in rows:
        writer.writerow(row)
    return writer.close()


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


def build_suppliers(ctx: GenContext, n_suppliers: int, regions):
    suppliers = []
    for supplier_id in range(1, n_suppliers + 1):
        region = ctx.rnd.choice(regions)
        suppliers.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": ctx.faker.company(),
                "region_id": region["region_id"],
                "lead_time_days": ctx.rnd.randint(3, 30),
                "reliability_score": round(ctx.rnd.uniform(0.70, 0.99), 2),
            }
        )
    return suppliers


def build_purchase_orders_and_items(ctx: GenContext, suppliers, stores, products):
    purchase_orders = []
    purchase_order_items = []
    po_id = 1
    po_item_id = 1
    orphan_product_rows = 0
    total_days = daterange_days(ctx.order_start, ctx.order_end)

    for supplier in suppliers:
        n_pos = ctx.rnd.randint(3, 12)
        for _ in range(n_pos):
            store = ctx.rnd.choice(stores)
            order_date = ctx.order_start + timedelta(days=ctx.rnd.randint(0, total_days))
            expected_date = order_date + timedelta(
                days=supplier["lead_time_days"] + ctx.rnd.randint(-2, 5)
            )
            status = ctx.rnd.choices(PO_STATUSES, weights=PO_STATUS_WEIGHTS, k=1)[0]
            purchase_orders.append(
                {
                    "po_id": po_id,
                    "supplier_id": supplier["supplier_id"],
                    "store_id": store["store_id"],
                    "order_date": order_date.isoformat(),
                    "expected_date": expected_date.isoformat(),
                    "status": status,
                }
            )

            n_items = ctx.rnd.choices(PO_ITEM_COUNT_CHOICES, weights=PO_ITEM_COUNT_WEIGHTS, k=1)[0]
            for _ in range(n_items):
                product = ctx.rnd.choice(products)
                product_id_fk = product["product_id"]
                if ctx.rnd.random() < PO_ORPHAN_PRODUCT_RATE:
                    product_id_fk = DANGLING_FK_OFFSET + product_id_fk
                    orphan_product_rows += 1
                purchase_order_items.append(
                    {
                        "po_item_id": po_item_id,
                        "po_id": po_id,
                        "product_id": product_id_fk,
                        "quantity": ctx.rnd.randint(10, 200),
                        "unit_cost": round(product["unit_price"] * ctx.rnd.uniform(0.4, 0.7), 2),
                    }
                )
                po_item_id += 1
            po_id += 1

    return purchase_orders, purchase_order_items, orphan_product_rows


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


def generate_orders_pipeline(
    ctx: GenContext,
    n_orders: int,
    customers,
    stores,
    products,
    promotions,
    out_dir: Path,
    order_fields: list[str],
    item_fields: list[str],
    payment_fields: list[str],
    return_fields: list[str],
) -> tuple[dict[int, tuple], dict[str, int], dict[str, tuple[int, str]]]:
    """Streams orders.csv, order_items.csv, payments.csv, and
    returns_refunds.csv inline within a single per-order loop (the same
    iteration that draws payment_method/order_total/refund_amount), so those
    fields never need to be reconstructed from a compact summary later.
    Returns the bounded order_id -> (customer_id, store_id, order_date,
    status) summary needed by shipments + web_events checkout-linkage, the
    inline data-quality counters, and (row_count, sha256) per streamed file.
    """
    active_products = [p for p in products if p["is_active"]] or products

    orders_w = StreamWriter(out_dir / "orders.csv", order_fields)
    items_w = StreamWriter(out_dir / "order_items.csv", item_fields)
    payments_w = StreamWriter(out_dir / "payments.csv", payment_fields)
    returns_w = StreamWriter(out_dir / "returns_refunds.csv", return_fields)

    order_item_id = 1
    return_id = 1
    order_summary: dict[int, tuple] = {}
    counters = {
        "invalid_order_status_rows": 0,
        "late_arriving_order_rows": 0,
        "orphan_fk_order_item_rows": 0,
        "duplicate_order_rows": 0,
        "null_promotion_id_rows": 0,
    }

    for order_id in range(1, n_orders + 1):
        customer = ctx.rnd.choice(customers)
        store = ctx.rnd.choice(stores)
        channel = store["channel"]
        order_date = month_weighted_date(ctx)
        promo = active_promotion_for(promotions, order_date, channel)

        status = ctx.rnd.choices(VALID_ORDER_STATUSES, weights=[0.82, 0.06, 0.05, 0.07], k=1)[0]
        if ctx.rnd.random() < INVALID_STATUS_RATE:
            status = ctx.rnd.choice(INVALID_ORDER_STATUS_VALUES)
            counters["invalid_order_status_rows"] += 1

        payment_method = ctx.rnd.choice(PAYMENT_METHODS)

        recorded_at = datetime.combine(order_date, datetime.min.time(), tzinfo=timezone.utc)
        if ctx.rnd.random() < LATE_ARRIVING_RATE:
            recorded_at = recorded_at + timedelta(days=ctx.rnd.randint(3, 14))
            counters["late_arriving_order_rows"] += 1

        n_items = ctx.rnd.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.15, 0.1, 0.05], k=1)[0]
        chosen_products = ctx.rnd.sample(active_products, k=min(n_items, len(active_products)))
        order_total = 0.0
        for prod in chosen_products:
            qty = ctx.rnd.randint(1, 4)
            discount_pct = promo["discount_pct"] if promo else 0.0
            unit_price = prod["unit_price"]
            line_total = round(qty * unit_price * (1 - discount_pct), 2)
            order_total += line_total

            product_id_fk = prod["product_id"]
            if ctx.rnd.random() < ORPHAN_FK_RATE:
                product_id_fk = DANGLING_FK_OFFSET + product_id_fk
                counters["orphan_fk_order_item_rows"] += 1

            items_w.writerow(
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

        promotion_id = promo["promotion_id"] if promo else None
        if ctx.rnd.random() < NULL_OPTIONAL_RATE:
            if promotion_id is not None:
                counters["null_promotion_id_rows"] += 1
            promotion_id = None

        order_row = {
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "store_id": store["store_id"],
            "order_date": order_date.isoformat(),
            "recorded_at": recorded_at.isoformat(),
            "channel": channel,
            "status": status,
            "payment_method": payment_method,
            "promotion_id": promotion_id,
            "order_total": round(order_total, 2),
        }
        orders_w.writerow(order_row)
        if ctx.rnd.random() < DUPLICATE_RATE:
            orders_w.writerow(dict(order_row))
            counters["duplicate_order_rows"] += 1

        payments_w.writerow(
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
            returns_w.writerow(
                {
                    "return_id": return_id,
                    "order_id": order_id,
                    "reason": ctx.rnd.choice(RETURN_REASONS),
                    "refund_amount": round(returned_item["unit_price"], 2),
                    "return_date": (order_date + timedelta(days=ctx.rnd.randint(2, 20))).isoformat(),
                }
            )
            return_id += 1

        order_summary[order_id] = (
            customer["customer_id"],
            store["store_id"],
            order_date.isoformat(),
            status,
        )

    file_stats = {
        "orders.csv": orders_w.close(),
        "order_items.csv": items_w.close(),
        "payments.csv": payments_w.close(),
        "returns_refunds.csv": returns_w.close(),
    }
    return order_summary, counters, file_stats


def build_inventory_movements(ctx: GenContext, products, stores):
    inventory_movements = []
    movement_id = 1
    active_products = [p for p in products if p["is_active"]] or products
    offline_stores = [s for s in stores if s["channel"] == "offline"] or stores
    for prod in active_products:
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
    return inventory_movements


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


def build_shipments(
    ctx: GenContext, path: Path, fieldnames: list[str], order_summary: dict[int, tuple]
) -> tuple[int, str, int]:
    """Streams shipments.csv by iterating the bounded per-order summary
    index (not full order/item rows), keyed off orders with
    status in (completed, returned)."""
    writer = StreamWriter(path, fieldnames)
    in_transit_rows = 0
    shipment_id = 1
    for order_id, (_customer_id, _store_id, order_date_str, status) in order_summary.items():
        if status not in ("completed", "returned"):
            continue
        order_date = date.fromisoformat(order_date_str)
        ship_date = order_date + timedelta(days=ctx.rnd.randint(1, 4))
        carrier = ctx.rnd.choice(CARRIERS)

        delivered_date = None
        if ctx.rnd.random() < IN_TRANSIT_RATE:
            ship_status = "in_transit"
            in_transit_rows += 1
        else:
            delivered_date = ship_date + timedelta(days=ctx.rnd.randint(1, 10))
            ship_status = "delayed" if ctx.rnd.random() < 0.1 else "delivered"

        writer.writerow(
            {
                "shipment_id": shipment_id,
                "order_id": order_id,
                "carrier": carrier,
                "ship_date": ship_date.isoformat(),
                "delivered_date": delivered_date.isoformat() if delivered_date else None,
                "ship_status": ship_status,
            }
        )
        shipment_id += 1

    count, sha = writer.close()
    return count, sha, in_transit_rows


def build_web_sessions(ctx: GenContext, n_sessions: int, customers) -> list[dict]:
    sessions = []
    total_days = daterange_days(ctx.order_start, ctx.order_end)
    for session_id in range(1, n_sessions + 1):
        customer_id = (
            ctx.rnd.choice(customers)["customer_id"] if ctx.rnd.random() < 0.6 else None
        )
        started_at = (
            datetime.combine(
                ctx.order_start + timedelta(days=ctx.rnd.randint(0, total_days)),
                datetime.min.time(),
                tzinfo=timezone.utc,
            )
            + timedelta(minutes=ctx.rnd.randint(0, 1439))
        )
        ended_at = started_at + timedelta(minutes=ctx.rnd.randint(1, 45))
        sessions.append(
            {
                "session_id": session_id,
                "customer_id": customer_id,
                "channel": ctx.rnd.choice(WEB_CHANNELS),
                "device": ctx.rnd.choice(WEB_DEVICES),
                "started_at": started_at.isoformat(),
                "ended_at": ended_at.isoformat(),
                "landing_page": ctx.rnd.choice(LANDING_PAGES),
            }
        )
    return sessions


def write_web_events(
    ctx: GenContext,
    path: Path,
    fieldnames: list[str],
    sessions: list[dict],
    products,
    order_id_pool: list[int],
    max_events: int | None,
) -> tuple[int, str, int]:
    """Streams web_events.csv. Event volume is derived from sessions x a
    per-session event count draw, capped by `max_events` (a hard ceiling on
    total emitted rows, so generation simply stops once reached -- no
    lookback/truncation bookkeeping needed). A deterministic fraction of
    checkout events link to a real order_id from the bounded order summary
    index built by generate_orders_pipeline."""
    writer = StreamWriter(path, fieldnames)
    orphan_rows = 0
    event_id = 1
    emitted = 0

    for session in sessions:
        if max_events is not None and emitted >= max_events:
            break
        n_events = ctx.rnd.choices(
            EVENTS_PER_SESSION_CHOICES, weights=EVENTS_PER_SESSION_WEIGHTS, k=1
        )[0]
        session_started = datetime.fromisoformat(session["started_at"])

        for i in range(n_events):
            if max_events is not None and emitted >= max_events:
                break
            event_type = ctx.rnd.choices(EVENT_TYPES, weights=EVENT_TYPE_WEIGHTS, k=1)[0]
            event_ts = session_started + timedelta(minutes=i * ctx.rnd.randint(1, 5))
            product_id = (
                ctx.rnd.choice(products)["product_id"]
                if event_type in ("product_view", "add_to_cart", "checkout")
                else None
            )
            linked_order_id = None
            if (
                event_type == "checkout"
                and order_id_pool
                and ctx.rnd.random() < CHECKOUT_ORDER_LINK_RATE
            ):
                linked_order_id = ctx.rnd.choice(order_id_pool)

            session_id_fk = session["session_id"]
            if ctx.rnd.random() < WEB_EVENT_ORPHAN_RATE:
                session_id_fk = DANGLING_FK_OFFSET + session_id_fk
                orphan_rows += 1

            writer.writerow(
                {
                    "event_id": event_id,
                    "session_id": session_id_fk,
                    "event_type": event_type,
                    "event_ts": event_ts.isoformat(),
                    "product_id": product_id,
                    "order_id": linked_order_id,
                }
            )
            event_id += 1
            emitted += 1

    count, sha = writer.close()
    return count, sha, orphan_rows


def inject_optional_nulls(ctx: GenContext, rows: list[dict], fields: list[str]) -> int:
    """Nulls out `fields` at NULL_OPTIONAL_RATE and returns how many values this
    call actually changed from non-null to null. Some fields (e.g. orders.promotion_id)
    are already null for unrelated business reasons (no campaign matched that
    order's date/channel), so counting every null in the final column would wildly
    overstate this scenario's rate; only count nulls this injection caused."""
    injected = 0
    for row in rows:
        for field in fields:
            if field in row and ctx.rnd.random() < NULL_OPTIONAL_RATE:
                if row[field] is not None:
                    injected += 1
                row[field] = None
    return injected


def inject_duplicates(ctx: GenContext, rows: list[dict]) -> list[dict]:
    if not rows:
        return rows
    n_dupes = max(1, int(len(rows) * DUPLICATE_RATE))
    dupes = [dict(r) for r in ctx.rnd.sample(rows, k=min(n_dupes, len(rows)))]
    return rows + dupes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(SCALE_PROFILES), default="small")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "raw"
    )
    parser.add_argument(
        "--max-orders",
        type=int,
        default=None,
        help="Cap the number of orders generated below the profile's default (no cap by default).",
    )
    parser.add_argument(
        "--max-web-events",
        type=int,
        default=None,
        help="Cap the number of web_events rows generated (no cap by default).",
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

    n_orders = scale["orders"] if args.max_orders is None else min(scale["orders"], args.max_orders)

    args.out.mkdir(parents=True, exist_ok=True)
    manifest_tables: dict[str, tuple[int, str]] = {}

    # --- Dimensions (bounded, held in memory for FK sampling) ---
    regions, stores = build_regions_and_stores(ctx, scale["stores"])
    categories, products = build_categories_and_products(ctx, scale["products"])
    customers = build_customers(ctx, scale["customers"], regions)
    promotions = build_promotions(ctx)
    suppliers = build_suppliers(ctx, scale["suppliers"], regions)
    purchase_orders, purchase_order_items, po_orphan_product_rows = build_purchase_orders_and_items(
        ctx, suppliers, stores, products
    )

    null_email_injected = inject_optional_nulls(ctx, customers, ["email"])
    customers_before_dupes = len(customers)
    customers = inject_duplicates(ctx, customers)

    manifest_tables["regions.csv"] = write_table(
        args.out / "regions.csv",
        ["region_id", "region_name"],
        [{"region_id": r["region_id"], "region_name": r["region_name"]} for r in regions],
    )
    manifest_tables["stores.csv"] = write_table(
        args.out / "stores.csv",
        ["store_id", "store_name", "store_type", "channel", "region_id", "city"],
        stores,
    )
    manifest_tables["product_categories.csv"] = write_table(
        args.out / "product_categories.csv",
        ["category_id", "category_name", "min_price", "max_price"],
        [
            {
                "category_id": c["category_id"],
                "category_name": c["category_name"],
                "min_price": c["min_price"],
                "max_price": c["max_price"],
            }
            for c in categories
        ],
    )
    manifest_tables["products.csv"] = write_table(
        args.out / "products.csv",
        ["product_id", "sku", "product_name", "category_id", "unit_price", "is_active"],
        products,
    )
    manifest_tables["customers.csv"] = write_table(
        args.out / "customers.csv",
        ["customer_id", "first_name", "last_name", "email", "region_id", "city",
         "loyalty_tier", "signup_date", "is_active"],
        customers,
    )
    manifest_tables["promotions.csv"] = write_table(
        args.out / "promotions.csv",
        ["promotion_id", "promo_name", "discount_pct", "start_date", "end_date", "channel"],
        promotions,
    )
    manifest_tables["suppliers.csv"] = write_table(
        args.out / "suppliers.csv",
        ["supplier_id", "supplier_name", "region_id", "lead_time_days", "reliability_score"],
        suppliers,
    )
    manifest_tables["purchase_orders.csv"] = write_table(
        args.out / "purchase_orders.csv",
        ["po_id", "supplier_id", "store_id", "order_date", "expected_date", "status"],
        purchase_orders,
    )
    manifest_tables["purchase_order_items.csv"] = write_table(
        args.out / "purchase_order_items.csv",
        ["po_item_id", "po_id", "product_id", "quantity", "unit_cost"],
        purchase_order_items,
    )

    # --- Per-order loop: orders, order_items, payments, returns_refunds
    # stream inline; only a compact order_id -> summary index is retained. ---
    order_summary, order_counters, order_file_stats = generate_orders_pipeline(
        ctx,
        n_orders,
        customers,
        stores,
        products,
        promotions,
        args.out,
        order_fields=["order_id", "customer_id", "store_id", "order_date", "recorded_at", "channel",
                      "status", "payment_method", "promotion_id", "order_total"],
        item_fields=["order_item_id", "order_id", "product_id", "quantity", "unit_price",
                     "discount_pct", "line_total"],
        payment_fields=["payment_id", "order_id", "payment_method", "amount", "payment_status",
                        "payment_date"],
        return_fields=["return_id", "order_id", "reason", "refund_amount", "return_date"],
    )
    manifest_tables.update(order_file_stats)

    inventory_movements = build_inventory_movements(ctx, products, stores)
    manifest_tables["inventory_movements.csv"] = write_table(
        args.out / "inventory_movements.csv",
        ["movement_id", "product_id", "store_id", "movement_type", "quantity", "movement_date"],
        inventory_movements,
    )

    n_reviews = max(20, n_orders // 8)
    reviews = build_reviews(ctx, customers, products, n_reviews)
    null_review_text_injected = inject_optional_nulls(ctx, reviews, ["review_text"])
    manifest_tables["reviews.csv"] = write_table(
        args.out / "reviews.csv",
        ["review_id", "product_id", "customer_id", "rating", "review_text", "review_date"],
        reviews,
    )

    # --- Post-order-loop streaming: shipments, web sessions/events ---
    ship_count, ship_sha, in_transit_rows = build_shipments(
        ctx,
        args.out / "shipments.csv",
        ["shipment_id", "order_id", "carrier", "ship_date", "delivered_date", "ship_status"],
        order_summary,
    )
    manifest_tables["shipments.csv"] = (ship_count, ship_sha)

    web_sessions = build_web_sessions(ctx, scale["web_sessions"], customers)
    manifest_tables["web_sessions.csv"] = write_table(
        args.out / "web_sessions.csv",
        ["session_id", "customer_id", "channel", "device", "started_at", "ended_at", "landing_page"],
        web_sessions,
    )

    order_id_pool = list(order_summary.keys())
    events_count, events_sha, orphan_web_event_rows = write_web_events(
        ctx,
        args.out / "web_events.csv",
        ["event_id", "session_id", "event_type", "event_ts", "product_id", "order_id"],
        web_sessions,
        products,
        order_id_pool,
        args.max_web_events,
    )
    manifest_tables["web_events.csv"] = (events_count, events_sha)

    late_arriving_order_rows = order_counters["late_arriving_order_rows"]

    manifest = {
        "profile": args.profile,
        "seed": args.seed,
        "generated_at": utc_now().isoformat(),
        "order_date_range": {"start": order_start.isoformat(), "end": order_end.isoformat()},
        "tables": {
            filename: {"row_count": count, "sha256": sha}
            for filename, (count, sha) in manifest_tables.items()
        },
        "quality_summary": {
            "targets": {
                "duplicate_rate": DUPLICATE_RATE,
                "null_optional_rate": NULL_OPTIONAL_RATE,
                "invalid_status_rate": INVALID_STATUS_RATE,
                "late_arriving_rate": LATE_ARRIVING_RATE,
                "orphan_fk_rate": ORPHAN_FK_RATE,
                "invalid_status_values": INVALID_ORDER_STATUS_VALUES,
                "in_transit_rate": IN_TRANSIT_RATE,
                "web_event_orphan_rate": WEB_EVENT_ORPHAN_RATE,
                "po_orphan_product_rate": PO_ORPHAN_PRODUCT_RATE,
            },
            "observed": {
                "duplicate_customer_rows": len(customers) - customers_before_dupes,
                "duplicate_order_rows": order_counters["duplicate_order_rows"],
                "null_email_rows": null_email_injected,
                "null_promotion_id_rows": order_counters["null_promotion_id_rows"],
                "null_review_text_rows": null_review_text_injected,
                "invalid_order_status_rows": order_counters["invalid_order_status_rows"],
                "late_arriving_order_rows": late_arriving_order_rows,
                "orphan_fk_order_item_rows": order_counters["orphan_fk_order_item_rows"],
                "in_transit_shipment_rows": in_transit_rows,
                "orphan_web_event_rows": orphan_web_event_rows,
                "orphan_fk_purchase_order_item_rows": po_orphan_product_rows,
            },
        },
    }

    manifest_path = args.out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    total_rows = sum(t["row_count"] for t in manifest["tables"].values())
    print(f"Generated profile={args.profile} seed={args.seed} -> {args.out}")
    print(f"Total rows across {len(manifest['tables'])} tables: {total_rows}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
