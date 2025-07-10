import pandas as pd
import os

# Load combined file
df = pd.read_excel('output/Combined_Raw.xlsx')

# Audit metrics
audit_log = {}

# Total entries
audit_log['Total Rows'] = len(df)

# 1. Check for duplicate Invoice ID + Product + Date
duplicates = df.duplicated(subset=['Invoice ID', 'Product line', 'Date'], keep=False)
duplicate_rows = df[duplicates]
audit_log['Duplicate Entries'] = duplicate_rows.shape[0]

# 2. Price mismatch for same Product line across branches
price_mismatch_rows = df.groupby(['Product line'])['Unit price'].nunique()
mismatch_products = price_mismatch_rows[price_mismatch_rows > 1].index.tolist()
mismatched_rows = df[df['Product line'].isin(mismatch_products)]
audit_log['Products with Price Mismatches'] = len(mismatch_products)

# 3. Missing data
missing_values = df.isnull().sum().sum()
audit_log['Missing Values'] = missing_values

# Save mismatched and duplicate entries for review
duplicate_rows.to_excel('output/Duplicates.xlsx', index=False)
mismatched_rows.to_excel('output/Price_Mismatches.xlsx', index=False)

# Save audit summary
audit_summary = pd.DataFrame(list(audit_log.items()), columns=['Issue', 'Count'])
audit_summary.to_csv('output/Audit_Log.csv', index=False)

print("✅ Audit complete! Duplicates.xlsx, Price_Mismatches.xlsx, and Audit_Log.csv created in 'output/' folder.")
