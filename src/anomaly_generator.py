
import json
from pathlib import Path
import pandas as pd


def generate_anomaly_cases():
    """
    Creates isolated anomaly test cases and their expected decisions.
    These cases are kept separate from the valid operational datasets.
    """

    output_dir = Path("data/exports")
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = [
        {
            "case_id": "ANOM-001",
            "entity": "Shipment",
            "anomaly_type": "MISSING_PURCHASE_ORDER",
            "test_input": {
                "shipment_id": "SHP-TEST-001",
                "purchase_order_id": "PO-NOT-EXIST"
            },
            "expected_detection": "Shipment references a purchase order that does not exist.",
            "expected_decision": "REJECT",
            "severity": "HIGH"
        },
        {
            "case_id": "ANOM-002",
            "entity": "DeliveryEvent",
            "anomaly_type": "DELIVERY_BEFORE_DISPATCH",
            "test_input": {
                "shipment_id": "SHP-TEST-002",
                "dispatch_date": "2026-05-10",
                "delivery_date": "2026-05-08"
            },
            "expected_detection": "Delivery date occurs before dispatch date.",
            "expected_decision": "REJECT",
            "severity": "HIGH"
        },
        {
            "case_id": "ANOM-003",
            "entity": "SupplierScore",
            "anomaly_type": "FUTURE_DATA_USED",
            "test_input": {
                "supplier_id": "SUP-TEST-003",
                "score_as_of_date": "2026-06-30",
                "source_event_date": "2026-07-05"
            },
            "expected_detection": "Supplier score uses information recorded after its scoring date.",
            "expected_decision": "REJECT",
            "severity": "CRITICAL"
        },
        {
            "case_id": "ANOM-004",
            "entity": "RiskSignal",
            "anomaly_type": "MISSING_SOURCE_AND_DATE",
            "test_input": {
                "risk_signal_id": "RSK-TEST-004",
                "supplier_id": "SUP-TEST-004",
                "source": None,
                "signal_date": None
            },
            "expected_detection": "Risk signal has no source or signal date.",
            "expected_decision": "REJECT",
            "severity": "HIGH"
        },
        {
            "case_id": "ANOM-005",
            "entity": "Site",
            "anomaly_type": "SUPPLIER_SITE_CONFLATION",
            "test_input": {
                "site_id": "SITE-TEST-005",
                "supplier_id": "SUP-TEST-005",
                "actual_supplier_id": "SUP-TEST-006"
            },
            "expected_detection": "Site is associated with a different supplier than its actual owner.",
            "expected_decision": "REJECT",
            "severity": "HIGH"
        }
    ]

    # Save detailed anomaly test cases
    anomaly_df = pd.DataFrame(cases)
    anomaly_df["test_input"] = anomaly_df["test_input"].apply(
        lambda value: json.dumps(value)
    )

    anomaly_df.to_csv(
        output_dir / "anomaly_cases.csv",
        index=False
    )

    # Save ground truth labels separately
    ground_truth = []

    for case in cases:
        ground_truth.append({
            "case_id": case["case_id"],
            "entity": case["entity"],
            "anomaly_type": case["anomaly_type"],
            "expected_decision": case["expected_decision"],
            "severity": case["severity"],
            "expected_detection": case["expected_detection"]
        })

    ground_truth_df = pd.DataFrame(ground_truth)

    ground_truth_df.to_csv(
        output_dir / "ground_truth.csv",
        index=False
    )

    print("\nANOMALY TEST CASES GENERATED")
    print("--------------------------------")
    print("Total anomaly cases:", len(anomaly_df))
    print("Ground truth labels:", len(ground_truth_df))
    print("\nExpected decisions:")
    print(ground_truth_df[
        ["case_id", "anomaly_type", "expected_decision"]
    ].to_string(index=False))

    print("\nFiles saved successfully:")
    print("data/exports/anomaly_cases.csv")
    print("data/exports/ground_truth.csv")


if __name__ == "__main__":
    generate_anomaly_cases()
