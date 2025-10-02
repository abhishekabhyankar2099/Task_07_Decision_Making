import pandas as pd

# Load dataset
df = pd.read_excel("C:/Users/Hp/Downloads/sportsref_download.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Helper: per-game calculation
df['PTS_per_game'] = df['PTS'] / df['G']
df['AST_per_game'] = df['AST'] / df['G']
df['TRB_per_game'] = df['TRB'] / df['G']
df['AST_to_TOV'] = df['AST'] / df['TOV']
df['Combined_per_game'] = (df['PTS'] + df['TRB'] + df['AST']) / df['G']
df['FG%'] = df['FG'] / df['FGA']

# ------------------------------
# Level 1 – Factual Retrieval
# ------------------------------

# Q1: Top scorer (total points)
q1 = df.loc[df['PTS'].idxmax(), ['Player', 'PTS']]

# Q2: Highest FG%
q2 = df.loc[df['FG%'].idxmax(), ['Player', 'FG%']]

# Q3: Most triple-doubles
q3 = df.loc[df['Trp-Dbl'].idxmax(), ['Player', 'Trp-Dbl']]

# ------------------------------
# Level 2 – Calculated Metrics
# ------------------------------

# Q4: Highest points per game
q4 = df.loc[df['PTS_per_game'].idxmax(), ['Player', 'PTS_per_game']]

# Q5: Best assist-to-turnover ratio
q5 = df.loc[df['AST_to_TOV'].idxmax(), ['Player', 'AST_to_TOV']]

# Q6: Highest combined PTS+REB+AST per game
q6 = df.loc[df['Combined_per_game'].idxmax(), ['Player', 'Combined_per_game']]

# ------------------------------
# Level 3 – Analytical Reasoning
# ------------------------------

# Q7: Player with highest contribution index (Combined_per_game)
q7 = df.loc[df['Combined_per_game'].idxmax(), ['Player', 'Combined_per_game']]

# Q8: Player most likely to get triple-double (pick highest combined_per_game among those with >=2 triple-doubles)
q8_candidates = df[df['Trp-Dbl'] >= 2]
if not q8_candidates.empty:
    q8 = q8_candidates.loc[q8_candidates['Combined_per_game'].idxmax(), ['Player', 'Combined_per_game']]
else:
    q8 = "No player had 2 or more triple-doubles."

# Q9: New top scorer if top 5 removed
df_sorted_pts = df.sort_values(by='PTS', ascending=False)
df_no_top5 = df_sorted_pts.iloc[5:]
q9 = df_no_top5.loc[df_no_top5['PTS'].idxmax(), ['Player', 'PTS']]

# ------------------------------
# Level 4 – Subjective/Narrative
# ------------------------------
# Q10 is subjective — you can base it on q7 + awards
q10 = df.loc[df['Combined_per_game'].idxmax(), ['Player', 'Combined_per_game', 'Awards']]

# ------------------------------
# Print Results
# ------------------------------
print("\n--- Level 1: Factual ---")
print("Q1 Top Scorer:", q1.to_dict())
print("Q2 Highest FG%:", q2.to_dict())
print("Q3 Most Triple-Doubles:", q3.to_dict())

print("\n--- Level 2: Calculated ---")
print("Q4 Highest Points/Game:", q4.to_dict())
print("Q5 Best Assist-to-Turnover Ratio:", q5.to_dict())
print("Q6 Highest Combined/Game:", q6.to_dict())

print("\n--- Level 3: Analytical ---")
print("Q7 Highest Contribution Index:", q7.to_dict())
print("Q8 Likely Triple-Double Candidate:", q8 if isinstance(q8, str) else q8.to_dict())
print("Q9 New Top Scorer (no top 5):", q9.to_dict())

print("\n--- Level 4: Narrative ---")
print("Q10 Best All-Around Player Suggestion:", q10.to_dict())
