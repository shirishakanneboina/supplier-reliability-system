
import pandas as pd
import random
from datetime import datetime, timedelta

# Fixed random seed
rng = random.Random(20261029)

inspection_types = [
    "Incoming Quality Check",
    "Visual Inspection",
    "Functional Test",
    "Sample Inspection"
]


def generate_inspections(shipments_df):

    inspections = []

    # Generate exactly 20,000 inspections
    for i in range(1, 20001):

        # Select an existing shipment
        shipment = shipments_df.iloc[
            rng.randrange(len(shipments_df))
        ]

        shipment_id = shipment["shipment_id"]
        supplier_id = shipment["supplier_id"]

        shipment_date = datetime.strptime(
            shipment["shipment_date"],
            "%Y-%m-%d"
        ).date()

        inspection_date = shipment_date + timedelta(
            days=rng.randint(0, 10)
        )

        inspected_quantity = rng.randint(10, 500)

        defective_quantity = rng.randint(
            0, min(inspected_quantity, 50)
        )

        defect_rate = round(
            (defective_quantity / inspected_quantity) * 100,
            2
        )

        if defect_rate <= 2:
            quality_status = "Passed"
        elif defect_rate <= 10:
            quality_status = "Conditional"
        else:
            quality_status = "Failed"

        inspection = {
            "inspection_id": f"INSP{i:05d}",
            "shipment_id": shipment_id,
            "supplier_id": supplier_id,
            "inspection_date": inspection_date.isoformat(),
            "inspection_type": rng.choice(inspection_types),
            "inspected_quantity": inspected_quantity,
            "defective_quantity": defective_quantity,
            "defect_rate": defect_rate,
            "quality_status": quality_status
        }

        inspections.append(inspection)

    return pd.DataFrame(inspections)
