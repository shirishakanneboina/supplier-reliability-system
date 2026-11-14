
import pandas as pd
import random
from datetime import datetime, timedelta

rng = random.Random(20261028)

locations = [
    "Hyderabad",
    "Bangalore",
    "Mumbai",
    "Chennai",
    "Delhi",
    "Pune",
    "Kolkata"
]


def generate_delivery_events(shipments_df):
    delivery_events = []
    event_counter = 1

    status_events = {
        "Delivered": [
            "Picked Up",
            "In Transit",
            "Out for Delivery",
            "Delivered"
        ],
        "In Transit": [
            "Picked Up",
            "In Transit"
        ],
        "Shipped": [
            "Picked Up"
        ],
        "Delayed": [
            "Picked Up",
            "In Transit",
            "Delayed"
        ],
        "Cancelled": [
            "Cancelled"
        ]
    }

    for _, shipment in shipments_df.iterrows():

        shipment_date = datetime.strptime(
            shipment["shipment_date"],
            "%Y-%m-%d"
        ).date()

        shipment_status = shipment["status"]

        events = status_events.get(
            shipment_status,
            ["Picked Up"]
        )

        for event_number, event_type in enumerate(events):

            event_date = shipment_date + timedelta(
                days=event_number
            )

            event = {
                "delivery_event_id": f"DE{event_counter:06d}",
                "shipment_id": shipment["shipment_id"],
                "event_type": event_type,
                "event_date": event_date.isoformat(),
                "location": rng.choice(locations),
                "remarks": "Synthetic shipment tracking update"
            }

            delivery_events.append(event)
            event_counter += 1

    return pd.DataFrame(delivery_events)
