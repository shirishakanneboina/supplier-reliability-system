
import pandas as pd
import random
from datetime import datetime, timedelta

rng = random.Random(20261030)


def generate_invoices(purchase_orders_df):
    invoices = []

    for i, (_, po) in enumerate(purchase_orders_df.iterrows(), start=1):
        invoice_date = datetime.strptime(
            po["order_date"], "%Y-%m-%d"
        ).date() + timedelta(days=rng.randint(1, 15))

        invoice_amount = round(
            float(po["total_amount"]) * rng.uniform(0.95, 1.05), 2
        )

        status = rng.choice(["Paid", "Pending", "Overdue"])

        invoices.append({
            "invoice_id": f"INV{i:05d}",
            "purchase_order_id": po["purchase_order_id"],
            "supplier_id": po["supplier_id"],
            "invoice_date": invoice_date.isoformat(),
            "invoice_amount": invoice_amount,
            "payment_status": status
        })

    return pd.DataFrame(invoices)


def generate_risk_signals(suppliers_df):
    signals = []

    risk_types = [
        "Delivery Delay",
        "Quality Issue",
        "Financial Risk",
        "Compliance Risk",
        "Capacity Risk"
    ]

    severities = ["Low", "Medium", "High", "Critical"]

    signal_counter = 1

    for _, supplier in suppliers_df.iterrows():
        number_of_signals = rng.randint(0, 3)

        for _ in range(number_of_signals):
            signals.append({
                "risk_signal_id": f"RISK{signal_counter:05d}",
                "supplier_id": supplier["supplier_id"],
                "risk_type": rng.choice(risk_types),
                "severity": rng.choice(severities),
                "description": "Synthetic supplier risk indicator",
                "status": rng.choice(["Open", "Monitoring", "Resolved"])
            })

            signal_counter += 1

    return pd.DataFrame(signals)


def generate_supplier_scores(
    suppliers_df,
    shipments_df,
    inspections_df,
    contracts_df,
    risk_signals_df
):
    scores = []

    for _, supplier in suppliers_df.iterrows():
        supplier_id = supplier["supplier_id"]

        supplier_shipments = shipments_df[
            shipments_df["supplier_id"] == supplier_id
        ]

        supplier_inspections = inspections_df[
            inspections_df["supplier_id"] == supplier_id
        ]

        supplier_contracts = contracts_df[
            contracts_df["supplier_id"] == supplier_id
        ]

        supplier_risks = risk_signals_df[
            risk_signals_df["supplier_id"] == supplier_id
        ]

        # Delivery score: percentage of delivered shipments
        if len(supplier_shipments) > 0:
            delivery_score = (
                supplier_shipments["status"].eq("Delivered").mean() * 100
            )
        else:
            delivery_score = 50

        # Quality score: percentage of passed inspections
        if len(supplier_inspections) > 0:
            quality_score = (
                supplier_inspections["quality_status"].eq("Passed").mean()
                * 100
            )
        else:
            quality_score = 50

        # Cost score: synthetic baseline score
        cost_score = rng.randint(60, 100)

        # Capacity score: synthetic baseline score
        capacity_score = rng.randint(60, 100)

        # Compliance score: based on active contracts
        if len(supplier_contracts) > 0:
            compliance_score = (
                supplier_contracts["status"].eq("Active").mean() * 100
            )
        else:
            compliance_score = 50

        # Risk score: more severe/open risks reduce the score
        penalties = {
            "Low": 2,
            "Medium": 5,
            "High": 10,
            "Critical": 20
        }

        risk_penalty = sum(
            penalties.get(severity, 0)
            for severity in supplier_risks["severity"]
            if severity is not None
        )

        risk_score = max(0, 100 - risk_penalty)

        # Overall weighted score
        overall_score = round(
            delivery_score * 0.25
            + quality_score * 0.25
            + cost_score * 0.15
            + capacity_score * 0.10
            + compliance_score * 0.15
            + risk_score * 0.10,
            2
        )

        scores.append({
            "supplier_score_id": f"SCORE{len(scores) + 1:05d}",
            "supplier_id": supplier_id,
            "delivery_score": round(delivery_score, 2),
            "quality_score": round(quality_score, 2),
            "cost_score": cost_score,
            "capacity_score": capacity_score,
            "compliance_score": round(compliance_score, 2),
            "risk_score": round(risk_score, 2),
            "overall_score": overall_score,
            "score_explanation": (
                "Weighted score using delivery, quality, cost, "
                "capacity, compliance and risk"
            )
        })

    return pd.DataFrame(scores)
