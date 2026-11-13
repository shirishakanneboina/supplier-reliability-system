
import pandas as pd
import random
from datetime import date, timedelta

# Fixed random seed
rng = random.Random(20261024)

# Possible contract details
contract_types = [
    "Annual Supply",
    "Fixed Price",
    "Service Agreement",
    "Long Term Agreement"
]

payment_terms = [
    "Net 30",
    "Net 45",
    "Net 60"
]

contract_statuses = [
    "Active",
    "Expired",
    "Pending"
]


def generate_contracts(suppliers_df):
    contracts = []
    contract_counter = 1

    # Generate 1 to 3 contracts for each supplier
    for supplier_id in suppliers_df["supplier_id"]:

        number_of_contracts = rng.randint(1, 3)

        for _ in range(number_of_contracts):

            start_date = date(2025, 1, 1) + timedelta(
                days=rng.randint(0, 600)
            )

            end_date = start_date + timedelta(
                days=rng.randint(180, 730)
            )

            contract = {
                "contract_id": f"CON{contract_counter:04d}",
                "supplier_id": supplier_id,
                "contract_type": rng.choice(contract_types),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "contract_value": rng.randint(100000, 1000000),
                "payment_terms": rng.choice(payment_terms),
                "status": rng.choice(contract_statuses)
            }

            contracts.append(contract)
            contract_counter += 1

    return pd.DataFrame(contracts)
