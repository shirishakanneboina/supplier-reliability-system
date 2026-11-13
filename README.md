# Supplier Reliability Scoring and Data Generation System

## Project Overview

The Supplier Reliability Scoring and Data Generation System is a Python-based application that generates synthetic supplier business data, stores it in a relational database, analyzes supplier performance, and presents insights through an interactive dashboard.

## Objectives

- Generate synthetic supplier-related datasets.
- Maintain relational data using SQLite.
- Analyze supplier delivery, quality, and risk indicators.
- Identify potential supplier reliability issues.
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
- Primary key and foreign key validation.
- Supplier reliability analysis.
- Interactive dashboard with KPI metrics.
- Supplier exploration and ranking.
- Anomaly monitoring.
- Data filtering and CSV downloads.

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
│   └── database_export.py
│
├── docs/
│   └── PROJECT_DOCUMENTATION.md
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

The generated database and export files are stored in the `data/exports/` directory.

## Run the Dashboard

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The dashboard will open in your web browser.

### Database Tables

The SQLite database contains the following 11 tables:

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

## Validation

The project includes database validation checks for primary key uniqueness, null identifiers, duplicate identifiers, and foreign key integrity.

## AI Usage Disclosure

AI assistance was used for technical problem-solving, debugging, implementation guidance, and documentation. The prompt history is maintained in the `prompts/` directory.

The developer is responsible for reviewing, understanding, and validating the submitted implementation.

## Limitations

- The project uses synthetic data.
- Reliability scores depend on the implemented scoring assumptions.
- The system is intended for demonstration and educational purposes.

## Future Improvements

- Expand automated test coverage.
- Improve supplier risk prediction.
- Add more analytical visualizations.
- Evaluate the scoring methodology using validated real-world datasets.

# Disclaimer

All generated business records are synthetic and are not actual supplier records.
