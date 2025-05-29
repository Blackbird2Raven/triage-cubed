import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SignalAnalyzer:
    def __init__(self, csv_path: str):
        """Initialize the signal analyzer with the path to the signals CSV file."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Input file not found: {csv_path}\n"
                f"Please ensure the CSV file exists in the data directory.\n"
                f"Current working directory: {os.getcwd()}"
            )
        
        try:
            self.df = pd.read_csv(csv_path)
            if self.df.empty:
                raise ValueError("The input CSV file is empty")
            
            # Validate required columns
            required_columns = ['detectionname', 'detectionconfidence', 'detectionscore', 
                              'falsepositive', 'occurrences', 'suspectuser', 'targethost']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}")
            
            self.total_signals = len(self.df)
            self.time_window = 86400  # 1 day in seconds
            logger.info(f"Successfully loaded {self.total_signals} signals from {csv_path}")
            
        except pd.errors.EmptyDataError:
            raise ValueError("The input CSV file is empty")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error loading CSV file: {str(e)}")
    
    def generate_group_key(self, row: pd.Series) -> str:
        """Generate a group key for a signal based on detectionname and relevant fields."""
        relevant_fields = [
            'suspectaction', 'suspecthash', 'suspecthost', 'suspectlocation',
            'suspectobject', 'suspectprocess', 'suspecturl', 'suspectuser',
            'targethost', 'targetport', 'targetresource', 'targetuser'
        ]
        
        # Get non-null fields
        non_null_fields = [str(row[field]) for field in relevant_fields 
                          if field in row and pd.notna(row[field])]
        
        # Create group key
        group_key = f"{row['detectionname']}:{'_'.join(non_null_fields)}"
        return group_key
    
    def calculate_false_positive_probability(self, group_df: pd.DataFrame) -> float:
        """Calculate false positive probability for a signal group."""
        false_positives = len(group_df[group_df['falsepositive'] == True])
        total_signals = len(group_df)
        return false_positives / total_signals if total_signals > 0 else 0.0
    
    def calculate_recurrence_frequency(self, group_df: pd.DataFrame) -> float:
        """Calculate recurrence frequency for a signal group."""
        occurrences = group_df['occurrences'].sum()  # Use the occurrences column
        return occurrences / self.time_window
    
    def calculate_suppression_impact(self, group_df: pd.DataFrame) -> float:
        """Calculate suppression impact score for a signal group."""
        occurrences = group_df['occurrences'].sum()  # Use the occurrences column
        return (occurrences / self.total_signals) * 100
    
    def generate_tuning_recommendation(self, group_data: Dict[str, Any]) -> str:
        """Generate tuning recommendation based on signal group metrics."""
        if group_data['P_fp'] > 0.6:
            return "High false positive rate - Consider suppression or threshold adjustment"
        elif group_data['R_freq'] > 0.0001:  # More than 8.64 occurrences per day
            return "High recurrence - Consider threshold adjustment or context-based filtering"
        elif group_data['I_suppress'] > 30:
            return "High suppression impact - Consider targeted suppression"
        else:
            return "Monitor - No immediate tuning required"
    
    def analyze_signals(self) -> pd.DataFrame:
        """Analyze all signals and generate recommendations."""
        # Add group key to dataframe
        self.df['group_key'] = self.df.apply(self.generate_group_key, axis=1)
        
        # Group signals and calculate metrics
        results = []
        for group_key, group_df in self.df.groupby('group_key'):
            p_fp = self.calculate_false_positive_probability(group_df)
            r_freq = self.calculate_recurrence_frequency(group_df)
            i_suppress = self.calculate_suppression_impact(group_df)
            
            group_data = {
                'Signal Name': group_df['detectionname'].iloc[0],
                'P_fp': p_fp,
                'R_freq': r_freq,
                'I_suppress': i_suppress,
                'Occurrences': group_df['occurrences'].sum(),
                'Confidence': group_df['detectionconfidence'].iloc[0],
                'Score': group_df['detectionscore'].iloc[0],
                'Severity': group_df['detectionseverity'].iloc[0] if 'detectionseverity' in group_df else 'Unknown',
                'Technique': group_df['detectiontechnique'].iloc[0] if 'detectiontechnique' in group_df else 'Unknown'
            }
            
            group_data['Recommendation'] = self.generate_tuning_recommendation(group_data)
            results.append(group_data)
        
        return pd.DataFrame(results)
    
    def generate_report(self, output_path: str):
        """Generate and save the analysis report."""
        results_df = self.analyze_signals()
        
        # Sort by suppression impact
        results_df = results_df.sort_values('I_suppress', ascending=False)
        
        # Save to CSV
        results_df.to_csv(output_path, index=False)
        logger.info(f"Report generated and saved to {output_path}")
        
        return results_df

if __name__ == "__main__":
    try:
        # Ensure data directory exists
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"Created data directory: {data_dir}")
        
        # Ensure reports directory exists
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            logger.info(f"Created reports directory: {reports_dir}")
        
        # Check if input file exists
        input_file = os.path.join(data_dir, "signals.csv")
        if not os.path.exists(input_file):
            logger.error(
                f"Input file not found: {input_file}\n"
                "Please place your signals CSV file in the data directory."
            )
            sys.exit(1)
        
        # Run analysis
        analyzer = SignalAnalyzer(input_file)
        output_file = os.path.join(reports_dir, "signal_analysis_report.csv")
        report_df = analyzer.generate_report(output_file)
        
        print("\nSignal Analysis Report:")
        print(report_df.to_string())
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1) 