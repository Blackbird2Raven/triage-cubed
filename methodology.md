---
layout: page
title: Methodology
permalink: /methodology/
---

# TRIAGE³ Methodology

## The Three-Dimensional Approach

TRIAGE³ revolutionizes SOC signal management through a unique three-dimensional analysis framework. Each dimension provides critical insights that, when combined, create a comprehensive understanding of your security signals.

### 1. False Positive Probability (P_fp)

The first dimension focuses on signal reliability through the False Positive Probability metric:

```
P_fp = Count_FP(g) / Count_Total(g)
```

Where:
- Count_FP(g) = Number of false positives in signal group
- Count_Total(g) = Total signals in the group

This metric helps identify:
- Signals with high false positive rates
- Patterns in false positive occurrences
- Opportunities for tuning

### 2. Recurrence Frequency (R_freq)

The second dimension analyzes signal patterns over time:

```
R_freq = f(g) / T_w
```

Where:
- f(g) = Frequency of signals in group
- T_w = Time window (typically 86400 seconds)

This helps:
- Identify persistent issues
- Understand signal patterns
- Plan resource allocation

### 3. Suppression Impact (I_suppress)

The third dimension evaluates the consequences of tuning decisions:

```
I_suppress = (Occurrences / TotalSignals) * 100
```

This ensures:
- Critical signals aren't lost
- Tuning decisions are balanced
- Coverage is maintained

## Implementation Guidelines

### Signal Grouping

1. Create composite keys:
   ```
   groupKey = DetectionName + ":" + Join("_", AllNonNullFields([...]))
   ```

2. Consider context:
   - Technical attributes
   - Business impact
   - Historical patterns

### Thresholds

Recommended thresholds for each dimension:

- P_fp > 0.6: High false positive rate
- R_freq > 0.0001: High recurrence
- I_suppress > 30%: Significant impact

### Tuning Process

1. **Analysis**
   - Calculate all three metrics
   - Identify signal groups
   - Review historical data

2. **Decision Making**
   - Evaluate against thresholds
   - Consider business context
   - Plan tuning actions

3. **Implementation**
   - Apply tuning changes
   - Monitor results
   - Adjust as needed

## Benefits

- **Reduced Alert Fatigue**: Up to 60% reduction in some implementations
- **Improved Accuracy**: Data-driven tuning decisions
- **Better Resource Allocation**: Focus on high-value signals
- **Vendor Agnostic**: Works with any security stack

## Getting Started

1. Export your signal data
2. Calculate the three metrics
3. Group similar signals
4. Apply the framework
5. Monitor and adjust

[Download Implementation Guide](/resources/implementation-guide)
[View Example Analysis](/resources/example-analysis) 