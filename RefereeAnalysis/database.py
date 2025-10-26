import pandas as pd
from utils.PoomsaeProCleaning import load_data, categorize_event, categorize_belt
import numpy as np

# Compute referee scores (combine Accuracy and Presentation for each form)
def compute_referee_score(row):
    forms = ['A', 'B', 'T']
    score = 0
    count = 0
    for form in forms:
        if row.get(f'FormName_{form}') not in [None, 'None', '']:
            acc = row.get(f'Accuracy_{form}', np.nan)
            pre = row.get(f'Presentation_{form}', np.nan)
            if pd.notna(acc) and pd.notna(pre) and acc != -1 and pre != -1:
                score += acc + pre
                count += 1
    return score / count if count > 0 else None

# Compute Official Placement based on simplified rule, only for Round_ID >= 9
def compute_official_placement(df):
    df['Official_Placement'] = df['Placement'].copy()
    # Apply rules only for single-elimination rounds (Round_ID >= 9)
    single_elim_mask = df['Round_ID'] >= 9
    df.loc[single_elim_mask & (df['Placement'] == 0), 'Official_Placement'] = 1
    df.loc[single_elim_mask & (df['Placement'] > 2), 'Official_Placement'] = 2
    return df

# Compute Referee_Placement
def compute_referee_placement(group):
    # Initialize columns for ranking metrics
    group['Avg_Acc_Pres_AB'] = np.nan
    group['Avg_Pres_AB'] = np.nan
    group['Acc_Pres_T'] = np.nan
    group['Ranking_Score'] = np.nan

    # Calculate metrics for each performance
    for idx in group.index:
        acc_a = group.at[idx, 'Accuracy_A'] if 'Accuracy_A' in group.columns else np.nan
        pre_a = group.at[idx, 'Presentation_A'] if 'Presentation_A' in group.columns else np.nan
        form_b = group.at[idx, 'FormName_B'] if 'FormName_B' in group.columns else ''
        acc_b = group.at[idx, 'Accuracy_B'] if 'Accuracy_B' in group.columns else np.nan
        pre_b = group.at[idx, 'Presentation_B'] if 'Presentation_B' in group.columns else np.nan
        acc_t = group.at[idx, 'Accuracy_T'] if 'Accuracy_T' in group.columns else np.nan
        pre_t = group.at[idx, 'Presentation_T'] if 'Presentation_T' in group.columns else np.nan

        # Primary metric: Average of Acc+Pres for A and B (if B is valid)
        if pd.notna(acc_a) and pd.notna(pre_a) and acc_a != -1 and pre_a != -1:
            ab_scores = [acc_a + pre_a]
            if form_b not in [None, 'None', ''] and pd.notna(acc_b) and pd.notna(pre_b) and acc_b != -1 and pre_b != -1:
                ab_scores.append(acc_b + pre_b)
            group.at[idx, 'Avg_Acc_Pres_AB'] = np.mean(ab_scores)
        
        # Tiebreaker 1: Average of Presentation for A and B (if B is valid)
        if pd.notna(pre_a) and pre_a != -1:
            pres_scores = [pre_a]
            if form_b not in [None, 'None', ''] and pd.notna(pre_b) and pre_b != -1:
                pres_scores.append(pre_b)
            group.at[idx, 'Avg_Pres_AB'] = np.mean(pres_scores)
        
        # Tiebreaker 2: Acc+Pres for T (if T is valid)
        if (group.at[idx, 'FormName_T'] not in [None, 'None', ''] if 'FormName_T' in group.columns else False) and pd.notna(acc_t) and pd.notna(pre_t) and acc_t != -1 and pre_t != -1:
            group.at[idx, 'Acc_Pres_T'] = acc_t + pre_t

        # Compute Ranking_Score
        avg_acc_pres_ab = group.at[idx, 'Avg_Acc_Pres_AB']
        avg_pres_ab = group.at[idx, 'Avg_Pres_AB']
        acc_pres_t = group.at[idx, 'Acc_Pres_T']
        ranking_score = 0
        if pd.notna(avg_acc_pres_ab):
            ranking_score += avg_acc_pres_ab
        if pd.notna(avg_pres_ab):
            ranking_score += avg_pres_ab / 10**3
        if pd.notna(acc_pres_t):
            ranking_score += acc_pres_t / 10**6
        group.at[idx, 'Ranking_Score'] = ranking_score if ranking_score != 0 else np.nan

    # Rank performances
    if group['Round_ID'].iloc[0] >= 9:
        # Single-elimination: pair athletes by OrderOfPerform summing to target_sum
        round_id = group['Round_ID'].iloc[0]
        round_size = 2 ** (7 - (round_id - 9))
        target_sum = round_size + 1
        group['Referee_Placement'] = np.nan

        # Find pairs where OrderOfPerform sums to target_sum
        for i, row1 in group.iterrows():
            order1 = row1['OrderOfPerform']
            if pd.isna(order1):
                continue
            # Look for a matching athlete
            match = group[
                (group['OrderOfPerform'] == target_sum - order1) &
                (group.index != i)
            ]
            if not match.empty:
                row2 = match.iloc[0]
                # Compare metrics
                metrics1 = (
                    row1['Avg_Acc_Pres_AB'] or -np.inf,
                    row1['Avg_Pres_AB'] or -np.inf,
                    row1['Acc_Pres_T'] or -np.inf
                )
                metrics2 = (
                    row2['Avg_Acc_Pres_AB'] or -np.inf,
                    row2['Avg_Pres_AB'] or -np.inf,
                    row2['Acc_Pres_T'] or -np.inf
                )
                # Rank 1 for higher, 2 for lower, 1.5 for ties
                if metrics1 > metrics2:
                    group.at[i, 'Referee_Placement'] = 1
                    group.at[row2.name, 'Referee_Placement'] = 2
                elif metrics1 < metrics2:
                    group.at[i, 'Referee_Placement'] = 2
                    group.at[row2.name, 'Referee_Placement'] = 1
                else:
                    group.at[i, 'Referee_Placement'] = 1.5
                    group.at[row2.name, 'Referee_Placement'] = 1.5
    else:
        # Non-single-elimination: rank all athletes by Ranking_Score
        if group['Ranking_Score'].notna().any():
            group['Referee_Placement'] = group['Ranking_Score'].rank(
                method='average', ascending=False, na_option='bottom'
            )
        else:
            group['Referee_Placement'] = np.nan

    return group[['Performance_ID', 'Referee_Placement', 'Ranking_Score']]

