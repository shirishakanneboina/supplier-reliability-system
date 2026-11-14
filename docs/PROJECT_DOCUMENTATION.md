# Supplier Reliability Scoring and Data Generation System

## 1. Problem Statement

Supplier reliability plays an important role in maintaining business operations, product quality, and timely deliveries. Organizations need to monitor supplier performance to identify potential delivery delays, quality issues, invoice-related problems, capacity limitations, compliance concerns, and other risk indicators.

This project develops a Python-based Supplier Reliability Scoring and Data Generation System. It generates interconnected synthetic supplier business data, stores the data in a relational SQLite database, evaluates supplier performance using multiple reliability indicators, validates data consistency, and presents insights through an interactive Streamlit dashboard.

The system also includes isolated anomaly scenarios and reproducibility testing to demonstrate data quality, traceability, and reliable data generation.

## 2. Project Objectives

- Generate interconnected synthetic supplier business datasets.
- Maintain relational data using SQLite.
- Analyze supplier delivery, quality, cost, capacity, compliance, and risk indicators.
- Calculate supplier reliability scores using available performance information.
- Identify potential supplier reliability issues and data anomalies.
- Validate primary keys, foreign keys, and selected business rules.
- Maintain separate anomaly test cases and expected decisions.
- Support repeatable data generation using a fixed random seed.
- Present supplier performance insights through an interactive dashboard.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation and data generation |
| Pandas | Data processing and manipulation |
| NumPy | Numerical operations and data generation |
| SQLite | Relational database storage |
| Streamlit | Interactive dashboard application |
| Plotly | Data visualization |
| JSON | Structured data export |
| CSV | Dataset and report export |
| SQL | Database schema and data export |

## 4. System Architecture

The project follows a modular data generation, storage, validation, scoring, and visualization workflow.

1. Generate synthetic supplier master information.
2. Generate related sites and contracts.
3. Generate purchase orders and purchase order lines.
4. Generate shipments and delivery tracking events.
5. Generate quality inspections and invoice records.
6. Generate supplier risk signals.
7. Calculate supplier reliability scores.
8. Export datasets into CSV and JSON formats.
9. Create SQL exports and an SQLite database.
10. Execute data validation checks.
11. Generate isolated anomaly cases and expected decisions.
12. Run reproducibility checks on generated raw CSV datasets.
13. Display analytical results through the Streamlit dashboard.

## 5. Project Structure

