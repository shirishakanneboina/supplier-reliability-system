
# ============================================================
# SUPPLIER RELIABILITY SCORING SYSTEM
# Main Data Generation and Database Export
# ============================================================


# Step 1: Import required functions

from contract_generator import generate_contracts
from supplier_generator import generate_suppliers
from site_generator import generate_sites
from purchase_order_generator import generate_purchase_orders
from po_line_generator import generate_po_lines
from shipment_generator import generate_shipments
from delivery_event_generator import generate_delivery_events
from inspection_generator import generate_inspections

from final_generators import (
    generate_invoices,
    generate_risk_signals,
    generate_supplier_scores
)

from database_export import create_database_and_exports


# Step 2: Generate Suppliers

print("\nSUPPLIER RELIABILITY SYSTEM")
print("=" * 60)

suppliers_df = generate_suppliers(1000)

print("\nSUPPLIER DETAILS:")
print(suppliers_df.head(10).to_string(index=False))
print("\nTotal suppliers:", len(suppliers_df))

suppliers_df.to_csv(
    "data/raw/suppliers.csv",
    index=False
)

print("Supplier data saved successfully!")


# Step 3: Generate Sites

sites_df = generate_sites(suppliers_df)

print("\nSITE DETAILS:")
print(sites_df.head(10).to_string(index=False))
print("\nTotal sites:", len(sites_df))

sites_df.to_csv(
    "data/raw/sites.csv",
    index=False
)

print("Site data saved successfully!")


# Step 4: Generate Contracts

contracts_df = generate_contracts(suppliers_df)

print("\nCONTRACT DETAILS:")
print(contracts_df.head(10).to_string(index=False))
print("\nTotal contracts:", len(contracts_df))

contracts_df.to_csv(
    "data/raw/contracts.csv",
    index=False
)

print("Contract data saved successfully!")


# Step 5: Generate Purchase Orders

purchase_orders_df = generate_purchase_orders(
    suppliers_df,
    contracts_df
)

print("\nPURCHASE ORDER DETAILS:")
print(purchase_orders_df.head(10).to_string(index=False))
print("\nTotal purchase orders:", len(purchase_orders_df))

purchase_orders_df.to_csv(
    "data/raw/purchase_orders.csv",
    index=False
)

print("Purchase order data saved successfully!")


# Step 6: Generate Purchase Order Lines

po_lines_df = generate_po_lines(purchase_orders_df)

print("\nPURCHASE ORDER LINES DETAILS:")
print(po_lines_df.head(10).to_string(index=False))
print("\nTotal purchase order lines:", len(po_lines_df))

po_lines_df.to_csv(
    "data/raw/po_lines.csv",
    index=False
)

print("Purchase order lines data saved successfully!")


# Step 7: Generate Shipments

shipments_df = generate_shipments(purchase_orders_df)

print("\nSHIPMENT DETAILS:")
print(shipments_df.head(10).to_string(index=False))
print("\nTotal shipments:", len(shipments_df))

shipments_df.to_csv(
    "data/raw/shipments.csv",
    index=False
)

print("Shipment data saved successfully!")


# Step 8: Generate Delivery Events

delivery_events_df = generate_delivery_events(shipments_df)

print("\nDELIVERY EVENT DETAILS:")
print(delivery_events_df.head(10).to_string(index=False))
print("\nTotal delivery events:", len(delivery_events_df))

delivery_events_df.to_csv(
    "data/raw/delivery_events.csv",
    index=False
)

print("Delivery events data saved successfully!")


# Step 9: Generate Inspections

inspections_df = generate_inspections(shipments_df)

print("\nINSPECTION DETAILS:")
print(inspections_df.head(10).to_string(index=False))
print("\nTotal inspections:", len(inspections_df))

inspections_df.to_csv(
    "data/raw/inspections.csv",
    index=False
)

print("Inspection data saved successfully!")


# Step 10: Generate Invoices

invoices_df = generate_invoices(purchase_orders_df)

print("\nINVOICE DETAILS:")
print(invoices_df.head(10).to_string(index=False))
print("\nTotal invoices:", len(invoices_df))

invoices_df.to_csv(
    "data/raw/invoices.csv",
    index=False
)

print("Invoice data saved successfully!")


# Step 11: Generate Risk Signals

risk_signals_df = generate_risk_signals(suppliers_df)

print("\nRISK SIGNAL DETAILS:")
print(risk_signals_df.head(10).to_string(index=False))
print("\nTotal risk signals:", len(risk_signals_df))

risk_signals_df.to_csv(
    "data/raw/risk_signals.csv",
    index=False
)

print("Risk signal data saved successfully!")


# Step 12: Generate Supplier Scores

supplier_scores_df = generate_supplier_scores(
    suppliers_df,
    shipments_df,
    inspections_df,
    contracts_df,
    risk_signals_df,
    purchase_orders_df,
    po_lines_df,
    invoices_df,
    delivery_events_df
)

print("\nSUPPLIER SCORE DETAILS:")
print(supplier_scores_df.head(10).to_string(index=False))
print("\nTotal supplier scores:", len(supplier_scores_df))

supplier_scores_df.to_csv(
    "data/raw/supplier_scores.csv",
    index=False
)

print("Supplier score data saved successfully!")


# Step 13: Prepare All Tables for Database Export

tables = {
    "suppliers": suppliers_df,
    "sites": sites_df,
    "contracts": contracts_df,
    "purchase_orders": purchase_orders_df,
    "po_lines": po_lines_df,
    "shipments": shipments_df,
    "delivery_events": delivery_events_df,
    "inspections": inspections_df,
    "invoices": invoices_df,
    "risk_signals": risk_signals_df,
    "supplier_scores": supplier_scores_df
}


# Step 14: Create Database and Export Files

print("\nCREATING DATABASE AND EXPORT FILES...")
create_database_and_exports(tables)


# Step 15: Final Completion Message

print("\n" + "=" * 60)
print("SUPPLIER RELIABILITY SYSTEM COMPLETED!")
print("=" * 60)

print("All datasets generated successfully.")
print("Database created successfully.")
print("CSV, JSON and SQL exports completed.")
