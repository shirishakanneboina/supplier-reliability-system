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

An overall supplier reliability score is calculated using the available performance components and the implemented scoring weights.

The system also provides score explanations to support interpretation of supplier performance.

Missing performance information is represented explicitly rather than automatically treated as a perfect score.

## Run the Dashboard

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The dashboard provides the following sections:

1. Executive Overview
2. Supplier Explorer
3. Anomaly Monitoring
4. Data Records

Users can explore supplier performance, view reliability indicators, monitor anomalies, and inspect generated records.

## Data Validation

The project includes 30 validation checks covering:

- Primary key uniqueness and null identifiers.
- Foreign key integrity across related datasets.
- Inspection quantity validation.
- Defect rate calculation.
- Purchase order line arithmetic.
- Supplier score range and missing-value handling.
- Risk signal source and date validation.

### Latest Validation Results

| Metric | Result |
|---|---:|
| Total checks | 30 |
| Passed checks | 30 |
| Failed checks | 0 |
| Validation status | PASS |

Run validation using:

```bash
python src/validation.py
```

Validation reports are saved in:

- `data/exports/validation_details.csv`
- `data/exports/validation_summary.csv`

## Anomaly Testing and Ground Truth

The project includes five labelled anomaly test cases covering:

- Shipment without a purchase order.
- Delivery date before dispatch.
- Supplier score using future data.
- Risk signal without source and date.
- Supplier site conflation.

Anomaly test cases and ground-truth labels are maintained separately from the normal operational datasets.

Files:

- `data/exports/anomaly_cases.csv`
- `data/exports/ground_truth.csv`

The expected decision for the generated anomaly cases is REJECT.

## Reproducibility

The system uses a fixed random seed (20261030) to ensure consistent synthetic data generation.

The reproducibility test generates the datasets twice and compares their checksums.

Run the reproducibility test:

```bash
python src/reproducibility_check.py
```

Latest result:

**REPRODUCIBILITY TEST PASSED**

All 11 generated raw CSV datasets were identical across both runs, confirming reproducibility of the raw data generation process.

## Documentation

Additional project documentation is available in the `docs/` directory:

- `PROJECT_DOCUMENTATION.md` – Project objectives, architecture, methodology, scoring, and implementation details.
- `DATA_DICTIONARY.md` – Dataset entities, fields, descriptions, and relationships.
- `SOURCE_MANIFEST.md` – Dataset generation sequence, source files, and export details.

AI assistance and prompt history are documented in:

- `prompts/AI_PROMPT_HISTORY.md`

## AI Usage Disclosure

AI assistance was used for technical problem-solving, debugging, implementation guidance, and documentation.

The prompt history is maintained in the `prompts/` directory.

The developer is responsible for reviewing, understanding, and validating the submitted implementation.

## Limitations

- The project uses synthetic data rather than actual supplier business records.
- Reliability scores depend on the implemented scoring assumptions and available data.
- Some supplier performance components may be unavailable when supporting data is missing.
- The system is intended for demonstration and educational purposes.

## Future Improvements

- Expand automated test coverage.
- Improve supplier risk prediction.
- Add more analytical visualizations.
- Improve anomaly detection and exception reporting.
- Evaluate the scoring methodology using validated real-world datasets.

## Disclaimer

All generated business records are synthetic and are not actual supplier records.
