# data_processing.py
import pandas as pd
from scipy.stats import binomtest

# Calculate win rates by division group
def calculate_win_rates_by_division(seq_df):
    grouped = seq_df.groupby('division_group')
    results = []
    
    for division, group in grouped:
        hong_wins = len(group[group['Winner'] == 'Hong'])
        total_matches = len(group)
        win_rate = hong_wins / total_matches if total_matches > 0 else 0
        results.append({
            'Division Group': division,
            'Hong Wins': hong_wins,
            'Total Matches': total_matches,
            'Win Rate': win_rate
        })
    
    return pd.DataFrame(results)

# Calculate win rates by EventName
def calculate_win_rates_by_event(seq_df):
    grouped = seq_df.groupby('EventName')
    results = []
    
    for event, group in grouped:
        hong_wins = len(group[group['Winner'] == 'Hong'])
        total_matches = len(group)
        win_rate = hong_wins / total_matches if total_matches > 0 else 0
        results.append({
            'EventName': event,
            'Hong Wins': hong_wins,
            'Total Matches': total_matches,
            'Win Rate': win_rate
        })
    
    return pd.DataFrame(results)

# Two-sided binomial test
def binomial_test(wins, total):
    if total == 0:
        return 0, 1.0  # No matches, no significance
    result = binomtest(wins, total, p=0.5, alternative='two-sided')
    return 0, result.pvalue  # Return 0 for statistic (not used)