# User Guide: Signals Tuning Recommendation Tool

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Data Preparation](#data-preparation)
4. [Running the Analysis](#running-the-analysis)
5. [Understanding the Results](#understanding-the-results)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Introduction

This tool helps detection engineers optimize their signal configurations by analyzing signal patterns and providing data-driven recommendations for tuning. It's particularly useful for:
- Reducing false positives
- Optimizing signal thresholds
- Identifying noisy signals
- Improving signal quality

## Getting Started

### Prerequisites
- Python 3.8 or higher
- DNIF HYPERCLOUD platform access
- Basic understanding of detection engineering concepts

### Installation
1. Clone the repository
2. Set up a virtual environment
3. Install dependencies
4. Verify installation

## Data Preparation

### Exporting Data from DNIF HYPERCLOUD
1. Log into your DNIF HYPERCLOUD platform
2. Navigate to the Signals section
3. Set the time range to last 30 days
4. Export the data as CSV
5. Ensure all required columns are included

### Required CSV Columns
```
detectionname        - Name of the detection
detectionconfidence  - Confidence level (Low/Medium/High)
detectionscore      - Numerical score
falsepositive       - Boolean (true/false)
occurrences         - Number of occurrences
suspectuser         - User associated with the signal
targethost          - Target host
```

### Optional Columns
```
detectionseverity   - Severity level
detectiontechnique  - MITRE ATT&CK technique
detectiontactic     - MITRE ATT&CK tactic
```

## Running the Analysis

### Basic Usage
```bash
python src/signal_analyzer.py
```

### Expected Output
The tool will:
1. Load and validate the input data
2. Group similar signals
3. Calculate metrics
4. Generate recommendations
5. Save the report

## Understanding the Results

### Report Columns
- **Signal Name**: Name of the detection
- **P_fp**: False positive probability (0-1)
- **R_freq**: Recurrence frequency (occurrences per second)
- **I_suppress**: Suppression impact score (percentage)
- **Occurrences**: Total number of occurrences
- **Confidence**: Detection confidence level
- **Score**: Detection score
- **Severity**: Detection severity
- **Technique**: MITRE ATT&CK technique
- **Recommendation**: Tuning suggestion

### Interpreting Metrics

#### False Positive Probability (P_fp)
- 0-0.3: Low false positive rate
- 0.3-0.6: Medium false positive rate
- >0.6: High false positive rate

#### Recurrence Frequency (R_freq)
- <0.0001: Low frequency
- 0.0001-0.001: Medium frequency
- >0.001: High frequency

#### Suppression Impact (I_suppress)
- <30%: Low impact
- 30-50%: Medium impact
- >50%: High impact

## Best Practices

### Data Collection
1. Export data for a meaningful time period (30 days recommended)
2. Include all relevant fields
3. Ensure data quality and completeness

### Analysis
1. Review high-impact signals first
2. Consider context when implementing recommendations
3. Validate recommendations against security requirements

### Implementation
1. Start with high-confidence recommendations
2. Test changes in a controlled environment
3. Monitor impact after implementation
4. Document all changes

## Troubleshooting

### Common Issues

#### Input File Not Found
```
Error: Input file not found: data/signals.csv
```
Solution: Ensure the CSV file is in the data directory

#### Missing Required Columns
```
Error: Missing required columns in CSV: detectionname
```
Solution: Check CSV export from DNIF HYPERCLOUD

#### Empty CSV File
```
Error: The input CSV file is empty
```
Solution: Verify data export and time range

### Getting Help
1. Check the [README](../README.md)
2. Review this user guide
3. Open an issue in the repository
4. Contact the detection engineering team

## Examples

### Example 1: Basic Analysis
```bash
# Place signals.csv in data directory
python src/signal_analyzer.py
```

### Example 2: Reviewing Results
1. Open the generated report in the reports directory
2. Sort by I_suppress to identify high-impact signals
3. Review recommendations for these signals
4. Implement changes based on recommendations

### Example 3: Best Practice Workflow
1. Export data from DNIF HYPERCLOUD
2. Run the analysis
3. Review high-impact signals
4. Validate recommendations
5. Implement changes
6. Monitor results
7. Document changes 