
import pandas as pd
import random
from datetime import date, timedelta

# Fixed random seed
rng = random.Random(20261025)


def generate_purchase_orders(suppliers_df, contracts_df):
    purchase_orders = []

    # Generate exactly 10,000 purchase orders
    for i in range(1, 10001):

        # Select one supplier
        supplier = suppliers_df.sample(
            n=1,
            random_state=rng.randint(1, 1000000)
        ).iloc[0]

        supplier_id = supplier["supplier_id"]

        # Find contracts belonging to this supplier
        supplier_contracts = contracts_df[
            contracts_df["supplier_id"] == supplier_id
        ]

        # Select one of that supplier's contracts
        contract = supplier_contracts.iloc[
            rng.randint(0, len(supplier_contracts) - 1)
        ]

        contract_id = contract["contract_id"]

        # Generate order date
        order_date = date(2025, 1, 1) + timedelta(
            days=rng.randint(0, 600)
        )

        # Generate expected delivery date
        expected_date = order_date + timedelta(
            days=rng.randint(7, 60)
        )

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
