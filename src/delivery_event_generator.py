
import pandas as pd
import random
from datetime import datetime, timedelta

# Fixed random seed
rng = random.Random(20261028)

# Possible delivery event types
event_types = [
    "Picked Up",
    "In Transit",
    "Arrived at Facility",
    "Out for Delivery",
    "Delivered",
    "Delivery Attempt Failed",
    "Delayed"
]

# Possible locations
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

    # Generate 1 to 4 events for every shipment
    for _, shipment in shipments_df.iterrows():

        number_of_events = rng.randint(1, 4)

        shipment_date = datetime.strptime(
            shipment["shipment_date"],
            "%Y-%m-%d"
        ).date()

        for event_number in range(number_of_events):

            event_date = shipment_date + timedelta(
                days=event_number
            )

            event = {
                "delivery_event_id": f"DE{event_counter:06d}",
                "shipment_id": shipment["shipment_id"],
                "event_type": rng.choice(event_types),
                "event_date": event_date.isoformat(),
                "location": rng.choice(locations),
                "remarks": "Shipment tracking update"
            }

            delivery_events.append(event)
            event_counter += 1

    return pd.DataFrame(delivery_events)
