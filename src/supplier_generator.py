import pandas as pd
import random

# Fixed random seed for reproducible data
SEED = 20261022
random.seed(SEED)

# Supplier names and countries
supplier_names = [
    "ABC Technologies",
    "Global Components",
    "Prime Materials",
    "Sunrise Electronics",
    "Reliable Industries"
]

countries = [
    "India",
    "USA",
    "Germany",
    "Japan",
    "UK"
]


def generate_suppliers(number_of_suppliers):
    suppliers = []

    for i in range(1, number_of_suppliers + 1):

        supplier = {
            "supplier_id": f"SUP{i:03d}",
            "supplier_name": random.choice(supplier_names),
            "country": random.choice(countries)
        }

        suppliers.append(supplier)

    return pd.DataFrame(suppliers)