# Signals Fine Tuning Recommendation Report

A powerful tool for analyzing security signals from DNIF HYPERCLOUD platform to generate automated tuning recommendations for signal suppression and threshold adjustments.

## Overview

This tool helps detection engineers:
- Analyze signal patterns and false positives
- Identify noisy signals that need tuning
- Generate data-driven recommendations for signal optimization
- Reduce alert fatigue by focusing on high-value signals

## Features

- **Signal Grouping**: Intelligently groups similar signals based on detection name and context
- **False Positive Analysis**: Calculates false positive probability for each signal group
- **Recurrence Analysis**: Measures signal frequency and patterns
- **Impact Assessment**: Evaluates the impact of potential suppressions
- **Automated Recommendations**: Generates tuning suggestions based on multiple metrics
- **Detailed Reporting**: Produces comprehensive CSV reports with actionable insights

## Prerequisites

- Python 3.8 or higher
- DNIF HYPERCLOUD platform access
- Signals data exported in CSV format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/signals-tuning-recommendation.git
cd signals-tuning-recommendation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Export your signals data from DNIF HYPERCLOUD as a CSV file
2. Place the CSV file in the `data` directory
3. Run the analyzer:
```bash
python src/signal_analyzer.py
```

The report will be generated in the `reports` directory.

### Input CSV Format

The input CSV file should contain the following required columns:
- `detectionname`: Name of the detection
- `detectionconfidence`: Confidence level of the detection
- `detectionscore`: Score assigned to the detection
- `falsepositive`: Boolean indicating if the signal is a false positive
- `occurrences`: Number of times the signal occurred
- `suspectuser`: User associated with the signal
- `targethost`: Target host of the signal

Optional columns:
- `detectionseverity`: Severity level of the detection
- `detectiontechnique`: Technique used in the detection
- Other suspect and target fields for context

### Output Report

The generated report includes:
- Signal Name
- False Positive Probability (P_fp)
- Recurrence Frequency (R_freq)
- Suppression Impact Score (I_suppress)
- Number of Occurrences
- Confidence Level
- Score
- Severity
- Technique
- Tuning Recommendation

## Analysis Logic

### Signal Grouping
Signals are grouped using a composite key:
```
groupKey = DetectionName + ":" + Join("_", AllNonNullFields([...]))
```

### Metrics Calculation

1. **False Positive Probability (P_fp)**
   - Formula: Count_FP(g) / Count_Total(g)
   - Threshold: > 0.6 indicates high false positive rate

2. **Recurrence Frequency (R_freq)**
   - Formula: f(g) / T_w
   - T_w = 86400 seconds (1 day)
   - Threshold: > 0.0001 indicates high recurrence

3. **Suppression Impact (I_suppress)**
   - Formula: (Occurrences / TotalSignals) * 100
   - Threshold: > 30% indicates significant impact

### Tuning Recommendations

The tool generates recommendations based on:
- False positive probability
- Recurrence frequency
- Suppression impact
- Signal confidence and score

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue in the repository
3. Contact the detection engineering team

## Authors

- Siddhant Mishra
- Professional Services Team
