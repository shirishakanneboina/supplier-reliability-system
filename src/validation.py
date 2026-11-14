
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
EXPORT_DIR = Path("data/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

checks = []


def record_check(name, passed, details=""):
    checks.append({
        "check_name": name,
        "status": "PASS" if passed else "FAIL",
        "details": details
    })


def load_csv(filename):
    path = RAW_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    return pd.read_csv(path)


# Load all datasets
suppliers = load_csv("suppliers.csv")
sites = load_csv("sites.csv")
contracts = load_csv("contracts.csv")
purchase_orders = load_csv("purchase_orders.csv")
po_lines = load_csv("po_lines.csv")
shipments = load_csv("shipments.csv")
delivery_events = load_csv("delivery_events.csv")
inspections = load_csv("inspections.csv")
invoices = load_csv("invoices.csv")
risk_signals = load_csv("risk_signals.csv")
scores = load_csv("supplier_scores.csv")


# 1. Primary key validation
primary_keys = {
    "suppliers": (suppliers, "supplier_id"),
    "sites": (sites, "site_id"),
    "contracts": (contracts, "contract_id"),
    "purchase_orders": (purchase_orders, "purchase_order_id"),
    "po_lines": (po_lines, "po_line_id"),
    "shipments": (shipments, "shipment_id"),
    "delivery_events": (delivery_events, "delivery_event_id"),
    "inspections": (inspections, "inspection_id"),
    "invoices": (invoices, "invoice_id"),
    "risk_signals": (risk_signals, "risk_signal_id"),
    "supplier_scores": (scores, "supplier_score_id")
}

for name, (df, column) in primary_keys.items():
    invalid = (
        df[column].isna().sum()
        + df[column].duplicated().sum()
    )

    record_check(
        f"Primary key: {name}",
        invalid == 0,
        f"Null or duplicate IDs: {invalid}"
    )


# 2. Foreign key validation
foreign_keys = [
    (sites, "supplier_id", suppliers, "supplier_id"),
    (contracts, "supplier_id", suppliers, "supplier_id"),
    (purchase_orders, "supplier_id", suppliers, "supplier_id"),
    (purchase_orders, "contract_id", contracts, "contract_id"),
    (po_lines, "purchase_order_id", purchase_orders, "purchase_order_id"),
    (shipments, "purchase_order_id", purchase_orders, "purchase_order_id"),
    (shipments, "supplier_id", suppliers, "supplier_id"),
    (delivery_events, "shipment_id", shipments, "shipment_id"),
    (inspections, "shipment_id", shipments, "shipment_id"),
    (inspections, "supplier_id", suppliers, "supplier_id"),
    (invoices, "purchase_order_id", purchase_orders, "purchase_order_id"),
    (invoices, "supplier_id", suppliers, "supplier_id"),
    (risk_signals, "supplier_id", suppliers, "supplier_id"),
    (scores, "supplier_id", suppliers, "supplier_id")
]

for child, child_col, parent, parent_col in foreign_keys:
    invalid = (
        child[child_col].isna()
        | ~child[child_col].isin(parent[parent_col])
    ).sum()

    record_check(
        f"Foreign key: {child_col}",
        invalid == 0,
        f"Invalid references: {invalid}"
    )


# 3. Inspection quantity validation
invalid_quantities = (
    (inspections["inspected_quantity"] <= 0)
    | (inspections["defective_quantity"] < 0)
    | (
        inspections["defective_quantity"]
        > inspections["inspected_quantity"]
    )
).sum()

record_check(
    "Inspection quantity validation",
    invalid_quantities == 0,
    f"Invalid inspection records: {invalid_quantities}"
)


# 4. Defect rate validation
expected_defect_rate = (
    inspections["defective_quantity"]
    / inspections["inspected_quantity"]
) * 100

defect_mismatches = (
    (
        inspections["defect_rate"]
        - expected_defect_rate
    ).abs() > 0.011
).sum()

record_check(
    "Defect rate calculation",
    defect_mismatches == 0,
    f"Mismatched records: {defect_mismatches}"
)


# 5. Purchase order line arithmetic
expected_line_total = (
    po_lines["quantity"] * po_lines["unit_price"]
)

line_mismatches = (
    (
        po_lines["line_total"]
        - expected_line_total
    ).abs() > 0.01
).sum()

record_check(
    "Purchase order line arithmetic",
    line_mismatches == 0,
    f"Mismatched records: {line_mismatches}"
)


# 6. Supplier score range and missing-value validation
score_columns = [
    "delivery_score",
    "quality_score",
    "cost_score",
    "capacity_score",
    "compliance_score",
    "risk_score",
    "overall_score"
]

component_columns = [
    "delivery_score",
    "quality_score",
    "cost_score",
    "capacity_score",
    "compliance_score"
]

# Missing component scores are allowed when data is unavailable.
# Risk score and overall score must always be available.
missing_required = scores[
    ["risk_score", "overall_score"]
].isna().sum().sum()

# All available scores must be between 0 and 100.
out_of_range = (
    (scores[score_columns] < 0)
    | (scores[score_columns] > 100)
).any(axis=1).sum()

missing_optional = scores[
    component_columns
].isna().sum().sum()

record_check(
    "Supplier score range",
    out_of_range == 0 and missing_required == 0,
    (
        f"Out-of-range records: {out_of_range}; "
        f"missing required scores: {missing_required}; "
        f"missing optional component scores: {missing_optional}"
    )
)


# 7. Risk signal source and date validation
invalid_risks = (
    risk_signals["source"].isna()
    | (
        risk_signals["source"]
        .astype(str)
        .str.strip() == ""
    )
    | risk_signals["signal_date"].isna()
).sum()

record_check(
    "Risk signal source and date",
    invalid_risks == 0,
    f"Invalid risk records: {invalid_risks}"
)


# 8. Save detailed validation report
results = pd.DataFrame(checks)

total_checks = len(results)
passed_checks = (
    results["status"] == "PASS"
).sum()

failed_checks = total_checks - passed_checks

results.to_csv(
    EXPORT_DIR / "validation_details.csv",
    index=False
)


# 9. Save validation summary
summary = pd.DataFrame([{
    "total_checks": total_checks,
    "passed_checks": passed_checks,
    "failed_checks": failed_checks,
    "validation_status": (
        "PASS" if failed_checks == 0 else "FAIL"
    )
}])

summary.to_csv(
    EXPORT_DIR / "validation_summary.csv",
    index=False
)


# 10. Display validation results
print("\n========== VALIDATION RESULTS ==========\n")

print(results.to_string(index=False))

print("\n========== VALIDATION SUMMARY ==========\n")

print("Total checks:", total_checks)
print("Passed checks:", passed_checks)
print("Failed checks:", failed_checks)

if failed_checks == 0:
    print("\nALL VALIDATION CHECKS PASSED!")
else:
    print("\nFAILED CHECK DETAILS:")

    print(
        results[
            results["status"] == "FAIL"
        ].to_string(index=False)
    )

print("\nValidation reports saved successfully!")
