
import pandas as pd
import random
from datetime import datetime, timedelta

# Fixed random seed for reproducible data
rng = random.Random(20261027)

carriers = [
    "DHL",
    "FedEx",
    "Blue Dart",
    "UPS",
    "India Post"
]

shipment_statuses = [
    "Shipped",
    "In Transit",
    "Delivered",
    "Delayed",
    "Cancelled"
]


def generate_shipments(purchase_orders_df):

    shipments = []

    for i in range(1, 15001):

        # Select a purchase order
        purchase_order = purchase_orders_df.iloc[
            rng.randrange(len(purchase_orders_df))
        ]

        purchase_order_id = purchase_order["purchase_order_id"]
        supplier_id = purchase_order["supplier_id"]

        order_date = datetime.strptime(
            purchase_order["order_date"],
            "%Y-%m-%d"
        ).date()

        expected_date = datetime.strptime(
            purchase_order["expected_delivery_date"],
            "%Y-%m-%d"
        ).date()

        # Generate shipment date after the order date
        shipment_date = order_date + timedelta(
            days=rng.randint(1, 5)
        )

        # Ensure shipment date is before expected delivery date
        if shipment_date >= expected_date:
            shipment_date = order_date + timedelta(days=1)

        shipment = {
            "shipment_id": f"SHIP{i:05d}",
            "purchase_order_id": purchase_order_id,
            "supplier_id": supplier_id,
            "shipment_date": shipment_date.isoformat(),
            "expected_delivery_date": expected_date.isoformat(),
            "carrier": rng.choice(carriers),
            "tracking_number": f"TRK{i:08d}",
            "status": rng.choice(shipment_statuses)
        }

        shipments.append(shipment)

    return pd.DataFrame(shipments)
