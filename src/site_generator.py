
import pandas as pd
import random

# Use a fixed seed for repeatable results
rng = random.Random(20261023)

# Possible site locations
cities = [
    "Hyderabad",
    "Bangalore",
    "Mumbai",
    "Chennai",
    "Delhi",
    "Pune",
    "Kolkata"
]

site_types = [
    "Manufacturing",
    "Warehouse",
    "Office",
    "Distribution"
]


def generate_sites(suppliers_df):
    sites = []
    site_counter = 1

    # Create 1 to 3 sites for every supplier
    for supplier_id in suppliers_df["supplier_id"]:

        number_of_sites = rng.randint(1, 3)

        for _ in range(number_of_sites):

            site = {
                "site_id": f"SITE{site_counter:04d}",
                "supplier_id": supplier_id,
                "city": rng.choice(cities),
                "site_type": rng.choice(site_types)
            }

            sites.append(site)
            site_counter += 1

    return pd.DataFrame(sites)
