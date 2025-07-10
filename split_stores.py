import pandas as pd
import os

# Set paths
input_path = 'supermarket_sales.csv'
output_dir = 'data'

# Create 'data' folder if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the CSV
df = pd.read_csv(input_path)

# Split by Branch and save each to an Excel file
for branch in df['Branch'].unique():
    branch_df = df[df['Branch'] == branch]
    output_file = os.path.join(output_dir, f'store_{branch}.xlsx')
    branch_df.to_excel(output_file, index=False)

print("✅ Split complete: Files saved as store_A.xlsx, store_B.xlsx, and store_C.xlsx in 'data/' folder.")
