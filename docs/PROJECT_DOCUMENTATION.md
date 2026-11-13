# Supplier Reliability Scoring and Data Generation System

## 1. Problem Statement

Supplier reliability plays an important role in maintaining business operations, product quality, and timely deliveries. Organizations need to monitor supplier performance to identify potential delivery delays, quality issues, invoice-related problems, and other risk indicators.

This project generates synthetic supplier business data, stores it in a relational database, analyzes supplier performance, and presents insights through an interactive dashboard.

## 2. Project Objectives

- Generate interconnected synthetic supplier datasets.
- Store and manage structured data using SQLite.
- Evaluate supplier performance using reliability indicators.
- Identify delivery, quality, invoice, and risk-related issues.
- Validate database consistency and relationships.
- Present analytical results through an interactive dashboard.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation and data generation |
| Pandas | Data processing and manipulation |
| SQLite | Relational database storage |
| Streamlit | Interactive dashboard application |
| Plotly | Data visualization |

## 4. System Architecture

The project follows a data generation, storage, validation, and visualization workflow.

1. Generate synthetic business data using Python generator modules.
2. Process and organize datasets using Pandas.
3. Export generated datasets into CSV and JSON formats.
4. Create SQL exports and an SQLite database.
5. Validate database records and relationships.
6. Analyze supplier performance using reliability indicators.
7. Display analytical results through a Streamlit dashboard.

## 5. Project Structure

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

## 6. Data Model

The SQLite database contains the following 11 tables:

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

These tables represent different aspects of supplier operations, purchasing, delivery, inspection, invoicing, and reliability analysis.

## 7. Supplier Reliability Analysis

Supplier performance is analyzed using indicators related to:

- Delivery performance.
- Inspection quality.
- Invoice status.
- Supplier risk signals.

The system generates supplier scores to support performance comparison and ranking.

The scoring methodology and component weights should be interpreted from the actual implementation in the source code. Scores should be treated as analytical indicators rather than verified predictions of future supplier performance.

## 8. Data Validation

The project includes database validation checks for:

- Primary key uniqueness.
- Null primary key detection.
- Duplicate primary key detection.
- Foreign key integrity.
- Database table record counts.

These checks help verify the consistency and integrity of generated records.

## 9. Dashboard Features

The Streamlit dashboard provides the following sections:

- Executive Overview.
- Supplier Explorer.
- Anomaly Monitoring.
- Data Records.
- Performance indicators and charts.
- Supplier filtering and searching.
- CSV downloads.

Plotly is used for interactive data visualization.

## 10. Design Decisions and Trade-offs

- **SQLite:** Selected for lightweight relational data storage without requiring a separate database server.
- **Pandas:** Used for structured data processing and manipulation.
- **Streamlit:** Selected to build an interactive dashboard using Python.
- **Synthetic Data:** Used to avoid exposing real supplier business information.
- **Modular Python Files:** Separate generator modules help organize data generation responsibilities.

## 11. Testing and Verification

The project was executed in a local Python environment.

The following activities were performed:

- Executed the data generation program.
- Checked generated CSV and JSON exports.
- Verified SQLite database creation.
- Checked database table record counts.
- Reviewed primary key and foreign key validation results.
- Started the Streamlit dashboard and checked its functionality.

These activities represent manual execution and verification. They should not be interpreted as a completed automated test suite.

## 12. Limitations

- The project uses synthetic rather than real supplier data.
- Reliability scores depend on the implemented scoring assumptions.
- Synthetic patterns may not represent every real-world supplier scenario.
- The system is a demonstration project and requires further evaluation before production use.
- Automated test coverage can be expanded.

## 13. Future Improvements

- Add more advanced supplier risk analysis.
- Introduce automated test coverage.
- Improve scoring calibration using validated real-world data.
- Add additional analytical reports and visualizations.
- Improve monitoring of supplier performance over time.

## 14. AI Usage Disclosure

AI assistance was used for technical problem-solving, debugging, implementation guidance, and documentation.

The project includes an AI prompt history file in the `prompts/` directory. The developer reviewed and tested the implementation and is responsible for understanding the submitted code, design decisions, dependencies, and limitations.

## 15. Conclusion

The Supplier Reliability Scoring and Data Generation System demonstrates a Python-based workflow for synthetic data generation, relational database management, supplier performance analysis, data validation, and interactive business intelligence visualization.

The project provides a foundation for exploring supplier reliability indicators and identifying potential performance issues using structured synthetic business data.