# Renormalize Placement and Referee_Placement
def normalize_ranks(group):
    # Check Round_ID for the group
    round_id = group['Round_ID'].iloc[0]
    group['Placement_Normalized'] = group['Placement'].copy()
    group['Referee_Placement_Normalized'] = group['Referee_Placement'].copy()
    if round_id >= 9:
        # For single-elimination rounds, use rank - 1
        group['Placement_Normalized'] = group['Placement'] - 1
        group['Referee_Placement_Normalized'] = group['Referee_Placement'] - 1
    else:
        # For non-single-elimination rounds, use (rank - 1) / (n - 1)
        n = group['Performance_ID'].nunique()
        if n > 1:
            group['Placement_Normalized'] = (group['Placement'] - 1) / (n - 1)
            group['Referee_Placement_Normalized'] = (group['Referee_Placement'] - 1) / (n - 1)
        else:
            # If n=1, set to 0 (highest rank)
            group['Placement_Normalized'] = 0
            group['Referee_Placement_Normalized'] = 0
    return group[['Performance_ID', 'Placement_Normalized', 'Referee_Placement_Normalized']]

def build_database(db_path: str, sql_file_path: str) -> pd.DataFrame:

    # Load data
    df = load_data(db_path, sql_file_path)

    if df is None or df.empty:
        raise Exception("Failed to load data from database or no data returned.")

    # Reset index to ensure uniqueness
    df = df.reset_index(drop=True)

    # Define expected columns for forms
    forms = ['A', 'B', 'T']
    expected_columns = []
    for form in forms:
        expected_columns.extend([
            f'Accuracy_{form}', f'Presentation_{form}',
            f'Acc_Avg_{form}', f'Pre_Avg_{form}'
        ])
    expected_columns.extend([
        'Placement', 'Round_ID', 'OrderOfPerform', 'EventName', 'Division',
        'Gender', 'Category', 'Round', 'RefereeName', 'Performance_ID',
        'FormName_A', 'FormName_B', 'FormName_T', 'ScoreSource', 'MatchNo'
    ])

    # Check for missing columns
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        #logger.error(f"Missing columns in DataFrame: {missing_columns}")
        raise KeyError(f"Missing required columns: {missing_columns}")

    # Convert score, average, placement, and order columns to numeric, coercing errors to NaN
    for form in forms:
        if f'Accuracy_{form}' in df.columns:
            df[f'Accuracy_{form}'] = pd.to_numeric(df[f'Accuracy_{form}'], errors='coerce')
        if f'Presentation_{form}' in df.columns:
            df[f'Presentation_{form}'] = pd.to_numeric(df[f'Presentation_{form}'], errors='coerce')
        if f'Acc_Avg_{form}' in df.columns:
            df[f'Acc_Avg_{form}'] = pd.to_numeric(df[f'Acc_Avg_{form}'], errors='coerce')
        if f'Pre_Avg_{form}' in df.columns:
            df[f'Pre_Avg_{form}'] = pd.to_numeric(df[f'Pre_Avg_{form}'], errors='coerce')
    df['Placement'] = pd.to_numeric(df['Placement'], errors='coerce')
    df['Round_ID'] = pd.to_numeric(df['Round_ID'], errors='coerce')
    df['OrderOfPerform'] = pd.to_numeric(df['OrderOfPerform'], errors='coerce')

    # Add Belt column using categorize_belt
    df['Belt'] = df['Category'].apply(categorize_belt)

    # Apply Official Placement computation
    df = compute_official_placement(df)
    df['Placement'] = df['Official_Placement']
    df = df.drop(columns=['Official_Placement'])

    # Apply Referee_Placement computation
    placement_df = df.groupby(['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName']).apply(compute_referee_placement, include_groups=False).reset_index()

    # Merge while preserving grouping columns
    df = df.merge(placement_df, on=['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'Performance_ID'])

    # Apply normalization within each group
    normalized_df = df.groupby(['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName']).apply(normalize_ranks, include_groups=False).reset_index()

    # Merge normalized placements back to df
    df = df.merge(normalized_df[['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'Performance_ID', 'Placement_Normalized', 'Referee_Placement_Normalized']], 
                on=['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'Performance_ID'], 
                how='left')

    # Compute difference columns for Accuracy and Presentation, with validation
    for form in forms:
        if (f'Accuracy_{form}' in df.columns and f'Acc_Avg_{form}' in df.columns and 
            f'Presentation_{form}' in df.columns and f'Pre_Avg_{form}' in df.columns):
            df[f'Acc_Diff_{form}'] = df[f'Accuracy_{form}'] - df[f'Acc_Avg_{form}']
            df[f'Pre_Diff_{form}'] = df[f'Presentation_{form}'] - df[f'Pre_Avg_{form}']
        #else:
            #logger.warning(f"Skipping difference computation for form {form} due to missing columns")

    # Preprocess data
    df['Event_Category'] = df['Division'].apply(categorize_event)

    # Apply referee score calculation
    df['Referee_Score'] = df.apply(compute_referee_score, axis=1)

    return df