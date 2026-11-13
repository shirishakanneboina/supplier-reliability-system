# Supplier Reliability Scoring and Data Generation System

## 1. Problem Statement

Supplier reliability is important for maintaining business operations, product quality and timely deliveries. This project generates synthetic supplier business data and provides a system to analyze supplier performance and identify potential reliability issues.

## 2. Project Objectives

- Generate interconnected synthetic supplier datasets.
- Store and manage data using SQLite.
- Evaluate supplier performance using reliability indicators.
- Identify delivery, quality, invoice and risk-related issues.
- Present analytical results through an interactive dashboard.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| Pandas | Data processing |
| SQLite | Relational database |
| Streamlit | Dashboard application |
| Plotly | Data visualization |

## 4. System Architecture

The project follows this workflow:

1. Generate synthetic business data using Python.
2. Process and organize datasets using Pandas.
3. Export datasets into CSV, JSON and SQL formats.
4. Store structured records in an SQLite database.
5. Analyze supplier performance.
6. Display results through a Streamlit dashboard.

## 5. Data Model

The database contains 11 entities:

- Suppliers
- Sites
- Contracts
- Purchase Orders
- Purchase Order Lines
- Shipments
- Delivery Events
- Inspections
- Invoices
- Risk Signals
- Supplier Scores

These entities represent different aspects of supplier operations and performance.

## 6. Supplier Reliability Analysis

Supplier performance is analyzed using indicators related to:

- Delivery performance.
- Inspection quality.
- Invoice status.
- Supplier risk signals.

The scoring implementation is used to compare supplier performance and support supplier ranking. The exact scoring formula and component weights should be understood from the implemented source code.

## 7. Data Validation

Validation checks include:

- Primary key uniqueness.
- Null primary key detection.
- Duplicate primary key detection.
- Foreign key integrity.
- Database table record counts.

Validation results are used to check the consistency of generated data.

## 8. Dashboard Features

The dashboard provides:

- Executive Overview.
- Supplier Explorer.
- Anomaly Monitoring.
- Data Records.
- Performance indicators and charts.
- Supplier filtering and searching.
- CSV downloads.

## 9. Design Decisions and Trade-offs

- SQLite was selected for lightweight relational data storage.
- Pandas was used for structured data processing.
- Streamlit was selected to build an interactive dashboard using Python.
- Synthetic data was used to avoid exposing real business information.
- A fixed random seed supports reproducible data generation.

## 10. Testing and Verification

The project was executed in a local Python environment. The data generation process, database creation, validation output and dashboard execution were checked.

Detailed test cases and their actual results should be maintained separately.

## 11. Limitations

- The project uses synthetic rather than real supplier data.
- Reliability scores depend on the implemented scoring assumptions.
- Synthetic patterns may not represent every real-world supplier scenario.
- The system is a demonstration project and requires further evaluation before production use.

## 12. Future Improvements

- Add more advanced supplier risk analysis.
- Introduce automated test coverage.
- Improve scoring calibration using real-world validated data.
- Add additional analytical reports and visualizations.

## 13. Conclusion

The Supplier Reliability Scoring and Data Generation System demonstrates a Python-based workflow for synthetic data generation, relational database management, supplier performance analysis, validation and interactive business intelligence visualization.