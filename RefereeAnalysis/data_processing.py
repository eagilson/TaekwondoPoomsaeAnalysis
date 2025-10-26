# data_processing.py
import pandas as pd
import numpy as np


def compute_stats(group):
    """
    Computes the summary statistics for each Referee, Tournament, and Event combination.    
    """
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
                if f'Pre_Diff_{form}' in valid_rows.columns:
                    pre_diff = valid_rows[f'Pre_Diff_{form}']
                    if not pre_diff.empty and pre_diff.notna().any():
                        pre_diffs.extend(pre_diff[pre_diff.notna()])
                if f'Acc_Diff_{form}' in valid_rows.columns:
                    acc_diff = valid_rows[f'Acc_Diff_{form}']
                    if not acc_diff.empty and acc_diff.notna().any():
                        acc_diffs.extend(acc_diff[acc_diff.notna()])
    
    pre_diffs = pd.Series(pre_diffs)
    acc_diffs = pd.Series(acc_diffs)
    
    stats = {
        'Athletes': group['Performance_ID'].nunique(),
        'Presentation_Diff_SD': pre_diffs.std() if not pre_diffs.empty else np.nan,
        'Accuracy_Diff_SD': acc_diffs.std() if not acc_diffs.empty else np.nan,
        'Presentation_Diff_Mean': pre_diffs.mean() if not pre_diffs.empty else np.nan,
        'Accuracy_Diff_Mean': acc_diffs.mean() if not acc_diffs.empty else np.nan,
    }
    valid_rows = group[['Referee_Placement_Normalized', 'Placement_Normalized']].dropna()
    if len(valid_rows) > 1 and valid_rows['Referee_Placement_Normalized'].std() > 0 and valid_rows['Placement_Normalized'].std() > 0:
        stats['Correlation'] = valid_rows['Referee_Placement_Normalized'].corr(valid_rows['Placement_Normalized'])
    else:
        stats['Correlation'] = np.nan
    return pd.Series(stats), acc_diffs, pre_diffs


def singleeliminationgaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame of referee-specific score component gaps for single-elimination matches.
    
    Excludes match only if ALL forms (A, B, T) have Presentation < 1.5 for at least one athlete.
    Keeps match if ANY form has both athletes >= 1.5.
    """
    se_df = df[df['Round_ID'] >= 9].copy()
    if se_df.empty:
        return pd.DataFrame()

    # === ADD COMBINED SCORES ===
    forms = ['A', 'B', 'T']
    for form in forms:
        acc_col = f'Accuracy_{form}'
        pre_col = f'Presentation_{form}'
        score_col = f'Referee_Form_{form}_Score'
        if acc_col in se_df.columns and pre_col in se_df.columns:
            se_df[score_col] = se_df[acc_col] + se_df[pre_col]
            se_df.loc[se_df[acc_col] == -1, score_col] = np.nan
            se_df.loc[se_df[pre_col] == -1, score_col] = np.nan
        else:
            se_df[score_col] = np.nan

    components = [
        'Accuracy_A', 'Presentation_A',
        'Accuracy_B', 'Presentation_B',
        'Accuracy_T', 'Presentation_T',
        'Acc_Avg_A', 'Pre_Avg_A',
        'Acc_Avg_B', 'Pre_Avg_B',
        'Acc_Avg_T', 'Pre_Avg_T',
        'Referee_Score', 'FinalScore',
        'Referee_Form_A_Score', 'Referee_Form_B_Score', 'Referee_Form_T_Score'
    ]

    gap_rows = []
    group_keys = ['EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'MatchNo', 'Round_ID']

    for group_key, group in se_df.groupby(group_keys):
        if len(group) < 2:
            continue

        round_id = group['Round_ID'].iloc[0]
        round_size = 2 ** (7 - (round_id - 9))
        target_sum = round_size + 1

        processed = set()
        for i, row1 in group.iterrows():
            if i in processed:
                continue
            order1 = row1['OrderOfPerform']
            if pd.isna(order1):
                continue

            match = group[
                (group['OrderOfPerform'] == target_sum - order1) &
                (group.index != i)
            ]
            if match.empty:
                continue

            row2 = match.iloc[0]
            processed.add(i)
            processed.add(row2.name)

            # === NEW FILTER LOGIC ===
            # Keep match if ANY form has both athletes >= 1.5
            keep_match = False
            for form in forms:
                pre_col = f'Presentation_{form}'
                if pre_col not in row1 or pre_col not in row2:
                    continue  # Skip if column missing
                p1 = row1[pre_col]
                p2 = row2[pre_col]
                if pd.notna(p1) and pd.notna(p2) and p1 >= 1.5 and p2 >= 1.5:
                    keep_match = True
                    break  # One good form → keep entire match

            if not keep_match:
                continue  # Skip match only if ALL forms fail

            # Determine winner/loser
            placement1 = row1.get('Referee_Placement', np.nan)
            placement2 = row2.get('Referee_Placement', np.nan)

            if pd.notna(placement1) and pd.notna(placement2):
                if placement1 == 1 or (placement1 == 1.5 and placement2 == 1.5):
                    winner, loser = row1, row2
                else:
                    winner, loser = row2, row1
            else:
                score1 = row1.get('Referee_Score', -np.inf)
                score2 = row2.get('Referee_Score', -np.inf)
                if score1 >= score2:
                    winner, loser = row1, row2
                else:
                    winner, loser = row2, row1

            # Compute absolute gaps
            gaps = {}
            for comp in components:
                val1 = winner.get(comp, np.nan)
                val2 = loser.get(comp, np.nan)
                if pd.notna(val1) and pd.notna(val2) and val1 != -1 and val2 != -1:
                    gaps[f'{comp}_Gap'] = val1 - val2
                else:
                    gaps[f'{comp}_Gap'] = np.nan

            gap_row = {
                **dict(zip(group_keys, group_key)),
                'Performance_ID_Winner': winner['Performance_ID'],
                'Performance_ID_Loser': loser['Performance_ID'],
                'OrderOfPerform_Winner': winner['OrderOfPerform'],
                'OrderOfPerform_Loser': loser['OrderOfPerform'],
                'Referee_Placement_Winner': winner.get('Referee_Placement', np.nan),
                'Referee_Placement_Loser': loser.get('Referee_Placement', np.nan),
            }
            gap_row.update(gaps)
            gap_rows.append(gap_row)

    if not gap_rows:
        return pd.DataFrame()

    gap_df = pd.DataFrame(gap_rows)
    meta_cols = [
        'EventName', 'Division', 'Gender', 'Category', 'Round', 'RefereeName', 'MatchNo', 'Round_ID',
        'Performance_ID_Winner', 'Performance_ID_Loser',
        'OrderOfPerform_Winner', 'OrderOfPerform_Loser',
        'Referee_Placement_Winner', 'Referee_Placement_Loser'
    ]
    gap_cols = sorted([col for col in gap_df.columns if col not in meta_cols])
    return gap_df[meta_cols + gap_cols]


def poomsaemajors(df: pd.DataFrame) -> pd.DataFrame:
    """Augments the df with the number of majors."""
    major_df = df.copy()
    major_df['Major_Count'] = np.nan
    major_df['Major_Diff'] = np.nan
    return major_df