import pandas as pd

# Load the combined file
df = pd.read_excel('output/Combined_Raw.xlsx')

# 1. Drop exact duplicate rows (same Invoice ID + Product + Date)
df_cleaned = df.drop_duplicates(subset=['Invoice ID', 'Product line', 'Date'])

# 2. Fill missing values (optional step, can also log them)
df_cleaned.fillna('MISSING', inplace=True)

# 3. Fix price mismatches (optional step):
# For now, just flag products that have different prices across branches
price_check = df_cleaned.groupby(['Product line'])['Unit price'].transform('nunique')
df_cleaned['Price_Flag'] = price_check > 1

# Save cleaned file
df_cleaned.to_excel('output/Cleaned_Data.xlsx', index=False)

print("✅ Cleaning complete! Cleaned_Data.xlsx created in 'output/' folder.")
