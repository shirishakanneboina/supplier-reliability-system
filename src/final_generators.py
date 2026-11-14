
import pandas as pd
import random
from datetime import datetime, timedelta

SEED = 20261030
rng = random.Random(SEED)

REFERENCE_DATE = datetime(2026, 11, 14).date()

RISK_TYPES = [
    "Delivery Delay",
    "Quality Issue",
    "Financial Risk",
    "Compliance Risk",
    "Capacity Risk"
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]

RISK_SOURCES = [
    "Delivery Monitoring",
    "Quality Inspection",
    "Financial Review",
    "Compliance Audit",
    "Capacity Assessment"
]

PENALTIES = {
    "Low": 2,
    "Medium": 5,
    "High": 10,
    "Critical": 20
}

SCORE_WEIGHTS = {
    "delivery_score": 0.25,
    "quality_score": 0.25,
    "cost_score": 0.15,
    "capacity_score": 0.10,
    "compliance_score": 0.15,
    "risk_score": 0.10
}


# ============================================================
# 1. GENERATE INVOICES
# ============================================================

def generate_invoices(purchase_orders_df):

    invoices = []

    for i, (_, po) in enumerate(
        purchase_orders_df.iterrows(),
        start=1
    ):

        order_date = datetime.strptime(
            po["order_date"],
            "%Y-%m-%d"
        ).date()

        invoice_date = order_date + timedelta(
            days=rng.randint(1, 15)
        )

        invoice_amount = round(
            float(po["total_amount"]) *
            rng.uniform(0.95, 1.05),
            2
        )

        payment_status = rng.choice([
            "Paid",
            "Pending",
            "Overdue"
        ])

        invoices.append({
            "invoice_id": f"INV{i:05d}",
            "purchase_order_id": po["purchase_order_id"],
            "supplier_id": po["supplier_id"],
            "invoice_date": invoice_date.isoformat(),
            "invoice_amount": invoice_amount,
            "payment_status": payment_status
        })

    return pd.DataFrame(invoices)


# ============================================================
# 2. GENERATE RISK SIGNALS
# ============================================================

def generate_risk_signals(suppliers_df):

    signals = []
    signal_counter = 1

    for _, supplier in suppliers_df.iterrows():

        number_of_signals = rng.randint(0, 3)

        for _ in range(number_of_signals):

            risk_type = rng.choice(RISK_TYPES)

            source_mapping = {
                "Delivery Delay": "Delivery Monitoring",
                "Quality Issue": "Quality Inspection",
                "Financial Risk": "Financial Review",
                "Compliance Risk": "Compliance Audit",
                "Capacity Risk": "Capacity Assessment"
            }

            signal_date = (
                datetime(2025, 1, 1).date()
                + timedelta(days=rng.randint(0, 682))
            )

            signals.append({
                "risk_signal_id": f"RISK{signal_counter:05d}",
                "supplier_id": supplier["supplier_id"],
                "risk_type": risk_type,
                "severity": rng.choice(SEVERITIES),
                "description": "Synthetic supplier risk indicator",
                "source": source_mapping[risk_type],
                "signal_date": signal_date.isoformat(),
                "status": rng.choice([
                    "Open",
                    "Monitoring",
                    "Resolved"
                ])
            })

            signal_counter += 1

    return pd.DataFrame(
        signals,
        columns=[
            "risk_signal_id",
            "supplier_id",
            "risk_type",
            "severity",
            "description",
            "source",
            "signal_date",
            "status"
        ]
    )


# ============================================================
# 3. GENERATE SUPPLIER RELIABILITY SCORES
# ============================================================