```text
Supplier-Reliability-System/
│
├── data/
│   ├── raw/
│   └── exports/
│       ├── anomaly_cases.csv
│       ├── ground_truth.csv
│       ├── validation_details.csv
│       └── validation_summary.csv
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

*Note: This is the documented project structure. Keep only files and folders that actually exist in your repository.*

## 6. Data Model and Generated Datasets

The system generates 11 interconnected datasets.

| Dataset | Generated Records | Description |
|---|---:|---|
| Suppliers | 1,000 | Supplier master information |
| Sites | 1,976 | Supplier operating locations |
| Contracts | 2,016 | Supplier contract information |
| Purchase Orders | 10,000 | Orders placed with suppliers |
| PO Lines | 20,011 | Individual products and quantities |
| Shipments | 15,000 | Shipment records |
| Delivery Events | 32,899 | Shipment tracking events |
| Inspections | 20,000 | Quality inspection results |
| Invoices | 10,000 | Supplier invoice information |
| Risk Signals | 1,514 | Supplier risk observations |
| Supplier Scores | 1,000 | Calculated supplier reliability scores |

The SQLite database contains corresponding relational tables:

1. `suppliers`
2. `sites`
3. `contracts`
4. `purchase_orders`
5. `po_lines`
6. `shipments`
7. `delivery_events`
8. `inspections`
9. `invoices`
10. `risk_signals`
11. `supplier_scores`

Primary-key and foreign-key relationships maintain consistency between related datasets.

## 7. Supplier Reliability Scoring

Supplier performance is evaluated using the following indicators:

- **Delivery Score:** Evaluates delivery performance using shipment delivery information and expected delivery dates.
- **Quality Score:** Evaluates product quality using inspected quantities and defective quantities.
- **Cost Score:** Evaluates cost performance using invoice-related information.
- **Capacity Score:** Evaluates supplier capacity in relation to monthly demand.
- **Compliance Score:** Evaluates contract compliance using contract information.
- **Risk Score:** Evaluates supplier risk using active risk signals.

The system calculates an overall supplier reliability score using the scoring weights implemented in the scoring generator.

Missing performance components are handled separately from genuine scores. When a component cannot be calculated because sufficient information is unavailable, it is not automatically treated as a score of 100.

The scoring system also generates explanations to support interpretation of supplier scores.

Scores are analytical indicators based on synthetic data and implemented assumptions, not verified predictions of future supplier performance.

## 8. Data Validation and Integrity

The project includes a validation module implemented in:

`src/validation.py`

The validation process checks:

- Primary-key uniqueness and null values.
- Foreign-key integrity.
- Inspection quantity consistency.
- Defect-rate calculation.
- Purchase order line arithmetic.
- Supplier score ranges and required score values.
- Risk signal source and date requirements.

**Completed validation results:**

| Metric | Result |
|---|---:|
| Total validation checks | 30 |
| Passed checks | 30 |
| Failed checks | 0 |

The 30 checks consist of:

- 11 primary-key checks.
- 14 foreign-key checks.
- 5 business-rule checks.

The validation reports are generated in:

- `data/exports/validation_details.csv`
- `data/exports/validation_summary.csv`

These results represent the checks implemented in the validation script. Additional documented business rules may require further automated validation.

## 9. Anomaly Detection and Ground Truth

The project includes a separate anomaly generation module:

`src/anomaly_generator.py`

Five labelled anomaly scenarios are generated:

| Anomaly ID | Scenario | Expected Decision |
|---|---|---|
| ANOM-001 | Missing purchase order reference | REJECT |
| ANOM-002 | Delivery before dispatch | REJECT |
| ANOM-003 | Future data used in scoring | REJECT |
| ANOM-004 | Missing risk source and date | REJECT |
| ANOM-005 | Supplier-site association inconsistency | REJECT |

Output files:

- `data/exports/anomaly_cases.csv`
- `data/exports/ground_truth.csv`

Anomaly cases and their expected decisions are maintained separately from the valid baseline datasets. This allows exception scenarios to be evaluated without contaminating normal relational data.

## 10. Reproducibility

The project uses a fixed random seed of `20261030` to support repeatable synthetic data generation.

The reproducibility checker is implemented in:

`src/reproducibility_check.py`

The script executes the generation process twice and compares hashes of the generated raw CSV datasets.

**Completed reproducibility result:**

- Raw CSV datasets checked: 11
- Matching datasets: 11
- Mismatched datasets: 0

All 11 raw CSV datasets matched across the two runs.

This result applies to the raw CSV datasets checked by the reproducibility script.

## 11. Database and Export Management

The project supports multiple data storage and export formats:

- CSV exports for individual datasets.
- JSON exports for structured data.
- SQL export for database portability.
- SQLite database for relational storage and querying.

These outputs support further analysis, inspection, and data reuse.

## 12. Dashboard Features

The Streamlit dashboard provides four main sections:

### 12.1 Executive Overview

Provides a high-level view of supplier performance and system-level metrics.

### 12.2 Supplier Explorer

Allows users to explore supplier information and compare supplier reliability indicators.

### 12.3 Anomaly Monitoring

Displays generated anomaly scenarios and related exception information.

### 12.4 Data Records

Provides access to generated dataset records for inspection.

Plotly is used for interactive data visualizations.

## 13. Design Decisions and Trade-offs

- **SQLite:** Selected for lightweight relational data storage without requiring a separate database server.
- **Pandas:** Used for structured data processing and manipulation.
- **Streamlit:** Selected to develop an interactive dashboard using Python.
- **Synthetic Data:** Used to avoid exposing real supplier business information.
- **Modular Python Files:** Separate generator modules organize data generation responsibilities.
- **Fixed Random Seed:** Supports repeatable generation of raw datasets.
- **Separate Ground Truth:** Keeps expected anomaly decisions separate from normal input data.

## 14. Testing and Verification

The following activities were completed:

- Executed the main data generation program.
- Generated all 11 datasets with the recorded baseline volumes.
- Checked CSV and JSON exports.
- Generated SQL export and SQLite database.
- Executed primary-key, foreign-key, and selected business-rule validation.
- Achieved 30 successful validation checks with zero failures.
- Generated five isolated anomaly scenarios.
- Created separate ground truth records.
- Executed reproducibility testing and confirmed that all 11 raw CSV datasets matched.
- Started the Streamlit dashboard and checked its functionality.

These activities represent the completed execution and verification work. They should not be interpreted as a full automated test suite covering every documented business rule.

## 15. Limitations

- The project uses synthetic rather than real supplier data.
- Reliability scores depend on the implemented scoring assumptions and weights.
- Synthetic patterns may not represent every real-world supplier scenario.
- Some supplier performance components may be unavailable because of missing source data.
- The implemented validation script does not automatically test every documented business rule.
- Reproducibility verification currently covers the 11 raw CSV datasets.
- The system is a demonstration project and requires further evaluation before production use.

## 16. Future Improvements

- Expand automated validation to cover all documented business rules.
- Add more advanced supplier risk analysis.
- Improve scoring calibration using validated real-world data.
- Add historical supplier performance trend analysis.
- Improve anomaly detection and exception reporting.
- Expand dashboard reporting and analytical capabilities.
- Extend reproducibility checks to JSON and SQL exports.

## 17. AI Usage Disclosure

AI assistance was used for technical problem-solving, debugging, implementation guidance, and documentation.

The project includes an AI prompt history file in the `prompts/` directory.

The developer reviewed and tested the implementation and is responsible for understanding the submitted code, design decisions, dependencies, and limitations.

## 18. Conclusion

The Supplier Reliability Scoring and Data Generation System demonstrates an end-to-end Python-based workflow for synthetic business data generation, relational database management, supplier performance analysis, data validation, anomaly testing, reproducibility, and interactive business intelligence visualization.

The project generates 11 interconnected datasets, evaluates supplier reliability using multiple performance indicators, maintains separate anomaly test cases and expected decisions, and presents insights through a Streamlit dashboard.

The completed implementation provides a foundation for exploring supplier reliability indicators, examining data quality, and identifying potential supplier performance issues using structured synthetic business data.