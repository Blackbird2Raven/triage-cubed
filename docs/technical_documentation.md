# Technical Documentation: Signals Tuning Recommendation Tool

## Architecture

### Overview
The tool follows a modular architecture with the following components:
- Data Loading and Validation
- Signal Analysis
- Metrics Calculation
- Recommendation Generation
- Report Generation

### Class Structure

#### SignalAnalyzer
Main class that orchestrates the analysis process.

```python
class SignalAnalyzer:
    def __init__(self, csv_path: str)
    def generate_group_key(self, row: pd.Series) -> str
    def calculate_false_positive_probability(self, group_df: pd.DataFrame) -> float
    def calculate_recurrence_frequency(self, group_df: pd.DataFrame) -> float
    def calculate_suppression_impact(self, group_df: pd.DataFrame) -> float
    def generate_tuning_recommendation(self, group_data: Dict[str, Any]) -> str
    def analyze_signals(self) -> pd.DataFrame
    def generate_report(self, output_path: str)
```

## Implementation Details

### Signal Grouping
```python
def generate_group_key(self, row: pd.Series) -> str:
    relevant_fields = [
        'suspectaction', 'suspecthash', 'suspecthost', 'suspectlocation',
        'suspectobject', 'suspectprocess', 'suspecturl', 'suspectuser',
        'targethost', 'targetport', 'targetresource', 'targetuser'
    ]
    
    non_null_fields = [str(row[field]) for field in relevant_fields 
                      if field in row and pd.notna(row[field])]
    
    return f"{row['detectionname']}:{'_'.join(non_null_fields)}"
```

### Metrics Calculation

#### False Positive Probability
```python
def calculate_false_positive_probability(self, group_df: pd.DataFrame) -> float:
    false_positives = len(group_df[group_df['falsepositive'] == True])
    total_signals = len(group_df)
    return false_positives / total_signals if total_signals > 0 else 0.0
```

#### Recurrence Frequency
```python
def calculate_recurrence_frequency(self, group_df: pd.DataFrame) -> float:
    occurrences = group_df['occurrences'].sum()
    return occurrences / self.time_window  # time_window = 86400 (1 day in seconds)
```

#### Suppression Impact
```python
def calculate_suppression_impact(self, group_df: pd.DataFrame) -> float:
    occurrences = group_df['occurrences'].sum()
    return (occurrences / self.total_signals) * 100
```

## Extending the Tool

### Adding New Metrics

1. Create a new calculation method:
```python
def calculate_new_metric(self, group_df: pd.DataFrame) -> float:
    # Implementation
    pass
```

2. Add the metric to the analysis:
```python
def analyze_signals(self) -> pd.DataFrame:
    # ... existing code ...
    new_metric = self.calculate_new_metric(group_df)
    group_data['New_Metric'] = new_metric
    # ... rest of the code ...
```

### Modifying Recommendations

Update the `generate_tuning_recommendation` method:
```python
def generate_tuning_recommendation(self, group_data: Dict[str, Any]) -> str:
    if group_data['New_Metric'] > threshold:
        return "New recommendation based on metric"
    # ... existing logic ...
```

## Testing

### Unit Tests
Create test cases for:
- Data loading and validation
- Metric calculations
- Group key generation
- Recommendation generation

### Integration Tests
Test the complete workflow:
1. Load sample data
2. Run analysis
3. Verify output format
4. Validate recommendations

## Performance Considerations

### Data Processing
- Use pandas for efficient data manipulation
- Implement chunking for large datasets
- Optimize group operations

### Memory Management
- Clear unnecessary data after processing
- Use appropriate data types
- Monitor memory usage

## Error Handling

### Input Validation
```python
def validate_input(self, csv_path: str):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Input file not found: {csv_path}")
    
    required_columns = ['detectionname', 'detectionconfidence', ...]
    missing_columns = [col for col in required_columns if col not in self.df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
```

### Exception Handling
```python
try:
    # Operation
except pd.errors.EmptyDataError:
    logger.error("Empty CSV file")
except pd.errors.ParserError as e:
    logger.error(f"CSV parsing error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

## Logging

### Configuration
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Usage
```python
logger.info("Starting analysis")
logger.warning("High false positive rate detected")
logger.error("Failed to process file")
```

## Future Improvements

### Planned Features
1. Support for multiple input formats
2. Advanced visualization capabilities
3. Machine learning-based recommendations
4. Real-time analysis capabilities

### Technical Debt
1. Improve error handling
2. Add comprehensive testing
3. Optimize performance
4. Enhance documentation

## Contributing Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- Add comments for complex logic

### Pull Request Process
1. Create feature branch
2. Add tests
3. Update documentation
4. Submit PR with description

### Review Process
1. Code review
2. Test verification
3. Documentation review
4. Performance check 