def generate_supplier_scores(
    suppliers_df,
    shipments_df,
    inspections_df,
    contracts_df,
    risk_signals_df,
    purchase_orders_df,
    po_lines_df,
    invoices_df,
    delivery_events_df
):

    scores = []

    # --------------------------------------------------------
    # Calculate measurement period
    # --------------------------------------------------------

    order_dates = pd.to_datetime(
        purchase_orders_df["order_date"]
    )

    if not order_dates.empty:

        first_date = order_dates.min()
        last_date = order_dates.max()

        months = max(
            1,
            (last_date.year - first_date.year) * 12
            + last_date.month - first_date.month + 1
        )

    else:
        months = 1

    # --------------------------------------------------------
    # Connect PO lines to suppliers
    # --------------------------------------------------------

    order_lines = po_lines_df.merge(
        purchase_orders_df[
            ["purchase_order_id", "supplier_id"]
        ],
        on="purchase_order_id",
        how="left"
    )

    # --------------------------------------------------------
    # Find actual delivery dates
    # --------------------------------------------------------

    delivered_events = delivery_events_df[
        delivery_events_df["event_type"] == "Delivered"
    ].copy()

    if not delivered_events.empty:

        delivered_events["event_date"] = pd.to_datetime(
            delivered_events["event_date"]
        )

        actual_delivery_dates = (
            delivered_events
            .groupby("shipment_id")["event_date"]
            .min()
            .reset_index()
            .rename(
                columns={
                    "event_date": "actual_delivery_date"
                }
            )
        )

    else:

        actual_delivery_dates = pd.DataFrame(
            columns=[
                "shipment_id",
                "actual_delivery_date"
            ]
        )

    shipment_data = shipments_df.merge(
        actual_delivery_dates,
        on="shipment_id",
        how="left"
    )

    shipment_data["expected_delivery_date"] = pd.to_datetime(
        shipment_data["expected_delivery_date"]
    )

    # --------------------------------------------------------
    # Process each supplier
    # --------------------------------------------------------

    for _, supplier in suppliers_df.iterrows():

        supplier_id = supplier["supplier_id"]

        supplier_shipments = shipment_data[
            shipment_data["supplier_id"] == supplier_id
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

        supplier_invoices = invoices_df[
            invoices_df["supplier_id"] == supplier_id
        ]

        supplier_lines = order_lines[
            order_lines["supplier_id"] == supplier_id
        ]

        # ----------------------------------------------------
        # 1. DELIVERY SCORE
        # ----------------------------------------------------

        delivered = supplier_shipments[
            supplier_shipments["actual_delivery_date"].notna()
        ]

        if len(delivered) > 0:

            on_time = (
                delivered["actual_delivery_date"]
                <= delivered["expected_delivery_date"]
            )

            delivery_score = (
                on_time.mean() * 100
            )

        else:
            delivery_score = None

        # ----------------------------------------------------
        # 2. QUALITY SCORE
        # ----------------------------------------------------

        total_inspected = (
            supplier_inspections["inspected_quantity"].sum()
        )

        total_defective = (
            supplier_inspections["defective_quantity"].sum()
        )

        if total_inspected > 0:

            quality_score = (
                1 - total_defective / total_inspected
            ) * 100

        else:
            quality_score = None

        # ----------------------------------------------------
        # 3. COST SCORE
        # ----------------------------------------------------

        cost_data = supplier_invoices.merge(
            purchase_orders_df[
                ["purchase_order_id", "total_amount"]
            ],
            on="purchase_order_id",
            how="inner"
        )

        if len(cost_data) > 0:

            valid_cost_data = cost_data[
                cost_data["total_amount"] > 0
            ].copy()

            if len(valid_cost_data) > 0:

                valid_cost_data["variance_percentage"] = (
                    abs(
                        valid_cost_data["invoice_amount"]
                        - valid_cost_data["total_amount"]
                    )
                    / valid_cost_data["total_amount"]
                ) * 100

                average_variance = (
                    valid_cost_data["variance_percentage"].mean()
                )

                cost_score = max(
                    0,
                    100 - average_variance * 10
                )

            else:
                cost_score = None

        else:
            cost_score = None

        # ----------------------------------------------------
        # 4. CAPACITY SCORE
        # ----------------------------------------------------

        monthly_demand = (
            supplier_lines["quantity"].sum() / months
            if len(supplier_lines) > 0
            else 0
        )

        supplier_capacity = supplier[
            "capacity_units_per_month"
        ]

        if monthly_demand > 0 and supplier_capacity > 0:

            capacity_ratio = (
                supplier_capacity / monthly_demand
            )

            # Score reflects capacity coverage.
            # 100 means capacity fully covers monthly demand.
            capacity_score = min(
                100,
                capacity_ratio * 100
            )

        else:
            capacity_score = None

        # ----------------------------------------------------
        # 5. COMPLIANCE SCORE
        # ----------------------------------------------------

        if len(supplier_contracts) > 0:

            compliance_score = (
                supplier_contracts["status"]
                .eq("Active")
                .mean() * 100
            )

        else:
            compliance_score = None

        # ----------------------------------------------------
        # 6. RISK SCORE
        # ----------------------------------------------------

        active_risks = supplier_risks[
            supplier_risks["status"].isin([
                "Open",
                "Monitoring"
            ])
        ]

        risk_penalty = sum(
            PENALTIES.get(severity, 0)
            for severity in active_risks["severity"]
        )

        risk_score = max(
            0,
            100 - risk_penalty
        )

        # ----------------------------------------------------
        # 7. WEIGHTED OVERALL SCORE
        # ----------------------------------------------------

        components = {
            "delivery_score": (
                delivery_score,
                SCORE_WEIGHTS["delivery_score"]
            ),
            "quality_score": (
                quality_score,
                SCORE_WEIGHTS["quality_score"]
            ),
            "cost_score": (
                cost_score,
                SCORE_WEIGHTS["cost_score"]
            ),
            "capacity_score": (
                capacity_score,
                SCORE_WEIGHTS["capacity_score"]
            ),
            "compliance_score": (
                compliance_score,
                SCORE_WEIGHTS["compliance_score"]
            ),
            "risk_score": (
                risk_score,
                SCORE_WEIGHTS["risk_score"]
            )
        }

        available_weight = sum(
            weight
            for value, weight in components.values()
            if value is not None
        )

        if available_weight > 0:

            overall_score = round(
                sum(
                    value * weight
                    for value, weight in components.values()
                    if value is not None
                ) / available_weight,
                2
            )

        else:
            overall_score = None

        # ----------------------------------------------------
        # 8. SAVE SCORE AND EXPLANATION
        # ----------------------------------------------------

        scores.append({

            "supplier_score_id": (
                f"SCORE{len(scores) + 1:05d}"
            ),

            "supplier_id": supplier_id,

            "delivery_score": (
                round(delivery_score, 2)
                if delivery_score is not None
                else None
            ),

            "quality_score": (
                round(quality_score, 2)
                if quality_score is not None
                else None
            ),

            "cost_score": (
                round(cost_score, 2)
                if cost_score is not None
                else None
            ),

            "capacity_score": (
                round(capacity_score, 2)
                if capacity_score is not None
                else None
            ),

            "compliance_score": (
                round(compliance_score, 2)
                if compliance_score is not None
                else None
            ),

            "risk_score": round(risk_score, 2),

            "overall_score": overall_score,

            "total_inspected_quantity": int(
                total_inspected
            ),

            "total_defective_quantity": int(
                total_defective
            ),

            "delivered_shipment_count": len(delivered),

            "active_risk_count": len(active_risks),

            "score_explanation": (
                "Weighted score: delivery 25%, quality 25%, "
                "cost 15%, capacity 10%, compliance 15%, "
                "risk 10%. Missing components are excluded "
                "and remaining weights are normalized. "
                "Delivery is measured using actual delivery "
                "events against expected dates."
            )
        })

    return pd.DataFrame(scores)
