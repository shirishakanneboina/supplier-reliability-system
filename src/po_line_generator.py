
import pandas as pd
import random

# Fixed random seed
rng = random.Random(20261026)

# Possible products
products = [
    "Laptop",
    "Keyboard",
    "Mouse",
    "Monitor",
    "Printer",
    "Processor",
    "Memory",
    "Hard Drive",
    "Cable",
    "Battery"
]


def generate_po_lines(purchase_orders_df):

    po_lines = []
    line_counter = 1

    # Generate 1 to 3 lines for every purchase order
    for _, purchase_order in purchase_orders_df.iterrows():

        number_of_lines = rng.randint(1, 3)

        for _ in range(number_of_lines):

            quantity = rng.randint(1, 100)
            unit_price = rng.randint(100, 50000)

            line = {
                "po_line_id": f"POL{line_counter:06d}",
                "purchase_order_id": purchase_order["purchase_order_id"],
                "product_name": rng.choice(products),
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": quantity * unit_price
            }

            po_lines.append(line)
            line_counter += 1

    return pd.DataFrame(po_lines)
