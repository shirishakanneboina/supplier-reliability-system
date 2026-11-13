
import os
import sqlite3
import pandas as pd


def create_database_and_exports(tables):

    os.makedirs("data/exports", exist_ok=True)

    database_path = "data/exports/supplier_reliability.db"

    # Primary key for every table
    primary_keys = {
        "suppliers": "supplier_id",
        "sites": "site_id",
        "contracts": "contract_id",
        "purchase_orders": "purchase_order_id",
        "po_lines": "po_line_id",
        "shipments": "shipment_id",
        "delivery_events": "delivery_event_id",
        "inspections": "inspection_id",
        "invoices": "invoice_id",
        "risk_signals": "risk_signal_id",
        "supplier_scores": "supplier_score_id"
    }

    # Foreign key relationships
    foreign_keys = {
        "sites": {
            "supplier_id": ("suppliers", "supplier_id")
        },
        "contracts": {
            "supplier_id": ("suppliers", "supplier_id")
        },
        "purchase_orders": {
            "supplier_id": ("suppliers", "supplier_id"),
            "contract_id": ("contracts", "contract_id")
        },
        "po_lines": {
            "purchase_order_id": (
                "purchase_orders", "purchase_order_id"
            )
        },
        "shipments": {
            "purchase_order_id": (
                "purchase_orders", "purchase_order_id"
            ),
            "supplier_id": ("suppliers", "supplier_id")
        },
        "delivery_events": {
            "shipment_id": ("shipments", "shipment_id")
        },
        "inspections": {
            "shipment_id": ("shipments", "shipment_id"),
            "supplier_id": ("suppliers", "supplier_id")
        },
        "invoices": {
            "purchase_order_id": (
                "purchase_orders", "purchase_order_id"
            ),
            "supplier_id": ("suppliers", "supplier_id")
        },
        "risk_signals": {
            "supplier_id": ("suppliers", "supplier_id")
        },
        "supplier_scores": {
            "supplier_id": ("suppliers", "supplier_id")
        }
    }

    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON")

    # Remove previous tables in reverse dependency order
    for table_name in reversed(list(tables.keys())):
        conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    # Create tables with primary and foreign keys
    for table_name, df in tables.items():

        columns = []

        for column in df.columns:
            dtype = df[column].dtype

            if pd.api.types.is_integer_dtype(dtype):
                sql_type = "INTEGER"
            elif pd.api.types.is_numeric_dtype(dtype):
                sql_type = "REAL"
            else:
                sql_type = "TEXT"

            columns.append(f'"{column}" {sql_type}')

        columns.append(
            f'PRIMARY KEY ("{primary_keys[table_name]}")'
        )

        for column, reference in foreign_keys.get(
            table_name, {}
        ).items():

            parent_table, parent_column = reference

            columns.append(
                f'FOREIGN KEY ("{column}") '
                f'REFERENCES "{parent_table}" ("{parent_column}")'
            )

        create_sql = (
            f'CREATE TABLE "{table_name}" '
            f'({", ".join(columns)})'
        )

        conn.execute(create_sql)

    # Insert all DataFrames into SQLite
    for table_name, df in tables.items():
        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

    conn.commit()

    print("\nDATABASE CREATED SUCCESSFULLY!")

    # Validate primary keys and foreign keys
    print("\nDATABASE VALIDATION:")

    for table_name, df in tables.items():

        primary_key = primary_keys[table_name]

        duplicate_count = df[primary_key].duplicated().sum()
        null_count = df[primary_key].isna().sum()

        print(
            f"{table_name}: "
            f"duplicate primary keys = {duplicate_count}, "
            f"null primary keys = {null_count}"
        )

        if duplicate_count > 0 or null_count > 0:
            raise ValueError(
                f"Primary key validation failed: {table_name}"
            )

    foreign_key_errors = conn.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    if foreign_key_errors:
        print("Foreign key validation FAILED:")
        print(foreign_key_errors)
        raise ValueError("Foreign key validation failed")

    print("Foreign key validation PASSED!")

    # Check record counts
    print("\nDATABASE TABLE COUNTS:")

    for table_name in tables:

        count = conn.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

        print(f"{table_name}: {count}")

    # Export JSON files
    for table_name, df in tables.items():

        json_path = f"data/exports/{table_name}.json"

        df.to_json(
            json_path,
            orient="records",
            indent=2
        )

    print("\nJSON EXPORTS COMPLETED!")

    # Export SQL seed file
    with open(
        "data/exports/supplier_reliability.sql",
        "w",
        encoding="utf-8"
    ) as sql_file:

        for statement in conn.iterdump():
            sql_file.write(statement + "\n")

    print("SQL EXPORT COMPLETED!")

    conn.close()

    print("\nDATABASE AND EXPORTS COMPLETED!")
