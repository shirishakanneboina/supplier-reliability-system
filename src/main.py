
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

# Step 2: Generate 1000 suppliers
suppliers_df = generate_suppliers(1000)

# Step 3: Display supplier details
print("\nSUPPLIER RELIABILITY SYSTEM")
print("=" * 50)

print("\nSUPPLIER DETAILS:")
print(suppliers_df.head(10).to_string(index=False))

print("\nTotal suppliers:", len(suppliers_df))
print("\nSupplier generation completed successfully!")

# Step 4: Save supplier data into CSV
suppliers_df.to_csv(
    "data/raw/suppliers.csv",
    index=False
)

print("\nSupplier data saved successfully!")

# Step 5: Generate site records
sites_df = generate_sites(suppliers_df)

# Step 6: Display site details
print("\nSITE DETAILS:")
print(sites_df.head(10).to_string(index=False))

print("\nTotal sites:", len(sites_df))

# Step 7: Save sites into CSV
sites_df.to_csv(
    "data/raw/sites.csv",
    index=False
)

print("\nSite data saved successfully!")

# Step 8: Generate contract records
contracts_df = generate_contracts(suppliers_df)

# Step 9: Display contract details
print("\nCONTRACT DETAILS:")
print(contracts_df.head(10).to_string(index=False))

print("\nTotal contracts:", len(contracts_df))

# Step 10: Save contracts into CSV
contracts_df.to_csv(
    "data/raw/contracts.csv",
    index=False
)

print("\nContract data saved successfully!")

# Step 11: Generate purchase orders
purchase_orders_df = generate_purchase_orders(
    suppliers_df,
    contracts_df
)

# Step 12: Display purchase order details
print("\nPURCHASE ORDER DETAILS:")
print(purchase_orders_df.head(10).to_string(index=False))

print("\nTotal purchase orders:", len(purchase_orders_df))

# Step 13: Save purchase orders into CSV
purchase_orders_df.to_csv(
    "data/raw/purchase_orders.csv",
    index=False
)

print("\nPurchase order data saved successfully!")


# Step 14: Generate Purchase Order Lines
po_lines_df = generate_po_lines(purchase_orders_df)

# Step 15: Display Purchase Order Lines
print("\nPURCHASE ORDER LINES DETAILS:")
print(po_lines_df.head(10).to_string(index=False))

print("\nTotal purchase order lines:", len(po_lines_df))

# Step 16: Save Purchase Order Lines into CSV
po_lines_df.to_csv(
    "data/raw/po_lines.csv",
    index=False
)

print("\nPurchase order lines data saved successfully!")

# Step 17: Generate Shipments
shipments_df = generate_shipments(purchase_orders_df)

# Step 18: Display Shipment Details
print("\nSHIPMENT DETAILS:")
print(shipments_df.head(10).to_string(index=False))

print("\nTotal shipments:", len(shipments_df))

# Step 19: Save Shipment Data into CSV
shipments_df.to_csv(
    "data/raw/shipments.csv",
    index=False
)

print("\nShipment data saved successfully!")

# Step 20: Generate Delivery Events
delivery_events_df = generate_delivery_events(shipments_df)

# Step 21: Display Delivery Event Details
print("\nDELIVERY EVENT DETAILS:")
print(delivery_events_df.head(10).to_string(index=False))

print("\nTotal delivery events:", len(delivery_events_df))

# Step 22: Save Delivery Events into CSV
delivery_events_df.to_csv(
    "data/raw/delivery_events.csv",
    index=False
)

print("\nDelivery events data saved successfully!")

# Step 23: Generate Inspections
inspections_df = generate_inspections(shipments_df)

# Step 24: Display Inspection Details
print("\nINSPECTION DETAILS:")
print(inspections_df.head(10).to_string(index=False))

print("\nTotal inspections:", len(inspections_df))

# Step 25: Save Inspections into CSV
inspections_df.to_csv(
    "data/raw/inspections.csv",
    index=False
)

print("\nInspection data saved successfully!")

# Step 26: Generate Invoices
invoices_df = generate_invoices(purchase_orders_df)

print("\nINVOICE DETAILS:")
print(invoices_df.head(10).to_string(index=False))
print("\nTotal invoices:", len(invoices_df))

invoices_df.to_csv("data/raw/invoices.csv", index=False)
print("Invoice data saved successfully!")


# Step 27: Generate Risk Signals
risk_signals_df = generate_risk_signals(suppliers_df)

print("\nRISK SIGNAL DETAILS:")
print(risk_signals_df.head(10).to_string(index=False))
print("\nTotal risk signals:", len(risk_signals_df))

risk_signals_df.to_csv("data/raw/risk_signals.csv", index=False)
print("Risk signal data saved successfully!")


# Step 28: Generate Supplier Scores
supplier_scores_df = generate_supplier_scores(
    suppliers_df,
    shipments_df,
    inspections_df,
    contracts_df,
    risk_signals_df
)

print("\nSUPPLIER SCORE DETAILS:")
print(supplier_scores_df.head(10).to_string(index=False))
print("\nTotal supplier scores:", len(supplier_scores_df))

supplier_scores_df.to_csv(
    "data/raw/supplier_scores.csv",
    index=False
)

print("Supplier score data saved successfully!")

# Step 29: Create database and export files

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

create_database_and_exports(tables)
