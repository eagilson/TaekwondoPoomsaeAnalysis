import pandas as pd
import numpy as np

# Compute summary statistics
def compute_stats(group):
    # Initialize lists for valid differences
    pre_diffs = []
    acc_diffs = []
    
    # Filter rows for each form based on valid FormName and non -1 scores
    forms = ['A', 'B', 'T']
    for form in forms:
        if (f'FormName_{form}' in group.columns and 
            f'Accuracy_{form}' in group.columns and 
            f'Presentation_{form}' in group.columns):
            valid_rows = group[
                (group[f'FormName_{form}'].notna()) & 
                (group[f'FormName_{form}'] != 'None') & 
                (group[f'FormName_{form}'] != '') & 
                (group[f'Accuracy_{form}'] != -1) & 
                (group[f'Presentation_{form}'] != -1)
            ]
            if not valid_rows.empty:
                # Extract differences where scores are valid
                if f'Pre_Diff_{form}' in valid_rows.columns:
                    pre_diff = valid_rows[f'Pre_Diff_{form}']
                    if not pre_diff.empty and pre_diff.notna().any():
                        pre_diffs.extend(pre_diff[pre_diff.notna()])
                if f'Acc_Diff_{form}' in valid_rows.columns:
                    acc_diff = valid_rows[f'Acc_Diff_{form}']
                    if not acc_diff.empty and acc_diff.notna().any():
                        acc_diffs.extend(acc_diff[acc_diff.notna()])
    
    # Convert to Series for computation
    pre_diffs = pd.Series(pre_diffs)
    acc_diffs = pd.Series(acc_diffs)
    
    stats = {
        'Athletes': group['Performance_ID'].nunique(),
        'Presentation_Diff_SD': pre_diffs.std() if not pre_diffs.empty else np.nan,
        'Accuracy_Diff_SD': acc_diffs.std() if not acc_diffs.empty else np.nan,
        'Presentation_Diff_Mean': pre_diffs.mean() if not pre_diffs.empty else np.nan,
        'Accuracy_Diff_Mean': acc_diffs.mean() if not acc_diffs.empty else np.nan,
    }
    # Compute correlation between normalized referee placement and placement
    valid_rows = group[['Referee_Placement_Normalized', 'Placement_Normalized']].dropna()
    if len(valid_rows) > 1 and valid_rows['Referee_Placement_Normalized'].std() > 0 and valid_rows['Placement_Normalized'].std() > 0:
        stats['Correlation'] = valid_rows['Referee_Placement_Normalized'].corr(valid_rows['Placement_Normalized'])
    else:
        stats['Correlation'] = np.nan
    return pd.Series(stats), acc_diffs, pre_diffs