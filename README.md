# Supplier Reliability Scoring and Data Generation System

## Project Overview

The Supplier Reliability Scoring and Data Generation System is a Python-based application that generates synthetic supplier business data, stores it in a relational database, analyzes supplier performance, and presents insights through an interactive dashboard.

The system evaluates supplier reliability using delivery performance, product quality, cost, capacity, compliance, and risk indicators.

## Objectives

- Generate synthetic supplier-related datasets.
- Maintain relational data using SQLite.
- Analyze supplier delivery, quality, cost, capacity, compliance, and risk indicators.
- Identify potential supplier reliability issues.
- Generate explainable supplier reliability scores.
- Preserve data integrity and traceability.
- Visualize supplier performance through an interactive dashboard.

## Technology Stack

- Python
- Pandas
- SQLite
- Streamlit
- Plotly

## Key Features

- Synthetic business data generation.
- CSV, JSON, and SQL exports.
- SQLite database creation.
- Relational primary key and foreign key validation.
- Supplier reliability scoring.
- Delivery and quality performance analysis.
- Cost and capacity evaluation.
- Compliance and risk signal analysis.
- Explainable supplier score calculations.
- Interactive dashboard with KPI metrics.
- Supplier exploration and ranking.
- Anomaly monitoring.
- Data filtering and CSV downloads.
- Reproducible data generation using a fixed random seed.
- Separate anomaly test cases and ground-truth labels.

## Project Structure

```text
Supplier-Reliability-System/
│
├── data/
│   ├── raw/
│   └── exports/
│
├── src/
│   ├── main.py
│   ├── supplier_generator.py
│   ├── site_generator.py
│   ├── contract_generator.py
│   ├── purchase_order_generator.py
│   ├── po_line_generator.py
│   ├── shipment_generator.py
│   ├── delivery_event_generator.py
│   ├── inspection_generator.py
│   ├── final_generators.py
│   ├── database_export.py
│   ├── anomaly_generator.py
│   ├── validation.py
│   └── reproducibility_check.py
│
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── DATA_DICTIONARY.md
│   └── SOURCE_MANIFEST.md
│
├── prompts/
│   └── AI_PROMPT_HISTORY.md
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shirishakanneboina/supplier-reliability-system.git
```

### 2. Navigate to the Project Directory

```bash
cd supplier-reliability-system
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Generate Data

Run the data generation program:

```bash
python src/main.py
```

The program generates supplier-related datasets and stores them in the `data/raw/` directory.

The generated database and export files are stored in the `data/exports/` directory.

## Database Tables

The SQLite database contains the following 11 related tables:

1. suppliers
2. sites
3. contracts
4. purchase_orders
5. po_lines
6. shipments
7. delivery_events
8. inspections
9. invoices
10. risk_signals
11. supplier_scores

## Supplier Reliability Scoring

Supplier reliability is evaluated using six performance dimensions:

- **Delivery Score:** Evaluates supplier delivery performance.
- **Quality Score:** Evaluates inspected and defective quantities.
- **Cost Score:** Evaluates invoice cost performance.
- **Capacity Score:** Evaluates supplier capacity against demand.
- **Compliance Score:** Evaluates contract compliance.
- **Risk Score:** Evaluates active supplier risk signals.

