
import pandas as pd
import random
from datetime import date, timedelta

# Fixed random seed
rng = random.Random(20261025)

# Purchase order generation period
MIN_ORDER_DATE = date(2025, 1, 1)
MAX_ORDER_DATE = date(2026, 8, 23)


def generate_purchase_orders(suppliers_df, contracts_df):
    purchase_orders = []

    # Convert contract dates into date objects
    contracts = contracts_df.copy()

    contracts["start_date"] = pd.to_datetime(
        contracts["start_date"]
    ).dt.date

    contracts["end_date"] = pd.to_datetime(
        contracts["end_date"]
    ).dt.date

    # Keep contracts that overlap the order generation period
    eligible_contracts = contracts[
        (contracts["start_date"] <= MAX_ORDER_DATE) &
        (contracts["end_date"] >= MIN_ORDER_DATE)
    ]

    if eligible_contracts.empty:
        raise ValueError(
            "No contracts are available for purchase order generation."
        )

    # Generate exactly 10,000 purchase orders
    for i in range(1, 10001):

        # Select a contract that overlaps the generation period
        contract = eligible_contracts.iloc[
            rng.randrange(len(eligible_contracts))
        ]

        supplier_id = contract["supplier_id"]
        contract_id = contract["contract_id"]

        # Calculate the valid order date range for this contract
        earliest_date = max(
            contract["start_date"],
            MIN_ORDER_DATE
        )

        latest_date = min(
            contract["end_date"],
            MAX_ORDER_DATE
        )

        # Generate order date within contract validity
        available_days = (latest_date - earliest_date).days

        order_date = earliest_date + timedelta(
            days=rng.randint(0, available_days)
        )

        # Generate expected delivery date
        expected_date = order_date + timedelta(
            days=rng.randint(7, 60)
        )

        # Generate purchase order
        purchase_order = {
            "purchase_order_id": f"PO{i:05d}",
            "supplier_id": supplier_id,
            "contract_id": contract_id,
            "order_date": order_date.isoformat(),
            "expected_delivery_date": expected_date.isoformat(),
            "total_amount": rng.randint(10000, 500000),
            "status": rng.choice([
                "Open",
                "Approved",
                "Completed",
                "Cancelled"
            ])
        }

        purchase_orders.append(purchase_order)

    return pd.DataFrame(purchase_orders)
